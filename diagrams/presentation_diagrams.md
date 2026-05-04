# 📊 عرض المشروع - المخططات والرسومات التوضيحية (Presentation Diagrams)

هذا الملف يحتوي على مجموعة من الرسوم البيانية (Diagrams) المصممة خصيصاً لعرضك التقديمي (Presentation) أمام الأستاذ. هذه المخططات تشرح كيف يعمل النظام من الداخل، وكيف تم بناؤه خطوة بخطوة.

يمكنك تصوير هذه المخططات (Screenshots) أو نسخ الكود الخاص بها إلى مواقع مثل [Mermaid Live Editor](https://mermaid.live/) لتحويلها إلى صور عالية الجودة وإضافتها إلى ملف الـ PowerPoint الخاص بك.

---

## 1. الهيكلة العامة للنظام (High-Level Architecture)
يشرح هذا المخطط المكونات الأساسية للمشروع وكيف تتواصل مع بعضها البعض (واجهة المستخدم، الخادم، قاعدة البيانات، ومحرك الذكاء الاصطناعي).

```mermaid
graph LR
    %% Styling
    classDef user fill:#3b82f6,stroke:#2563eb,color:#fff
    classDef backend fill:#1e293b,stroke:#475569,color:#fff
    classDef ai fill:#8b5cf6,stroke:#7c3aed,color:#fff
    classDef db fill:#10b981,stroke:#059669,color:#fff

    User([👤 User / Security Analyst]):::user <--> |HTTP / JSON| WebUI[🌐 Flask Web App\nFrontend & Backend]:::backend
    WebUI <--> |Orchestration| Langchain[🦜 Langchain\nFramework]:::backend
    
    subgraph "Secure Local Environment"
        Langchain --> |Semantic Search| ChromaDB[(📚 ChromaDB\nVector Database)]:::db
        Langchain --> |Inference| Ollama[⚙️ Ollama Engine]:::ai
        
        Ollama --> EmbedModel[🧮 nomic-embed-text\nEmbedding Model]:::ai
        Ollama --> LLM[🧠 CyberSec-Llama-2\nFine-Tuned LLM]:::ai
    end
```

---

## 2. مرحلة التدريب الدقيق (Fine-Tuning Workflow)
يشرح هذا المخطط كيف قمنا بأخذ نموذج أساسي (Llama-2) وتدريبه ليصبح خبيراً في الأمن السيبراني باستخدام تقنيات حديثة لتقليل استهلاك الموارد.

```mermaid
graph TD
    %% Styling
    classDef data fill:#f59e0b,stroke:#d97706,color:#fff
    classDef process fill:#3b82f6,stroke:#2563eb,color:#fff
    classDef model fill:#8b5cf6,stroke:#7c3aed,color:#fff

    Dataset[(📁 CyberSec Q&A Dataset\n5000+ Examples)]:::data --> Prep[Dataset Preparation & Formatting]:::process
    BaseModel[🤖 Llama-2 7B Base Model]:::model --> QLoRA[🛠️ QLoRA Adapter\nParameter-Efficient Tuning]:::process
    
    Prep --> Training[💻 Unsloth Training\non Google Colab GPU]:::process
    QLoRA --> Training
    
    Training --> LoRA_Weights[📦 Trained LoRA Weights]:::model
    BaseModel --> Merge[🔄 Merge & Quantize\nusing llama.cpp]:::process
    LoRA_Weights --> Merge
    
    Merge --> GGUF[⚙️ GGUF Format Model\nOptimized for CPU]:::model
    GGUF --> Deployment[🚀 Deployment via Ollama]:::process
```

---

## 3. خط أنابيب استيعاب البيانات (RAG Data Ingestion Pipeline)
يشرح كيف يتم إدخال مستندات الشركة (PDFs/TXTs) إلى النظام لتكوين قاعدة المعرفة الخاصة به.

```mermaid
graph TD
    %% Styling
    classDef docs fill:#f59e0b,stroke:#d97706,color:#fff
    classDef process fill:#3b82f6,stroke:#2563eb,color:#fff
    classDef db fill:#10b981,stroke:#059669,color:#fff

    RawDocs[📄 PDF & TXT Documents\nin 'data/' folder]:::docs --> Loader[📥 Langchain Document Loaders]:::process
    Loader --> Splitter[✂️ Text Splitter\nDivide into 800-char chunks]:::process
    
    Splitter --> Embeddings[🔢 Vector Embeddings\nvia nomic-embed-text]:::process
    
    Embeddings --> VectorDB[(💾 ChromaDB\nLocal Vector Store)]:::db
```

---

## 4. تدفق معالجة الأسئلة (RAG Query Workflow)
رسم تسلسلي (Sequence Diagram) يوضح خطوة بخطوة ما يحدث منذ أن يسأل المستخدم سؤالاً حتى يحصل على الإجابة المعززة بالمصادر.

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant App as 🌐 Flask App (app.py)
    participant Chroma as 📚 ChromaDB
    participant Model as 🧠 CyberSec LLM
    
    User->>App: 1. Asks a Cybersecurity Question
    App->>Chroma: 2. Search for similar text (Embeddings)
    Chroma-->>App: 3. Returns Top 3 Relevant Chunks
    
    Note over App: 4. Construct Prompt:<br/>[System Rules] + [Retrieved Chunks] + [User Question]
    
    App->>Model: 5. Send Prompt for Inference
    Note over Model: 6. Model generates answer<br/>restricted by system rules & context
    Model-->>App: 7. Return Structured Analysis
    
    App-->>User: 8. Display Answer + Citation Sources
```

---

## 💡 نصائح للعرض أمام الأستاذ:
1. **ركز على الـ RAG:** اشرح للأستاذ أن الميزة القوية في مشروعك هي أنه لا يختلق إجابات، بل يبحث في ملفات حقيقية (PDFs) ويستخرج منها الجواب.
2. **ركز على الخصوصية (Privacy-Preserving):** أشر إلى أن كل شيء يعمل محلياً (Local-first) 100%، ولا يتم إرسال أي بيانات حساسة إلى سيرفرات خارجية (مثل OpenAI)، مما يجعله مثالياً للشركات.
3. **ركز على تقنية التدريب (QLoRA):** وضح كيف استطعت تدريب نموذج عملاق (7 مليار بارامتر) بأقل تكلفة وموارد باستخدام تقنية QLoRA.
