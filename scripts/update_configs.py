import requests
import os
from bs4 import BeautifulSoup
import datetime

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

OUTPUT_FILE = os.path.join(os.getcwd(), "index.html")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

TITLE = "V2Ray Config Aggregator"

# استایل‌های تمیز برای ظاهر حرفه‌ای
CSS_STYLES = """
body {
    font-family: 'Tahoma', sans-serif;
    background-color: #f4f7f9;
    color: #333;
    margin: 0;
    padding: 20px;
}
.container {
    max-width: 1000px;
    margin: auto;
    background: #fff;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
h1 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 20px;
}
.config-section {
    margin-bottom: 30px;
    padding: 15px;
    border: 1px solid #ecf0f1;
    border-radius: 6px;
    background-color: #fafafa;
}
.config-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    cursor: pointer;
    font-weight: bold;
    color: #2980b9;
}
.config-content {
    display: none; /* پنهان کردن پیش‌فرض */
}
.config-content.active {
    display: block;
}
textarea {
    width: 100%;
    height: 150px;
    padding: 10px;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    resize: vertical;
    box-sizing: border-box;
    margin-top: 5px;
}
button {
    background-color: #2ecc71;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-left: 10px;
}
button:hover {
    background-color: #27ae60;
}
.icon {
    font-size: 1.2em;
}
.update-info {
    text-align: right;
    font-size: 0.8em;
    color: #7f8c8d;
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px dashed #ecf0f1;
}
"""

# اسکریپت جاوا اسکریپت برای قابلیت کپی کردن
JS_SCRIPT = """
function setupCopyButtons() {
    document.querySelectorAll('.config-header').forEach(header => {
        if (header.getAttribute('data-setup') === 'true') return;
        header.setAttribute('data-setup', 'true');

        const sourceId = header.id.replace('header-', 'content-');
        const contentDiv = document.getElementById(sourceId);

        const copyButton = document.createElement('button');
        copyButton.innerHTML = '<span class="icon">&#128206;</span> کپی';
        copyButton.onclick = function() {
            const textarea = contentDiv.querySelector('textarea');
            if (textarea) {
                textarea.select();
                document.execCommand('copy');
                copyButton.innerHTML = '<span class="icon">&#10003;</span> کپی شد!';
                setTimeout(() => {
                    copyButton.innerHTML = '<span class="icon">&#128206;</span> کپی';
                }, 2000);
            }
        };

        const toggleButton = document.createElement('span');
        toggleButton.className = 'icon';
        toggleButton.innerHTML = '&#9660;'; // مثلث رو به پایین

        header.appendChild(toggleButton);

        header.onclick = function() {
            contentDiv.classList.toggle('active');
            toggleButton.innerHTML = contentDiv.classList.contains('active') ? '&#9650;' : '&#9660;'; // مثلث بالا/پایین
        };

        header.style.cursor = 'pointer';
        header.appendChild(copyButton);
    });
}
window.onload = setupCopyButtons;
"""

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
    """ساخت کل محتوای HTML نهایی."""
    all_sections_html = ""
    update_time = datetime.datetime.utcnow().isoformat()

    for i, source_url in enumerate(CONFIG_SOURCES):
        content, source_name = fetch_config_content(source_url)

        # برای سادگی و اطمینان، محتوای دریافتی را مستقیماً درون تگ textarea می‌گذاریم.
        # این کار شامل متن‌های خطا نیز می‌شود تا کاربر در جریان مشکلات قرار گیرد.

        # ایجاد یک آیدی منحصر به فرد برای هر بخش
        source_id = f"source_{i}"

        section_html = f"""
        <div class="config-section">
            <div class="config-header" id="header-{source_id}">
                <span>کانفیگ شماره {i+1} ({source_name.split('from ')[-1]})</span>
            </div>
            <div class="config-content" id="content-{source_id}">
                <textarea readonly placeholder="Config Content Loading...">{content}</textarea>
            </div>
        </div>
        """
        all_sections_html += section_html

    final_html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <style>
        {CSS_STYLES}
    </style>
</head>
<body>
    <div class="container">
        <h1>{TITLE}</h1>
        <p>آخرین به‌روزرسانی: {update_time} (اجرا شده توسط GitHub Action)</p>

        {all_sections_html}

        <div class="update-info">
            <p>توجه: این صفحه توسط اسکریپت خودکار گیت‌هاب ساخته شده است.</p>
        </div>
    </div>

    <script>
        {JS_SCRIPT}
    </script>
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
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"فایل {OUTPUT_FILE} با موفقیت ذخیره شد.")
