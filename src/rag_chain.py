# src/rag_chain.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# NEW imports for Qdrant
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient

# 1) Initialize embeddings as before
embeddings = OpenAIEmbeddings()

# 2) Spin up an in-memory Qdrant client
qdrant_client = QdrantClient(":memory:")

# 3) Create (or connect to) a collection
VECTOR_COLLECTION = "b99_precinct"
vectorstore = Qdrant.from_client(
    client=qdrant_client,
    collection_name=VECTOR_COLLECTION,
    embeddings=embeddings,
    prefer_grpc=True,            # optional, for performance
    distance_func="Cosine"       # or "Dot"
)

# 4) Build a RetrievalQA chain
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
    """Run RetrievalQA to fetch an answer (or clue) for the given query."""
    return qa_chain.run(query)
