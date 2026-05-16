/* ============================================================
   SINDICATO AZA — main.js
   Navbar scroll, active links, scroll reveal
   Desarrollado por GoGoDevS
============================================================ */

document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const root = document.documentElement;

    // --- Tematizacion dinamica desde data attributes del body ---
    if (body.dataset.primaryColor) {
        root.style.setProperty("--aza-verde",   body.dataset.primaryColor);
        root.style.setProperty("--aza-primary", body.dataset.primaryColor);
        root.style.setProperty("--color-primary", body.dataset.primaryColor);
    }
    if (body.dataset.secondaryColor) {
        root.style.setProperty("--aza-secondary", body.dataset.secondaryColor);
    }
    if (body.dataset.accentColor) {
        root.style.setProperty("--aza-acento",  body.dataset.accentColor);
        root.style.setProperty("--aza-accent",  body.dataset.accentColor);
        root.style.setProperty("--color-accent", body.dataset.accentColor);
    }

    // --- Navbar: sombra al hacer scroll ---
    const header = document.querySelector(".site-header");
    if (header) {
        const handleScroll = () => {
            header.classList.toggle("scrolled", window.scrollY > 30);
        };
        window.addEventListener("scroll", handleScroll, { passive: true });
        handleScroll();
    }

    // --- Active link segun URL actual ---
    const currentPath = window.location.pathname;
    document.querySelectorAll(".site-header .nav-link").forEach(link => {
        const href = link.getAttribute("href");
        if (!href) return;
        if (href === "/" && currentPath === "/") {
            link.classList.add("active-link");
        } else if (href !== "/" && currentPath.startsWith(href)) {
            link.classList.add("active-link");
        }
    });

    // --- Scroll Reveal con IntersectionObserver ---
    const revealEls = document.querySelectorAll(".reveal");
    if (revealEls.length > 0 && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry, i) => {
                    if (entry.isIntersecting) {
                        setTimeout(() => {
                            entry.target.classList.add("revealed");
                        }, i * 90);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.10, rootMargin: "0px 0px -40px 0px" }
        );
        revealEls.forEach(el => observer.observe(el));
    } else {
        // Fallback: mostrar todo si no hay soporte
        revealEls.forEach(el => el.classList.add("revealed"));
    }

    // --- Smooth scroll a anchors internos ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });
});
