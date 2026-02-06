import requests
import os
import datetime
import json

CONFIG_SOURCES = [
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/Firmfox/Proxify/refs/heads/main/v2ray_configs/seperated_by_protocol/vless.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/refs/heads/main/All_Configs_Sub.txt",
]

TITLE = "دانلود کانفیگ‌های V2Ray رایگان برای ایران"
DESCRIPTION = "مجموعه‌ای از کانفیگ‌های V2Ray رایگان و آماده استفاده برای کاربران ایرانی. تمامی کانفیگ‌ها قابل کپی کردن و مستقیم استفاده در برنامه‌های V2Ray هستند."
KEYWORDS = "V2Ray, کانفیگ V2Ray, دانلود V2Ray, فیلترشکن, پراکسی, وی پی ان"

def fetch_config_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"

def generate_html():
    update_time = datetime.datetime.utcnow().isoformat()
    all_configs = ""

    for source_url in CONFIG_SOURCES:
        content = fetch_config_content(source_url)
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        all_configs += "\n".join(lines) + "\n"

    html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESCRIPTION}">
<meta name="keywords" content="{KEYWORDS}">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap" rel="stylesheet">
<style>
body {{
    font-family: 'Vazirmatn', monospace;
    background: #f4f7f9;
    margin: 0;
    padding: 20px;
}}
.container {{
    max-width: 1000px;
    margin: auto;
}}
h1 {{
    color: #2c3e50;
    margin-bottom: 15px;
}}
textarea#all-configs {{
    width: 100%;
    height: 90vh;
    font-family: monospace;
    font-size: 14px;
    padding: 10px;
    resize: none;
    box-sizing: border-box;
}}
.update-info {{
    margin-top: 15px;
    font-size: 0.85em;
    color: #555;
}}
</style>
</head>
<body>
<div class="container">
<h1>{TITLE}</h1>
<textarea id="all-configs" readonly>{all_configs}</textarea>
<div class="update-info">
<p>توجه: این صفحه توسط اسکریپت خودکار گیت‌هاب ساخته شده است.</p>
<p>آخرین به‌روزرسانی: {update_time} (UTC)</p>
</div>
</div>
</body>
</html>
"""
    return html_content

def generate_sitemap(base_url="https://yourdomain.com/"):
    urls = ["index.html"]
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap_xml += f"  <url>\n    <loc>{base_url}{url}</loc>\n    <lastmod>{datetime.datetime.utcnow().date()}</lastmod>\n  </url>\n"
    sitemap_xml += "</urlset>"
    return sitemap_xml

if __name__ == "__main__":
    # ذخیره HTML
    html_file = "index.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(generate_html())
    print(f"{html_file} با موفقیت ذخیره شد.")

    # ذخیره Sitemap
    sitemap_file = "sitemap.xml"
    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(generate_sitemap())
    print(f"{sitemap_file} با موفقیت ذخیره شد.")
