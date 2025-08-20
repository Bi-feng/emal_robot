from .emal_sender import send_html_email
from .web_scraper import scrape_website_title, scrape_qiushi_articles, scrape_articles_text, scrape_qiushi_journal
from .data_handler import save_journal_urls, load_journal_data,save_article_urls,load_article_data
from .ai_handler import generate_content,process_paper_with_ai
from .arxiv_paser import fetch_daily_arxiv_papers
from .utils import text_to_html
from .html_generator import ArxivHtmlGenerator

__all__ = [
    'send_html_email',
    'scrape_website_title',
    'scrape_qiushi_articles',
    'scrape_articles_text',
    'scrape_qiushi_journal',
    'save_journal_urls',
    'generate_content',
    'text_to_html',
    'load_journal_data',
    'save_article_urls',
    'load_article_data',
    'fetch_daily_arxiv_papers',
    'process_paper_with_ai',
    'ArxivHtmlGenerator'
]