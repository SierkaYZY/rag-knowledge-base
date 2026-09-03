
# 将返回的向量匹配度高的内容重新整理并输出
def build_context(results):
    """
    将返回的向量匹配度高的内容重新整理并输出
    Args:
        results(dict):
            存放多个高匹配文档内容和信息的字典
    Returns:
        str:
            整理完成后的完整资料信息
    """
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    formatted_documents = []

    for index,(document,metadata) in enumerate(
        zip(documents,metadatas),start =1
        ):
        format_document = (
            f"[资料{index}]\n"
            f"来源文件:{metadata['filename']}\n"
            f"Chunk ID:{metadata['chunk_id']}\n"
            f"内容:{document}"
                           )
        formatted_documents.append(format_document)
    context = "\n\n".join(formatted_documents)
    return context

# 构建提示词prompt
def build_prompt(query,context):
    """
    根据用户问题和参考资料构造完整提示词。
    Args:
        query(str):
            用户问题
        context(str):
            检索并整理后的参考资料
    Returns:
        str:
            完整的提示词
    """
    prompt = f"""你是一个知识库问答助手。
    
回答要求：
1. 只能依据提供的参考资料回答问题，不得使用参考资料之外的知识。
2. 回答中的事实或结论必须标注对应的资料编号，例如 [资料1]、[资料2]。
3. 如果一个结论同时由多个资料支持，可以写成 [资料1][资料2]。
4. 不得引用参考资料中不存在的资料编号。
5. 如果参考资料不足以回答问题，请明确说明资料不足，不要自行补充外部知识。

参考资料：
{context}

用户问题:
{query}

回答:
    """
    return prompt


