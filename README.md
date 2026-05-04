# 🛡️ Cybersecurity AI Assistant (RAG + Fine-Tuning)

An advanced AI assistant specialized in cybersecurity, combining **Retrieval-Augmented Generation (RAG)** for real-time knowledge and **Fine-Tuning** for specialized behavior.

## 🎯 Project Overview
This project builds a specialized assistant that:
- Answers complex questions about cybersecurity threats, attacks, and vulnerabilities.
- Utilizes real-world documents (OWASP, CVE reports, security logs) for context.
- Uses a fine-tuned **Llama-2-7B** model (via Unsloth) to ensure structured, professional security analysis.

## 🧱 Architecture
The system follows a modern RAG pipeline:
1. **User Query**: Input via Web Interface or CLI.
2. **Knowledge Retrieval**: ChromaDB vector database retrieves relevant chunks from security documents.
3. **LLM Processing**: A fine-tuned Llama-2 model processes the query using the retrieved context.
4. **Structured Output**: Response covering mechanisms, evidence, and recommendations.

## 🚀 Key Features
- **Hybrid Knowledge**: Combines pre-trained wisdom with specific document-based knowledge.
- **Fine-tuned Logic**: Specifically trained on 5,000+ cybersecurity Q&A pairs for better reasoning.
- **Web Interface**: Clean, interactive UI for seamless communication.
- **Multilingual Support**: Optimized for both English and Arabic cybersecurity terminology.

## 📁 Project Structure
- `app.py`: Flask-based web application.
- `ingest.py`: Script to process and embed documents into the vector database.
- `rag_bot.py`: CLI-based interaction script.
- `scripts/`: Contains fine-tuning and dataset preparation scripts.
- `templates/` & `static/`: Frontend assets for the web UI.

## 🛠️ Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cybersec-ai-assistant.git
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
   Follow the [TRAINING_GUIDE.md](TRAINING_GUIDE.md) to fine-tune and export the model to GGUF format.

## 📖 Usage
- **Ingest Documents**: Place PDF/TXT files in `/data` and run `python ingest.py`.
- **Start Web App**: Run `python app.py` and visit `http://127.0.0.1:5000`.
- **CLI Mode**: Run `python rag_bot.py` for direct terminal chat.

## ⚖️ License
This project is for educational and research purposes in cybersecurity.

---
© 2026 Cybersecurity AI Assistant Project