document.addEventListener("DOMContentLoaded", () => {

    const themeToggle =
        document.querySelector("[data-theme-toggle]");

    const themeIcon =
        document.querySelector("[data-theme-icon]");


    function applyTheme(theme) {

        document.documentElement.dataset.theme = theme;

        localStorage.setItem("snapboard-theme", theme);

        if (!themeIcon) return;

        if (theme === "light") {

            themeIcon.innerHTML = `
                <circle cx="12" cy="12" r="4"></circle>
                <path d="M12 2v2"></path>
                <path d="M12 20v2"></path>
                <path d="m4.93 4.93 1.41 1.41"></path>
                <path d="m17.66 17.66 1.41 1.41"></path>
                <path d="M2 12h2"></path>
                <path d="M20 12h2"></path>
                <path d="m4.93 19.07 1.41-1.41"></path>
                <path d="m17.66 6.34 1.41-1.41"></path>
            `;

        } else {

            themeIcon.innerHTML = `
                <path d="M21 12.8A8.5 8.5 0 1 1 11.2 3
                         6.7 6.7 0 0 0 21 12.8Z">
                </path>
            `;
        }
    }


    const savedTheme =
        localStorage.getItem("snapboard-theme") || "dark";


    applyTheme(savedTheme);


    themeToggle?.addEventListener("click", () => {

        const current =
            document.documentElement.dataset.theme;

        const next =
            current === "dark"
                ? "light"
                : "dark";

        applyTheme(next);

    });


    /* ================================================
       BOTÕES SALVAR
    ================================================= */

    document.querySelectorAll(".save-button")
        .forEach(button => {

            button.addEventListener("click", (event) => {

                event.preventDefault();

                event.stopPropagation();

                if (button.textContent.trim() === "Salvar") {

                    button.textContent = "Salvo";

                    button.style.background = "#242424";

                } else {

                    button.textContent = "Salvar";

                    button.style.background = "";

                }

            });

        });

});