import glob, os, re

THEME_CSS_FIX = """
        /* -- EXPLICIT CONTRACT FIX -- */
        h1, h2, h3, h4, h5, h6, p, label, td, th, li, span:not([class*="badge"]), div:not([class*="btn"]):not([class*="icon"]):not([class*="badge"]) {
            color: var(--text-color, var(--vintage-dark)) !important;
        }
        .gray-text, .text-muted, .activity-time, .stat-info p, .activity-details p, .page-title p {
            color: var(--gray, var(--vintage-brown)) !important;
        }
        input, textarea, select {
            background-color: var(--bg-color, var(--vintage-cream)) !important;
            color: var(--text-color, var(--vintage-dark)) !important;
            border: 1px solid var(--light, var(--vintage-light)) !important;
        }
        .btn, .btn-primary, .btn-submit, .badge, .status {
            color: #ffffff !important;
        }
        .btn-outline {
            color: var(--secondary, var(--vintage-gold)) !important;
        }
        .btn-outline:hover {
            color: #ffffff !important;
        }
"""

def fix_templates(base_path):
    for path in glob.glob(os.path.join(base_path, "*.html")):
        with open(path, encoding="utf-8") as f:
            src = f.read()

        # If we already added the fix, don't duplicate
        if "EXPLICIT CONTRACT FIX" not in src:
            src = src.replace('</style>', THEME_CSS_FIX + '\n    </style>', 1)
            
            with open(path, 'w', encoding="utf-8") as f:
                f.write(src)
            print(f"Fixed: {os.path.basename(path)}")

BASE = r"c:\Users\mahad\PycharmProjects\OnlineCarRecommendationSystem\myapp\templates"
fix_templates(os.path.join(BASE, "admin"))
fix_templates(os.path.join(BASE, "seller"))
fix_templates(os.path.join(BASE, "user"))

print("All templates reinforced for contrast.")
