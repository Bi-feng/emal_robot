# emal_robot

这是一个使用 Python、Selenium 和 smtplib 实现的自动化项目，它可以抓取指定网站的标题并通过邮件发送报告。

## 功能
- 使用 Selenium (Edge) 抓取网页标题。
- 使用 smtplib 发送邮件报告。
- 通过 `.env` 文件管理敏感配置。

## 安装与设置

1.  **克隆仓库**
    ```bash
    git clone <your-repo-url>
    cd email_project
    ```

2.  **创建并配置虚拟环境 (推荐)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

4.  **配置环境变量**
    - 复制 `.env.example` (如果有的话) 为 `.env`，或者手动创建一个 `.env` 文件。
    - 填入你的邮箱配置和目标 URL。
    ```
    SMTP_SERVER="smtp.example.com"
    SMTP_PORT=465
    SENDER_EMAIL="your_email@example.com"
    SENDER_PASSWORD="your_app_password"
    TARGET_URL="https://www.python.org"
    ```

5.  **【重要】设置 WebDriver**
    - 本项目使用 Selenium 控制 Microsoft Edge 浏览器。
    - **检查你的 Edge 浏览器版本** (设置 -> 关于 Microsoft Edge)。
    - **下载对应的 EdgeDriver**：访问 [Microsoft Edge WebDriver 官网](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)，下载与你浏览器版本完全匹配的驱动。
    - **在项目根目录下创建一个 `drivers/` 文件夹**。
    - 将下载的 `msedgedriver.exe` (或对应系统的驱动文件) 放入 `drivers/` 文件夹中。
    - 在config.py文件中修改DRIVER_PATH的路径
    - **注意**：`drivers/` 目录已被 `.gitignore` 忽略，不会被提交到版本库。

## 运行项目
```bash
python main.py
```
