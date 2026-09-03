# 导入平方根
from math import sqrt
# 计算余弦相似度

def cosine_similarity(vector_a,vector_b):
    """
    计算两向量的余弦相似度
    Args:
        vector_a(list):
            向量a
        vector_b(list):
            向量b
    Return:
        similarity(float):
            两向量余弦相似度
    """
    if  len(vector_a) != len(vector_b):
        raise ValueError("向量维度不相等")
    dot_product = sum(x*y for x,y in zip(vector_a,vector_b))
    norm_a = sqrt(sum(x*x for x in vector_a))
    norm_b = sqrt(sum(y*y for y in vector_b))
    if norm_a == 0 or norm_b == 0 :
        raise ValueError("向量长度不能为0")
    similarity = dot_product/(norm_a*norm_b)
    return similarity

