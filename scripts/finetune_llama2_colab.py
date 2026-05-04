# %% [markdown]
# # 🛡️ Cybersecurity AI Assistant — Fine-Tuning Llama-2-7B with Unsloth
#
# This notebook fine-tunes **Llama-2-7B** on a cybersecurity Q&A dataset
# using **Unsloth** (2x faster, 70% less VRAM) with **QLoRA**.
#
# **Requirements:** Google Colab with a **T4 GPU** (free tier works!)
#
# ---

# %% [markdown]
# ## Step 1: Install Dependencies
# This installs Unsloth and all required libraries. Takes ~3 minutes.

# %%
%%capture
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes

# %% [markdown]
# ## Step 2: Mount Google Drive
# Your training dataset (`cybersec_train_5000.jsonl`) must be in your Google Drive.

# %%
from google.colab import drive
drive.mount('/content/drive')

# Set the path to your dataset file in Google Drive
# ⚠️ CHANGE THIS PATH if you put the file in a different folder!
DATASET_PATH = "/content/drive/MyDrive/cybersec_train_5000.jsonl"

import os
if os.path.exists(DATASET_PATH):
    print(f"✅ Dataset found: {DATASET_PATH}")
    size_mb = os.path.getsize(DATASET_PATH) / (1024 * 1024)
    print(f"   Size: {size_mb:.1f} MB")
else:
    print(f"❌ Dataset NOT found at: {DATASET_PATH}")
    print("   Please upload 'cybersec_train_5000.jsonl' to your Google Drive root folder.")

# %% [markdown]
# ## Step 3: Load the Model with Unsloth
# We load Llama-2-7B in **4-bit quantization** (QLoRA) to fit in the T4's 16GB VRAM.

# %%
from unsloth import FastLanguageModel
import torch

# ─── Model Configuration ──────────────────────────────────
MODEL_NAME = "unsloth/llama-2-7b-bnb-4bit"  # Pre-quantized Llama-2-7B
MAX_SEQ_LENGTH = 4096   # Maximum context length
DTYPE = None             # Auto-detect (float16 for T4)
LOAD_IN_4BIT = True      # Use 4-bit quantization (saves VRAM)
# ───────────────────────────────────────────────────────────

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LENGTH,
    dtype=DTYPE,
    load_in_4bit=LOAD_IN_4BIT,
)

print(f"✅ Model loaded: {MODEL_NAME}")
print(f"   Max sequence length: {MAX_SEQ_LENGTH}")

# %% [markdown]
# ## Step 4: Add LoRA Adapters
# LoRA lets us fine-tune only a small fraction of the model's weights,
# making training fast and memory-efficient.

# %%
model = FastLanguageModel.get_peft_model(
    model,
    r=16,                          # LoRA rank (higher = more capacity, more VRAM)
    target_modules=[               # Which layers to adapt
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha=16,                 # LoRA scaling factor
    lora_dropout=0,                # No dropout (Unsloth optimized)
    bias="none",                   # No bias terms
    use_gradient_checkpointing="unsloth",  # 30% less VRAM
    random_state=3407,
    use_rslora=False,
    loftq_config=None,
)

print("✅ LoRA adapters added")
# Show trainable parameters
model.print_trainable_parameters()

# %% [markdown]
# ## Step 5: Load and Prepare the Dataset

# %%
from datasets import load_dataset

# Load our prepared JSONL dataset
dataset = load_dataset("json", data_files=DATASET_PATH, split="train")

print(f"✅ Dataset loaded: {len(dataset)} training examples")
print(f"\n📋 Sample entry (first 500 chars):")
print(dataset[0]["text"][:500])
print("...")

# %% [markdown]
# ## Step 6: Configure Training
# These settings are optimized for a Colab T4 GPU (16GB VRAM).

# %%
from trl import SFTTrainer
from transformers import TrainingArguments

# ─── Training Configuration ───────────────────────────────
OUTPUT_DIR = "/content/drive/MyDrive/cybersec-llama2-finetuned"
NUM_EPOCHS = 3
BATCH_SIZE = 2               # Per-device batch size
GRAD_ACCUM_STEPS = 4         # Effective batch size = 2 * 4 = 8
LEARNING_RATE = 2e-4
WARMUP_STEPS = 50
SAVE_STEPS = 200
LOGGING_STEPS = 25
# ───────────────────────────────────────────────────────────

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=MAX_SEQ_LENGTH,
    dataset_num_proc=2,
    packing=False,               # True can speed up training for short sequences
    args=TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM_STEPS,
        learning_rate=LEARNING_RATE,
        warmup_steps=WARMUP_STEPS,
        save_steps=SAVE_STEPS,
        logging_steps=LOGGING_STEPS,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        save_total_limit=3,      # Keep only last 3 checkpoints to save space
        report_to="none",        # Disable wandb/tensorboard
    ),
)

print("✅ Trainer configured")
print(f"   Epochs: {NUM_EPOCHS}")
print(f"   Effective batch size: {BATCH_SIZE * GRAD_ACCUM_STEPS}")
print(f"   Learning rate: {LEARNING_RATE}")
print(f"   Output: {OUTPUT_DIR}")

# %% [markdown]
# ## Step 7: Check GPU Memory Before Training

# %%
gpu_stats = torch.cuda.get_device_properties(0)
start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
max_memory = round(gpu_stats.total_mem / 1024 / 1024 / 1024, 3)

print(f"🖥️  GPU: {gpu_stats.name}")
print(f"   Total VRAM: {max_memory} GB")
print(f"   Currently reserved: {start_gpu_memory} GB")
print(f"   Available for training: {max_memory - start_gpu_memory:.1f} GB")

# %% [markdown]
# ## Step 8: 🚀 Start Training!
# This is the main training loop. On a T4 with 5000 examples:
# - **~1.5–3 hours** for 3 epochs
# - Progress bar will update every 25 steps

# %%
print("🚀 Starting fine-tuning...")
print("=" * 60)

trainer_stats = trainer.train()

print("=" * 60)
print("✅ Training complete!")
print(f"   Total training time: {trainer_stats.metrics['train_runtime'] / 60:.1f} minutes")
print(f"   Final loss: {trainer_stats.metrics['train_loss']:.4f}")

# Show final GPU stats
used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
print(f"   Peak VRAM usage: {used_memory} GB / {max_memory} GB")

# %% [markdown]
# ## Step 9: 💾 Save the Fine-Tuned Model
# We save the LoRA adapters to Google Drive. These are small (~100MB)
# and can be loaded with Ollama or merged into the full model later.

# %%
# Save LoRA adapters (small, portable)
LORA_OUTPUT = "/content/drive/MyDrive/cybersec-llama2-lora"

model.save_pretrained(LORA_OUTPUT)
tokenizer.save_pretrained(LORA_OUTPUT)

print(f"✅ LoRA adapters saved to: {LORA_OUTPUT}")

# Also save merged model in GGUF format for use with Ollama
GGUF_OUTPUT = "/content/drive/MyDrive/cybersec-llama2-gguf"

model.save_pretrained_gguf(
    GGUF_OUTPUT,
    tokenizer,
    quantization_method="q4_k_m",  # Good balance of quality and size
)

print(f"✅ GGUF model saved to: {GGUF_OUTPUT}")
print(f"   Format: Q4_K_M (recommended for Ollama)")

# %% [markdown]
# ## Step 10: 🧪 Test the Fine-Tuned Model
# Let's ask the model a cybersecurity question to see how it responds!

# %%
FastLanguageModel.for_inference(model)  # Switch to fast inference mode

# Test prompt
test_question = "How would you detect lateral movement using Windows Event ID correlation in an enterprise environment?"

prompt = (
    f"<s>[INST] <<SYS>>\n"
    f"You are an advanced AI assistant specialized in cybersecurity causal reasoning and threat analysis.\n"
    f"<</SYS>>\n\n"
    f"{test_question} [/INST] "
)

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1,
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("=" * 60)
print("🛡️  CYBERSECURITY AI ASSISTANT — TEST")
print("=" * 60)
print(f"\n❓ Question: {test_question}")
print(f"\n💡 Response:\n{response.split('[/INST]')[-1].strip()}")

# %% [markdown]
# ## ✅ Done!
#
# Your fine-tuned model has been saved to Google Drive:
#
# | File | Path | Use |
# |------|------|-----|
# | LoRA adapters | `cybersec-llama2-lora/` | For further training or merging |
# | GGUF model | `cybersec-llama2-gguf/` | For Ollama (local deployment) |
#
# ### 🏠 To use with Ollama locally:
# 1. Download `cybersec-llama2-gguf/` from Google Drive to your PC
# 2. Create a Modelfile:
#    ```
#    FROM ./unsloth.Q4_K_M.gguf
#    SYSTEM "You are an advanced AI assistant specialized in cybersecurity..."
#    ```
# 3. Run: `ollama create cybersec-assistant -f Modelfile`
# 4. Chat: `ollama run cybersec-assistant`
