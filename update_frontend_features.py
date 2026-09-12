# Upgrade index.html, styles.css, and app.js with features 2, 3, 4, 5
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "public", "index.html")
STYLES_PATH = os.path.join(BASE_DIR, "public", "styles.css")
APP_PATH = os.path.join(BASE_DIR, "public", "app.js")

# =========================================================================
# 1. UPGRADE index.html
# =========================================================================
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Head tags: manifest & theme-color
if 'manifest.json' not in html:
    html = html.replace(
        '<link rel="stylesheet" href="styles.css">',
        '<link rel="manifest" href="manifest.json">\n  <meta name="theme-color" content="#b91c1c">\n  <link rel="stylesheet" href="styles.css">'
    )

# Header right: Install App button
if 'btn-pwa-install' not in html:
    html = html.replace(
        '<div class="header-right">',
        '<div class="header-right">\n          <button id="btn-pwa-install" class="pwa-install-pill hidden" title="Install App on Device">📱 Install</button>'
    )

# Private Contest Banner in Contest Lobby
pc_banner = '''          <!-- Private Contest Quick Bar -->
          <div class="private-contest-banner">
            <div class="pc-banner-header">
              <span class="pc-badge">🔒 PRIVATE CONTESTS</span>
              <span style="font-size:11px; color:#cbd5e1">Play exclusively with friends</span>
            </div>
            <div class="pc-actions-row">
              <div class="pc-code-input-wrap">
                <input type="text" id="input-invite-code" placeholder="Enter Code (e.g. D11-882)" maxlength="10">
                <button id="btn-submit-code-join" class="btn-pc-join">Join</button>
              </div>
              <button id="btn-open-create-private" class="btn-pc-create">+ Create League</button>
            </div>
          </div>
'''

if 'private-contest-banner' not in html:
    html = html.replace(
        '<!-- Category Filter Bar -->',
        pc_banner + '\n          <!-- Category Filter Bar -->'
    )

if 'data-type="private"' not in html:
    html = html.replace(
        '<button class="type-pill" data-type="practice">Free Practice</button>',
        '<button class="type-pill" data-type="practice">Free Practice</button>\n            <button class="type-pill" data-type="private">🔒 Private</button>'
    )

# Live Match View: Sound and Language Toggles
live_toggles = '''          <!-- Stadium Audio & Bilingual Commentary Switcher -->
          <div class="live-action-toggles">
            <button id="btn-toggle-sound" class="live-pill-toggle active" title="Toggle Stadium Sound FX">
              <span id="sound-icon">🔊</span> <span id="sound-text">Sound ON</span>
            </button>
            <button id="btn-toggle-lang" class="live-pill-toggle" title="Toggle Commentary Language">
              🌐 <span id="lang-text">Commentary: English</span>
            </button>
          </div>
'''

if 'live-action-toggles' not in html:
    html = html.replace(
        '<!-- Live Match Scoreboard -->',
        live_toggles + '\n          <!-- Live Match Scoreboard -->'
    )

# 2D Pitch Modal: Add Football and Kabaddi fields
multi_pitch = '''      <!-- Dynamic 2D Pitch Field Container -->
      <div id="dynamic-pitch-wrapper" style="flex:1; display:flex; flex-direction:column; overflow:hidden">
        <!-- 1. Cricket Pitch Field -->
        <div id="pitch-field-cricket" class="cricket-pitch-field">
          <div class="pitch-grass-texture"></div>
          <div class="field-boundary-ring"></div>
          <div class="inner-circle-ring"></div>
          <div class="pitch-strip">
            <div class="bowling-crease top"></div>
            <div class="stumps top"></div>
            <div class="pitch-center-strip"></div>
            <div class="stumps bottom"></div>
            <div class="batting-crease bottom"></div>
          </div>

          <div class="field-players-overlay">
            <div class="pitch-row" id="pitch-row-wk">
              <div class="pitch-row-label">WICKET-KEEPERS</div>
              <div class="pitch-row-players" id="pitch-players-wk"></div>
            </div>
            <div class="pitch-row" id="pitch-row-bat">
              <div class="pitch-row-label">BATSMEN</div>
              <div class="pitch-row-players" id="pitch-players-bat"></div>
            </div>
            <div class="pitch-row" id="pitch-row-ar">
              <div class="pitch-row-label">ALL-ROUNDERS</div>
              <div class="pitch-row-players" id="pitch-players-ar"></div>
            </div>
            <div class="pitch-row" id="pitch-row-bowl">
              <div class="pitch-row-label">BOWLERS</div>
              <div class="pitch-row-players" id="pitch-players-bowl"></div>
            </div>
          </div>
        </div>

        <!-- 2. Football 2D Pitch Field -->
        <div id="pitch-field-football" class="football-pitch-field hidden">
          <div class="football-center-line"></div>
          <div class="football-center-circle"></div>
          <div class="football-penalty-area top"></div>
          <div class="football-penalty-area bottom"></div>

          <div class="field-players-overlay">
            <div class="pitch-row" id="pitch-row-gk">
              <div class="pitch-row-label">GOALKEEPER (GK)</div>
              <div class="pitch-row-players" id="pitch-players-gk"></div>
            </div>
            <div class="pitch-row" id="pitch-row-def">
              <div class="pitch-row-label">DEFENDERS (DEF)</div>
              <div class="pitch-row-players" id="pitch-players-def"></div>
            </div>
            <div class="pitch-row" id="pitch-row-mid">
              <div class="pitch-row-label">MIDFIELDERS (MID)</div>
              <div class="pitch-row-players" id="pitch-players-mid"></div>
            </div>
            <div class="pitch-row" id="pitch-row-fwd">
              <div class="pitch-row-label">FORWARDS (FWD)</div>
              <div class="pitch-row-players" id="pitch-players-fwd"></div>
            </div>
          </div>
        </div>

        <!-- 3. Kabaddi 2D Mat Field -->
        <div id="pitch-field-kabaddi" class="kabaddi-pitch-field hidden">
          <div class="kabaddi-midline"></div>
          <div class="kabaddi-baulk-line top"></div>
          <div class="kabaddi-baulk-line bottom"></div>
          <div class="kabaddi-bonus-line top"></div>
          <div class="kabaddi-bonus-line bottom"></div>
          <div class="kabaddi-lobby left"></div>
          <div class="kabaddi-lobby right"></div>

          <div class="field-players-overlay">
            <div class="pitch-row" id="pitch-row-kdef">
              <div class="pitch-row-label">DEFENDERS (DEF)</div>
              <div class="pitch-row-players" id="pitch-players-kdef"></div>
            </div>
            <div class="pitch-row" id="pitch-row-kall">
              <div class="pitch-row-label">ALL-ROUNDERS (ALL)</div>
              <div class="pitch-row-players" id="pitch-players-kall"></div>
            </div>
            <div class="pitch-row" id="pitch-row-krai">
              <div class="pitch-row-label">RAIDERS (RAI)</div>
              <div class="pitch-row-players" id="pitch-players-krai"></div>
            </div>
          </div>
        </div>
      </div>
'''

if 'pitch-field-football' not in html:
    # Replace existing cricket-pitch-field
    cricket_block_start = '<div class="cricket-pitch-field">'
    cricket_block_end = '<!-- 2. PRIZE BREAKUP MODAL -->'
    pos1 = html.find(cricket_block_start)
    pos2 = html.find(cricket_block_end)
    if pos1 != -1 and pos2 != -1:
        # Before pos2, there is </div>\n    </div>\n  </div>
        html = html[:pos1] + multi_pitch + '    </div>\n  </div>\n\n  ' + html[pos2:]

# Modals for Private Contests
private_modals = '''  <!-- 5. CREATE PRIVATE CONTEST MODAL -->
  <div class="modal-overlay hidden" id="modal-create-private-contest">
    <div class="bottom-sheet-modal">
      <div class="sheet-handle"></div>
      <div class="sheet-header">
        <h4>Create Private Contest</h4>
        <button class="sheet-close-btn" id="btn-close-create-private">✕</button>
      </div>
      <div class="sheet-body">
        <p style="font-size:12px; color:var(--text-muted); margin-bottom:12px">
          Challenge friends, colleagues or family. Get an exclusive invite code to share on WhatsApp or Telegram!
        </p>
        <form id="form-create-private-contest" class="admin-form">
          <div class="form-group">
            <label>Contest Name</label>
            <input type="text" id="pc-name" required value="Champs League with Friends" placeholder="e.g. Hostels Derby">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Total Spots</label>
              <select id="pc-spots">
                <option value="2">2 (Head to Head)</option>
                <option value="5">5 Spots</option>
                <option value="10" selected>10 Spots</option>
                <option value="25">25 Spots</option>
                <option value="50">50 Spots</option>
              </select>
            </div>
            <div class="form-group">
              <label>Entry Fee (₹)</label>
              <input type="number" id="pc-fee" required value="50" min="5" max="5000">
            </div>
          </div>
          <div class="pc-calc-summary">
            <div class="pc-calc-item">
              <span>Total Prize:</span>
              <strong id="pc-calc-total" style="color:#16a34a">₹500</strong>
            </div>
            <div class="pc-calc-item">
              <span>1st Prize:</span>
              <strong id="pc-calc-1st" style="color:var(--gold)">₹300</strong>
            </div>
          </div>
          <div class="form-group" style="margin-top:10px">
            <label>Select Your Team to Play With:</label>
            <div class="team-picker-list" id="pc-team-picker"></div>
          </div>
          <button type="submit" class="btn-primary" style="width:100%; margin-top:10px">
            🚀 CREATE & GET INVITE CODE
          </button>
        </form>
      </div>
    </div>
  </div>

  <!-- 6. PRIVATE CONTEST SHARE MODAL -->
  <div class="modal-overlay hidden" id="modal-private-code-share">
    <div class="bottom-sheet-modal" style="text-align:center">
      <div class="sheet-handle"></div>
      <div style="font-size:44px; margin-bottom:8px">🎉</div>
      <h4 style="font-size:18px; font-weight:900">Private Contest Created!</h4>
      <p style="font-size:12px; color:var(--text-muted); margin:4px 0 16px">
        Share this 6-character invite code with your friends to let them join:
      </p>
      <div class="share-code-box">
        <span class="share-code-text" id="share-modal-code">D11-882</span>
        <button class="btn-copy-code" id="btn-copy-share-code">📋 Copy</button>
      </div>
      <div class="share-buttons-row">
        <button class="btn-share-wa" id="btn-share-whatsapp">💬 Share via WhatsApp</button>
        <button class="btn-secondary" id="btn-done-share" style="width:100px">Done</button>
      </div>
    </div>
  </div>

  <!-- 7. JOIN PRIVATE CONTEST MODAL -->
  <div class="modal-overlay hidden" id="modal-join-private">
    <div class="bottom-sheet-modal">
      <div class="sheet-handle"></div>
      <div class="sheet-header">
        <h4>Join Private Contest</h4>
        <button class="sheet-close-btn" id="btn-close-join-private">✕</button>
      </div>
      <div class="sheet-body">
        <div class="join-private-card" id="join-private-details-box"></div>
        <div class="form-group" style="margin-top:12px">
          <label class="form-label">Select Your Fantasy Team to Join With:</label>
          <div class="team-picker-list" id="join-private-team-picker"></div>
        </div>
        <div class="payment-breakdown-box">
          <div class="pay-row">
            <span>Entry Fee</span>
            <strong id="jp-entry-fee">₹50</strong>
          </div>
          <div class="pay-row total">
            <span>To Pay</span>
            <strong id="jp-final-pay">₹50</strong>
          </div>
        </div>
        <button class="btn-join-pay-now" id="btn-confirm-join-private">
          PAY & JOIN PRIVATE LEAGUE ✓
        </button>
      </div>
    </div>
  </div>
'''

if 'modal-create-private-contest' not in html:
    html = html.replace(
        '<!-- Toast Notification Container -->',
        private_modals + '\n  <!-- Toast Notification Container -->'
    )

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("index.html upgraded successfully!")

# =========================================================================
# 2. UPGRADE styles.css
# =========================================================================
with open(STYLES_PATH, "r", encoding="utf-8") as f:
    css = f.read()

new_styles = '''
/* PWA Install Button */
.pwa-install-pill {
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: #fff;
  border: none;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(22,163,74,0.3);
  animation: pwaPulse 2.5s infinite;
}
@keyframes pwaPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Private Contest Banner & Modals */
.private-contest-banner {
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  border-radius: var(--radius-lg);
  padding: 12px 14px;
  margin-bottom: 12px;
  color: #fff;
  border: 1px solid #4338ca;
  box-shadow: 0 4px 14px rgba(30,27,75,0.25);
}
.pc-banner-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 11px;
}
.pc-badge {
  background: #4f46e5;
  color: #fff;
  font-weight: 900;
  font-size: 10px;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  letter-spacing: 0.5px;
}
.pc-actions-row {
  display: flex;
  gap: 8px;
}
.pc-code-input-wrap {
  display: flex;
  flex: 1;
  background: #fff;
  border-radius: var(--radius-sm);
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}
.pc-code-input-wrap input {
  flex: 1;
  border: none;
  padding: 8px 10px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  outline: none;
  font-family: inherit;
  color: #0f172a;
}
.btn-pc-join {
  background: var(--primary);
  color: #fff;
  border: none;
  padding: 0 14px;
  font-weight: 800;
  font-size: 11px;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-pc-join:hover { background: var(--primary-dark); }
.btn-pc-create {
  background: #f59e0b;
  color: #000;
  border: none;
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s;
}
.btn-pc-create:hover { background: #d97706; }

.pc-calc-summary {
  background: #f8fafc;
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 700;
  margin-top: 8px;
  border: 1px solid #e2e8f0;
}
.share-code-box {
  background: #f1f5f9;
  border: 2px dashed #94a3b8;
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.share-code-text {
  font-size: 26px;
  font-weight: 900;
  letter-spacing: 3px;
  color: var(--primary);
}
.btn-copy-code {
  background: #1e293b;
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
.share-buttons-row {
  display: flex;
  gap: 8px;
}
.btn-share-wa {
  flex: 1;
  background: #25d366;
  color: #fff;
  border: none;
  padding: 12px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
}
.join-private-card {
  background: #f8fafc;
  border-radius: var(--radius-md);
  padding: 14px;
  border: 1px solid #e2e8f0;
}

/* Stadium Audio & Bilingual Commentary Switcher */
.live-action-toggles {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}
.live-pill-toggle {
  background: #18181b;
  border: 1px solid #3f3f46;
  color: #a1a1aa;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s;
}
.live-pill-toggle.active {
  background: #166534;
  border-color: #22c55e;
  color: #bbf7d0;
}

/* 2D Football Pitch Field */
.football-pitch-field {
  flex: 1;
  background: #15803d;
  background-image: repeating-linear-gradient(0deg, #15803d, #15803d 35px, #166534 35px, #166534 70px);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 10px 6px;
  border: 3px solid rgba(255,255,255,0.7);
  border-radius: 8px;
}
.football-center-line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: rgba(255,255,255,0.7);
}
.football-center-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90px;
  height: 90px;
  border: 2px solid rgba(255,255,255,0.7);
  border-radius: 50%;
}
.football-penalty-area.top {
  position: absolute;
  top: 0;
  left: 25%;
  right: 25%;
  height: 55px;
  border: 2px solid rgba(255,255,255,0.7);
  border-top: none;
}
.football-penalty-area.bottom {
  position: absolute;
  bottom: 0;
  left: 25%;
  right: 25%;
  height: 55px;
  border: 2px solid rgba(255,255,255,0.7);
  border-bottom: none;
}

/* 2D Kabaddi Mat Field */
.kabaddi-pitch-field {
  flex: 1;
  background: #c2410c;
  background-image: radial-gradient(#ea580c 40%, #c2410c 90%);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 10px 6px;
  border: 3px solid #facc15;
  border-radius: 8px;
}
.kabaddi-midline {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 3px;
  background: #fff;
  box-shadow: 0 0 6px #fff;
}
.kabaddi-baulk-line.top {
  position: absolute;
  top: 32%;
  left: 0;
  right: 0;
  height: 2px;
  background: #fef08a;
  border-top: 1.5px dashed #fef08a;
}
.kabaddi-baulk-line.bottom {
  position: absolute;
  bottom: 32%;
  left: 0;
  right: 0;
  height: 2px;
  background: #fef08a;
  border-bottom: 1.5px dashed #fef08a;
}
.kabaddi-bonus-line.top {
  position: absolute;
  top: 20%;
  left: 0;
  right: 0;
  height: 2px;
  background: #f87171;
}
.kabaddi-bonus-line.bottom {
  position: absolute;
  bottom: 20%;
  left: 0;
  right: 0;
  height: 2px;
  background: #f87171;
}
.kabaddi-lobby.left {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 14px;
  background: rgba(0,0,0,0.25);
  border-right: 1.5px solid #fff;
}
.kabaddi-lobby.right {
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  width: 14px;
  background: rgba(0,0,0,0.25);
  border-left: 1.5px solid #fff;
}

/* Team Jersey Colors for Multi-Sport */
.pitch-player-card.rma .pitch-jersey { background: #ffffff; color: #1e3a8a; border-color: #1e3a8a; }
.pitch-player-card.mci .pitch-jersey { background: #38bdf8; color: #082f49; }
.pitch-player-card.pat .pitch-jersey { background: #15803d; color: #ffffff; }
.pitch-player-card.jai .pitch-jersey { background: #ec4899; color: #ffffff; }
'''

if 'pwa-install-pill' not in css:
    css += new_styles

with open(STYLES_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("styles.css upgraded successfully!")
