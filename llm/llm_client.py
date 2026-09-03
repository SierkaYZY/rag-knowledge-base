# 调用Python 标准库，读取环境变量
import os
# 读取 .env，把里面的键值加载进当前程序环境
from dotenv import load_dotenv
# 客户端类，连接OpenAI 兼容 API
from openai import OpenAI

# 调用创建client对象
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("未找到 DEEPSEEK_API_KEY，请检查项目根目录下的 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 调用大语言模型对提示词输出对应回答
def generate_answer(prompt):
    """
    将提示词发送给 DeepSeek，并返回模型回答。

    Args:
        prompt (str):
            发送给大语言模型的完整提示词。

    Returns:
        str:
            模型生成的回答。
    """

    response = client.chat.completions.create(
        model = "deepseek-v4-flash",
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ],
        extra_body = {
            "thinking":{
                "type":"disabled"
            }
        }  
    )

    answer = response.choices[0].message.content

    return answer

