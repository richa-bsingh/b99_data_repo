# src/rag_chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_chroma.vectorstores import Chroma

# 1) Load embeddings & vector store
embeddings = OpenAIEmbeddings()
vectordb  = Chroma(
    persist_directory="db/chroma_brooklyn99",
    embedding_function=embeddings
)

# 2) A single, generic prompt template that handles quotes + inference
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

# 3) Build the RAG chain
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
    # Quick smoke test
    print(answer("Did Charles and Genevieve meet at the bar or at the courthouse?"))
