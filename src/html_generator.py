from config import ARXIV_HTML_TEMPLATE,PAPER_CARD_TEMPLATE

class ArxivHtmlGenerator:
    def __init__(self):
        self.cards = []
        try:
            with open(ARXIV_HTML_TEMPLATE, 'r', encoding='utf-8') as f:
                self.template = f.read()
        except FileNotFoundError:
            print(f"错误: 模板文件 '{ARXIV_HTML_TEMPLATE}' 未找到。")
            raise

        try:
            with open(PAPER_CARD_TEMPLATE, 'r', encoding='utf-8') as f:
                self.paper_card_template = f.read()
        except FileNotFoundError:
            print(f"错误: 模板文件 '{PAPER_CARD_TEMPLATE}' 未找到。")
            raise

    def create_paper_card(self, paper_data: dict):
        """
        使用单篇论文的数据填充卡片模板。
        字典键值说明：
            - title_zh: 论文中文标题
            - title_en: 论文英文标题
            - authors: 作者列表
            - abstract_zh: 论文中文摘要
            - ai_analysis: AI分析
            - pdf_url: PDF下载链接
            - id: arXiv 页面 ID
        :param paper_data: 单篇论文的数据字典。
        """
        # 替换所有占位符
        paper_card = self.paper_card_template
        paper_card = paper_card.replace("{PAPER_TITLE_ZH}", paper_data.get("title_zh", "无标题"))
        paper_card = paper_card.replace("{PAPER_TITLE_EN}", paper_data.get("title_en", ""))
        paper_card = paper_card.replace("{PAPER_AUTHORS}", ", ".join(paper_data.get("authors", [])))
        paper_card = paper_card.replace("{PAPER_ABSTRACT_ZH}", paper_data.get("abstract_zh", "摘要不可用。"))
        paper_card = paper_card.replace("{AI_ANALYSIS}",
                                      paper_data.get("ai_analysis", "AI分析不可用。").replace("\n", "<br>"))  # 将换行符转为HTML换行
        paper_card = paper_card.replace("{PDF_URL}", paper_data.get("pdf_url", "#"))
        # 假设 arXiv 页面链接可以通过 ID 构建
        arxiv_id = paper_data.get("id", "").split('/')[-1]
        paper_card = paper_card.replace("{ARXIV_URL}", f"https://arxiv.org/abs/{arxiv_id}")

        self.cards.append(paper_card)

    def generate_arxiv_email(self)->str:
        """
        将所有论文卡片组装到主邮件模板中。
        :return: 完整的邮件html内容
        """
        final_email = self.template

        # 替换主模板中的占位符
        final_email = final_email.replace("{PAPER_COUNT}", str(len(self.cards)))
        final_email = final_email.replace("{PAPER_CARDS}", " ".join(self.cards))

        return final_email