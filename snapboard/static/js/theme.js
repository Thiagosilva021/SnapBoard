(() => {
    const root = document.documentElement;
    const toggle = document.querySelector("[data-theme-toggle]");
    const themeIcon = document.querySelector("[data-theme-icon]");

    const savedTheme = localStorage.getItem("snapboard-theme");
    const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initialTheme = savedTheme || (systemDark ? "dark" : "light");

    root.dataset.theme = initialTheme;

    function updateThemeIcon() {
        if (!themeIcon) return;
        const isDark = root.dataset.theme === "dark";
        themeIcon.innerHTML = isDark
            ? '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"></path>'
            : '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"></path>';
    }

    updateThemeIcon();

    toggle?.addEventListener("click", () => {
        const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
        root.dataset.theme = nextTheme;
        localStorage.setItem("snapboard-theme", nextTheme);
        updateThemeIcon();
    });

    document.querySelectorAll("[data-password-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const input = document.getElementById(button.dataset.passwordToggle);
            if (!input) return;

            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";

            button.innerHTML = isPassword
                ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 3l18 18"></path><path d="M10.6 10.6a2 2 0 0 0 2.8 2.8"></path><path d="M9.9 4.2A10.8 10.8 0 0 1 12 4c5.2 0 8.6 4.2 9.8 8a11.8 11.8 0 0 1-3.2 5.1"></path><path d="M6.2 6.2C4.2 7.5 2.8 9.8 2.2 12c1.2 3.8 4.6 8 9.8 8 1 0 2-.2 2.9-.5"></path></svg>'
                : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"></path><circle cx="12" cy="12" r="2.7"></circle></svg>';

            button.setAttribute("aria-label", isPassword ? "Ocultar senha" : "Mostrar senha");
        });
    });
})();
