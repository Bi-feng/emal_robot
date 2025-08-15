import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import Optional
from .utils import text_to_html

from config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, SENDER_PASSWORD

# 收件人信息
RECIPIENT_EMAIL = "case@outlook.com"  # 对方的邮箱地址

# --- 邮件内容 ---
def send_email(subject, body, recipient):
    """发送邮件的核心函数
    Args:
        subject: 邮件主题
        body: 邮件正文内容
        recipient: 收件人邮箱地址
        """

    # 1. 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = EMAIL_SENDER
    message['To'] = recipient
    message['Subject'] = Header(subject, 'utf-8')

    # 2. 邮件正文内容 (纯文本)
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # 3. 连接到 SMTP 服务器并发送邮件
    try:
        print("正在连接到 SMTP 服务器...")
        # 使用 SSL 加密的 SMTP
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

        print("正在登录...")
        server.login(EMAIL_SENDER, SENDER_PASSWORD)

        print("正在发送邮件...")
        server.sendmail(EMAIL_SENDER, [recipient] if isinstance(recipient, str) else recipient, message.as_string())

        print("邮件发送成功！")

    except smtplib.SMTPException as e:
        print(f"邮件发送失败，错误信息: {e}")
    finally:
        if 'server' in locals() and server:
            server.quit()
            print("已关闭服务器连接。")


def send_html_email(recipient: str, subject: str, html_content: str):
    """
    发送一封纯 HTML 格式的电子邮件。
    Args:
        recipient: 收件人邮箱地址。
        subject: 邮件主题。
        html_content: 完整的 HTML 邮件正文。
    """
    if not all([SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, SENDER_PASSWORD]):
        print("邮件配置不完整，跳过发送。")
        return
    try:
        # 创建一个 MIMEText 对象，指定 subtype 为 'html'
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient
        msg['Subject'] = subject

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, SENDER_PASSWORD)
        server.sendmail(EMAIL_SENDER, [recipient], msg.as_string())
        print(f"HTML 邮件已成功发送至 {recipient}")
    except Exception as e:
        print(f"发送邮件时发生错误: {e}")

# --- 主程序入口 ---
if __name__ == "__main__":
    email_subject = "一封来自 Python 的测试邮件"
    email_body = """
    你好！

    这是一封通过 Python 自动化脚本发送的邮件。
    如果能收到，说明脚本工作正常！

    祝好，
    你的 Python 机器人
    """
    final_html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 800px; margin: 20px auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .section {{ margin-bottom: 25px; }}
            h2 {{ color: #0056b3; border-bottom: 2px solid #0056b3; padding-bottom: 5px; }}
            pre {{ 
                background-color: #f8f9fa; 
                padding: 15px; 
                border: 1px solid #dee2e6;
                border-radius: 5px; 
                white-space: pre-wrap; /* 自动换行 */
                word-wrap: break-word; /* 长单词换行 */
                font-family: 'Courier New', Courier, monospace;
                font-size: 14px;
            }}
            .ai-analysis {{ border-top: 2px dashed #28a745; padding-top: 20px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="section">
                <h2>文章原文</h2>
                {text_to_html(email_body)}
            </div>
            <div class="section ai-analysis">
                <h2>AI 分析报告</h2>
            </div>
            <p>祝好！<br>你的自动化助手</p>
        </div>
    </body>
    </html>
    """
    send_html_email(RECIPIENT_EMAIL,email_subject, final_html_content)
