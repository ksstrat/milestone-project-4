// External link confirmation (Bootstrap 5 modal)
(() => {
    const modalEl = document.getElementById("externalLinkModal");
    if (!modalEl || typeof bootstrap === "undefined") return;

    // Modal refs
    const modal = new bootstrap.Modal(modalEl);
    const continueBtn = modalEl.querySelector("[data-pp-continue]");
    const hostSpan = modalEl.querySelector("[data-pp-host]");
    const urlAnchor = modalEl.querySelector("[data-pp-url]");

    const siteHost = window.location.hostname;
    let pendingUrl = null;
    let openInNewTab = false;

    // Trusted hosts
    const HOST_WHITELIST = new Set([
        siteHost,
        "www." + siteHost,
    ]);

    // Decide if an <a> should be treated as external
    function isExternalHttp(anchor) {
        try {
            const u = new URL(anchor.href, window.location.href);
            if (!/^https?:$/.test(u.protocol)) return false;
            if (u.hostname === siteHost) return false;
            if (HOST_WHITELIST.has(u.hostname)) return false;
            if (anchor.dataset.noWarning === "true" || anchor.classList.contains("no-external-warning")) return false;
            const extra = (anchor.dataset.whitelist || "").split(",").map(s => s.trim()).filter(Boolean);
            if (extra.includes(u.hostname)) return false;
            return true;
        } catch { return false; }
    }

    // Intercept left-clicks
    function handleClick(e) {
        if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
        const a = e.target.closest && e.target.closest("a[href]");
        if (!a) return;

        const url = new URL(a.href, window.location.href);

        // Block javascript entirely
        if (url.protocol === "javascript:") { e.preventDefault(); return; }

        const isTelOrMail = url.protocol === "tel:" || url.protocol === "mailto:";
        const shouldWarn = isTelOrMail || isExternalHttp(a);
        if (!shouldWarn) return;

        // Pause navigation and show modal
        e.preventDefault();
        pendingUrl = url.toString();
        openInNewTab = /^https?:$/.test(url.protocol) && a.target === "_blank";

        // Fill modal
        hostSpan.textContent = url.hostname || url.href;
        urlAnchor.href = pendingUrl;
        urlAnchor.textContent = pendingUrl;

        modal.show();
    }

    document.addEventListener("click", handleClick);

    // Proceed to external site
    continueBtn.addEventListener("click", () => {
        if (!pendingUrl) return;
        const target = openInNewTab ? "_blank" : "_self";
        window.open(pendingUrl, target, "noopener");
        modal.hide();
        pendingUrl = null;
        openInNewTab = false;
    });
})();