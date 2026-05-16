document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const root = document.documentElement;

    if (body.dataset.primaryColor) {
        root.style.setProperty("--aza-primary", body.dataset.primaryColor);
    }

    if (body.dataset.secondaryColor) {
        root.style.setProperty("--aza-secondary", body.dataset.secondaryColor);
    }

    if (body.dataset.accentColor) {
        root.style.setProperty("--aza-accent", body.dataset.accentColor);
    }
});
