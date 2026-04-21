import os, glob

# Dark mode overrides for user templates
USER_DARK_VARS = """
        [data-theme="dark"] {
            --vintage-dark: #f5f1e6;
            --vintage-brown: #d7ccc8;
            --vintage-light: #5d4037;
            --vintage-gold: #c9a96e;
            --vintage-cream: #1a1008;
            --vintage-red: #ff7043;
            --vintage-green: #4caf50;
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
            var btn = document.getElementById('themeToggleBtn');
            if (btn) btn.innerHTML = (next === 'dark') ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        }

        document.addEventListener('DOMContentLoaded', function() {
            var saved = localStorage.getItem('classicauto_theme') || 'light';
            var btn = document.getElementById('themeToggleBtn');
            if (btn) btn.innerHTML = (saved === 'dark') ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    </script>
"""

TOGGLE_BTN = '<button id="themeToggleBtn" onclick="toggleTheme()" style="background:transparent; border:none; color:var(--vintage-gold); font-size:1.2rem; cursor:pointer; margin-right:15px;" title="Toggle Dark/Light Mode"><i class="fas fa-moon"></i></button>'

BASE_DIR = r"c:\Users\mahad\PycharmProjects\OnlineCarRecommendationSystem\myapp\templates\user"
TARGETS = glob.glob(os.path.join(BASE_DIR, "*.html"))

for path in TARGETS:
    with open(path, encoding="utf-8") as f:
        src = f.read()

    if "[data-theme=\"dark\"]" not in src:
        src = src.replace('</style>', USER_DARK_VARS + '\n    </style>', 1)
    
    if 'id="themeToggleBtn"' not in src:
        if '<a href="/cart/"' in src:
            src = src.replace('<a href="/cart/"', TOGGLE_BTN + '\n                <a href="/cart/"', 1)
        elif '<div class="nav-icons">' in src:
            src = src.replace('<div class="nav-icons">', '<div class="nav-icons">\n                ' + TOGGLE_BTN, 1)

    if 'classicauto_theme' not in src:
        src = src.replace('</body>', THEME_JS + '\n</body>', 1)

    with open(path, 'w', encoding="utf-8") as f:
        f.write(src)
    print(f"  [DONE] {os.path.basename(path)}")

print("\nDone applying toggles to User templates.")
