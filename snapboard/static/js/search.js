/* =====================================================
   SNAPBOARD — SEARCH.JS
   Compartilhado entre home / perfil / feed.

   - Em páginas SEM grade de posts (Home, Perfil):
     o campo de busca redireciona para o Feed com
     a pesquisa já preenchida (?q=...).

   - Na página do Feed: filtra os posts ao digitar
     e também lê o parâmetro ?q= vindo de outra página.

   O modo é decidido pelo atributo data-search-target:
   se existir, é modo "redirecionar"; se não existir,
   é modo "filtrar aqui mesmo".
===================================================== */

(() => {
    const input = document.querySelector("[data-search-input]");
    if (!input) return;

    const target = input.dataset.searchTarget;

    /* ---------- MODO REDIRECIONAR (Home / Perfil) ---------- */

    if (target) {
        input.addEventListener("keydown", (event) => {
            if (event.key !== "Enter") return;

            event.preventDefault();

            const query = input.value.trim();
            window.location.href = query
                ? `${target}?q=${encodeURIComponent(query)}`
                : target;
        });

        return;
    }

    /* ---------- MODO FILTRAR (Feed) ---------- */

    const posts = document.querySelectorAll(".post-card[data-author]");
    const noResults = document.getElementById("noResults");

    function applyFilter(term) {
        const search = term.toLowerCase().trim();
        let visible = 0;

        posts.forEach((post) => {
            const author = post.dataset.author || "";
            const matches = author.includes(search);

            post.style.display = matches ? "" : "none";

            if (matches) visible++;
        });

        if (noResults) {
            noResults.hidden = visible !== 0 || posts.length === 0;
        }
    }

    input.addEventListener("input", () => applyFilter(input.value));

    // Veio pela aba "Buscar" da barra inferior — já abre o teclado no campo
    const params = new URLSearchParams(window.location.search);
    if (params.get("foco") === "busca") {
        input.focus();
    }
})();
