document.addEventListener("DOMContentLoaded", () => {
    // Toggle آکاردئون و دکمه کپی
    document.querySelectorAll(".config-column").forEach(column => {
        const header = column.querySelector(".config-header");
        const content = column.querySelector(".config-content");
        const copyBtn = header.querySelector(".copy-btn");

        // Toggle نمایش
        header.addEventListener("click", (e) => {
            // اگر روی دکمه کپی کلیک شد، Toggle نکن
            if (e.target === copyBtn) return;
            content.classList.toggle("active");
        });

        // کپی فقط برای همین سکشن
        copyBtn.addEventListener("click", () => {
            const textarea = content.querySelector("textarea");
            if (!textarea) return;
            textarea.select();
            document.execCommand("copy");

            copyBtn.innerText = "کپی شد!";
            setTimeout(() => {
                copyBtn.innerText = "کپی";
            }, 1500);
        });
    });
});
