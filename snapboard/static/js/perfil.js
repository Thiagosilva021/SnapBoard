document.addEventListener("DOMContentLoaded", () => {

    const themeToggle =
        document.getElementById("themeToggle");

    const themeIcon =
        document.getElementById("themeIcon");


    function setTheme(theme) {

        document.documentElement.dataset.theme =
            theme;

        localStorage.setItem(
            "snapboard-theme",
            theme
        );


        if (theme === "light") {

            themeIcon.innerHTML = `
                <circle
                    cx="12"
                    cy="12"
                    r="4"
                ></circle>

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
                <path
                    d="
                        M21 12.8
                        A8.5 8.5 0 1 1
                        11.2 3
                        A6.7 6.7 0 0 0
                        21 12.8Z
                    "
                ></path>
            `;
        }
    }


    const savedTheme =
        localStorage.getItem(
            "snapboard-theme"
        );


    if (savedTheme) {

        setTheme(savedTheme);

    } else {

        setTheme("dark");

    }


    themeToggle?.addEventListener(
        "click",
        () => {

            const currentTheme =
                document.documentElement.dataset.theme;

            setTheme(
                currentTheme === "dark"
                    ? "light"
                    : "dark"
            );

        }
    );

});