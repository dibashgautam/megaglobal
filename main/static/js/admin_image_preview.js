document.addEventListener("DOMContentLoaded", function () {
    function setupMainPreview(inputSelector, imgSelector, placeholderSelector) {
        const input = document.querySelector(inputSelector);
        const img = document.querySelector(imgSelector);
        const placeholder = document.querySelector(placeholderSelector);

        if (!input || !img) return;

        if (input.dataset.previewBound === "true") return;
        input.dataset.previewBound = "true";

        input.addEventListener("change", function () {
            const file = this.files && this.files[0];

            if (!file) {
                img.src = "";
                img.style.display = "none";
                if (placeholder) placeholder.style.display = "inline-flex";
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                img.src = e.target.result;
                img.style.display = "block";
                if (placeholder) placeholder.style.display = "none";
            };
            reader.readAsDataURL(file);
        });
    }

    function setupInlinePreviews() {
        const inlineRows = document.querySelectorAll(".inline-related");

        inlineRows.forEach(function (row) {
            const fileInput = row.querySelector('input[type="file"]');
            const previewImg = row.querySelector(".inline-image-preview");
            const placeholder = row.querySelector(".preview-placeholder");

            if (!fileInput || !previewImg) return;
            if (fileInput.dataset.previewBound === "true") return;

            fileInput.dataset.previewBound = "true";

            fileInput.addEventListener("change", function () {
                const file = this.files && this.files[0];

                if (!file) {
                    previewImg.src = "";
                    previewImg.style.display = "none";
                    if (placeholder) placeholder.style.display = "inline-flex";
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewImg.style.display = "block";
                    if (placeholder) placeholder.style.display = "none";
                };
                reader.readAsDataURL(file);
            });
        });
    }

    setupMainPreview("#id_image", "#main-image-preview", "#main-image-placeholder");
    setupMainPreview("#id_image", "#slider-image-preview", "#slider-image-placeholder");
    setupMainPreview("#id_image", "#category-image-preview", "#category-image-placeholder");

    setupInlinePreviews();

    document.body.addEventListener("click", function () {
        setTimeout(setupInlinePreviews, 300);
    });
});