document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // TEMA CLARO / ESCURO
    // =====================================================

    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");


    function setTheme(theme) {

        document.documentElement.dataset.theme = theme;

        localStorage.setItem(
            "snapboard-theme",
            theme
        );


        if (!themeIcon) {
            return;
        }


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


    // =====================================================
    // CARREGAR TEMA SALVO
    // =====================================================

    const savedTheme = localStorage.getItem(
        "snapboard-theme"
    );


    if (savedTheme) {

        setTheme(savedTheme);

    } else {

        setTheme("dark");

    }


    // =====================================================
    // BOTÃO DE TEMA
    // =====================================================

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


    // =====================================================
    // VISUALIZAÇÃO DA IMAGEM
    // =====================================================

    const modal = document.getElementById("imageModal");
    const modalImage = document.getElementById("modalImage");


    function abrirImagem(src) {

        if (!modal || !modalImage) {
            return;
        }


        modalImage.src = src;

        modal.classList.add("active");

        modal.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.classList.add(
            "modal-open"
        );
    }


    function fecharImagem() {

        if (!modal || !modalImage) {
            return;
        }


        modal.classList.remove("active");

        modal.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.classList.remove(
            "modal-open"
        );


        setTimeout(() => {

            if (!modal.classList.contains("active")) {

                modalImage.src = "";

            }

        }, 250);
    }


    // =====================================================
    // CLIQUE NAS IMAGENS
    // =====================================================

    document.querySelectorAll(".image-preview-button").forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const imagem =
                        button.dataset.image;

                    if (imagem) {

                        abrirImagem(imagem);

                    }

                }
            );

        });


    // =====================================================
    // FECHAR COM ESC
    // =====================================================

    document.addEventListener(
        "keydown",
        event => {

            if (event.key === "Escape") {

                fecharImagem();

            }

        }
    );


    // =====================================================
    // FECHAR CLICANDO NO FUNDO
    // =====================================================

    if (modal) {

        modal.addEventListener(
            "click",
            event => {

                if (
                    event.target === modal ||
                    event.target.classList.contains(
                        "image-modal-backdrop"
                    )
                ) {

                    fecharImagem();

                }

            }
        );

    }

});