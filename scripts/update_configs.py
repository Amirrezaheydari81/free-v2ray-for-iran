import requests
import os
import datetime
import json

# =============================================================================
# تنظیمات: این لیست را با آدرس‌های خام کانفیگ‌های V2Ray خود پر کنید
# =============================================================================
CONFIG_SOURCES_ENV = os.getenv("CONFIG_SOURCES", "")

if CONFIG_SOURCES_ENV.strip():
    CONFIG_SOURCES = [url.strip() for url in CONFIG_SOURCES_ENV.split(",") if url.strip()]
else:
    CONFIG_SOURCES = [
        "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt",
        "https://raw.githubusercontent.com/Firmfox/Proxify/refs/heads/main/v2ray_configs/seperated_by_protocol/vless.txt",
        "https://github.com/Epodonios/v2ray-configs/raw/refs/heads/main/All_Configs_Sub.txt",
    ]

TITLE = "V2Ray کانفیگ - جمع‌آوری و دانلود"
META_DESCRIPTION = "بهترین و جدیدترین کانفیگ‌های V2Ray به صورت یکجا. کپی سریع و استفاده آسان برای کاربران ایرانی."
META_KEYWORDS = "V2Ray, کانفیگ V2Ray, وی پی ان, پروکسی, ابزار اینترنت, دانلود کانفیگ"
BASE_URL = "https://amirrezaheydari81.github.io/free-v2ray-for-iran/"  # دامنه سایتت رو اینجا قرار بده

# ---------------------------------------------------------------------------
# دریافت محتوای هر URL
# ---------------------------------------------------------------------------
def fetch_config_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text, f"Source from {url}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}", f"Error fetching {url}"

# ---------------------------------------------------------------------------
# تولید HTML
# ---------------------------------------------------------------------------
def generate_html_content():
    update_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    all_configs_text = ""

    for source_url in CONFIG_SOURCES:
        content, _ = fetch_config_content(source_url)
        configs = [line.strip() for line in content.splitlines() if line.strip()]
        all_configs_text += "\n".join(configs) + "\n"

    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{META_DESCRIPTION}">
<meta name="keywords" content="{META_KEYWORDS}">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
body {{
    font-family: 'Vazirmatn', sans-serif;
    background-color: #f4f6f8;
    margin: 0;
    padding: 20px;
    color: #333;
}}
.container {{
    max-width: 900px;
    margin: auto;
}}
h1 {{
    text-align: center;
    color: #1e3a8a;
    margin-bottom: 20px;
}}
textarea {{
    width: 100%;
    height: 80vh;
    font-family: monospace;
    font-size: 14px;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    background-color: #fefefe;
    resize: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}}
.update-info {{
    text-align: center;
    margin-top: 15px;
    font-size: 0.85em;
    color: #555;
}}
</style>
</head>
<body>
<div class="container">
<h1>{TITLE}</h1>

<textarea readonly id="all-configs" placeholder="در حال بارگذاری کانفیگ‌ها...">{all_configs_text}</textarea>

<div class="update-info">
<p>آخرین به‌روزرسانی: {update_time} (اجرا شده توسط GitHub Action)</p>
<p>تمامی کانفیگ‌ها در یکجا برای کپی سریع آماده شده‌اند. برای کپی کل متن، Ctrl+A و سپس Ctrl+C را بزنید.</p>
</div>
</div>
</body>
</html>
"""
    return html_content

# ---------------------------------------------------------------------------
# تولید سایت‌مپ
# ---------------------------------------------------------------------------
def generate_sitemap():
    pages = ["index.html"]
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        sitemap_xml += f"  <url>\n"
        sitemap_xml += f"    <loc>{BASE_URL}{page}</loc>\n"
        sitemap_xml += f"    <lastmod>{datetime.datetime.utcnow().date()}</lastmod>\n"
        sitemap_xml += f"  </url>\n"
    sitemap_xml += "</urlset>"
    return sitemap_xml

# ---------------------------------------------------------------------------
# اجرای اصلی
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    html_content = generate_html_content()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html با موفقیت ساخته شد ✅")

    sitemap_content = generate_sitemap()
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("sitemap.xml با موفقیت ساخته شد ✅")
