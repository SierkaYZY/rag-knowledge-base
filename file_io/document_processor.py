# 调用模块内函数
# 调用文档读取函数
from file_io.document_loader import load_txt
# 调用文档信息创建函数
from data_structures.document_analyzer import build_document
# 调用文本字典切块函数
from text_splitter.text_splitter import split_document
# 调用路径
from pathlib import Path

def process_txt(path,chunk_size,chunk_overlap=0):
    """
    阅读文档,创建文档信息,并将字典信息分块
    Args:
        path(str):
            文件路径
        chunk_size(int):
            块的长度
        chunk_overlap(int):
            块的重复元素数
    Returns:
        list:
            切片后的文档字典信息
    """
    
    filename = Path(path).name
    text = load_txt(path)
    if text is None:
        return None
    document = build_document(filename,text)
    chunks = split_document(document,chunk_size,chunk_overlap)
    return chunks



       
