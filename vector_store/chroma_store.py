# 创建将切片的chunk存储进chroma的函数
def store_chunks(collection,embedded_chunks):
    """
    将带有向量的文本块存入 Chroma Collection
    Args:
        collection:
            Chroma Collection的对象
        embedded_chunks(list[dict]):
            带有向量的文本切块
    Returns:
        int:
            Collection里的记录总数

    """
    ids = []
    documents = []
    metadatas = []
    embeddings = []
    for chunk in embedded_chunks:
        document = chunk["content"]
        metadata = chunk["metadata"]
        embedding = chunk["embedding"]
        record_id = f'{metadata["filename"]}:{metadata["chunk_id"]}'
        ids.append(record_id)
        documents.append(document)
        metadatas.append(metadata)
        embeddings.append(embedding)
    collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
    )
    return collection.count()

# 根据查询文本，从 Chroma Collection 中检索相关文本块
def search_chunks(collection, query, model, top_k=3):
    """
    根据查询文本，从 Chroma Collection 中检索相关文本块。

    Args:
        collection:
            Chroma Collection 对象
        query(str):
            用户查询文本
        model:
            已加载的 SentenceTransformer 模型
        top_k(int):
            返回结果数量

    Returns:
        dict:
            Chroma 返回的查询结果
    """
    # 1. 把 query 转换成向量
    query_embedding = model.encode(query,normalize_embeddings = True)
    # 2. 调用 collection.query()
    results = collection.query(
        query_embeddings = [query_embedding.tolist()],
        n_results = top_k,
        include=["documents", "metadatas", "distances"]
    )
    # 3. 返回结果
    return results
