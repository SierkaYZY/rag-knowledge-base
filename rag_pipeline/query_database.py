# 函数调用
import chromadb
from sentence_transformers import SentenceTransformer
from vector_store.chroma_store import search_chunks

# 连接已有数据库输出与用户输入文本相关性高的结果
def query_document(query,model_name,top_k=2):
    """
    连接已有数据库检索与用户文本相似度高的结果并输出结果
    Args:
        query(str):
            用户输入文本
        model_name(str):
            所调用的切片转换向量的模型的名字
        top_k(int):
            取几个相似度高的结果
    Returns:
        dict:
            输出的相似度较高的结果
    """
    client = chromadb.PersistentClient(path = "./chroma_db")
    collection = client.get_collection(name="knowledge_chunks")
    model = SentenceTransformer(model_name)

    results = search_chunks(collection,query,model,top_k)
    return results


