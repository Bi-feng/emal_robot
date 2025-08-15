from .emal_sender import send_email
from .web_scraper import scrape_website_title, scrape_qiushi_articles, scrape_articles_text, scrape_qiushi_journal
from .data_handler import save_journal_urls, load_journal_data,save_article_urls

__all__ = [
    'send_email',
    'scrape_website_title',
    'scrape_qiushi_articles',
    'scrape_articles_text',
    'scrape_qiushi_journal',
    'save_journal_urls',
]