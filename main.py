from src import send_email, scrape_website_title, scrape_qiushi_articles, scrape_articles_text, scrape_qiushi_journal
from src import save_journal_urls, load_journal_data, save_article_urls
from config import QIUSHI_URL, EMAIL_RECEIVER, DATA_PATH
import os
from tqdm import tqdm

def scrape_all():
    """抓取《求是》全部文章并发送邮件。"""
    articles = scrape_qiushi_journal(QIUSHI_URL)
    save_journal_urls(articles)
    journals = load_journal_data()
    for journal in tqdm(journals):
        journal_title = journal['title']
        url = journal['url']
        articles = scrape_qiushi_articles(url)
        save_article_urls(journal_title, articles)
        for article in tqdm(articles):
            article_title = article['title']
            url = article['url']
            text = scrape_articles_text(url)
            with open(os.path.join(DATA_PATH, 'journals',f"{journal_title}", f"{article_title}.txt"), 'w', encoding='utf-8') as f:
                f.write(text)


    # 1. 调用抓取函数
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
    scrape_all()
    # 1. 调用抓取函数
    articles = scrape_qiushi_journal(QIUSHI_URL)
    # 2. 保存结果
    isupdated = save_journal_urls(articles)
    if isupdated:
        print("期刊目录有更新，正在准备抓取最新一期期刊的目录...")
        # 3. 调用抓取最新一期期刊目录的函数
        title= load_journal_data()[-1]['title']
        url = load_journal_data()[-1]['url']
        latest_articles = scrape_qiushi_articles(url)
        # 4. 保存最新一期期刊目录
        save_article_urls(title, latest_articles)


    # 2. 检查结果并发送邮件
    # if articles:
    #     print("文章目录获取成功，正在准备邮件...")
    #
    #     # 格式化邮件内容
    #     email_subject = "《求是》网最新文章目录"
    #     email_body = format_articles_for_email(articles)
    #
    #     # 打印到控制台预览
    #     print("\n--- 邮件内容预览 ---")
    #     print(f"主题: {email_subject}")
    #     print(email_body)
    #     print("---------------------\n")
    #
    #     # 发送邮件
    #     send_email(
    #         recipient=EMAIL_RECEIVER,
    #         subject=email_subject,
    #         body=email_body
    #     )
    # else:
    #     print("获取文章目录失败，任务中止。")
    # print("--- 任务执行完毕 ---")
