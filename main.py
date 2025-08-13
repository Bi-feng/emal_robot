from src import send_email, scrape_qiushi_articles
from config import QIUSHI_URL, EMAIL_RECEIVER

def format_articles_for_email(articles: list[dict]) -> str:
    """将文章列表格式化为漂亮的邮件正文。"""
    if not articles:
        return "未能获取到任何文章。"

    body = "你好，\n\n以下是《求是》网最新一期的文章目录：\n\n"
    for i, article in enumerate(articles, 1):
        body += f"{i}. {article['title']}\n"
        body += f"   链接: {article['url']}\n\n"

    body += "祝好！\n你的 Python 自动化助手"
    return body

if __name__ == '__main__':
    print("--- 开始执行《求是》网文章抓取任务 ---")
    # 1. 调用抓取函数
    articles = scrape_qiushi_articles(QIUSHI_URL)
    # 2. 检查结果并发送邮件
    if articles:
        print("文章目录获取成功，正在准备邮件...")

        # 格式化邮件内容
        email_subject = "《求是》网最新文章目录"
        email_body = format_articles_for_email(articles)

        # 打印到控制台预览
        print("\n--- 邮件内容预览 ---")
        print(f"主题: {email_subject}")
        print(email_body)
        print("---------------------\n")

        # 发送邮件
        send_email(
            recipient=EMAIL_RECEIVER,
            subject=email_subject,
            body=email_body
        )
    else:
        print("获取文章目录失败，任务中止。")
        # 你也可以在这里发送一封失败警报邮件
        # send_email(
        #     recipient=EMAIL_RECEIVER,
        #     subject="【警报】《求是》网抓取任务失败",
        #     body="尝试抓取《求是》网最新文章目录时发生错误，请检查日志。"
        # )
    print("--- 任务执行完毕 ---")
