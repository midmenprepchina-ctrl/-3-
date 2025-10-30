import os, json, re
from bs4 import BeautifulSoup

# 文章文件夹路径
ARTICLE_DIR = "./articles"   # 这里放你的所有文章html文件
OUTPUT_FILE = "articles.json"

articles = []

for file in os.listdir(ARTICLE_DIR):
    if file.endswith(".html"):
        filepath = os.path.join(ARTICLE_DIR, file)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")

        # 1️⃣ 获取标题
        title = soup.title.string.strip() if soup.title else file.replace(".html", "")

        # 2️⃣ 获取正文第一张图片
        img_tag = soup.find("img")
        image = img_tag["src"] if img_tag and "src" in img_tag.attrs else "images/default.jpg"

        # 3️⃣ 获取正文文字摘要
        text = soup.get_text().strip()
        text = re.sub(r"\s+", " ", text)
        desc = text[:120] + "..." if len(text) > 120 else text

        # 4️⃣ 构建条目
        article_data = {
            "title": title,
            "author": "木子AI",
            "date": "2025-10-30",
            "views": "0",
            "tags": [],
            "desc": desc,
            "image": image,
           "link": f"articles/{file}"
        }
        articles.append(article_data)

# 按文件名排序（最新的在前）
articles.sort(key=lambda x: x["title"], reverse=True)

# 写入 JSON 文件
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"✅ 已成功生成 {OUTPUT_FILE}，共 {len(articles)} 篇文章")
