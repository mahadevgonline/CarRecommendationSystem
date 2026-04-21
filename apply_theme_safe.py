"""
Safely inject ClassicAuto vintage theme via CSS variable overrides.
Does not destroy existing layout CSS.
"""
import os, glob

SAFE_CSS_OVERRIDE = """
        /* ── CLASSICAUTO VINTAGE THEME OVERRIDES ── */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lora:wght@400;500;600&display=swap');

        :root {
            --primary: #3e2723;
            --primary-dark: #2a1a17;
            --secondary: #c9a96e;
            --light: #d7ccc8;
            --dark: #3e2723;
            --gray: #5d4037;
            --bg-color: #f5f1e6;
            --surface: #ffffff;
            --text-color: #3e2723;
            --sidebar-width: 250px;
            --header-height: 70px;
            --transition: all 0.3s ease;
        }

        [data-theme="dark"] {
            --primary: #120a04;
            --primary-dark: #000000;
            --secondary: #c9a96e;
            --light: #5d4037;
            --dark: #f5f1e6;
            --gray: #d7ccc8;
            --bg-color: #1a1008;
            --surface: #2a1a10;
            --text-color: #f5f1e6;
        }

        body {
            background-color: var(--bg-color) !important;
            color: var(--text-color) !important;
            font-family: 'Lora', serif !important;
            transition: background 0.3s, color 0.3s;
        }

        h1, h2, h3, h4, h5, .sidebar-header h2, th {
            font-family: 'Cinzel', serif !important;
        }

        .sidebar {
            background: var(--primary) !important;
        }
        
        .sidebar-header {
            background: var(--primary-dark) !important;
            border-bottom: 1px solid rgba(201, 169, 110, 0.2) !important;
        }

        .header, .stat-card, .chart-container, .recent-activity, .top-cars, .card, .form-container, form, table, .seller-registration {
            background-color: var(--surface) !important;
            border-color: var(--light) !important;
        }

        input, select, textarea {
            background-color: var(--bg-color) !important;
            color: var(--text-color) !important;
            border: 1px solid var(--light) !important;
        }

        /* Force text visibility */
        .header-left h1, .stat-info h3, .page-title h2, .activity-details h4, .table-header h3, th, td, label {
            color: var(--text-color) !important;
        }
        
        .stat-info p, .page-title p, .activity-details p, .activity-time {
            color: var(--gray) !important;
        }

        .menu-item {
            color: var(--gray) !important;
        }

        .menu-item.active, .menu-item:hover {
            color: var(--secondary) !important;
            background: rgba(201, 169, 110, 0.1) !important;
            border-left-color: var(--secondary) !important;
        }

        .btn-primary, .btn-submit {
            background: var(--secondary) !important;
            color: var(--primary-dark) !important;
            font-family: 'Cinzel', serif !important;
        }

        .theme-toggle {
            background: var(--secondary);
            border: none;
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 1rem;
            cursor: pointer;
            color: var(--primary-dark);
            font-weight: 700;
        }
"""

THEME_JS = """
    <script>
        (function() {
            var saved = localStorage.getItem('classicauto_theme') || 'light';
            document.documentElement.setAttribute('data-theme', saved);
        })();

        function toggleTheme() {
            var current = document.documentElement.getAttribute('data-theme');
            var next = (current === 'dark') ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('classicauto_theme', next);
            var btn = document.getElementById('themeToggle');
            if (btn) btn.innerHTML = (next === 'dark') ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
        }

        document.addEventListener('DOMContentLoaded', function() {
            var saved = localStorage.getItem('classicauto_theme') || 'light';
            var btn = document.getElementById('themeToggle');
            if (btn) btn.innerHTML = (saved === 'dark') ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
        });
    </script>
"""

TOGGLE_BTN = '<button class="theme-toggle" id="themeToggle" onclick="toggleTheme()" title="Toggle Dark/Light Mode">🌙</button>'

BASE_DIR = r"c:\Users\mahad\PycharmProjects\OnlineCarRecommendationSystem\myapp\templates"
TARGETS = (
    list(glob.glob(os.path.join(BASE_DIR, "admin", "*.html"))) +
    list(glob.glob(os.path.join(BASE_DIR, "seller", "*.html")))
)

def process(path):
    with open(path, encoding="utf-8") as f:
        src = f.read()

    if "CLASSICAUTO VINTAGE THEME OVERRIDES" in src:
        print(f"  [SKIP] {os.path.basename(path)}")
        return

    # Append CSS before </style>
    if '</style>' in src:
        src = src.replace('</style>', SAFE_CSS_OVERRIDE + '\n    </style>', 1)
    
    # Insert Toggle Button in the header
    # Usually next to <div class="header-right"> or inside it
    if 'id="themeToggle"' not in src:
        if '<div class="header-right">' in src:
            src = src.replace('<div class="header-right">', '<div class="header-right">\n                    ' + TOGGLE_BTN, 1)
        elif '<div class="nav-right">' in src:
            src = src.replace('<div class="nav-right">', '<div class="nav-right">\n                    ' + TOGGLE_BTN, 1)

    # Append JS before </body>
    if 'classicauto_theme' not in src:
        src = src.replace('</body>', THEME_JS + '\n</body>', 1)

    with open(path, 'w', encoding="utf-8") as f:
        f.write(src)
    print(f"  [DONE] {os.path.basename(path)}")

print("Injecting Vintage Theme Overrides...")
for p in sorted(TARGETS):
    process(p)
print("Done.")
