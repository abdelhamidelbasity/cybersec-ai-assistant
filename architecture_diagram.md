# CyberGuard AI - System Architecture

This diagram illustrates the complete workflow of the AI CyberSecurity Assistant, from when the user types a message in the Web Interface, to how the RAG (Retrieval-Augmented Generation) system pulls data, down to the final AI processing.

```mermaid
graph TD
    %% Styling definitions
    classDef userBase fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff
    classDef webBase fill:#1e293b,stroke:#475569,stroke-width:2px,color:#fff
    classDef ragBase fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    classDef llmBase fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
    
    %% User Node
    User((👤 You)):::userBase

    %% Web UI Environment
    subgraph "🌐 Web User Interface (Frontend)"
        Browser["🖥️ Browser\n(HTML / CSS / JS)"]:::webBase
        ChatUI["💬 Chat Box\n(Script.js fetches Data)"]:::webBase
    end

    %% Flask Application Environment
    subgraph "⚙️ Application Server (Backend)"
        Flask["🐍 Flask Server\n(app.py / REST API)"]:::webBase
        Router["🔀 Route: /api/chat"]:::webBase
    end

    %% Knowledge Base / RAG Component
    subgraph "📚 RAG Knowledge Base"
        Ingest["📥 ingest.py\n(Loads & Splits PDFs)"]:::ragBase
        EmbedModel["🧮 nomic-embed-text\n(Converts Text to Numbers)"]:::ragBase
        ChromaDB[("📂 ChromaDB\n(Local Vector Database)")]:::ragBase
    end

    %% AI Core
    subgraph "🧠 Artificial Intelligence Core"
        Prompt["📝 Prompt Template\n(Combines Rules + Question + Context)"]:::llmBase
        Ollama["⚙️ Ollama Engine\n(Runs Models Locally)"]:::llmBase
        FineTunedModel["🛡️ CyberSec-Llama-2\n(Base Model + LoRA Adapter)"]:::llmBase
    end

    %% Workflow Connections
    User -- "1. Asks a question" --> Browser
    Browser -- "Displays UI" --> ChatUI
    ChatUI -- "2. Sends JSON Request (fetch)" --> Router
    Router -- "3. Forwards Query" --> Flask
    
    %% RAG Data flow
    Ingest -. "Pre-processes Docs" .-> EmbedModel
    EmbedModel -. "Saves 🔢 Embeddings" .-> ChromaDB
    
    %% Query Flow
    Flask -- "4. Searches for Matches" --> ChromaDB
    ChromaDB -- "5. Returns Similar Text Chunks" --> Flask
    
    Flask -- "6. Combines Chunks & Query" --> Prompt
    Prompt -- "7. Sends Structured Prompt" --> Ollama
    
    Ollama -- "Executes" --> FineTunedModel
    FineTunedModel -- "8. Generates Contextual Answer" --> Ollama
    
    Ollama -- "9. Returns Analysis" --> Flask
    Flask -- "10. Sends JSON Response" --> ChatUI
    ChatUI -- "11. Renders Markdown & Animations" --> User
```

## Key Interactions Explained:
- **🟢 RAG Pathway (Green):** Before the AI answers you, the system searches your `chroma_db` for relevant paragraphs from your loaded PDFs.
- **🟣 AI Core (Purple):** The prompt restricts the AI to act specifically as a cybersecurity expert, applying your fine-tuned `LoRA` parameters safely inside the `Ollama` engine.
- **⚪ Web Server (Dark):** The entire process stays fully local and secure via the Python Flask server that ties the Frontend UI to the Deep Learning engines.
