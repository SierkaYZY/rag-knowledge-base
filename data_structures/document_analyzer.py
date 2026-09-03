# 调用text_tool.py的函数
from function.text_tool import count_chars, count_words

# 任务一:把文本转换成行列表
def get_valid_lines(text):
    """
    将文本转换成行列表,并删除空行
    Args:
        text(str):
            输入文本
    Returuns:
        list:
            文本行列式
    """
    lines=text.split("\n")
    valid_lines=[] 
    for line in lines:
        if line.strip()!= "":
            valid_lines.append(line)
    return valid_lines 
# 不要忘了return返回值,否则返回none,会导致后续的代码报错

# 任务二:创建文档信息字典
def build_document_info(filename, text):
    """
    创建文档信息字典
    Args:
        filename(str):
            文档名
        text(str):
            文档内容
    Returns:
        dict:
            文档信息字典
    """
    valid_lines = get_valid_lines(text)
    return{
        "filename":filename,
        "line_count":len(valid_lines),
        "char_count":count_chars(text),
        "word_count":count_words(text)
    }

def build_document(filename,text):
     """
     创建文档信息字典,包含内容和元数据
     Args:
        filename(str):
            文档名
        text(str):
            文档内容
    Returns:
        dict:
            文档信息字典,包含内容和元数据
    """
     valid_lines = get_valid_lines(text)
     return{
          "content":text,
          "metadata":{
               "filename":filename,
               "line_count":len(valid_lines),
               "char_count":count_chars(text),
               "word_count":count_words(text)
          }
     }

# 任务三:处理多个文档
def analyze_doucuments(documents):
    """
    处理多个文档,并返回文档信息字典列表
    Args:
        documents(list):
            文档信息列表
    Returns:
        list:
            文档字典信息列表
    """
    doucument_info_list=[]
    for document in documents:
            document_info=build_document_info(document["filename"],document["text"])
            doucument_info_list.append(document_info)
    return doucument_info_list
        
