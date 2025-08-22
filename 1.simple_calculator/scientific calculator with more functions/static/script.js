document.addEventListener("DOMContentLoaded", function () {
    const themeSelect = document.getElementById('themeSelect');
    const body = document.body;

    function applyTheme(theme) {
        body.classList.remove('bg-dark', 'bg-body');
        if (theme === 'dark') {
            body.classList.add('bg-dark');
        } else if (theme === 'light') {
            body.classList.add('bg-body');
        } else if (theme === 'auto') {
            const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            body.classList.add(isDark ? 'bg-dark' : 'bg-body');
        }
        localStorage.setItem('theme', theme);
    }

    const savedTheme = localStorage.getItem('theme') || 'auto';
    themeSelect.value = savedTheme;
    applyTheme(savedTheme);

    themeSelect.addEventListener('change', function () {
        applyTheme(this.value);
    });
});
