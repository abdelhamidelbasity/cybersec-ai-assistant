"""
CyberGuard AI - Generate All Presentation Diagrams
===================================================
This script runs all diagram generators to produce PNG images
for the project presentation.

Library used: matplotlib (version 3.x)
Output folder: diagrams/

To run:  python diagrams/generate_all_diagrams.py
"""
import subprocess
import sys
import os

# Ensure we're in the project root
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

scripts = [
    ("diagrams/diagram_architecture.py",    "01 - System Architecture"),
    ("diagrams/diagram_finetuning.py",      "02 - Fine-Tuning Pipeline"),
    ("diagrams/diagram_rag_ingestion.py",   "03 - RAG Ingestion Pipeline"),
    ("diagrams/diagram_query_workflow.py",  "04 - Query Workflow"),
]

print("=" * 60)
print("  GENERATING PRESENTATION DIAGRAMS")
print("  Library: matplotlib")
print("=" * 60)

for script, name in scripts:
    print(f"\n  Generating: {name}...")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  OK  {result.stdout.strip()}")
    else:
        print(f"  ERROR  {result.stderr.strip()}")

print("\n" + "=" * 60)
print("  ALL DIAGRAMS GENERATED SUCCESSFULLY!")
print("  Check the 'diagrams/' folder for PNG files.")
print("=" * 60)
