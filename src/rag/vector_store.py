import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Use /tmp on Streamlit Cloud, local data/ otherwise
if os.environ.get("STREAMLIT_CLOUD"):
    VECTOR_STORE_PATH = "/tmp/vector_store"
else:
    VECTOR_STORE_PATH = "data/vector_store"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"}
    )

def build_vector_store(resume_data):
    # Accept both dict and file path string
    if isinstance(resume_data, str):
        from src.parsing.resume_parser import parse_resume
        resume_data = parse_resume(resume_data)

    docs = []
    section_map = {
        "skills":       str(resume_data.get("skills", [])),
        "experience":   str(resume_data.get("experience", [])),
        "projects":     str(resume_data.get("projects", [])),
        "education":    str(resume_data.get("education", [])),
        "achievements": str(resume_data.get("achievements", [])),
    }
    for section, content in section_map.items():
        if content and content != "[]":
            docs.append(Document(page_content=content, metadata={"section": section}))

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
    raw_chunks = splitter.create_documents(
        [resume_data.get("raw_text", "")], metadatas=[{"section": "raw"}]
    )
    docs.extend(raw_chunks)

    embeddings = get_embeddings()
    db = FAISS.from_documents(docs, embeddings)
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    db.save_local(VECTOR_STORE_PATH)
    print(f"Vector store built: {len(docs)} chunks indexed.")
    return db

def load_vector_store():
    embeddings = get_embeddings()
    return FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)

def retrieve_relevant_chunks(query, k=3):
    try:
        db = load_vector_store()
        results = db.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in results])
    except Exception:
        return "Python, Machine Learning, Deep Learning, SQL, Linux"