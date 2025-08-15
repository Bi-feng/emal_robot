from openai import OpenAI
from config import AI_API_KEY
import markdown

def generate_content(path: str) -> str:
    """
    :param path: str: 读取的文件路径
    :return: str：生成的HTML内容
    """
    client = OpenAI(
        base_url="https://feiai.chat/v1",
        api_key=AI_API_KEY,
    )
    with open(path, 'r', encoding='utf-8') as f:
        c_data = f.read()
    response = client.chat.completions.create(
        model="gemini-2.5-pro",
        messages=[
            {"role": "system",
             "content": "你是一个求是杂志解读员，擅长用通俗易懂的语言讲解总结出杂志内容，并能读懂杂志的文字中的暗示，并能给出辅助用户经济决策的信息。"},
            {"role": "user", "content": f"{c_data}"},
        ],
        timeout=100,
        temperature=0.5,
    )
    return response.choices[0].message.content
if __name__ == '__main__':
    html_content = generate_content(r'D:\code\robot\data\journals\《求是》2025年第15期\求是专访│下半年中国经济走势怎么看？.txt')
    print(html_content)