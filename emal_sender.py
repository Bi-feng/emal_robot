import smtplib
from email.message import EmailMessage
import ssl

# --- 邮件配置 ---
# 替换成你自己的信息
EMAIL_SENDER = "bifeng_zhe@qq.com"  # 你的发件邮箱
EMAIL_PASSWORD = "tiowakznihlujibc"  # 你的邮箱授权码 (不是登录密码!)
EMAIL_RECEIVER = "bifeng_zhe@outlook.com"  # 收件人邮箱

# --- 邮件内容 ---
subject = "Python 邮件测试"
body = """
你好！

这是一封通过 Python 脚本自动发送的邮件。
祝好！
"""

# 创建一个 EmailMessage 对象
em = EmailMessage()
em['From'] = EMAIL_SENDER
em['To'] = EMAIL_RECEIVER
em['Subject'] = subject
em.set_content(body)

# 使用 SSL 加密连接，更安全
context = ssl.create_default_context()

# --- 连接到 SMTP 服务器并发送邮件 ---
# 注意：不同的邮箱服务商，SMTP 服务器地址和端口可能不同
# QQ邮箱: smtp.qq.com, 端口 465
# 163邮箱: smtp.163.com, 端口 465
# Gmail: smtp.gmail.com, 端口 465
try:
    with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:
        print("正在登录邮箱...")
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        print("登录成功！正在发送邮件...")
        smtp.send_message(em)
        print("邮件发送成功！")
except Exception as e:
    print(f"邮件发送失败，错误信息: {e}")

