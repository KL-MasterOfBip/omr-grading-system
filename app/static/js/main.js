// OMR System — main.js

document.addEventListener('DOMContentLoaded', () => {
    // Auto-hide flash messages after 4 seconds
    document.querySelectorAll('.flash').forEach(el => {
        setTimeout(() => el.remove(), 4000);
    });

    // File input label update
    document.querySelectorAll('input[type=file]').forEach(input => {
        input.addEventListener('change', () => {
            const label = input.previousElementSibling;
            if (label && input.files.length > 0) {
                label.textContent = input.files[0].name;
            }
        });
    });
});
