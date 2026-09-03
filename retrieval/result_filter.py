def filter_results_by_distance(results, max_distance):
    """
    根据检索距离过滤 Chroma 查询结果。

    Args:
        results (dict):
            Chroma 查询结果。
        max_distance (float):
            允许保留的最大距离。

    Returns:
        dict:
            过滤后的查询结果。
    """

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    filtered_ids = []
    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []
    for i in range(len(ids)):
        if distances[i] <= max_distance:
            filtered_ids.append(ids[i])
            filtered_documents.append(documents[i])
            filtered_metadatas.append(metadatas[i])
            filtered_distances.append(distances[i])

    filtered_results = {
        "ids": [filtered_ids],
        "documents": [filtered_documents],
        "metadatas": [filtered_metadatas],
        "distances": [filtered_distances]
    }

    return filtered_results