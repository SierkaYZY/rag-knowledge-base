# 读取TXT文件内容
def load_txt(path):
    """
    读取TXT文件内容
    Args:
        path(str):
            文件路径
    Returns:
        str:
            文件中的文件内容
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        return None

