# src/rag_chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from ingest import load_transcripts_from_json

# 1. Load docs + embeddings
docs = load_transcripts_from_json()
embeddings = OpenAIEmbeddings()

# 2. Use in-memory Qdrant (no SQLite, no server needed)
client = QdrantClient(":memory:")
vectorstore = Qdrant.from_documents(
    documents=docs,
    embedding=embeddings,
    client=client,
    collection_name="b99"
)

# 3. Prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are “99 Assistant,” an in‑character detective advisor (Jake Peralta or Captain Holt) for Brooklyn Nine‑Nine.

Your task:
1. Use the retrieved transcript excerpts below to answer the user’s question.
2. **If an explicit transcript quote directly answers the question**, include it verbatim and cite the episode code.
3. **If no explicit quote is available**, then logically infer the most likely answer from the context, and clearly label that portion as [Inference].

Here are the retrieved excerpts:
{context}

User Question:
{question}

Answer in character below, mixing quotes and labeled inference as needed.
"""
)

# 4. RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4", temperature=0.7),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt},
)

def answer(question: str) -> str:
    return qa_chain.run(question)

if __name__ == "__main__":
    print(answer("Where did Terry meet his wife?"))
