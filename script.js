function setupCopyButtons() {
    document.querySelectorAll('.config-header').forEach(header => {
        if (header.getAttribute('data-setup') === 'true') return;
        header.setAttribute('data-setup', 'true');

        const sourceId = header.id.replace('header-', 'content-');
        const contentDiv = document.getElementById(sourceId);

        const copyButton = document.createElement('button');
        copyButton.innerHTML = '<span class="icon">&#128206;</span> کپی';
        copyButton.onclick = function () {
            const codeBlock = contentDiv.querySelector('pre code');
            if (codeBlock) {
                const selection = window.getSelection();
                const range = document.createRange();
                range.selectNodeContents(codeBlock);
                selection.removeAllRanges();
                selection.addRange(range);

                document.execCommand('copy');
                selection.removeAllRanges();

                copyButton.innerHTML = '<span class="icon">&#10003;</span> کپی شد!';
                setTimeout(() => {
                    copyButton.innerHTML = '<span class="icon">&#128206;</span> کپی';
                }, 2000);
            }
        };

        // Toggle آکاردئونی
        const toggleButton = document.createElement('span');
        toggleButton.className = 'icon';
        toggleButton.innerHTML = '&#9660;'; // مثلث پایین
        header.appendChild(toggleButton);

        header.onclick = function () {
            contentDiv.classList.toggle('active');
            toggleButton.innerHTML = contentDiv.classList.contains('active') ? '&#9650;' : '&#9660;'; // مثلث بالا/پایین
        };

        header.style.cursor = 'pointer';
        header.appendChild(copyButton);
    });
}
window.onload = setupCopyButtons;
