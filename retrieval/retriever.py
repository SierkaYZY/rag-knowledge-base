from embedding.similarity import cosine_similarity
from sentence_transformers import SentenceTransformer
from file_io.document_processor import process_txt
from embedding.embedding_model import embed_chunks

# 检索与询问内容余弦相似度最高的块
def retrieve(query, embedded_chunks,model,top_k=3):
    """
    检测与询问文本向量余弦相似度最高的块并返回
    Args:
        query(str):
            查询信息文本
        embedded_chunk(list[dict]):
            嵌入向量的块
        model:
            已加载的 SentenceTransformer 模型对象
        top_k(int):
            取几个相似度高的向量
    Returns:
        list(dict):
            该模块的内容,元数据和相似分数
    """
    query_embedding = model.encode(query, normalize_embeddings = True)
    results = []
    for embedded_chunk in embedded_chunks:
        chunk_embedding = embedded_chunk["embedding"]
        score = cosine_similarity(query_embedding,chunk_embedding)
        result = {"content":embedded_chunk["content"],"metadata":embedded_chunk["metadata"],"score":float(score)}
        results.append(result)

    results.sort(key=get_score, reverse= True)
    return results[:top_k]

# 读取分数
def get_score(result):
    return result["score"] 

