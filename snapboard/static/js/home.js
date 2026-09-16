document.addEventListener("DOMContentLoaded", () => {

    /* =================================================
       BOTÕES SALVAR (grade de pins, se presente na página)
    ================================================= */

    document.querySelectorAll(".save-button").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();

            const saved = button.classList.toggle("saved");

            button.textContent = saved ? "Salvo" : "Salvar";
            button.setAttribute("aria-pressed", saved ? "true" : "false");
        });
    });

});
