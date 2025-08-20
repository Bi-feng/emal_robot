import os
from dotenv import load_dotenv
from pathlib import Path
import json

def create_arxiv_template(filename):
    """
    创建一个名为 config.json 的模板文件，如果它尚不存在。
    模板中包含了如何配置收件人、领域、关键词和作者的示例。
    """
    # 检查文件是否已存在
    if os.path.exists(filename):
        return
    print(f"文件 '{filename}' 不存在，正在为您创建模板...")
    # 定义模板的数据结构，使用 _comment 字段来添加说明
    template_data = {
        "_comment": "这是学术论文追踪机器人的配置文件。您可以添加多个收件人。必填项为 email、name、categories、keywords，可选字段为 authors。",
        "recipients": [
            {
                "email": "researcher_A@example.com",
                "name": "Alice",
                "config": {
                    "categories": [
                        "cs.LG",
                        "cs.AI",
                        "cs.CL"
                    ],
                    "keywords": [
                        "Large Language Model",
                        "Instruction Tuning",
                        "Reinforcement Learning from Human Feedback"
                    ],
                    "authors": [
                        "Yann LeCun",
                        "Geoffrey Hinton"
                    ]
                }
            },
            {
                "email": "student_B@example.com",
                "name": "Bob",
                "config": {
                    "categories": [
                        "cs.CV"
                    ],
                    "keywords": [
                        "3D Generation",
                        "NeRF",
                        "Gaussian Splatting"
                    ],
                    "authors": None  # 使用 null 表示不按作者筛选
                }
            },
        ]
    }
    # 将Python字典写入JSON文件
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, indent=4, ensure_ascii=False)
        print(f"成功创建模板文件: '{filename}'")
        print("请根据您的需求修改此文件。")
    except IOError as e:
        print(f"错误：无法写入文件 '{filename}'. 错误信息: {e}")

load_dotenv()
try:
    # 读取配置
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465)) # 提供一个默认值
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD") # 授权码而非邮箱密码
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER").split(",") # 接收者邮箱列表

    # dirvers
    PROJECT_ROOT = Path(__file__).resolve().parent
    os.makedirs(PROJECT_ROOT / "drivers", exist_ok=True)
    DRIVER_PATH = PROJECT_ROOT / "drivers" / "msedgedriver"

    # URLs
    QIUSHI_URL = os.getenv("QIUSHI_URL")

    # Data
    DATA_PATH = PROJECT_ROOT / "data"
    AI_API_KEY = os.getenv("AI_API_KEY")

    # arxiv
    os.makedirs(DATA_PATH / "arxiv", exist_ok=True)
    ARXIV_PATH = DATA_PATH / "arxiv" / "arxiv.json"
    create_arxiv_template(ARXIV_PATH)

except:
    print("读取配置失败")
