from openai import OpenAI, APITimeoutError, APIConnectionError, RateLimitError, InternalServerError
from config import AI_API_KEY
import markdown2
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

@retry(
    wait=wait_random_exponential(multiplier=2, min=10, max=60),
    stop=stop_after_attempt(10),
    retry=retry_if_exception_type((
        APITimeoutError,        # 请求超时
        APIConnectionError,     # 网络连接问题
        RateLimitError,         # 达到频率限制
        InternalServerError     # 服务器内部错误 (5xx)，正是你遇到的问题
    ))
)
def generate_content(text: str) -> str:
    """
    :param text: str: 文本
    :return: str：生成的HTML内容
    """
    try:
        client = OpenAI(
            base_url="https://feiai.chat/v1",
            api_key=AI_API_KEY,
        )
        response = client.chat.completions.create(
            model="gemini-2.5-pro",
            messages=[
                {"role": "system",
                "content": "你是一个求是杂志解读员，擅长用通俗易懂的语言讲解总结出杂志内容，并能读懂杂志的文字中的暗示，并能给出辅助用户经济决策的信息。"},
                {"role": "user", "content": f"{text}"},
            ],
            timeout=100,
            temperature=0.2,
        )
    except Exception as e:
        print(f"AI API 调用在多次重试后仍然失败: {e}")
        raise
    return markdown2.markdown(response.choices[0].message.content)
if __name__ == '__main__':
    with open(r'D:\code\robot\data\journals\《求是》2025年第15期\求是专访│下半年中国经济走势怎么看？.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    html_content = generate_content(text)
    print(html_content)