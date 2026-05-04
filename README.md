# 🛡️ Cybersecurity AI Assistant (Web App + RAG)

An advanced AI assistant specialized in cybersecurity, combining **Retrieval-Augmented Generation (RAG)** for real-time knowledge and a fine-tuned model for specialized security analysis.

## 🎯 Project Overview
This project provides a specialized web-based assistant that:
- Answers complex questions about cybersecurity threats, attacks, and vulnerabilities.
- Utilizes local documents (PDF/TXT) via RAG for context-aware responses.
- Uses a fine-tuned **Llama-2** model to ensure structured, professional security analysis.

## 🚀 Key Features
- **Knowledge Retrieval**: Built-in system to upload and index security documents.
- **Web Interface**: Modern, interactive chat UI for seamless communication.
- **Ollama Integration**: Runs locally using Ollama for privacy and speed.
- **Multilingual**: Supports security analysis in multiple languages.

## 📁 Project Structure
- `app.py`: Main Flask application (handles Chat API and Document Management).
- `templates/` & `static/`: Frontend UI assets.
- `Modelfile`: Configuration for the Ollama model.
- `requirements.txt`: Python dependencies.
- `test_model.py`: Utility to test model connectivity.

## 🛠️ Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/abdelhamidelbasity/cybersec-ai-assistant.git
   cd cybersec-ai-assistant
   ```

2. **Set up Virtual Environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Ollama**:
   Ensure [Ollama](https://ollama.com/) is installed and running.

4. **Prepare the Model**:
   Ensure you have your fine-tuned GGUF model and create the assistant:
   ```bash
   ollama create cybersec-assistant -f Modelfile
   ```

## 📖 Usage
1. **Start the Web App**:
   ```bash
   python app.py
   ```
2. **Access the UI**: Visit `http://127.0.0.1:5000` in your browser.
3. **Upload Docs**: Use the "Documents" tab to upload PDF or TXT files to give the AI specific knowledge.

## ⚖️ License
This project is for educational and research purposes in cybersecurity.

---
© 2026 Cybersecurity AI Assistant Project
