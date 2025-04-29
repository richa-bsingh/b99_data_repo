import json
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def load_transcripts_from_json(path: Path | str = None) -> list[Document]:
    """
    Reads the unified JSON dump of B99 transcripts,
    joins each episode’s dialogue, splits into overlapping chunks,
    and tags each chunk with season/episode metadata.
    """
    if path is None:
        path = Path(__file__).resolve().parent.parent / "data" / "unified-dump.json"
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No transcript JSON found at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs: list[Document] = []

    for ep in data.get("episodes", []):
        season = ep.get("season")
        episode = ep.get("episode")
        full_text = "\n".join(ep.get("dialogue", []))
        chunks = splitter.split_text(full_text)
        for idx, chunk in enumerate(chunks):
            docs.append(Document(
                page_content=chunk,
                metadata={
                    "source": f"S{season:02d}E{episode:02d}",
                    "season": season,
                    "episode": episode,
                    "chunk_id": idx
                }
            ))

    print(f"Loaded {len(docs)} chunks from {path}")
    return docs

if __name__ == "__main__":
    load_transcripts_from_json()
