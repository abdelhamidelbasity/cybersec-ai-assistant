"""
=============================================================
  Dataset Preparation Script for Fine-Tuning Llama-2-7B
=============================================================
  Run this LOCALLY before uploading to Google Colab.
  It takes the large JSONL file and creates a smaller,
  clean training file.

  Usage:
    python prep_dataset.py
=============================================================
"""

import json
import random
import os

# ─── Configuration ────────────────────────────────────────
INPUT_FILE = "CyberSec-Dataset_escaped.jsonl"
OUTPUT_FILE = "cybersec_train_5000.jsonl"
SAMPLE_SIZE = 5000       # Number of examples to use for training
MAX_TOTAL_LENGTH = 8000  # Skip entries where system+user+assistant > this many chars
SEED = 42
# ──────────────────────────────────────────────────────────

def load_jsonl(path):
    """Load all lines from a JSONL file."""
    data = []
    skipped = 0
    print(f"📂 Loading {path}...")
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                # Validate required keys
                if "system" in obj and "user" in obj and "assistant" in obj:
                    data.append(obj)
                else:
                    skipped += 1
            except json.JSONDecodeError:
                skipped += 1
            
            if (i + 1) % 10000 == 0:
                print(f"   ...processed {i + 1} lines")
    
    print(f"✅ Loaded {len(data)} valid entries (skipped {skipped})")
    return data


def filter_quality(data, max_len):
    """Filter out entries that are too long or too short."""
    filtered = []
    for item in data:
        total_len = len(item["system"]) + len(item["user"]) + len(item["assistant"])
        # Skip very short answers (likely bad data)
        if len(item["assistant"]) < 100:
            continue
        # Skip overly long entries (would exceed context window)
        if total_len > max_len:
            continue
        filtered.append(item)
    
    print(f"🔍 After quality filter: {len(filtered)} entries (removed {len(data) - len(filtered)})")
    return filtered


def format_for_llama2(item):
    """
    Convert to Llama-2 chat format.
    
    Format:
    <s>[INST] <<SYS>>
    {system}
    <</SYS>>

    {user} [/INST] {assistant} </s>
    """
    system_msg = item["system"].strip()
    user_msg = item["user"].strip()
    assistant_msg = item["assistant"].strip()
    
    # Unescape the double-escaped newlines in the assistant output
    assistant_msg = assistant_msg.replace("\\\\n", "\n")
    
    text = (
        f"<s>[INST] <<SYS>>\n"
        f"{system_msg}\n"
        f"<</SYS>>\n\n"
        f"{user_msg} [/INST] {assistant_msg} </s>"
    )
    
    return {"text": text}


def main():
    print("=" * 60)
    print("  CyberSec Dataset Preparation for Llama-2 Fine-Tuning")
    print("=" * 60)
    print()
    
    # 1. Load
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found in current directory!")
        print(f"   Make sure you run this script from the same folder as the dataset.")
        return
    
    data = load_jsonl(INPUT_FILE)
    
    # 2. Filter
    data = filter_quality(data, MAX_TOTAL_LENGTH)
    
    # 3. Sample
    random.seed(SEED)
    if len(data) > SAMPLE_SIZE:
        data = random.sample(data, SAMPLE_SIZE)
        print(f"🎲 Randomly sampled {SAMPLE_SIZE} entries")
    else:
        print(f"ℹ️  Using all {len(data)} entries (less than requested {SAMPLE_SIZE})")
    
    # 4. Format for Llama-2
    formatted = [format_for_llama2(item) for item in data]
    
    # 5. Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in formatted:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print()
    print(f"✅ Saved {len(formatted)} training examples to: {OUTPUT_FILE}")
    print(f"   File size: {file_size_mb:.1f} MB")
    print()
    print("=" * 60)
    print("  NEXT STEPS:")
    print(f"  1. Upload '{OUTPUT_FILE}' to your Google Drive")
    print("  2. Open the Colab notebook and run it!")
    print("=" * 60)


if __name__ == "__main__":
    main()
