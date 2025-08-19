import json
import os
from config import DATA_PATH
# 定义我们的“数据库”文件名

os.makedirs(DATA_PATH, exist_ok=True)
JOURNALS_DICT = DATA_PATH / 'journals'
os.makedirs(JOURNALS_DICT, exist_ok=True)
JOURNALS_FILE = JOURNALS_DICT / 'journals.json'

def load_journal_data() -> list[dict]:
    """
    从 JSON 文件中加载完整的期刊文章数据。
    如果文件不存在或无效，返回一个空列表。
    """
    if not os.path.exists(JOURNALS_FILE):
        return []

    try:
        with open(JOURNALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 确保返回的是一个列表
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        # 如果文件损坏或为空，也返回空列表
        return []
def load_article_data(title:str)-> list[dict]:
    """
    读取articles.json文件，按照期刊title分文件夹存放在JOURNALS_DICT下。
    每个文件夹下存放当前期刊的所有文章的url的JSON文件。
    title:期刊名称
    返回当前期刊的所有文章的url的JSON文件
    """
    title_path = JOURNALS_DICT / title
    data_file = title_path / 'articles.json'
    if not os.path.exists(data_file):
        return []
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except (json.JSONDecodeError, IOError):
        # 如果文件损坏或为空，也返回空列表
        return []
def save_journal_urls(data:  list[dict])-> bool:
    """
    将更新后的 URL 集合保存回 JSON 文件。
    如果JSON长度有变化，则返回 True，否则返回 False。
    """

    old_data = load_journal_data()
    old_length = len(old_data)

    new_length = len(data)

    with open(JOURNALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return old_length != new_length

def save_article_urls(title:str, data:  list[dict]):
    """
    读取jouranls.json文件，按照期刊title分文件夹存放在JOURNALS_DICT下。
    每个文件夹下存放当前期刊的所有文章的url的JSON文件。
    title:期刊名称
    data:文章url的列表,格式：[{'title': '文章1', 'url': 'https://www.example.com/article1'},{dict2},...]
    """
    title_path = JOURNALS_DICT / title
    title_path.mkdir(exist_ok=True)
    data_file = title_path / 'articles.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

