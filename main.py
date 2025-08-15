from src import send_email, scrape_website_title, scrape_qiushi_articles, scrape_articles_text, scrape_qiushi_journal
from src import save_journal_urls, load_journal_data, save_article_urls
from src import send_html_email
from src import text_to_html,generate_content
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
    # 1. 调用抓取函数
    journals = scrape_qiushi_journal(QIUSHI_URL)
    # 2. 保存结果
    isupdated = save_journal_urls(journals)

    if isupdated:
        print("期刊目录有更新，正在准备抓取最新一期期刊...")
        # 3. 调用抓取最新一期期刊目录的函数
        journal_title= load_journal_data()[-1]['title']
        journal_url = load_journal_data()[-1]['url']
        latest_articles = scrape_qiushi_articles(journal_url)
        # 4. 保存最新一期期刊目录
        save_article_urls(journal_title, latest_articles)

        for x in latest_articles:
            title = x['title']
            url = x['url']
            txt_path = os.path.join(DATA_PATH, 'journals', f"{journal_title}", f"{title}.txt")
            if not os.path.exists(txt_path):
                with open(txt_path, 'w', encoding='utf-8') as f:
                    text = scrape_articles_text(url)
                    f.write(text)
            else:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    text = f.read()

            # 发送邮件
            print(f'正在AI分析《{title}》...')
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
                            {text_to_html(text)}
                        </div>
                        <div class="section ai-analysis">
                            <h2>AI分析</h2>
                            {generate_content(text)}
                            
                        </div>
                        <p>祝好！<br>你的自动化助手</p>
                    </div>
                </body>
                </html>
                """
            send_html_email(EMAIL_RECEIVER, f"{title}", final_html_content)




