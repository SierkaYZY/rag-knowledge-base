# 函数功能调用
from file_io.document_processor import process_txt
from embedding.embedding_model import embed_chunks
from vector_store.chroma_store import store_chunks
import chromadb
from sentence_transformers import SentenceTransformer

# 将文本转转换成向量写入向量库
def index_document(path,model_name,chunk_size,chunk_overlap):
    """
    调取文本内容,并将文本内容切片,嵌套向量,再存入向量数据库
    Args:
        path(str):
            文本文件所在路径
        chunk_size(int):
            文本切片长度
        chunk_overlap(int):
            文本重叠长度
        model_name(str):
            调用文本转换向量模型的名字
    Returns:
        int:
            数据库记录数量

    """
    client = chromadb.PersistentClient(path = "./chroma_db")
    collection = client.get_or_create_collection(name = "knowledge_chunks")
    chunks = process_txt(path,chunk_size,chunk_overlap)
    model = SentenceTransformer(model_name)
    embedded_chunks = embed_chunks(chunks,model)
    collection_counts = store_chunks(collection,embedded_chunks)
    return collection_counts

if __name__ == "__main__":
    path = "data/sample/sample.txt"
    model_name = "BAAI/bge-small-zh-v1.5"
    chunk_size = 200
    chunk_overlap = 50

    count = index_document(
        path,
        model_name,
        chunk_size,
        chunk_overlap
    )

    print("Indexed chunks:", count)