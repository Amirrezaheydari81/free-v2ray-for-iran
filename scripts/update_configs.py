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

TITLE = "V2Ray Config Aggregator"
BASE_URL = "https://yourdomain.com/"  # دامنه سایتت رو اینجا قرار بده

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
    update_time = datetime.datetime.utcnow().isoformat()
    sections_data = []

    # جمع‌آوری همه کانفیگ‌ها
    all_configs_text = ""
    for i, source_url in enumerate(CONFIG_SOURCES):
        content, source_name = fetch_config_content(source_url)
        configs = [line.strip() for line in content.splitlines() if line.strip()]
        sections_data.append({
            "id": f"source_{i}",
            "source_name": source_name,
            "configs": configs
        })
        all_configs_text += "\n".join(configs) + "\n"

    sections_json = json.dumps(sections_data, ensure_ascii=False)

    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap" rel="stylesheet">
<title>{TITLE}</title>
</head>
<body>
<div class="container">
<h1>{TITLE}</h1>
<p>آخرین به‌روزرسانی: {update_time} (اجرا شده توسط GitHub Action)</p>

<!-- textarea بزرگ برای همه کانفیگ‌ها -->
<textarea id="all-configs" readonly style="width:100%; height:80vh; font-family: monospace;">{all_configs_text}</textarea>

<div class="update-info">
<p>توجه: این صفحه توسط اسکریپت خودکار گیت‌هاب ساخته شده است.</p>
</div>
</div>

<script>
// داده‌های کانفیگ‌ها برای استفاده در آینده
const sectionsData = {sections_json};

// امکان کپی سریع: کاربر می‌تواند Ctrl+A و سپس Ctrl+C بزند
</script>
</body>
</html>
"""
    return html_content

# ---------------------------------------------------------------------------
# تولید سایت‌مپ
# ---------------------------------------------------------------------------
def generate_sitemap():
    pages = ["index.html"]  # در صورت وجود صفحات دیگر، اینجا اضافه کن
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
    # ساخت HTML
    html_content = generate_html_content()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html با موفقیت ساخته شد ✅")

    # ساخت سایت‌مپ
    sitemap_content = generate_sitemap()
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print("sitemap.xml با موفقیت ساخته شد ✅")
