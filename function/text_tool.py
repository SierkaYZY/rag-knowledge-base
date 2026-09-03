# 任务一：文本长度统计
def count_chars(text):
    """
    统计文本中的字符数,并检查输入是否正确
    Args:
        text (str):
            输入文本
    Returns:
        int:
            文本的字符数
    """
    if not isinstance(text, str):
        return 0
    return len(text)

def count_words(text):
    """
    统计文本中的单词数,并检查输入是否正确
    Args:
        text (str):
            输入文本
    Returns:
        int:
            文本的单词数
    """
    if not isinstance(text, str):
        return 0
    return len(text.split())
    

# 任务二：文本清理
def clean_text(text):
    """
    清理文本前后空格
    Args:
        text (str):
            输入文本
    Returns:
        str:
            清理后的文本
    """
    return text.strip()

# 任务三：文本信息统计
def text_info(text):
    """
    统计文本的单词数和字符数
    Args:
        text (str):
            输入文本
    Returns:
        dict:
            字符数,单词数
    """
    return{"char_count":count_chars(text),"word_count":count_words(text)}

# 任务四:实现删除空行
def remove_empty_lines(text):
    """
    删除文本中的空行
    Args:
        text (str):
            输入文本
    Returns:
        str:
            删除空行后的文本
    """
    lines=text.split("\n")
    return "\n".join(line 
                     for line in lines 
                     if line.strip())

