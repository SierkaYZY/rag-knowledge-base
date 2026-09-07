# 函数调用
from rag_pipeline.query_database import query_document
from rag_pipeline.prompt_builder import build_context, build_prompt
from llm.llm_client import generate_answer
from retrieval.result_filter import filter_results_by_distance

#  根据知识库检索结果生成最终回答
def rag_answer(
        query, 
        top_k=2,
        max_distance = 0.95,
        debug= False
    ):
    """
    根据知识库检索结果生成最终回答。

    Args:
        query (str):
            用户问题。
        model_name (str):
            Embedding 模型名称。
        top_k (int):
            检索返回的相关文本数量。

    Returns:
        str:
            大语言模型生成的最终回答。
    """

    raw_results = query_document(query,top_k)

    results = filter_results_by_distance(
    raw_results,
    max_distance
    )

    if not results["documents"][0]:
        return "没有找到足够相关的参考资料，无法回答该问题。"

    context = build_context(results)
    
    prompt = build_prompt(query,context)

    if debug:
       
        print(context)

    answer = generate_answer(prompt)
    
    return answer

