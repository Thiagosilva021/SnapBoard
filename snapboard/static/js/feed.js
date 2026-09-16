document.addEventListener("DOMContentLoaded", () => {

    /* =================================================
       CURTIDAS
       Envia via fetch para não recarregar a página;
       se o fetch falhar por qualquer motivo, deixa o
       formulário seguir o envio normal (POST + reload).
    ================================================= */

    document.querySelectorAll("[data-like-form]").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector(".like-button");
            if (!button || button.disabled) return;

            button.disabled = true;

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                    body: new FormData(form),
                });

                if (!response.ok) throw new Error("Falha ao curtir");

                const dados = await response.json();

                button.classList.toggle("liked", dados.curtiu);
                button.setAttribute("aria-pressed", dados.curtiu ? "true" : "false");
                button.title = dados.curtiu ? "Remover curtida" : "Curtir postagem";
                button.setAttribute("aria-label", button.title);
            } catch (erro) {
                // Sem JS/fetch disponível ou erro de rede: envia como formulário normal
                window.snapboardToast?.("Não foi possível curtir agora. Tentando de novo...");
                form.removeAttribute("data-like-form");
                form.submit();
            } finally {
                button.disabled = false;
            }
        });
    });

    /* =================================================
       FILTROS "TODAS" / "RECENTES"

       Assume que o backend já entrega `fotos` ordenado
       do mais novo para o mais antigo (padrão comum em
       feeds). "Recentes" mostra só os primeiros itens;
       "Todas" mostra tudo. Se a ordenação do backend for
       diferente, ajuste aqui.
    ================================================= */

    const filterButtons = document.querySelectorAll(".filter-button");
    const allCards = Array.from(document.querySelectorAll(".post-card"));
    const RECENT_LIMIT = 12;

    filterButtons.forEach((button) => {
        button.addEventListener("click", () => {
            filterButtons.forEach((item) => {
                item.classList.remove("active");
                item.setAttribute("aria-pressed", "false");
            });

            button.classList.add("active");
            button.setAttribute("aria-pressed", "true");

            const filter = button.dataset.filter;

            allCards.forEach((card, index) => {
                const withinLimit = index < RECENT_LIMIT;
                const shouldShow = filter === "recent" ? withinLimit : true;

                card.style.display = shouldShow ? "" : "none";
            });
        });
    });

});
