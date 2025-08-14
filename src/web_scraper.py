from typing import Optional

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin

from config import DRIVER_PATH,QIUSHI_URL

# --- 配置  无头模式 ---
edge_options = Options()

# edge_options.add_argument("--headless")# 如果你不想在后台运行（无头模式），可以注释下面这行

edge_options.add_argument("--disable-gpu")  # 有时在无头模式下有帮助
edge_options.add_argument("--window-size=1920,1080")
webdriver_service = Service(DRIVER_PATH)


def scrape_website_title(url: str) -> Optional[str]:
    """
    使用 Selenium (无头模式) 访问一个 URL 并返回其页面标题。

    Args:
        url: 要访问的网站地址。

    Returns:
        如果成功，返回页面标题字符串；如果失败，返回 None。
    """
    print(f"正在使用 Selenium 访问: {url}")


    driver = None
    try:
        # 初始化 WebDriver
        driver = webdriver.Edge(service=webdriver_service, options=edge_options)

        # 访问页面
        driver.get(url)

        # 获取标题
        title = driver.title
        print(f"成功获取标题: '{title}'")
        return title

    except Exception as e:
        print(f"网页抓取失败: {e}")
        return None

    finally:
        # 确保无论成功还是失败，浏览器都会被关闭
        if driver:
            driver.quit()
            print("Selenium 浏览器已关闭。")

def scrape_qiushi_journal(url: str) -> list[dict]:
    """
        访问《求是》网，抓取所有期的标题和链接。

        Args:
            url: 《求是》网的2025年所有期刊的目录 URL。

        Returns:
            一个包含文章信息的字典列表，例如:
            [{'title': '期刊标题1', 'url': '完整链接'}, ...]
            如果失败则返回空列表。
    """
    print(f"正在抓取 {url} 的最新期刊...")
    driver = None
    results = []
    try:
        driver = webdriver.Edge(service=webdriver_service, options=edge_options)
        driver.get(url)
        # 使用显式等待，等待文章列表的容器加载完成，这让脚本更稳定
        # 我们等待 IDs 为 "detailContent" 的元素出现，最长等待20秒
        wait = WebDriverWait(driver, 20)
        detail_content_div = wait.until(
            EC.presence_of_element_located((By.ID, "detailContent"))
        )

        # 在容器内查找所有的 <a> 标签
        article_links = detail_content_div.find_elements(By.TAG_NAME, "a")

        print(f"找到了 {len(article_links)} 篇期刊链接。")
        for link_element in article_links:
            title = link_element.text.strip()  # .strip() 去除首尾多余的空格
            relative_url = link_element.get_attribute('href')

            # 确保标题和链接都有效
            if title and relative_url:
                # 使用 urljoin 将基础 URL 和相对路径安全地拼接成完整 URL
                full_url = urljoin(url, relative_url)
                results.append({'title': title, 'url': full_url})
    except Exception as e:
        print(f"抓取《求是》网文章失败: {e}")
        # 发生异常时返回空列表
        return []

    finally:
        if driver:
            driver.quit()

    return results

def scrape_qiushi_articles(url: str) -> list[dict]:
    pass

def scrape_articles_text(url: str) -> str:
    print(f"正在抓取 {url} 的文章内容...")
    driver = None
    results = []
    try:
        driver = webdriver.Edge(service=webdriver_service, options=edge_options)
        driver.get(url)
        # 使用显式等待，等待文章列表的容器加载完成，这让脚本更稳定
        # 我们等待 IDs 为 "detailContent" 的元素出现，最长等待20秒
        wait = WebDriverWait(driver, 20)
        detail_content_div = wait.until(
            EC.presence_of_element_located((By.ID, "detailContent"))
        )

        # 在容器内查找所有的 <a> 标签
        article_links = detail_content_div.find_elements(By.TAG_NAME, "p")

        results = '\n'.join([x.text for x in article_links])
        print(f"成功获取文章内容。")
    except Exception as e:
        print(f"抓取《求是》网文章失败: {e}")
        # 发生异常时返回空字符串
        return ''

    finally:
        if driver:
            driver.quit()

    return results

# Example usage:
if __name__ == "__main__":
    url = 'http://www.qstheory.cn/20250731/c9eb828df29e495d92e940755483bc8b/c.html'
    results = scrape_articles_text(url)
    print(results)
