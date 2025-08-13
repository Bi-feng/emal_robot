import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, SENDER_PASSWORD

# 收件人信息
RECIPIENT_EMAIL = "bifeng_zhe@outlook.com"  # 对方的邮箱地址

# --- 邮件内容 ---
def send_email(subject, body, recipient=RECIPIENT_EMAIL):
    """发送邮件的核心函数"""

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
    send_email(email_subject, email_body, recipient=RECIPIENT_EMAIL)
