# 🛡️ Cybersecurity AI Assistant — Training Guide

## Overview

This guide walks you through fine-tuning **Llama-2-7B** on a cybersecurity Q&A dataset using **Unsloth** on **Google Colab** (free T4 GPU).

---

## 📁 Files in This Project

| File | What it does | Run where? |
|------|-------------|------------|
| `CyberSec-Dataset_escaped.jsonl` | Raw dataset (84K entries, ~344MB) | — |
| `prep_dataset.py` | Samples 5000 entries and formats for Llama-2 | **Your PC** |
| `cybersec_train_5000.jsonl` | Training-ready dataset (created by prep script) | Upload to Drive |
| `finetune_llama2_colab.py` | Complete training script for Colab | **Google Colab** |

---

## 🚀 Step-by-Step Instructions

### Step 1: Prepare the Dataset (on your PC)

Open a terminal in your project folder and run:

```bash
cd "c:\Users\GSI\OneDrive\Scans\rapport project"
python prep_dataset.py
```

This will create `cybersec_train_5000.jsonl` (~20-40MB), a smaller file ready for training.

---

### Step 2: Upload to Google Drive

1. Go to [Google Drive](https://drive.google.com)
2. Upload `cybersec_train_5000.jsonl` to the **root** of your Google Drive (My Drive)

> ⚠️ If you put it in a subfolder, update the `DATASET_PATH` variable in the Colab script.

---

### Step 3: Open the Training Script in Colab

**Option A — Upload .py file:**
1. Go to [Google Colab](https://colab.research.google.com)
2. Click **File → Upload notebook**
3. Upload `finetune_llama2_colab.py`
4. Colab will automatically convert it into a notebook with cells

**Option B — Create new notebook and paste:**
1. Create a new Colab notebook
2. Copy each cell from the `.py` file (separated by `# %%` markers)

---

### Step 4: Enable GPU in Colab

1. In Colab, go to **Runtime → Change runtime type**
2. Select **T4 GPU** (available in the free tier)
3. Click **Save**

---

### Step 5: Run All Cells

1. Click **Runtime → Run all** or run each cell one by one
2. When prompted, authorize Google Drive access
3. Training will take approximately **1.5–3 hours** on a T4 GPU

---

### Step 6: Download Your Model

After training completes, you'll find two folders in your Google Drive:

| Folder | Size | Use |
|--------|------|-----|
| `cybersec-llama2-lora/` | ~100MB | LoRA adapter weights (for further training) |
| `cybersec-llama2-gguf/` | ~4GB | GGUF model file (for Ollama) |

---

### Step 7: Use with Ollama (on your PC)

1. Download the `cybersec-llama2-gguf/` folder from Google Drive
2. Find the `.gguf` file inside it (e.g., `unsloth.Q4_K_M.gguf`)
3. Create a file called `Modelfile` in the same folder:

```
FROM ./unsloth.Q4_K_M.gguf

SYSTEM """You are an advanced AI assistant specialized in cybersecurity causal reasoning and threat analysis. You provide structured analysis covering attack mechanisms, evidence assessment, temporal dynamics, and practical security recommendations."""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
```

4. Open a terminal and run:

```bash
ollama create cybersec-assistant -f Modelfile
ollama run cybersec-assistant
```

5. 🎉 Ask it cybersecurity questions!

---

## ⚙️ Configuration Reference

You can tweak these values in the training script:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SAMPLE_SIZE` (prep script) | 5000 | Number of training examples |
| `NUM_EPOCHS` | 3 | Training passes over the data |
| `BATCH_SIZE` | 2 | Samples per GPU step |
| `GRAD_ACCUM_STEPS` | 4 | Effective batch = 2×4 = 8 |
| `LEARNING_RATE` | 2e-4 | How fast the model learns |
| `r` (LoRA rank) | 16 | Adapter capacity (8/16/32) |
| `MAX_SEQ_LENGTH` | 4096 | Max tokens per example |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "CUDA out of memory" | Reduce `BATCH_SIZE` to 1 or `MAX_SEQ_LENGTH` to 2048 |
| "Dataset not found" | Check `DATASET_PATH` in the Colab script matches your Drive location |
| Training is very slow | Make sure GPU is enabled (Runtime → Change runtime type → T4) |
| Colab disconnects | Use Colab Pro, or re-run from the last checkpoint (saved every 200 steps) |
| Loss doesn't decrease | Try reducing `LEARNING_RATE` to 1e-4 |

---

## 📊 What to Expect

- **Training loss** should decrease from ~2.5 → ~0.8 over 3 epochs
- **Total training time**: ~1.5–3 hours on T4
- **Final model quality**: The model will produce structured cybersecurity analyses following the template in the dataset
