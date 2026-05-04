import argparse
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM

CHROMA_DIR = "chroma_db"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "cybersec-assistant" # Your fine-tuned model

def main():
    parser = argparse.ArgumentParser(description="Cybersecurity RAG Assistant")
    parser.add_argument("--test", action="store_true", help="Run a hardcoded test query")
    args = parser.parse_args()

    print("=" * 60)
    print("🛡️  INITIALIZING CYBERSECURITY RAG ASSISTANT...")
    print("=" * 60)

    # 1. Load Embeddings and Vector DB
    try:
        embeddings = OllamaEmbeddings(model=EMBED_MODEL)
        vector_db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
        retriever = vector_db.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 relevant chunks
        print("✅ Vector Database loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading Vector Database: {e}")
        print("   Did you run 'python ingest.py' first?")
        return

    # 2. Setup the LLM
    try:
        llm = OllamaLLM(model=LLM_MODEL, temperature=0.3)
        print("✅ LLM Model connected successfully.")
    except Exception as e:
        print(f"❌ Error connecting to LLM: {e}")
        return

    template_base = """You are CyberGuard, an advanced cybersecurity AI assistant.
Below are pieces of context extracted from local documents. 
CRITICAL RULE: If the user's input is a simple greeting (like "hi", "hello", "bonjour", "salam") or casual conversation, IGNORE the context entirely and just respond naturally with a polite greeting. Do not mention phishing or any cybersecurity topic unless the user explicitly asks about it.
If the user DOES ask a cybersecurity question, use the context to help answer it and provide a Structured Analysis.
Always respond in the same language as the user.

Context: 
{context}

User Input: {question}

Response:"""
    
    print("✅ RAG System ready.\n")

    def query_rag(user_question):
        # Retrieve context from ChromaDB
        docs = retriever.invoke(user_question)
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        # Format the prompt
        prompt = template_base.format(context=context_text, question=user_question)
        
        # Generate answer
        answer = llm.invoke(prompt)
        
        return answer, docs

    if args.test:
        question = "What vulnerabilities are mentioned in the documents?"
        print(f"❓ Test Question: {question}\n")
        print("⏳ Searching documents and generating answer...\n")
        
        answer, source_docs = query_rag(question)
        
        print(answer)
        print("\n---")
        print("📄 Sources used:")
        for doc in source_docs:
            print(f"- {doc.metadata.get('source', 'Unknown')} (Snippet: {doc.page_content[:100]}...)")
        
        return

    # Interactive Chat Loop
    print("💬 You can now chat! Type 'exit' or 'quit' to close.")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n👤 You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            if not user_input.strip():
                continue

            print("⏳ Thinking...")
            answer, source_docs = query_rag(user_input)
            
            print(f"\n🛡️  CyberSec AI:\n{answer}\n")
            
            print("---")
            print("📄 Sources:")
            sources = set([doc.metadata.get('source', 'Unknown') for doc in source_docs])
            if sources:
                for s in sources:
                    print(f"  - {s}")
            else:
                print("  - No direct sources found for this answer.")
            print("-" * 60)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error during generation: {e}")

    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
