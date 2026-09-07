# 函数调用
import chromadb
from sentence_transformers import SentenceTransformer
from vector_store.chroma_store import search_chunks

MODEL_NAME = "BAAI/bge-small-zh-v1.5"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "knowledge_chunks"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

model = SentenceTransformer(
    MODEL_NAME
)

# 连接已有数据库输出与用户输入文本相关性高的结果
def query_document(query,top_k=2):
    """
    连接已有数据库检索与用户文本相似度高的结果并输出结果
    Args:
        query(str):
            用户输入文本
        top_k(int):
            取几个相似度高的结果
    Returns:
        dict:
            输出的相似度较高的结果
    """
    results = search_chunks(
        collection,
        query,
        model,
        top_k
    )

    return results


def retrieve_knowledge(query, top_k=3):
    results = query_document(
        query,
        top_k
    )

    documents = results["documents"][0]    
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    retrieved = []

    for id,document,metadata,distance in zip(ids,documents,metadatas,distances):
        retrieved.append(
            {
                "id": id,
                "content": document,
                "filename": metadata["filename"],
                "chunk_id": metadata["chunk_id"],
                "distance": distance
            }
        )

    return retrieved

if __name__ == "__main__":
    results = retrieve_knowledge(
        "What is RAG?",
        3
    )
    print(results)