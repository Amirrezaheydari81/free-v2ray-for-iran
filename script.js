window.onload = function () {
    const headers = document.querySelectorAll('.config-header');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            content.classList.toggle('active');
        });

        const copyBtn = header.querySelector('.copy-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', e => {
                e.stopPropagation();
                const textarea = header.nextElementSibling.querySelector('textarea');
                textarea.select();
                document.execCommand('copy');
                copyBtn.innerText = '✔ کپی شد';
                setTimeout(() => copyBtn.innerText = 'کپی', 2000);
            });
        }
    });
};
