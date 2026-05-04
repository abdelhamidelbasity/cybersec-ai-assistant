import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"

def main():
    print("=" * 60)
    print("📚 CYBERSECURITY RAG - DOCUMENT INGESTION")
    print("=" * 60)

    # 1. Load documents
    print(f"\n📂 Looking for documents in '{DATA_DIR}'...")
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"   Created '{DATA_DIR}' directory. Please add PDF or TXT files and run again.")
        return

    # Load PDFs and TXTs
    pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    txt_loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader)

    docs = []
    try:
        docs.extend(pdf_loader.load())
    except Exception as e:
        print(f"   Warning loading PDFs: {e}")
        
    try:
        docs.extend(txt_loader.load())
    except Exception as e:
        print(f"   Warning loading TXTs: {e}")

    if not docs:
        print("❌ No documents found! Please put PDF or TXT files inside the 'data' folder.")
        return

    print(f"✅ Loaded {len(docs)} document pages/files.")

    # 2. Split text into chunks
    print("\n✂️  Splitting documents into smaller chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} text chunks.")

    # 3. Create Embeddings and Store in Vector DB
    print("\n🧠 Generating embeddings and saving to Vector DB (Chroma)...")
    print("   (This might take a few moments depending on the number of documents)")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Save to disk
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    
    print(f"\n✅ SUCCESSFULLY INGESTED! Vector database saved in '{CHROMA_DIR}'.")
    print("=" * 60)

if __name__ == "__main__":
    main()
