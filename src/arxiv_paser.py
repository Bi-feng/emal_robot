import arxiv
from datetime import datetime, timedelta, timezone

def fetch_daily_arxiv_papers():
    """
    获取昨天在指定领域内新提交到 arXiv 的所有论文。
    """
    # 1. 定义你感兴趣的领域
    # 可以从 arXiv 官网找到所有领域的缩写
    target_categories = "cs.CV OR cs.LG OR cs.AI OR cs.CL OR stat.ML"
    query = f"cat:({target_categories})"

    # 2. 设置搜索参数
    # 按提交日期降序排序，获取最新的论文
    search = arxiv.Search(
        query=query,
        max_results=500,  # 设置一个足够大的数字以覆盖一天的论文量
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    # 3. 在客户端按日期过滤
    # 获取昨天的日期。注意处理时区问题，arXiv 使用的是 UTC 时间。
    yesterday_utc = datetime.now(timezone.utc) - timedelta(days=1)
    
    candidate_papers = []
    for result in search.results():
        # result.published 和 result.updated 都是带时区的 datetime 对象
        # 我们关心的是初次提交的日期
        if result.published.date() == yesterday_utc.date():
            paper_data = {
                "id": result.entry_id,
                "title": result.title,
                "abstract": result.summary,
                "authors": [author.name for author in result.authors],
                "pdf_url": result.pdf_url,
                "published_date": result.published.date(),
                "comments": result.comment # 这个字段非常重要，常包含会议信息
            }
            candidate_papers.append(paper_data)
        # 因为结果是按日期降序的，一旦日期早于昨天，就可以停止了
        elif result.published.date() < yesterday_utc.date():
            break
    
    print(f"成功获取 {len(candidate_papers)} 篇昨日发布的候选论文。")
    return candidate_papers

# 运行函数
if __name__ == "__main__":
    daily_papers = fetch_daily_arxiv_papers()
    for paper in daily_papers:
        print(f"标题: {paper['title']}")
        print(f"作者: {', '.join(paper['authors'])}")
        print(f"发布日期: {paper['published_date']}")
        print(f"摘要: {paper['abstract'][:100]}...")  # 只打印摘要的前100个字符
        print(f"PDF链接: {paper['pdf_url']}")
        print(f"评论: {paper['comments']}\n")

