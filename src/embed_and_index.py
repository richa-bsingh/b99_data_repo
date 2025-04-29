from pathlib import Path
import shutil

from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from ingest import load_transcripts_from_json

def create_vectorstore(
    json_path: Path | str = None,
    persist_dir: str = "db/chroma_brooklyn99"
):
    """
    Loads transcript chunks, creates OpenAI embeddings, and
    builds & persists a fresh Chroma vector store.
    """
    # remove old store if present (so we don’t hit stale config errors)
    store_path = Path(persist_dir)
    if store_path.exists():
        print(f"ℹ️  Removing old Chroma store at {store_path}")
        shutil.rmtree(store_path)

    # load docs & index
    docs = load_transcripts_from_json(path=json_path)
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    # NO vectordb.persist() here—writing is handled by from_documents
    print(f"✅ Vector store created & persisted at '{persist_dir}'")

if __name__ == "__main__":
    create_vectorstore()
