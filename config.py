import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
try:
    # 读取配置
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465)) # 提供一个默认值
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD") # 授权码而非邮箱密码
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

    # dirvers
    PROJECT_ROOT = Path(__file__).resolve().parent
    DRIVER_PATH = PROJECT_ROOT / "drivers" / "msedgedriver.exe"

    # URLs
    QIUSHI_URL = os.getenv("QIUSHI_URL")

    # Data
    DATA_PATH = PROJECT_ROOT / "data"

    AI_API_KEY = os.getenv("AI_API_KEY")
except:
    print("读取配置失败")
