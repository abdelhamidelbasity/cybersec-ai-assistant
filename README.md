# 🛡️ Cybersecurity AI Assistant

A ready-to-use AI assistant specialized in cybersecurity, powered by a **fine-tuned Llama-2** model with **RAG** (Retrieval-Augmented Generation).

Ask it about threats, vulnerabilities, attacks, incident response — in **English, French, or Arabic**.

---

## 🚀 Quick Start

### Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)
- [Ollama](https://ollama.com/) installed and running
- [Git LFS](https://git-lfs.com/) (to download the model file)

### 1. Clone & Install
```bash
git lfs install
git clone https://github.com/abdelhamidelbasity/cybersec-ai-assistant.git
cd cybersec-ai-assistant

python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Load the Model into Ollama
```bash
ollama create cybersec-assistant -f Modelfile
```
This uses the included `cybersec-lora.gguf` fine-tuned model.

### 3. Run the Web App
```bash
python app.py
```
Then open your browser at **http://127.0.0.1:5000**

---

## 📖 Usage

### Web Interface (Recommended)
Run `python app.py` — a clean chat interface where you can:
- Ask cybersecurity questions
- Upload PDF/TXT documents for the AI to reference
- Adjust settings (temperature, language)

### CLI Mode
```bash
python rag_bot.py
```
Chat directly in the terminal.

### Add Your Own Documents
Place PDF or TXT files in the `data/` folder, then either:
- Use the upload button in the web interface, or
- Run `python ingest.py` to process all files at once

### Test the Model
```bash
python test_model.py
```

---

## 📁 Project Structure
```
├── app.py              # Flask web application
├── ingest.py           # Document ingestion into vector DB
├── rag_bot.py          # CLI chat interface
├── test_model.py       # Quick model test
├── Modelfile           # Ollama model configuration
├── cybersec-lora.gguf  # Fine-tuned model weights (Git LFS)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web UI
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
├── data/               # Place your documents here
└── RUN_GUIDE.md        # Detailed run instructions
```

---

## ⚡ How It Works
1. **You ask a question** via the web UI or CLI
2. **RAG retrieves** relevant chunks from your documents (ChromaDB)
3. **Fine-tuned Llama-2** generates a structured cybersecurity analysis using the context
4. **You get** a professional response with sources

---

## 🛠️ Requirements
- Python 3.10+
- Ollama running locally
- ~200MB disk space for the model
- 8GB+ RAM recommended

---

© 2026 Cybersecurity AI Assistant — Built by Abdelhamid El Basity