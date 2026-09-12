# Dream11 Multi-Feature Upgrade Script
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
DATA_PATH = os.path.join(BASE_DIR, "data", "fantasy_data.json")

# 1. PWA manifest.json
manifest = {
    "name": "Dream11 Fantasy Sports",
    "short_name": "Dream11",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0b0f19",
    "theme_color": "#b91c1c",
    "orientation": "portrait",
    "icons": [
        {
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23D11A2A'/><text x='50' y='68' font-size='55' font-weight='900' font-style='italic' fill='white' text-anchor='middle'>D</text></svg>",
            "sizes": "192x192 512x512",
            "type": "image/svg+xml",
            "purpose": "any maskable"
        }
    ]
}

with open(os.path.join(PUBLIC_DIR, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

# 2. PWA sw.js
sw_code = """
const CACHE_NAME = 'dream11-v2';
const ASSETS = ['/', '/index.html', '/styles.css', '/app.js', '/manifest.json'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then(keys => Promise.all(
    keys.map(k => k !== CACHE_NAME ? caches.delete(k) : null)
  )));
});

self.addEventListener('fetch', (e) => {
  if (e.request.url.includes('/api/')) {
    e.respondWith(fetch(e.request));
  } else {
    e.respondWith(caches.match(e.request).then(res => res || fetch(e.request)));
  }
});
"""

with open(os.path.join(PUBLIC_DIR, "sw.js"), "w", encoding="utf-8") as f:
    f.write(sw_code)

print("PWA manifest and service worker created!")
# 3. Update fantasy_data.json with Football and Kabaddi matches + bilingual simulation
with open(DATA_PATH, "r", encoding="utf-8") as f:
    fdata = json.load(f)

# Add sport field to cricket matches
for m in fdata["matches"]:
    m["sport"] = "cricket"

# Football match
football_match = {
    "id": "rma-mci-ucl",
    "sport": "football",
    "title": "Real Madrid vs Manchester City",
    "series": "UEFA Champions League Semi-Final",
    "venue": "Santiago Bernabéu, Madrid",
    "team1": { "name": "Real Madrid", "shortName": "RMA", "color": "#ffffff", "secondaryColor": "#1e3a8a", "logo": "⚪" },
    "team2": { "name": "Manchester City", "shortName": "MCI", "color": "#38bdf8", "secondaryColor": "#0284c7", "logo": "🩵" },
    "status": "upcoming",
    "lineupsOut": True,
    "startTime": "Tomorrow, 12:30 AM",
    "timeLeftSeconds": 54000,
    "megaPrize": "₹25 Crores",
    "entryFee": 35,
    "pitchReport": "Pristine Bernabéu pitch. Fast ball circulation and wet grass favoring quick wingers.",
    "players": [
        # RMA
        {"id": "rma_1", "name": "Thibaut Courtois", "team": "RMA", "role": "GK", "credits": 8.5, "points": 210, "selectedBy": "74.2%", "isPlaying": True, "cBy": "5.1%", "vcBy": "7.2%"},
        {"id": "rma_2", "name": "Antonio Rüdiger", "team": "RMA", "role": "DEF", "credits": 8.5, "points": 240, "selectedBy": "81.0%", "isPlaying": True, "cBy": "6.0%", "vcBy": "8.5%"},
        {"id": "rma_3", "name": "Dani Carvajal", "team": "RMA", "role": "DEF", "credits": 8.5, "points": 225, "selectedBy": "65.4%", "isPlaying": True, "cBy": "4.2%", "vcBy": "6.0%"},
        {"id": "rma_4", "name": "Ferland Mendy", "team": "RMA", "role": "DEF", "credits": 8.0, "points": 180, "selectedBy": "51.0%", "isPlaying": True, "cBy": "2.0%", "vcBy": "4.1%"},
        {"id": "rma_5", "name": "Jude Bellingham", "team": "RMA", "role": "MID", "credits": 10.0, "points": 490, "selectedBy": "93.4%", "isPlaying": True, "cBy": "28.5%", "vcBy": "21.0%"},
        {"id": "rma_6", "name": "Federico Valverde", "team": "RMA", "role": "MID", "credits": 9.0, "points": 340, "selectedBy": "78.2%", "isPlaying": True, "cBy": "11.0%", "vcBy": "14.2%"},
        {"id": "rma_7", "name": "Eduardo Camavinga", "team": "RMA", "role": "MID", "credits": 8.5, "points": 260, "selectedBy": "59.0%", "isPlaying": True, "cBy": "5.0%", "vcBy": "7.0%"},
        {"id": "rma_8", "name": "Vinícius Jr", "team": "RMA", "role": "FWD", "credits": 10.5, "points": 530, "selectedBy": "95.0%", "isPlaying": True, "cBy": "35.2%", "vcBy": "24.1%"},
        {"id": "rma_9", "name": "Kylian Mbappé", "team": "RMA", "role": "FWD", "credits": 10.5, "points": 540, "selectedBy": "94.2%", "isPlaying": True, "cBy": "32.0%", "vcBy": "22.5%"},
        {"id": "rma_10", "name": "Rodrygo Goes", "team": "RMA", "role": "FWD", "credits": 9.0, "points": 360, "selectedBy": "68.5%", "isPlaying": True, "cBy": "8.4%", "vcBy": "11.0%"},
        # MCI
        {"id": "mci_1", "name": "Ederson", "team": "MCI", "role": "GK", "credits": 8.5, "points": 215, "selectedBy": "68.0%", "isPlaying": True, "cBy": "4.8%", "vcBy": "6.9%"},
        {"id": "mci_2", "name": "Rúben Dias", "team": "MCI", "role": "DEF", "credits": 9.0, "points": 260, "selectedBy": "82.5%", "isPlaying": True, "cBy": "7.0%", "vcBy": "9.1%"},
        {"id": "mci_3", "name": "Kyle Walker", "team": "MCI", "role": "DEF", "credits": 8.5, "points": 210, "selectedBy": "61.0%", "isPlaying": True, "cBy": "3.5%", "vcBy": "5.4%"},
        {"id": "mci_4", "name": "Joško Gvardiol", "team": "MCI", "role": "DEF", "credits": 8.5, "points": 270, "selectedBy": "72.4%", "isPlaying": True, "cBy": "8.1%", "vcBy": "9.8%"},
        {"id": "mci_5", "name": "Rodri", "team": "MCI", "role": "MID", "credits": 9.5, "points": 410, "selectedBy": "87.0%", "isPlaying": True, "cBy": "14.5%", "vcBy": "17.0%"},
        {"id": "mci_6", "name": "Kevin De Bruyne", "team": "MCI", "role": "MID", "credits": 10.0, "points": 510, "selectedBy": "92.0%", "isPlaying": True, "cBy": "26.0%", "vcBy": "22.4%"},
        {"id": "mci_7", "name": "Phil Foden", "team": "MCI", "role": "MID", "credits": 9.5, "points": 460, "selectedBy": "89.5%", "isPlaying": True, "cBy": "19.2%", "vcBy": "18.0%"},
        {"id": "mci_8", "name": "Bernardo Silva", "team": "MCI", "role": "MID", "credits": 9.0, "points": 330, "selectedBy": "64.0%", "isPlaying": True, "cBy": "6.5%", "vcBy": "9.0%"},
        {"id": "mci_9", "name": "Erling Haaland", "team": "MCI", "role": "FWD", "credits": 10.5, "points": 570, "selectedBy": "96.5%", "isPlaying": True, "cBy": "38.0%", "vcBy": "25.0%"},
        {"id": "mci_10", "name": "Jérémy Doku", "team": "MCI", "role": "FWD", "credits": 8.5, "points": 280, "selectedBy": "54.0%", "isPlaying": True, "cBy": "4.0%", "vcBy": "7.0%"}
    ]
}

# Kabaddi match
kabaddi_match = {
    "id": "pat-jai-pkl",
    "sport": "kabaddi",
    "title": "Patna Pirates vs Jaipur Pink Panthers",
    "series": "Pro Kabaddi League 2026 - Match 32",
    "venue": "Patliputra Sports Complex, Patna",
    "team1": { "name": "Patna Pirates", "shortName": "PAT", "color": "#15803d", "secondaryColor": "#166534", "logo": "🟢" },
    "team2": { "name": "Jaipur Pink Panthers", "shortName": "JAI", "color": "#ec4899", "secondaryColor": "#be185d", "logo": "🌸" },
    "status": "upcoming",
    "lineupsOut": True,
    "startTime": "Today, 8:30 PM",
    "timeLeftSeconds": 7200,
    "megaPrize": "₹15 Crores",
    "entryFee": 29,
    "pitchReport": "Standard PKL indoor mat. High grip surface with aggressive ankle-hold tendencies.",
    "players": [
        # PAT
        {"id": "pat_1", "name": "Sachin Tanwar", "team": "PAT", "role": "RAI", "credits": 10.5, "points": 480, "selectedBy": "92.0%", "isPlaying": True, "cBy": "30.0%", "vcBy": "22.0%"},
        {"id": "pat_2", "name": "Sudhakar M", "team": "PAT", "role": "RAI", "credits": 9.0, "points": 340, "selectedBy": "72.0%", "isPlaying": True, "cBy": "10.0%", "vcBy": "14.0%"},
        {"id": "pat_3", "name": "Sandeep Kumar", "team": "PAT", "role": "RAI", "credits": 8.5, "points": 290, "selectedBy": "55.0%", "isPlaying": True, "cBy": "5.0%", "vcBy": "7.0%"},
        {"id": "pat_4", "name": "Ankit Jaglan", "team": "PAT", "role": "ALL", "credits": 9.5, "points": 410, "selectedBy": "85.0%", "isPlaying": True, "cBy": "16.0%", "vcBy": "18.0%"},
        {"id": "pat_5", "name": "Sajin C", "team": "PAT", "role": "ALL", "credits": 8.5, "points": 280, "selectedBy": "58.0%", "isPlaying": True, "cBy": "4.0%", "vcBy": "6.0%"},
        {"id": "pat_6", "name": "Krishan Dhull", "team": "PAT", "role": "DEF", "credits": 10.0, "points": 460, "selectedBy": "89.0%", "isPlaying": True, "cBy": "20.0%", "vcBy": "19.0%"},
        {"id": "pat_7", "name": "Manish Dhull", "team": "PAT", "role": "DEF", "credits": 8.5, "points": 270, "selectedBy": "50.0%", "isPlaying": True, "cBy": "3.0%", "vcBy": "5.0%"},
        # JAI
        {"id": "jai_1", "name": "Arjun Deshwal", "team": "JAI", "role": "RAI", "credits": 10.5, "points": 520, "selectedBy": "95.0%", "isPlaying": True, "cBy": "36.0%", "vcBy": "24.0%"},
        {"id": "jai_2", "name": "V Ajith Kumar", "team": "JAI", "role": "RAI", "credits": 9.0, "points": 330, "selectedBy": "68.0%", "isPlaying": True, "cBy": "8.0%", "vcBy": "12.0%"},
        {"id": "jai_3", "name": "Bhavani Rajput", "team": "JAI", "role": "RAI", "credits": 8.5, "points": 250, "selectedBy": "48.0%", "isPlaying": True, "cBy": "3.0%", "vcBy": "5.0%"},
        {"id": "jai_4", "name": "Sunil Kumar", "team": "JAI", "role": "ALL", "credits": 9.5, "points": 430, "selectedBy": "88.0%", "isPlaying": True, "cBy": "18.0%", "vcBy": "17.0%"},
        {"id": "jai_5", "name": "Reza Mirbagheri", "team": "JAI", "role": "ALL", "credits": 9.0, "points": 360, "selectedBy": "75.0%", "isPlaying": True, "cBy": "9.0%", "vcBy": "13.0%"},
        {"id": "jai_6", "name": "Ankush Rathee", "team": "JAI", "role": "DEF", "credits": 10.0, "points": 470, "selectedBy": "91.0%", "isPlaying": True, "cBy": "22.0%", "vcBy": "20.0%"},
        {"id": "jai_7", "name": "Sahul Kumar", "team": "JAI", "role": "DEF", "credits": 8.5, "points": 290, "selectedBy": "56.0%", "isPlaying": True, "cBy": "4.0%", "vcBy": "6.0%"}
    ]
}

# Add matches if not already present
match_ids = [m["id"] for m in fdata["matches"]]
if "rma-mci-ucl" not in match_ids:
    fdata["matches"].append(football_match)
if "pat-jai-pkl" not in match_ids:
    fdata["matches"].append(kabaddi_match)

# Enhance simulationScript with sound cues and Hindi commentary
for ev in fdata["simulationScript"]:
    if ev.get("isWicket"):
        ev["sound"] = "timber"
    elif ev.get("runs") == 6:
        ev["sound"] = "six"
    elif ev.get("runs") == 4:
        ev["sound"] = "four"
    elif ev.get("runs") > 0:
        ev["sound"] = "single"
    else:
        ev["sound"] = "dot"

    # Hindi commentary
    if ev.get("isWicket"):
        ev["commentHindi"] = f"आउट! गिल्लियां हवा में उड़ गईं! {ev['bowler']} की जादुई गेंद ने {ev['batsman']} को पवेलियन भेजा! शानदार विकेट!"
    elif ev.get("runs") == 6:
        ev["commentHindi"] = f"छक्का! गेंद सीमा रेखा के पार दर्शक दीर्घा में! {ev['batsman']} का गगनचुंबी प्रहार!"
    elif ev.get("runs") == 4:
        ev["commentHindi"] = f"चौका! गैप में खूबसूरती से ड्राइव किया {ev['batsman']} ने, गेंद गोली की रफ्तार से बाउंड्री के पार!"
    elif ev.get("runs") > 0:
        ev["commentHindi"] = f"कसी हुई गेंद, {ev['batsman']} ने हल्के हाथों से खेलकर {ev['runs']} रन चुरा लिए।"
    else:
        ev["commentHindi"] = f"शानदार डॉट गेंद! {ev['bowler']} का सटीक लाइन और लेंथ, बल्लेबाज पूरी तरह बीट हुए।"

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(fdata, f, indent=2, ensure_ascii=False)

print("fantasy_data.json updated with Football, Kabaddi, and Bilingual Audio simulation events!")
