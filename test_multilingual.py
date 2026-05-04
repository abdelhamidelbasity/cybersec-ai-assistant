import subprocess

# Test in French
test_question = "Comment détecter une attaque par force brute sur un serveur SSH ?"

print("=" * 60)
print("[CYBERSECURITY AI ASSISTANT -- MULTILINGUAL TEST]")
print("=" * 60)
print(f"Question (French): {test_question}\n")
print("Generating response...")
print("-" * 60)

# Run ollama using subprocess
# Using a 2-minute timeout just in case CPU inference takes a bit
try:
    result = subprocess.run(
        ["ollama", "run", "cybersec-assistant", test_question], 
        capture_output=True, 
        text=True,
        timeout=300 
    )

    if result.returncode == 0:
        print(result.stdout)
    else:
        print("❌ Error running model:")
        print(result.stderr)
except subprocess.TimeoutExpired:
    print("⚠️  Warning: Inference is taking a long time on CPU. You can check the output manually in your terminal with 'ollama run cybersec-assistant'.")

print("=" * 60)
