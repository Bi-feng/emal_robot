import html
def text_to_html(plain_text: str) -> str:
    """
    将纯文本转换为适合在 HTML 中安全显示的格式。
    - 转义特殊 HTML 字符。
    - 将换行符转换为 <br> 标签。
    Args:
        plain_text: 纯文本字符串。
    Returns:
         HTML 字符串。
    """

    escaped_text = html.escape(plain_text)

    return f"<pre>{escaped_text}</pre>"
