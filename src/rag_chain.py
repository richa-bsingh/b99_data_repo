# src/rag_chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# → Chroma vectorstore:
from langchain.vectorstores import Chroma
# Document loaders/splitters (adapt paths to your data)
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1) Embeddings
embeddings = OpenAIEmbeddings()

# 2) Load & split your Brooklyn Nine-Nine transcripts (or whatever docs)
loader = DirectoryLoader("data/transcripts", glob="**/*.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = splitter.split_documents(docs)

# 3) Build (or load) a Chroma collection with duckdb+parquet backend
vectorstore = Chroma.from_documents(
    texts,
    embeddings,
    persist_directory="db"           # triggers DuckDB+Parquet storage
)

# :contentReference[oaicite:0]{index=0}

# 4) Create your RetrievalQA chain as before
prompt = PromptTemplate(
    input_variables=["query"],
    template="Use the Brooklyn Nine-Nine transcripts to answer: {query}"
)
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4", temperature=0.2),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

def answer(query: str) -> str:
    return qa_chain.run(query)
