window.onload = function () {
    const container = document.getElementById("configs-container");

    sectionsData.forEach((section, idx) => {
        // ساخت بخش
        const sectionDiv = document.createElement("div");
        sectionDiv.className = "config-section";

        // Header
        const header = document.createElement("div");
        header.className = "config-header";
        header.id = `header-${section.id}`;
        header.innerHTML = `<span>کانفیگ شماره ${idx + 1} (${section.source_name.split('from ').pop()})</span> <span class="icon">&#9660;</span>`;

        // Content
        const contentDiv = document.createElement("div");
        contentDiv.className = "config-content";
        contentDiv.id = `content-${section.id}`;

        const pre = document.createElement("pre");
        pre.textContent = section.configs.join("\n");
        contentDiv.appendChild(pre);

        // دکمه کپی فقط برای این سکشن
        const copyBtn = document.createElement("button");
        copyBtn.className = "copy-btn";
        copyBtn.textContent = "کپی تمام کانفیگ‌ها";
        copyBtn.onclick = () => {
            const range = document.createRange();
            range.selectNodeContents(pre);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            document.execCommand("copy");
            sel.removeAllRanges();
            copyBtn.textContent = "کپی شد!";
            setTimeout(() => copyBtn.textContent = "کپی تمام کانفیگ‌ها", 2000);
        };
        contentDiv.appendChild(copyBtn);

        // Toggle آکاردئون
        header.onclick = () => {
            contentDiv.classList.toggle("active");
            header.classList.toggle("active");
        };

        // اضافه کردن به بخش
        sectionDiv.appendChild(header);
        sectionDiv.appendChild(contentDiv);
        container.appendChild(sectionDiv);
    });
};
