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

def fetch_config_content(url):
    """دریافت محتوای خام یک URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text, f"Source from {url}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}", f"Error fetching {url}"

def generate_html_content():
    update_time = datetime.datetime.utcnow().isoformat()
    sections_data = []

    # جمع‌آوری همه کانفیگ‌ها
    for i, source_url in enumerate(CONFIG_SOURCES):
        content, source_name = fetch_config_content(source_url)
        configs = [line.strip() for line in content.splitlines() if line.strip()]
        sections_data.append({
            "id": f"source_{i}",
            "source_name": source_name,
            "configs": configs
        })

    # JSON برای JS
    sections_json = json.dumps(sections_data, ensure_ascii=False)

    # HTML مینیمال و یک textarea بزرگ
    final_html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap" rel="stylesheet">
<style>
body {{
    font-family: 'Vazirmatn', monospace;
    margin: 0; padding: 0; background: #f4f7f9; color: #333;
}}
.container {{
    max-width: 1000px;
    margin: 20px auto;
    padding: 10px;
}}
textarea#all-configs {{
    width: 100%;
    height: 90vh;
    font-family: monospace;
    font-size: 14px;
    padding: 10px;
    box-sizing: border-box;
    resize: none;
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
    <textarea id="all-configs" readonly placeholder="در حال بارگذاری کانفیگ‌ها..."></textarea>
    <div class="update-info">
        <p>توجه: این صفحه توسط اسکریپت خودکار گیت‌هاب ساخته شده است.</p>
        <p>آخرین به‌روزرسانی: {update_time} (اجرا شده توسط GitHub Action)</p>
    </div>
</div>
<script>
const sectionsData = {sections_json};
let allConfigs = "";
sectionsData.forEach(sec => {{
    allConfigs += sec.configs.join("\\n") + "\\n";
}});
document.getElementById("all-configs").value = allConfigs;
</script>
</body>
</html>
"""
    final_html += f"\n<!-- build timestamp: {datetime.datetime.utcnow().isoformat()} -->\n"
    return final_html

if __name__ == "__main__":
    html_content = generate_html_content()
    OUTPUT_FILE = os.path.join(os.getcwd(), "index.html")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"فایل {OUTPUT_FILE} با موفقیت ذخیره شد.")
