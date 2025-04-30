from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.ingest import load_transcripts_from_json
import os

# 1. Embeddings
embeddings = OpenAIEmbeddings()
persist_directory = "db/chroma_brooklyn99"

# 2. Manually configure client_settings to avoid SQLite
client_settings = {
    "chroma_db_impl": "duckdb+parquet",
    "persist_directory": persist_directory
}

# 3. Load or build vectorstore
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        client_settings=client_settings
    )
else:
    docs = load_transcripts_from_json()
    vectordb = Chroma.from_documents(
        docs,
        embedding=embeddings,
        persist_directory=persist_directory,
        client_settings=client_settings
    )



# 4) Prompt
template = """
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

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

# 5) Build RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4", temperature=0.7),
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt},
)

def answer(question: str) -> str:
    return qa_chain.run(question)

if __name__ == "__main__":
    print(answer("Did Charles and Genevieve meet at the bar or at the courthouse?"))
