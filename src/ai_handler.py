from openai import OpenAI, APITimeoutError, APIConnectionError, RateLimitError, InternalServerError
from config import AI_API_KEY
import markdown2
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type
import json

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
def generate_content(text: str, prompt: str) -> str:
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
                "content": f"{prompt}"},
                {"role": "user", "content": f"{text}"},
            ],
            timeout=100,
            temperature=0.2,
        )
    except Exception as e:
        print(f"AI API 调用在多次重试后仍然失败: {e}")
        raise
    return markdown2.markdown(response.choices[0].message.content)

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

def process_paper_with_ai(title_en, abstract_en):
    """
    使用 OpenAI API 翻译论文标题、摘要，并生成AI分析。
    :param title_en: str, 论文的英文标题
    :param abstract_en: str, 论文的英文摘要
    :return: dict, 包含翻译和分析结果的字典，或在失败时返回 None
    """
    # 设计一个强大的 Prompt，让 AI 一次性完成所有任务
    prompt = f"""
    你是一个顶级的科研助理，请对以下学术论文信息进行处理，并严格按照指定的JSON格式返回结果。
    任务要求:
    1.  将论文标题 (title) 翻译成简洁、专业、信达雅的中文。
    2.  将论文摘要 (abstract) 翻译成流畅、准确的中文。
    3.  基于英文摘要，生成一段“AI分析”，用通俗易懂的语言总结这篇论文的核心贡献、关键方法和潜在影响。分析应分为三点，每点用 1. 2. 3. 标出。
    待处理的论文信息:
    - 英文标题: "{title_en}"
    - 英文摘要: "{abstract_en}"
    请严格按照以下JSON格式输出，不要添加任何额外的解释或文字：
    {{
      "title_zh": "你的中文翻译标题",
      "abstract_zh": "你的中文翻译摘要",
      "ai_analysis": "<b>1. 核心贡献:</b><br> ... <br> <b>2. 关键方法:</b><br>...<br> <b>3. 潜在影响:</b><br>..."
    }}
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
                "content": f"{prompt}"},
                {"role": "user", "content": f"{prompt}"},
            ],
            timeout=100,
            temperature=0.2,
            response_format={"type":"json_object"},
        )
    except Exception as e:
        print(f"AI API 调用在多次重试后仍然失败: {e}")
        raise
    return json.loads(response.choices[0].message.content)

if __name__ == '__main__':
    pass
    # with open(r'D:\code\robot\data\journals\《求是》2025年第15期\求是专访│下半年中国经济走势怎么看？.txt', 'r', encoding='utf-8') as f:
    #     text = f.read()
    # html_content = generate_content(text,"你是一个求是杂志解读员，擅长用通俗易懂的语言讲解总结出杂志内容，并能读懂杂志的文字中的暗示，并能给出辅助用户经济决策的信息。")
    # print(html_content)
