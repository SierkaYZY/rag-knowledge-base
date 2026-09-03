from sentence_transformers import SentenceTransformer
from file_io.document_processor import process_txt

#在chunk中引入嵌入向量
def embed_chunks(chunks,model):
    """
    在块中引入嵌入向量
    Args:
        chunks(list[dict]):
            文本的分块
        model:
            已加载的 SentenceTransformer 模型对象
    Returns:
        list[dict]:
            引入嵌入向量后的块
    """ 
    texts = []
    for chunk in chunks: 
        texts.append(chunk["content"])

    embeddings = model.encode(texts,normalize_embeddings=True)

    embedded_chunks = []
    for chunk,embedding in zip(chunks,embeddings):
        embedded_chunk = {
             "content":chunk["content"],
             "metadata":chunk["metadata"].copy(),
             "embedding":embedding.tolist()
        }
        embedded_chunks.append(embedded_chunk)
    return embedded_chunks

