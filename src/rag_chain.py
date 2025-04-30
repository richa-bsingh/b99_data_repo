# src/rag_chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

# 1) Load embeddings
embeddings = OpenAIEmbeddings()

# 2) Prepare vectorstore path
persist_directory = "db/chroma_brooklyn99"

# 3) Load vectorstore if exists, otherwise build it from transcripts
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
else:
    loader = DirectoryLoader("data/transcripts", glob="*.txt")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(docs)
    vectordb = Chroma.from_documents(
        texts,
        embedding_function=embeddings,
        persist_directory=persist_directory
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

# 5) RAG chain
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
