document.addEventListener("DOMContentLoaded", function () {
    function setupMainPreview(inputSelector, imgSelector, placeholderSelector) {
        const input = document.querySelector(inputSelector);
        const img = document.querySelector(imgSelector);
        const placeholder = document.querySelector(placeholderSelector);

        if (!input || !img) return;

        input.addEventListener("change", function () {
            const file = this.files && this.files[0];
            if (!file) return;

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

            fileInput.addEventListener("change", function () {
                const file = this.files && this.files[0];
                if (!file) return;

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

    setupMainPreview('#id_image', '#main-image-preview', '#main-image-placeholder');
    setupMainPreview('#id_image', '#slider-image-preview', '#slider-image-placeholder');
    setupInlinePreviews();

    document.body.addEventListener("click", function () {
        setTimeout(setupInlinePreviews, 300);
    });
});