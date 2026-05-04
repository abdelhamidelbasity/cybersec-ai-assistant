import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# ==========================================
# Configuration
# ==========================================
DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "cybersec-assistant"
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# Mutable settings (can be changed via API)
settings = {
    "temperature": 0.3,
    "k": 3,
    "language": "auto"
}

# ==========================================
# RAG Setup (Loaded once at startup)
# ==========================================
print("System: Initializing Cybersecurity RAG...")
try:
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vector_db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": settings["k"]})

    llm = OllamaLLM(model=LLM_MODEL, temperature=settings["temperature"])

    TEMPLATE = """You are CyberGuard, an advanced cybersecurity AI assistant.
Below are pieces of context extracted from local documents. 
CRITICAL RULE: If the user's input is a simple greeting (like "hi", "hello", "bonjour", "salam") or casual conversation, IGNORE the context entirely and just respond naturally with a polite greeting. Do not mention phishing or any cybersecurity topic unless the user explicitly asks about it.
If the user DOES ask a cybersecurity question, use the context to help answer it and provide a Structured Analysis.
Always respond in the same language as the user.

Context: 
{context}

User Input: {question}

Response:"""
    print("System: RAG Initialized Successfully.")
except Exception as e:
    print(f"System Error: {e}")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_ingestion(filepath):
    """Ingest a single file into the vector database."""
    global vector_db, retriever
    try:
        ext = filepath.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            loader = PyPDFLoader(filepath)
        elif ext == 'txt':
            loader = TextLoader(filepath, encoding='utf-8')
        else:
            return False, "Unsupported file type"

        docs = loader.load()
        if not docs:
            return False, "No content found in file"

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR
        )
        retriever = vector_db.as_retriever(search_kwargs={"k": settings["k"]})

        return True, f"Ingested {len(chunks)} chunks"
    except Exception as e:
        return False, str(e)


def query_rag(user_question):
    try:
        docs = retriever.invoke(user_question)
        context_text = "\n\n".join([doc.page_content for doc in docs])

        prompt = TEMPLATE.format(context=context_text, question=user_question)
        answer = llm.invoke(prompt)

        sources = list(set([doc.metadata.get('source', 'Unknown') for doc in docs]))
        return {"answer": answer, "sources": sources, "error": False}
    except Exception as e:
        return {"answer": str(e), "sources": [], "error": True}


# ==========================================
# Routes — Pages
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')


# ==========================================
# Routes — Chat API
# ==========================================
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": True, "answer": "Message cannot be empty."}), 400

    result = query_rag(user_message)
    return jsonify(result)


# ==========================================
# Routes — File Management API
# ==========================================
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file provided."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Only PDF and TXT files are allowed."}), 400

    os.makedirs(DATA_DIR, exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(DATA_DIR, filename)
    file.save(filepath)

    # Auto-ingest into RAG
    success, msg = run_ingestion(filepath)
    if success:
        return jsonify({"success": True, "message": f"'{filename}' uploaded and ingested. {msg}."})
    else:
        return jsonify({"success": False, "message": f"File saved but ingestion failed: {msg}"}), 500


@app.route('/api/files', methods=['GET'])
def list_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    files = []
    for f in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, f)
        if os.path.isfile(fpath) and allowed_file(f):
            size = os.path.getsize(fpath)
            files.append({
                "name": f,
                "size": size,
                "size_display": f"{size / 1024:.1f} KB" if size < 1048576 else f"{size / 1048576:.1f} MB"
            })
    return jsonify({"files": files, "count": len(files)})


@app.route('/api/files/delete', methods=['POST'])
def delete_file():
    data = request.json
    filename = data.get('filename', '')
    if not filename:
        return jsonify({"success": False, "message": "No filename provided."}), 400

    filepath = os.path.join(DATA_DIR, secure_filename(filename))
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"success": True, "message": f"'{filename}' deleted."})
    else:
        return jsonify({"success": False, "message": "File not found."}), 404


@app.route('/api/files/download/<filename>')
def download_file(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)


@app.route('/api/ingest', methods=['POST'])
def ingest_all():
    """Run full RAG ingestion on ALL files in data/ folder."""
    global vector_db, retriever
    os.makedirs(DATA_DIR, exist_ok=True)

    all_docs = []
    processed = []
    errors = []

    for f in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, f)
        if not os.path.isfile(fpath) or not allowed_file(f):
            continue
        try:
            ext = f.rsplit('.', 1)[1].lower()
            if ext == 'pdf':
                loader = PyPDFLoader(fpath)
            elif ext == 'txt':
                loader = TextLoader(fpath, encoding='utf-8')
            else:
                continue
            docs = loader.load()
            all_docs.extend(docs)
            processed.append(f)
        except Exception as e:
            errors.append(f"{f}: {str(e)}")

    if not all_docs:
        return jsonify({"success": False, "message": "No documents found to ingest.", "processed": [], "errors": errors})

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(all_docs)

        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR
        )
        retriever = vector_db.as_retriever(search_kwargs={"k": settings["k"]})

        return jsonify({
            "success": True,
            "message": f"Successfully ingested {len(processed)} file(s) into {len(chunks)} chunks.",
            "processed": processed,
            "chunks": len(chunks),
            "errors": errors
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Ingestion failed: {str(e)}", "processed": [], "errors": errors}), 500


# ==========================================
# Routes — Settings API
# ==========================================
@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(settings)


@app.route('/api/settings', methods=['POST'])
def update_settings():
    global llm, retriever
    data = request.json

    if 'temperature' in data:
        settings['temperature'] = float(data['temperature'])
        llm = OllamaLLM(model=LLM_MODEL, temperature=settings['temperature'])

    if 'k' in data:
        settings['k'] = int(data['k'])
        retriever = vector_db.as_retriever(search_kwargs={"k": settings['k']})

    if 'language' in data:
        settings['language'] = data['language']

    return jsonify({"success": True, "settings": settings})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
