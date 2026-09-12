# Rename DREAM11 to Fantasy11 across all app files
import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "public", "index.html")
APP_PATH = os.path.join(BASE_DIR, "public", "app.js")
STYLES_PATH = os.path.join(BASE_DIR, "public", "styles.css")
MANIFEST_PATH = os.path.join(BASE_DIR, "public", "manifest.json")
SW_PATH = os.path.join(BASE_DIR, "public", "sw.js")
SERVER_PATH = os.path.join(BASE_DIR, "server.py")
BAT_PATH = os.path.join(BASE_DIR, "start_app.bat")

# 1. index.html
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Replace title
html = html.replace("<title>Dream11 - Play Fantasy Cricket & Win Real Cash</title>", "<title>Fantasy11 - Play Fantasy Sports & Win Real Cash</title>")
# Replace Brand Logo and Text
html = html.replace('<span class="brand-d">D</span>\n            <span class="brand-text">DREAM11</span>', '<span class="brand-d">F</span>\n            <span class="brand-text">FANTASY11</span>')
html = html.replace('<span class="brand-d">D</span>', '<span class="brand-d">F</span>')
html = html.replace('<span class="brand-text">DREAM11</span>', '<span class="brand-text">FANTASY11</span>')
# Replace SMS texts
html = html.replace("MESSAGES • DREAM11 OTP", "MESSAGES • FANTASY11 OTP")
html = html.replace("Your Dream11 Bank Withdrawal OTP is", "Your Fantasy11 Bank Withdrawal OTP is")
html = html.replace("Your Dream11 security OTP is", "Your Fantasy11 security OTP is")
# Replace Wallet & Points
html = html.replace("<h4>My Dream11 Wallet</h4>", "<h4>My Fantasy11 Wallet</h4>")
html = html.replace("Dream11 Points", "Fantasy11 Points")
html = html.replace("Dream11 Standard", "Fantasy11 Standard")
html = html.replace("Credited to your Dream11 Deposited Balance", "Credited to your Fantasy11 Deposited Balance")
html = html.replace("dream11.pay@icici", "fantasy11.pay@icici")
# QR code center badge
html = html.replace('<text x="80" y="86" font-size="16" font-weight="bold" fill="white" text-anchor="middle">D</text>', '<text x="80" y="86" font-size="16" font-weight="bold" fill="white" text-anchor="middle">F</text>')
# Placeholder code in inputs
html = html.replace("D11-882", "F11-882")
html = html.replace("D11-", "F11-")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html renamed to Fantasy11!")

# 2. manifest.json
manifest = {
    "name": "Fantasy11 Sports",
    "short_name": "Fantasy11",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0b0f19",
    "theme_color": "#b91c1c",
    "orientation": "portrait",
    "icons": [
        {
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23D11A2A'/><text x='50' y='68' font-size='55' font-weight='900' font-style='italic' fill='white' text-anchor='middle'>F</text></svg>",
            "sizes": "192x192 512x512",
            "type": "image/svg+xml",
            "purpose": "any maskable"
        }
    ]
}
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
print("manifest.json updated with Fantasy11 & 'F' icon!")

# 3. sw.js
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw = f.read()
sw = sw.replace("dream11-v2", "fantasy11-v1")
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw)
print("sw.js updated cache name!")

# 4. app.js
with open(APP_PATH, "r", encoding="utf-8") as f:
    app_js = f.read()
app_js = app_js.replace("DREAM11 FANTASY SPORTS", "FANTASY11 SPORTS")
app_js = app_js.replace("Dream11 ServiceWorker", "Fantasy11 ServiceWorker")
app_js = app_js.replace("Join my Dream11 Private", "Join my Fantasy11 Private")
app_js = app_js.replace("📱 Dream11 installed", "📱 Fantasy11 installed")
app_js = app_js.replace("Your Dream11 security OTP", "Your Fantasy11 security OTP")
app_js = app_js.replace("Your Dream11 Bank Withdrawal OTP", "Your Fantasy11 Bank Withdrawal OTP")
app_js = app_js.replace("Dream11 Deposited Balance", "Fantasy11 Deposited Balance")
app_js = app_js.replace("dream11.pay@icici", "fantasy11.pay@icici")
app_js = app_js.replace("Dream11 Wallet", "Fantasy11 Wallet")
# Support F11 code generation
app_js = app_js.replace("D11-", "F11-")

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(app_js)
print("app.js updated with Fantasy11!")

# 5. start_app.bat
with open(BAT_PATH, "r", encoding="utf-8") as f:
    bat = f.read()
bat = bat.replace("Dream11 Fantasy Cricket App", "Fantasy11 Sports App")
bat = bat.replace("DREAM11 FANTASY SPORTS WEB APPLICATION", "FANTASY11 SPORTS WEB APPLICATION")
with open(BAT_PATH, "w", encoding="utf-8") as f:
    f.write(bat)
print("start_app.bat updated!")

# 6. server.py
with open(SERVER_PATH, "r", encoding="utf-8") as f:
    srv = f.read()
srv = srv.replace("Dream11 Server running", "Fantasy11 Server running")
srv = srv.replace("Dream11Handler", "Fantasy11Handler")
srv = srv.replace("Dream11 Wallet", "Fantasy11 Wallet")
srv = srv.replace('code = f"D11-{random.randint(100, 999)}"', 'code = f"F11-{random.randint(100, 999)}"')
srv = srv.replace('"utr": f"D11/ENT/', '"utr": f"F11/ENT/')
srv = srv.replace('"utr": f"D11/PRIV/', '"utr": f"F11/PRIV/')

with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.write(srv)
print("server.py updated with Fantasy11!")
