"""
Converts the finetune_llama2_colab.py script into a proper
.ipynb notebook file that Google Colab can open.
"""
import json

cells = []

# --- Cell 1: Title (Markdown) ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# \ud83d\udee1\ufe0f Cybersecurity AI Assistant \u2014 Fine-Tuning Llama-2-7B with Unsloth\n",
        "\n",
        "This notebook fine-tunes **Llama-2-7B** on a cybersecurity Q&A dataset using **Unsloth** (2x faster, 70% less VRAM) with **QLoRA**.\n",
        "\n",
        "**Requirements:** Google Colab with a **T4 GPU** (free tier works!)\n",
        "\n",
        "---"
    ]
})

# --- Cell 2: Install Dependencies ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 1: Install Dependencies\n", "This installs Unsloth and all required libraries. Takes ~3 minutes."]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "%%capture\n",
        "!pip install \"unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git\"\n",
        "!pip install --no-deps \"xformers<0.0.27\" \"trl<0.9.0\" peft accelerate bitsandbytes"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 3: Mount Google Drive ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 2: Mount Google Drive\n", "Your training dataset (`cybersec_train_5000.jsonl`) must be in your Google Drive."]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/drive')\n",
        "\n",
        "# Set the path to your dataset file in Google Drive\n",
        "# \u26a0\ufe0f CHANGE THIS PATH if you put the file in a different folder!\n",
        "DATASET_PATH = \"/content/drive/MyDrive/cybersec_train_5000.jsonl\"\n",
        "\n",
        "import os\n",
        "if os.path.exists(DATASET_PATH):\n",
        "    print(f\"\u2705 Dataset found: {DATASET_PATH}\")\n",
        "    size_mb = os.path.getsize(DATASET_PATH) / (1024 * 1024)\n",
        "    print(f\"   Size: {size_mb:.1f} MB\")\n",
        "else:\n",
        "    print(f\"\u274c Dataset NOT found at: {DATASET_PATH}\")\n",
        "    print(\"   Please upload 'cybersec_train_5000.jsonl' to your Google Drive root folder.\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 4: Load Model ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 3: Load the Model with Unsloth\n", "We load Llama-2-7B in **4-bit quantization** (QLoRA) to fit in the T4's 16GB VRAM."]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "from unsloth import FastLanguageModel\n",
        "import torch\n",
        "\n",
        "# --- Model Configuration ---\n",
        "MODEL_NAME = \"unsloth/llama-2-7b-bnb-4bit\"  # Pre-quantized Llama-2-7B\n",
        "MAX_SEQ_LENGTH = 4096   # Maximum context length\n",
        "DTYPE = None             # Auto-detect (float16 for T4)\n",
        "LOAD_IN_4BIT = True      # Use 4-bit quantization (saves VRAM)\n",
        "\n",
        "model, tokenizer = FastLanguageModel.from_pretrained(\n",
        "    model_name=MODEL_NAME,\n",
        "    max_seq_length=MAX_SEQ_LENGTH,\n",
        "    dtype=DTYPE,\n",
        "    load_in_4bit=LOAD_IN_4BIT,\n",
        ")\n",
        "\n",
        "print(f\"\u2705 Model loaded: {MODEL_NAME}\")\n",
        "print(f\"   Max sequence length: {MAX_SEQ_LENGTH}\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 5: Add LoRA ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 4: Add LoRA Adapters\n", "LoRA lets us fine-tune only a small fraction of the model's weights, making training fast and memory-efficient."]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "model = FastLanguageModel.get_peft_model(\n",
        "    model,\n",
        "    r=16,                          # LoRA rank\n",
        "    target_modules=[\n",
        "        \"q_proj\", \"k_proj\", \"v_proj\", \"o_proj\",\n",
        "        \"gate_proj\", \"up_proj\", \"down_proj\",\n",
        "    ],\n",
        "    lora_alpha=16,\n",
        "    lora_dropout=0,\n",
        "    bias=\"none\",\n",
        "    use_gradient_checkpointing=\"unsloth\",\n",
        "    random_state=3407,\n",
        "    use_rslora=False,\n",
        "    loftq_config=None,\n",
        ")\n",
        "\n",
        "print(\"\u2705 LoRA adapters added\")\n",
        "model.print_trainable_parameters()"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 6: Load Dataset ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 5: Load and Prepare the Dataset"]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "from datasets import load_dataset\n",
        "\n",
        "dataset = load_dataset(\"json\", data_files=DATASET_PATH, split=\"train\")\n",
        "\n",
        "print(f\"\u2705 Dataset loaded: {len(dataset)} training examples\")\n",
        "print(f\"\\n\ud83d\udccb Sample entry (first 500 chars):\")\n",
        "print(dataset[0][\"text\"][:500])\n",
        "print(\"...\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 7: Configure Training ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 6: Configure Training\n", "These settings are optimized for a Colab T4 GPU (16GB VRAM)."]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "from trl import SFTTrainer\n",
        "from transformers import TrainingArguments\n",
        "\n",
        "# --- Training Configuration ---\n",
        "OUTPUT_DIR = \"/content/drive/MyDrive/cybersec-llama2-finetuned\"\n",
        "NUM_EPOCHS = 3\n",
        "BATCH_SIZE = 2\n",
        "GRAD_ACCUM_STEPS = 4\n",
        "LEARNING_RATE = 2e-4\n",
        "WARMUP_STEPS = 50\n",
        "SAVE_STEPS = 200\n",
        "LOGGING_STEPS = 25\n",
        "\n",
        "trainer = SFTTrainer(\n",
        "    model=model,\n",
        "    tokenizer=tokenizer,\n",
        "    train_dataset=dataset,\n",
        "    dataset_text_field=\"text\",\n",
        "    max_seq_length=MAX_SEQ_LENGTH,\n",
        "    dataset_num_proc=2,\n",
        "    packing=False,\n",
        "    args=TrainingArguments(\n",
        "        output_dir=OUTPUT_DIR,\n",
        "        num_train_epochs=NUM_EPOCHS,\n",
        "        per_device_train_batch_size=BATCH_SIZE,\n",
        "        gradient_accumulation_steps=GRAD_ACCUM_STEPS,\n",
        "        learning_rate=LEARNING_RATE,\n",
        "        warmup_steps=WARMUP_STEPS,\n",
        "        save_steps=SAVE_STEPS,\n",
        "        logging_steps=LOGGING_STEPS,\n",
        "        fp16=not torch.cuda.is_bf16_supported(),\n",
        "        bf16=torch.cuda.is_bf16_supported(),\n",
        "        optim=\"adamw_8bit\",\n",
        "        weight_decay=0.01,\n",
        "        lr_scheduler_type=\"linear\",\n",
        "        seed=3407,\n",
        "        save_total_limit=3,\n",
        "        report_to=\"none\",\n",
        "    ),\n",
        ")\n",
        "\n",
        "print(\"\u2705 Trainer configured\")\n",
        "print(f\"   Epochs: {NUM_EPOCHS}\")\n",
        "print(f\"   Effective batch size: {BATCH_SIZE * GRAD_ACCUM_STEPS}\")\n",
        "print(f\"   Learning rate: {LEARNING_RATE}\")\n",
        "print(f\"   Output: {OUTPUT_DIR}\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 8: GPU Check ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 7: Check GPU Memory Before Training"]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "gpu_stats = torch.cuda.get_device_properties(0)\n",
        "start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)\n",
        "max_memory = round(gpu_stats.total_mem / 1024 / 1024 / 1024, 3)\n",
        "\n",
        "print(f\"\ud83d\udda5\ufe0f  GPU: {gpu_stats.name}\")\n",
        "print(f\"   Total VRAM: {max_memory} GB\")\n",
        "print(f\"   Currently reserved: {start_gpu_memory} GB\")\n",
        "print(f\"   Available for training: {max_memory - start_gpu_memory:.1f} GB\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 9: Train! ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 8: \ud83d\ude80 Start Training!\n",
        "This is the main training loop. On a T4 with 5000 examples:\n",
        "- **~1.5\u20133 hours** for 3 epochs\n",
        "- Progress bar will update every 25 steps"
    ]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "print(\"\ud83d\ude80 Starting fine-tuning...\")\n",
        "print(\"=\" * 60)\n",
        "\n",
        "trainer_stats = trainer.train()\n",
        "\n",
        "print(\"=\" * 60)\n",
        "print(\"\u2705 Training complete!\")\n",
        "print(f\"   Total training time: {trainer_stats.metrics['train_runtime'] / 60:.1f} minutes\")\n",
        "print(f\"   Final loss: {trainer_stats.metrics['train_loss']:.4f}\")\n",
        "\n",
        "used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)\n",
        "print(f\"   Peak VRAM usage: {used_memory} GB / {max_memory} GB\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 10: Save Model ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 9: \ud83d\udcbe Save the Fine-Tuned Model\n",
        "We save the LoRA adapters and a GGUF model (for Ollama) to Google Drive."
    ]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "# Save LoRA adapters (small, portable)\n",
        "LORA_OUTPUT = \"/content/drive/MyDrive/cybersec-llama2-lora\"\n",
        "model.save_pretrained(LORA_OUTPUT)\n",
        "tokenizer.save_pretrained(LORA_OUTPUT)\n",
        "print(f\"\u2705 LoRA adapters saved to: {LORA_OUTPUT}\")\n",
        "\n",
        "# Save merged model in GGUF format for use with Ollama\n",
        "GGUF_OUTPUT = \"/content/drive/MyDrive/cybersec-llama2-gguf\"\n",
        "model.save_pretrained_gguf(\n",
        "    GGUF_OUTPUT,\n",
        "    tokenizer,\n",
        "    quantization_method=\"q4_k_m\",\n",
        ")\n",
        "print(f\"\u2705 GGUF model saved to: {GGUF_OUTPUT}\")\n",
        "print(f\"   Format: Q4_K_M (recommended for Ollama)\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 11: Test Model ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## Step 10: \ud83e\uddea Test the Fine-Tuned Model\n", "Let's ask the model a cybersecurity question to see how it responds!"]
})

cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": [
        "FastLanguageModel.for_inference(model)\n",
        "\n",
        "test_question = \"How would you detect lateral movement using Windows Event ID correlation in an enterprise environment?\"\n",
        "\n",
        "prompt = (\n",
        "    f\"<s>[INST] <<SYS>>\\n\"\n",
        "    f\"You are an advanced AI assistant specialized in cybersecurity causal reasoning and threat analysis.\\n\"\n",
        "    f\"<</SYS>>\\n\\n\"\n",
        "    f\"{test_question} [/INST] \"\n",
        ")\n",
        "\n",
        "inputs = tokenizer(prompt, return_tensors=\"pt\").to(\"cuda\")\n",
        "\n",
        "outputs = model.generate(\n",
        "    **inputs,\n",
        "    max_new_tokens=512,\n",
        "    temperature=0.7,\n",
        "    top_p=0.9,\n",
        "    repetition_penalty=1.1,\n",
        ")\n",
        "\n",
        "response = tokenizer.decode(outputs[0], skip_special_tokens=True)\n",
        "\n",
        "print(\"=\" * 60)\n",
        "print(\"\ud83d\udee1\ufe0f  CYBERSECURITY AI ASSISTANT \u2014 TEST\")\n",
        "print(\"=\" * 60)\n",
        "print(f\"\\n\u2753 Question: {test_question}\")\n",
        "print(f\"\\n\ud83d\udca1 Response:\\n{response.split('[/INST]')[-1].strip()}\")"
    ],
    "execution_count": None,
    "outputs": []
})

# --- Cell 12: Done ---
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## \u2705 Done!\n",
        "\n",
        "Your fine-tuned model has been saved to Google Drive:\n",
        "\n",
        "| File | Path | Use |\n",
        "|------|------|-----|\n",
        "| LoRA adapters | `cybersec-llama2-lora/` | For further training or merging |\n",
        "| GGUF model | `cybersec-llama2-gguf/` | For Ollama (local deployment) |\n",
        "\n",
        "### \ud83c\udfe0 To use with Ollama locally:\n",
        "1. Download `cybersec-llama2-gguf/` from Google Drive to your PC\n",
        "2. Create a Modelfile:\n",
        "   ```\n",
        "   FROM ./unsloth.Q4_K_M.gguf\n",
        "   SYSTEM \"You are an advanced AI assistant specialized in cybersecurity...\"\n",
        "   ```\n",
        "3. Run: `ollama create cybersec-assistant -f Modelfile`\n",
        "4. Chat: `ollama run cybersec-assistant`"
    ]
})

# Build the notebook
notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "colab": {
            "provenance": [],
            "gpuType": "T4"
        },
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python"
        },
        "accelerator": "GPU"
    },
    "cells": cells
}

output_path = "finetune_llama2_colab.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=True)

print(f"✅ Notebook saved: {output_path}")
print(f"   Cells: {len(cells)}")
print(f"   Upload this .ipynb file to Google Colab!")
