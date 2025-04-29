# src/rag_chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_chroma.vectorstores import Chroma

# load persisted vector store
embeddings = OpenAIEmbeddings()
vectordb = Chroma(
    persist_directory="db/chroma_brooklyn99",
    embedding_function=embeddings
)

# in-character prompt template
template = """
You are “99 Assistant,” an in-character detective advisor.
Use the retrieved transcript excerpts to answer the user’s question as Jake Peralta or Captain Holt,
and when quoting, reference the episode code.

{context}

User Question: {question}

Answer in-character, quoting the transcript.
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4", temperature=0.7),
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt},    # <<< move prompt inside chain_type_kwargs
)

def answer(question: str) -> str:
    return qa_chain.run(question)

if __name__ == "__main__":
    print(answer("What does Captain Holt say about teamwork?"))
