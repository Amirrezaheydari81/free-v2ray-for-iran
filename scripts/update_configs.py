import requests
import os
from bs4 import BeautifulSoup
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


def fetch_config_content(url):
    """دریافت محتوای خام یک URL."""
    try:
        # استفاده از User-Agent برای جلوگیری از بلاک شدن توسط برخی سرورها
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # فرض می‌کنیم محتوا متنی است و مستقیماً آن را برمی‌گردانیم
        # اگر نیاز به جداسازی محتوای خاصی بود، اینجا از BeautifulSoup استفاده می‌شود.
        return response.text, f"Source from {url}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}", f"Error fetching {url}"

def generate_html_content():
    all_sections_html = ""
    update_time = datetime.datetime.utcnow().isoformat()
    sections_data = []

    for i, source_url in enumerate(CONFIG_SOURCES):
        content, source_name = fetch_config_content(source_url)
        # تقسیم محتوا به خطوط غیرخالی
        configs = [line.strip() for line in content.splitlines() if line.strip()]
        sections_data.append({
            "id": f"source_{i}",
            "source_name": source_name,
            "configs": configs
        })

        # هر سکشن در دو ستون (فلکس)
        # برای ساده سازی، هر منبع یک ستون است، بعد در CSS دو ستون نمایش داده می‌شود
        section_html = f"""
        <div class="config-column">
            <div class="config-header">
                کانفیگ {i+1} ({source_name.split('from ')[-1]})
                <button class="copy-btn">کپی</button>
            </div>
            <div class="config-content">
                <textarea readonly id="textarea-{i+1}" >{content}</textarea>
            </div>
        </div>
        """
        all_sections_html += section_html

    # JSON برای JS
    sections_json = json.dumps(sections_data, ensure_ascii=False)

    final_html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./style.css">
<title>{TITLE}</title>
</head>
<body>
<div class="container">
<h1>{TITLE}</h1>
<p>آخرین به‌روزرسانی: {update_time} (اجرا شده توسط GitHub Action)</p>

<div class="grid" id="configs-container">
{all_sections_html}
</div>

<div class="update-info">
<p>توجه: این صفحه توسط اسکریپت خودکار گیت‌هاب ساخته شده است.</p>
</div>
</div>

<script>
const sectionsData = {sections_json};
</script>
<script src="./script.js"></script>
</body>
</html>
"""
    final_html += f"\n<!-- build timestamp: {datetime.datetime.utcnow().isoformat()} -->\n"
    return final_html


if __name__ == "__main__":
    if not CONFIG_SOURCES:
        print("هشدار: لیست CONFIG_SOURCES خالی است. لطفاً آدرس‌های کانفیگ خود را اضافه کنید.")
        # ساخت یک صفحه خالی با پیام خطا
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head><meta charset="UTF-8"><title>{TITLE}</title><style>{CSS_STYLES}</style></head>
        <body>
            <div class="container">
                <h1>خطای پیکربندی</h1>
                <p>اسکریپت اجرا شد، اما لیست منابع کانفیگ (CONFIG_SOURCES) در فایل update_configs.py خالی است. لطفاً آدرس‌های خام کانفیگ‌ها را وارد کنید.</p>
                <p>آخرین اجرا: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </body>
        </html>
        """
    else:
        print(f"شروع استخراج {len(CONFIG_SOURCES)} منبع...")
        html_content = generate_html_content()
        print("تولید HTML با موفقیت انجام شد.")
    # ذخیره فایل HTML نهایی در ریشه مخزن
    OUTPUT_FILE = os.path.join(os.getcwd(), "index.html")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"فایل {OUTPUT_FILE} با موفقیت ذخیره شد.")
