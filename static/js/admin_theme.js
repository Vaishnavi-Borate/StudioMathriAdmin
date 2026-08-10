
document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("studio-theme-toggle");

    if (!button) {
        console.log("Theme button not found");
        return;
    }

    let theme = localStorage.getItem("studio_mathri_theme") || "light";

    /* =========================================
       APPLY BUTTON BASE STYLES
    ========================================= */
    button.style.cssText = `
        position: fixed !important;
        top: 70px !important;
        right: 20px !important;
        left: auto !important;
        width: 90px !important;
        height: 38px !important;
        padding: 6px 12px !important;
        margin: 0 !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 7px !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15) !important;
        z-index: 999999 !important;
        white-space: nowrap !important;
    `;

    /* =========================================
       APPLY THEME FUNCTION
    ========================================= */
    function applyTheme() {
        if (theme === "dark") {
            document.documentElement.classList.add("studio-dark");
            document.body.classList.add("studio-dark");

            button.innerHTML = `
                <i class="fas fa-sun"></i>
                <span>Light</span>
            `;

            button.style.setProperty("background", "#f8f9fa", "important");
            button.style.setProperty("color", "#212529", "important");

            /* Force Jazzmin Dashboard Elements to Dark */
            const darkElements = document.querySelectorAll(`
                #content-main .module,
                #content-main .module table,
                #content-main .module tbody,
                #content-main .module tr,
                #content-main .module td,
                #content-main .module th,
                #content-main .card,
                #content-main .card-header,
                #content-main .card-body,
                #content-main .app-list,
                #content-main .model-group,
                .table-card,
                .table-card table,
                .table-card tbody,
                .table-card tr,
                .table-card td
            `);

            darkElements.forEach(function (element) {
                element.style.setProperty("background-color", "#292e33", "important");
                element.style.setProperty("color", "#eeeeee", "important");
                element.style.setProperty("border-color", "#454b52", "important");
            });

            /* Module Headers */
            document.querySelectorAll(`
                #content-main .module caption,
                #content-main .card-header,
                .table-card h4
            `).forEach(function (element) {
                element.style.setProperty("background-color", "#343a40", "important");
                element.style.setProperty("color", "#ffffff", "important");
            });

            /* Remove Bootstrap Striped White */
            document.querySelectorAll(
                "#content-main .table-striped > tbody > tr > *"
            ).forEach(function (element) {
                element.style.setProperty("background-color", "#292e33", "important");
                element.style.setProperty("box-shadow", "inset 0 0 0 9999px #292e33", "important");
                element.style.setProperty("color", "#eeeeee", "important");
            });

        } else {
            document.documentElement.classList.remove("studio-dark");
            document.body.classList.remove("studio-dark");

            button.innerHTML = `
                <i class="fas fa-moon"></i>
                <span>Dark</span>
            `;

            button.style.setProperty("background", "#343a40", "important");
            button.style.setProperty("color", "#ffffff", "important");

            /* Restore Normal Light Mode */
            document.querySelectorAll(`
                #content-main .module,
                #content-main .module table,
                #content-main .module tbody,
                #content-main .module tr,
                #content-main .module td,
                #content-main .module th,
                #content-main .card,
                #content-main .card-header,
                #content-main .card-body,
                #content-main .app-list,
                #content-main .model-group,
                .table-card,
                .table-card table,
                .table-card tbody,
                .table-card tr,
                .table-card td,
                #content-main .module caption,
                #content-main .card-header,
                .table-card h4,
                #content-main .table-striped > tbody > tr > *
            `).forEach(function (element) {
                element.style.removeProperty("background-color");
                element.style.removeProperty("color");
                element.style.removeProperty("border-color");
                element.style.removeProperty("box-shadow");
            });
        }

        localStorage.setItem("studio_mathri_theme", theme);
    }

    /* =========================================
       TOGGLE EVENT LISTENER
    ========================================= */
    button.addEventListener("click", function () {
        theme = theme === "light" ? "dark" : "light";
        applyTheme();
    });

    /* Initialize Theme */
    applyTheme();
});
(function () {
    let theme = localStorage.getItem("studio_mathri_theme") || "light";

    function applyTheme() {
        const button = document.getElementById("studio-theme-toggle");

        if (theme === "dark") {
            document.documentElement.classList.add("studio-dark");
            document.body.classList.add("studio-dark");

            if (button) {
                button.innerHTML = `<i class="fas fa-sun"></i> <span>Light</span>`;
                button.classList.add("is-dark");
                button.classList.remove("is-light");
            }
        } else {
            document.documentElement.classList.remove("studio-dark");
            document.body.classList.remove("studio-dark");

            if (button) {
                button.innerHTML = `<i class="fas fa-moon"></i> <span>Dark</span>`;
                button.classList.add("is-light");
                button.classList.remove("is-dark");
            }
        }

        localStorage.setItem("studio_mathri_theme", theme);
    }

    // Apply saved theme immediately on page load
    document.addEventListener("DOMContentLoaded", applyTheme);

    // Event delegation: Catches clicks anywhere on the page
    document.addEventListener("click", function (event) {
        const toggleBtn = event.target.closest("#studio-theme-toggle");
        if (toggleBtn) {
            event.preventDefault();
            theme = theme === "light" ? "dark" : "light";
            applyTheme();
        }
    });
    // Dark mode active ahe ka check kara
const isDarkMode = document.body.classList.contains('dark');
const textColor = isDarkMode ? '#a1a5b7' : '#5e6278';
const gridColor = isDarkMode ? '#2b2b40' : '#eff2f5';

// Chart Config Updates
const chartOptions = {
    responsive: true,
    scales: {
        x: {
            ticks: { color: textColor },
            grid: { color: gridColor }
        },
        y: {
            ticks: { color: textColor },
            grid: { color: gridColor }
        }
    },
    plugins: {
        legend: {
            labels: { color: textColor }
        }
    }
};
document.getElementById('studio-theme-toggle')?.addEventListener('click', function() {
    document.body.classList.toggle('studio-dark');
    
    const isDark = document.body.classList.contains('studio-dark');
    
    if (isDark) {
        this.classList.remove('is-light');
        this.classList.add('is-dark');
        localStorage.setItem('studio_theme', 'dark');
    } else {
        this.classList.remove('is-dark');
        this.classList.add('is-light');
        localStorage.setItem('studio_theme', 'light');
    }
});

// Load Stored Theme on Load
if (localStorage.getItem('studio_theme') === 'dark') {
    document.body.classList.add('studio-dark');
    const toggleBtn = document.getElementById('studio-theme-toggle');
    if (toggleBtn) {
        toggleBtn.classList.remove('is-light');
        toggleBtn.classList.add('is-dark');
    }
}
// Normal OpenStreetMap tiles aevaji Dark CartoDB tiles vapara
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap © CARTO'
}).addTo(map);
})();