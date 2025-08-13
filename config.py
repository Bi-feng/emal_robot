import os
from dotenv import load_dotenv

load_dotenv()

# 读取配置
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465)) # 提供一个默认值
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD") # 授权码而非邮箱密码
