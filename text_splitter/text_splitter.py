# 调用函数
import re
from file_io.document_loader import load_txt

# 文本切片
def split_text(text,chunk_size,chunk_overlap=0):
    """
    对文本按指定长度切片
    Args:
        text(str):
            文本内容
        chunk_size(int):
            切片的长度
    Returns:
        list:
            切片后的文本
    """
    sentences = split_sentences(text)

    chunks = group_sentences(
        sentences,
        chunk_size,
        chunk_overlap
    )

    return chunks


# 文本字典切片
def split_document(document,chunk_size,chunk_overlap=0):
    """
    对读取文本后的字典按指定长度切片
    Args:
        documnet(dict):
            文档信息字典
        chunk_size(int):
            切片长度
    Returns:
        list:
            切片后的字典
    """
    text= document["content"]
    text_chunks= split_text(text,chunk_size,chunk_overlap)
    chunks = []
    for chunk_id,chunk_text in enumerate(text_chunks):
        chunk_metadata= document["metadata"].copy()
        chunk_metadata["chunk_id"]= chunk_id
        chunk= {
            "content":chunk_text,
            "metadata":chunk_metadata
        }
        chunks.append(chunk)
    return chunks

# 文本句子切片
def split_sentences(text):
    """
    对文本内容按照句子来切片
    Args:
        text(str):
            文本内容
    Returns:
        list[str]:
            文本内容的每个句子
    """
    sentences = re.split(r"(?<=[。！？.!?])",text)
    splitted_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            splitted_sentences.append(sentence)

    return splitted_sentences

# 超长句切片
def split_long_sentence(sentence,chunk_size):
    words = sentence.split()

    chunks = []
    current_words = []

    for word in words:

        if len(word) > chunk_size:
            if current_words:
                chunks.append(" ".join(current_words))
                current_words = []
            for i in range(0,len(word),chunk_size):
                piece = word [i:i+chunk_size]
                chunks.append(piece)

            continue
        
        candidate_words =  current_words + [word]
        candidate = " ".join(candidate_words)

        if (len(candidate) <= chunk_size):
            current_words.append(word)

        else:
            chunks.append(" ".join(current_words))
            current_words = [word]

    

    if current_words:  
            chunks.append(" ".join(current_words))

    return chunks

# 把完整句子组合成chunk
def group_sentences(sentences, chunk_size,chunk_overlap= 0):
    """
    把切开的句子组合成chunk
    Args:
        sentences(list[str]):
            切开的完整句子
        chunk_size(int):
            块的长度
    Returns:
        list[str]:
            一个个chunk
    """
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap 必须满足 0 <= chunk_overlap < chunk_size")

    chunks = []
    current_sentences = []

    for sentence in sentences:
        if len(sentence) > chunk_size:
            if current_sentences:
                chunks.append(" ".join(current_sentences))
                current_sentences = []

            long_chunks = split_long_sentence(sentence, chunk_size)
            chunks.extend(long_chunks)

            continue

        candidate_sentences =  current_sentences + [sentence]
        candidate = " ".join(candidate_sentences)
        
        if len(candidate) <= chunk_size:
                current_sentences.append(sentence)
        else :
            chunks.append(" ".join(current_sentences))
            overlap_sentences = []

            for previous_sentence in reversed(current_sentences):
                candidate_overlap = [previous_sentence] + overlap_sentences

                overlap_text = " ".join(candidate_overlap)
                new_chunk_text = " ".join(candidate_overlap + [sentence])

                if (len(overlap_text) <= chunk_overlap and len(new_chunk_text) <= chunk_size):
                    overlap_sentences = candidate_overlap
                else:
                    break

            current_sentences = overlap_sentences + [sentence]
                
    if current_sentences:  
        chunks.append(" ".join(current_sentences))

    return chunks


