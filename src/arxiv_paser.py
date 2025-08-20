import arxiv
from datetime import datetime, timedelta, timezone

def fetch_daily_arxiv_papers(categories:list[str], keywords:list[str], authors:list[str] = None)->list[dict]:
    """
    获取昨天在指定领域内，且标题或摘要包含指定关键词的论文。

    :param authors: list of str, e.g., ["John Doe", "Jane Smith"]
    :param categories: list of str, e.g., ['cs.CV','cs.LG']
    :param keywords: list of str, e.g., ["diffusion model", "large language model"]
    """
    # 1. 构建关键词查询部分
    # 搜索范围是标题(ti)或摘要(abs)
    keyword_queries = [f'(ti:"{kw}" OR abs:"{kw}")' for kw in keywords]
    keyword_query_part = " OR ".join(keyword_queries)

    category_queries = [f'cat:{cat}' for cat in categories]
    category_query_part = " OR ".join(category_queries)

    author_queries = [f'au:"{au}"' for au in authors] if authors else []
    author_query_part =" OR  ".join(author_queries) if authors is not None else None

    # 2. 组合领域和关键词查询
    # 使用 AND 将两者连接，表示必须同时满足
    if author_query_part is not None:
        query = f"({category_query_part}) AND (({author_query_part}) OR ({keyword_query_part}))"
    else:
        query = f"({category_query_part}) AND ({keyword_query_part})"


    search = arxiv.Search(
        query=query,
        max_results=100,  # 结果会少很多，不需要设太大
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    client = arxiv.Client()

    # 3. 同样在客户端按日期过滤，确保是昨天发布的
    yesterday_utc = datetime.now(timezone.utc) - timedelta(days=1)

    candidate_papers = []
    for result in client.results(search):
        if result.published.date() == yesterday_utc.date():
            paper_data = {
                "id": result.entry_id,
                "title": result.title,
                "abstract": result.summary,
                "authors": [author.name for author in result.authors],
                "pdf_url": result.pdf_url,
                "published_date": result.published.date(),
                "comments": result.comment  # 这个字段非常重要，常包含会议信息
            }
            candidate_papers.append(paper_data)
        elif result.published.date() < yesterday_utc.date():
            break
    return candidate_papers

# 运行函数
if __name__ == "__main__":
    daily_papers = fetch_daily_arxiv_papers(["cs.CV"],["shadow removal", "image restoration"])
    print(f"找到{len(daily_papers)}篇论文")
    for paper in daily_papers:
        print(f"标题: {paper['title']}")
        print(f"作者: {', '.join(paper['authors'])}")
        print(f"发布日期: {paper['published_date']}")
        print(f"摘要: {paper['abstract'][:100]}...")  # 只打印摘要的前100个字符
        print(f"PDF链接: {paper['pdf_url']}")
        print(f"评论: {paper['comments']}\n")

