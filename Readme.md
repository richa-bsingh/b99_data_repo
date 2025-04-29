# Brooklyn Nine‑Nine RAG Assistant

A Retrieval‑Augmented Generation (RAG) chatbot that answers your questions about Brooklyn Nine‑Nine **in character**, quoting directly from episode transcripts.

## 🚀 Features

- Ingests **all episodes** from a unified JSON dump.
- Splits dialogues into overlapping chunks for better context.
- Embeds and indexes with **Chroma** (local) or swap in Pinecone/Milvus.
- Answers questions as Jake Peralta or Captain Holt, citing episode codes.
- Simple Streamlit UI—no frontend fuss.

## 🔧 Prerequisites

- Python 3.9+
- An OpenAI API key

## 📥 Setup

1. **Clone:**
   ```bash
   git clone https://github.com/yourusername/brooklyn99-assistant.git
   cd brooklyn99-assistant
   ```

2. **Install:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Env vars:**
   ```bash
   cp .env.example .env
   # then edit .env with your OPENAI_API_KEY
   ```

## 🛠️ Workflow

1. **Place** your `unified-dump.json` (with `"episodes": [...]`) into `data/`.
2. **Ingest & index**:
   ```bash
   python src/embed_and_index.py
   ```
3. **Run the app**:
   ```bash
   streamlit run src/app.py
   ```
4. **Ask** any B99 question and get in‑character, quote‑backed answers!

## 🐳 Docker

Build and run with Docker:

```bash
docker build -t brooklyn99-assistant .
docker run -p 8501:8501 --env-file .env brooklyn99-assistant
```

local setup:
python3.12 -m venv .venv                                               
source .venv/bin/activate 
pip install -r requirements.txt  
python -m streamlit run src/app.py

## ⚙️ Customization

- **Vector DB**: Swap `Chroma` for Pinecone/Milvus in `embed_and_index.py` & `rag_chain.py`.
- **Character styles**: Tweak the prompt template in `rag_chain.py` to add Rosa, Boyle, etc.
- **UI**: Replace Streamlit with Flask + React for a richer experience.

---

Enjoy cracking cases with your very own Nine‑Nine detective assistant! 🕵️‍♂️🎉
