document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       VISUALIZAÇÃO DA IMAGEM (modal)
    ===================================================== */

    const modal = document.getElementById("imageModal");
    const modalImage = document.getElementById("modalImage");

    let lastFocusedElement = null;

    function abrirImagem(src, trigger) {
        if (!modal || !modalImage) return;

        lastFocusedElement = trigger || document.activeElement;

        modalImage.src = src;

        modal.classList.add("active");
        modal.setAttribute("aria-hidden", "false");

        document.body.classList.add("modal-open");

        modal.querySelector(".modal-close")?.focus();
    }

    function fecharImagem() {
        if (!modal || !modalImage) return;

        modal.classList.remove("active");
        modal.setAttribute("aria-hidden", "true");

        document.body.classList.remove("modal-open");

        setTimeout(() => {
            if (!modal.classList.contains("active")) {
                modalImage.src = "";
            }
        }, 250);

        lastFocusedElement?.focus();
    }

    // Exposto globalmente porque o HTML ainda usa onclick="fecharImagem()"
    window.fecharImagem = fecharImagem;

    document.querySelectorAll(".image-preview-button").forEach((button) => {
        button.addEventListener("click", () => {
            const imagem = button.dataset.image;
            if (imagem) abrirImagem(imagem, button);
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") fecharImagem();
    });

    modal?.addEventListener("click", (event) => {
        if (
            event.target === modal ||
            event.target.classList.contains("image-modal-backdrop")
        ) {
            fecharImagem();
        }
    });

    /* =====================================================
       PREVIEW E FEEDBACK DO UPLOAD
    ===================================================== */

    const uploadForm = document.querySelector(".upload-form");
    const fileInput = uploadForm?.querySelector('input[type="file"]');
    const uploadArea = uploadForm?.querySelector(".upload-area");
    const uploadText = uploadForm?.querySelector(".upload-text");

    if (uploadForm && fileInput && uploadArea && uploadText) {

        let previewImg = null;
        const originalHTML = uploadText.innerHTML;

        fileInput.addEventListener("change", () => {
            const file = fileInput.files?.[0];

            if (!file) {
                uploadText.innerHTML = originalHTML;
                previewImg?.remove();
                previewImg = null;
                uploadArea.classList.remove("has-preview");
                return;
            }

            // Nome do arquivo + tamanho, para o usuário confirmar a escolha
            const sizeKb = Math.round(file.size / 1024);
            uploadText.innerHTML = `
                <strong>${file.name}</strong>
                <span>${sizeKb} KB — pronto para enviar</span>
            `;

            // Preview visual, sem depender de upload real (URL local)
            if (file.type.startsWith("image/")) {
                if (!previewImg) {
                    previewImg = document.createElement("img");
                    previewImg.className = "upload-preview-image";
                    previewImg.alt = "Pré-visualização da imagem selecionada";
                    uploadArea.prepend(previewImg);
                }

                previewImg.src = URL.createObjectURL(file);
                uploadArea.classList.add("has-preview");
            }
        });

        uploadForm.addEventListener("submit", () => {
            const submitButton = uploadForm.querySelector('button[type="submit"]');
            if (!submitButton) return;

            // Evita duplo envio e dá feedback de que o upload está em andamento
            submitButton.disabled = true;
            submitButton.dataset.originalText = submitButton.textContent;
            submitButton.textContent = "Enviando...";
        });
    }

    /* =====================================================
       SEGUIR / DEIXAR DE SEGUIR
    ===================================================== */

    document.querySelectorAll("[data-follow-form]").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector("[data-follow-button]");
            if (!button || button.disabled) return;

            button.disabled = true;

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                    body: new FormData(form),
                });

                if (!response.ok) throw new Error("Falha ao seguir");

                const dados = await response.json();

                button.classList.toggle("following", dados.seguindo);
                button.dataset.following = dados.seguindo ? "true" : "false";
                button.textContent = dados.seguindo ? "Seguindo" : "Seguir";

                const contadorSeguidores = document.querySelector("[data-contador-seguidores]");
                if (contadorSeguidores) {
                    contadorSeguidores.textContent = dados.total_seguidores;
                }

                window.snapboardToast?.(dados.seguindo ? "Você começou a seguir esse perfil." : "Você deixou de seguir esse perfil.");
            } catch (erro) {
                window.snapboardToast?.("Não foi possível concluir agora. Tentando de novo...");
                form.removeAttribute("data-follow-form");
                form.submit();
            } finally {
                button.disabled = false;
            }
        });
    });

});
