import subprocess

test_question = "How would you detect lateral movement using Windows Event ID correlation in an enterprise environment?"

print("=" * 60)
print("[CYBERSECURITY AI ASSISTANT -- TEST]")
print("=" * 60)
print(f"Question: {test_question}\n")
print("Generating response (this might take a few moments depending on your CPU)...")
print("-" * 60)

# Run ollama using subprocess
result = subprocess.run(
    ["ollama", "run", "cybersec-assistant", test_question], 
    capture_output=True, 
    text=True
)

if result.returncode == 0:
    print(result.stdout)
else:
    print("❌ Error running model:")
    print(result.stderr)

print("=" * 60)
