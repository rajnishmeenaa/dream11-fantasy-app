import re

INDEX_PATH = r"C:\Users\MY WORLD\.gemini\antigravity\scratch\dream11-fantasy-app\public\index.html"
STYLES_PATH = r"C:\Users\MY WORLD\.gemini\antigravity\scratch\dream11-fantasy-app\public\styles.css"
APP_PATH = r"C:\Users\MY WORLD\.gemini\antigravity\scratch\dream11-fantasy-app\public\app.js"

# 1. Update index.html
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Add admin pill in header if not present
if "btn-open-admin" not in html:
    html = html.replace(
        '<button id="btn-open-wallet"',
        '<button id="btn-open-admin" class="admin-pill" title="Open Admin Hub">⚙️ Admin</button>\n          <button id="btn-open-wallet"'
    )

# Add admin menu item in profile list if not present
if "menu-item-admin" not in html:
    html = html.replace(
        '<div class="profile-actions-list">',
        '<div class="profile-actions-list">\n            <div class="profile-menu-item" id="menu-item-admin" style="background:#fef2f2; color:#b91c1c; font-weight:800">\n              <span>⚙️ Admin & Manager Control Hub</span>\n              <strong>›</strong>\n            </div>'
    )

# Add view-admin before </main> if not present
ADMIN_HTML = """
        <!-- ================= VIEW 9: ADMIN CONTROL HUB ================= -->
        <section id="view-admin" class="app-view">
          <div class="sub-header" style="background:#1e1b4b">
            <button class="back-btn" id="btn-back-from-admin">←</button>
            <div class="sub-header-title">
              <h4 style="color:#facc15">⚙️ Admin & Manager Hub</h4>
              <span class="time-pill" style="color:#a5b4fc">Full Control Center</span>
            </div>
            <button class="pitch-btn" style="background:#4338ca" id="btn-exit-admin">Exit</button>
          </div>

          <!-- Admin Sub Tabs -->
          <div class="sub-tabs-bar" id="admin-sub-tabs">
            <button class="sub-tab active" data-admintab="contests">🏆 Contests</button>
            <button class="sub-tab" data-admintab="matches">🏏 Matches</button>
            <button class="sub-tab" data-admintab="wallet">💰 Wallet</button>
            <button class="sub-tab" data-admintab="godmode">⚡ Live Control</button>
          </div>

          <!-- Admin Tab 1: Contests Manager -->
          <div class="admin-section" id="admin-tab-contests">
            <div class="admin-card">
              <h4>Create New Contest</h4>
              <form id="form-create-contest" class="admin-form">
                <div class="form-group">
                  <label>Contest Name</label>
                  <input type="text" id="adm-c-name" required value="Super Sunday Mega Dhamaka" placeholder="e.g. Diwali Mega Super League">
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Category</label>
                    <select id="adm-c-type">
                      <option value="mega">Mega Contest</option>
                      <option value="h2h">Head-to-Head</option>
                      <option value="wta">Winner Takes All</option>
                      <option value="popular">Popular League</option>
                      <option value="practice">Practice (Free)</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>Badge Tag</label>
                    <input type="text" id="adm-c-badge" value="MEGA" placeholder="MEGA, HOT, SPECIAL">
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Total Prize Pool</label>
                    <input type="text" id="adm-c-prize" required value="₹10 Crores" placeholder="e.g. ₹10 Crores">
                  </div>
                  <div class="form-group">
                    <label>1st Prize</label>
                    <input type="text" id="adm-c-first-prize" required value="₹1 Crore + SUV" placeholder="e.g. ₹1 Crore">
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Entry Fee (₹)</label>
                    <input type="number" id="adm-c-fee" required value="39" min="0">
                  </div>
                  <div class="form-group">
                    <label>Total Spots</label>
                    <input type="number" id="adm-c-spots" required value="300000" min="2">
                  </div>
                </div>
                <button type="submit" class="btn-primary" style="width:100%; margin-top:8px">
                  🚀 PUBLISH CONTEST TO LOBBY
                </button>
              </form>
            </div>

            <div class="admin-card" style="margin-top:14px">
              <h4>Active Contests in App (<span id="admin-contest-count">0</span>)</h4>
              <div id="admin-contests-list" class="admin-items-list"></div>
            </div>
          </div>

          <!-- Admin Tab 2: Matches Manager -->
          <div class="admin-section hidden" id="admin-tab-matches">
            <div class="admin-card">
              <h4>Add New Match Fixture</h4>
              <form id="form-create-match" class="admin-form">
                <div class="form-group">
                  <label>Match Title</label>
                  <input type="text" id="adm-m-title" required value="India vs Pakistan" placeholder="e.g. India vs Pakistan">
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Series / Tournament</label>
                    <input type="text" id="adm-m-series" required value="ICC T20 World Cup 2026" placeholder="e.g. ICC T20 World Cup">
                  </div>
                  <div class="form-group">
                    <label>Venue</label>
                    <input type="text" id="adm-m-venue" required value="Melbourne Cricket Ground" placeholder="e.g. Wankhede Stadium">
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Team 1 (Name, Short, Flag)</label>
                    <input type="text" id="adm-m-t1" required value="India, IND, 🇮🇳">
                  </div>
                  <div class="form-group">
                    <label>Team 2 (Name, Short, Flag)</label>
                    <input type="text" id="adm-m-t2" required value="Pakistan, PAK, 🇵🇰">
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Mega Contest Prize</label>
                    <input type="text" id="adm-m-prize" value="₹75 Crores">
                  </div>
                  <div class="form-group">
                    <label>Entry Fee (₹)</label>
                    <input type="number" id="adm-m-fee" value="49" min="0">
                  </div>
                </div>
                <button type="submit" class="btn-primary" style="width:100%; margin-top:8px">
                  🏏 ADD MATCH FIXTURE
                </button>
              </form>
            </div>

            <div class="admin-card" style="margin-top:14px">
              <h4>Existing Fixtures</h4>
              <div id="admin-matches-list" class="admin-items-list"></div>
            </div>
          </div>

          <!-- Admin Tab 3: Wallet & Users -->
          <div class="admin-section hidden" id="admin-tab-wallet">
            <div class="admin-card">
              <h4>User Wallet Injector</h4>
              <p style="font-size:11px; color:var(--text-muted); margin-bottom:12px">Instantly credit or reset user balances</p>
              
              <div class="admin-quick-wallet-grid">
                <button type="button" class="btn-adm-wallet" data-action="add-dep" data-val="500">+ ₹500 Deposit</button>
                <button type="button" class="btn-adm-wallet" data-action="add-win" data-val="1000">+ ₹1,000 Winnings</button>
                <button type="button" class="btn-adm-wallet" data-action="add-bon" data-val="250">+ ₹250 Bonus</button>
                <button type="button" class="btn-adm-wallet reset" data-action="reset">🔄 Reset to ₹1,500</button>
              </div>

              <div style="margin-top:16px; border-top:1px solid #e2e8f0; padding-top:12px">
                <h5>Set Custom Balances Directly:</h5>
                <div class="form-row" style="margin-top:8px">
                  <div class="form-group">
                    <label>Deposit (₹)</label>
                    <input type="number" id="adm-w-dep" value="500">
                  </div>
                  <div class="form-group">
                    <label>Winnings (₹)</label>
                    <input type="number" id="adm-w-win" value="650">
                  </div>
                  <div class="form-group">
                    <label>Bonus (₹)</label>
                    <input type="number" id="adm-w-bon" value="350">
                  </div>
                </div>
                <button type="button" id="btn-adm-save-wallet" class="btn-primary" style="width:100%; margin-top:10px">
                  SAVE WALLET ADJUSTMENT ✓
                </button>
              </div>
            </div>
          </div>

          <!-- Admin Tab 4: Live Match God Mode -->
          <div class="admin-section hidden" id="admin-tab-godmode">
            <div class="admin-card">
              <h4 style="color:#b91c1c">⚡ Live Match Event Injector (God Mode)</h4>
              <p style="font-size:11px; color:var(--text-muted); margin-bottom:12px">
                Inject custom real-time events into the ongoing match. Watch points and leaderboards update live!
              </p>

              <form id="form-adm-godmode" class="admin-form">
                <div class="form-row">
                  <div class="form-group">
                    <label>Striker</label>
                    <input type="text" id="adm-gm-bat" value="Travis Head">
                  </div>
                  <div class="form-group">
                    <label>Bowler</label>
                    <input type="text" id="adm-gm-bowl" value="Jasprit Bumrah">
                  </div>
                </div>

                <div class="form-group">
                  <label>Outcome</label>
                  <div class="godmode-outcomes">
                    <label class="outcome-chip"><input type="radio" name="gm-outcome" value="0"> Dot (0)</label>
                    <label class="outcome-chip"><input type="radio" name="gm-outcome" value="1"> 1 Run</label>
                    <label class="outcome-chip"><input type="radio" name="gm-outcome" value="2"> 2 Runs</label>
                    <label class="outcome-chip four"><input type="radio" name="gm-outcome" value="4" checked> FOUR (4)</label>
                    <label class="outcome-chip six"><input type="radio" name="gm-outcome" value="6"> SIX (6)</label>
                    <label class="outcome-chip wicket"><input type="radio" name="gm-outcome" value="w"> WICKET</label>
                  </div>
                </div>

                <div class="form-group" id="adm-gm-wtype-group" style="display:none">
                  <label>Wicket Type</label>
                  <select id="adm-gm-wtype">
                    <option value="bowled">Bowled (+25 +8)</option>
                    <option value="caught">Caught (+25 +8)</option>
                    <option value="lbw">LBW (+25 +8)</option>
                    <option value="stumped">Stumped (+25 +12)</option>
                  </select>
                </div>

                <div class="form-group">
                  <label>Custom Commentary Text</label>
                  <input type="text" id="adm-gm-comment" value="CRACKING SHOT! Head leans into the drive and carves it through covers for FOUR!">
                </div>

                <button type="submit" class="btn-primary" style="width:100%; background:linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)">
                  ⚡ DELIVER CUSTOM BALL NOW 🏏
                </button>
              </form>
            </div>
          </div>
        </section>
"""

if "id=\"view-admin\"" not in html:
    html = html.replace("</main>", f"{ADMIN_HTML}\n      </main>")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html successfully updated with Admin UI!")

# 2. Update styles.css
with open(STYLES_PATH, "r", encoding="utf-8") as f:
    css = f.read()

ADMIN_CSS = """
/* ================= ADMIN DASHBOARD STYLES ================= */
.admin-pill {
  background: #312e81;
  border: 1px solid #6366f1;
  color: #e0e7ff;
  font-size: 11px;
  font-weight: 800;
  padding: 5px 10px;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.2s;
}
.admin-pill:hover {
  background: #4338ca;
  border-color: #818cf8;
}
.admin-card {
  background: #ffffff;
  border-radius: var(--radius-lg);
  padding: 16px;
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}
.admin-card h4 {
  font-size: 14px;
  font-weight: 800;
  margin-bottom: 12px;
  color: var(--text-main);
}
.admin-form .form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 10px;
}
.admin-form label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
}
.admin-form input, .admin-form select {
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--border-light);
  font-size: 12px;
  outline: none;
  font-family: inherit;
}
.admin-form input:focus, .admin-form select:focus {
  border-color: var(--primary);
}
.form-row {
  display: flex;
  gap: 10px;
}
.form-row .form-group {
  flex: 1;
}
.admin-items-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}
.admin-item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: var(--radius-md);
  border: 1px solid #e2e8f0;
}
.btn-delete-item {
  background: #fee2e2;
  color: #b91c1c;
  border: none;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
}
.btn-delete-item:hover { background: #fecaca; }

.admin-quick-wallet-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.btn-adm-wallet {
  background: #f8fafc;
  border: 1.5px solid #cbd5e1;
  padding: 10px;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}
.btn-adm-wallet:hover { border-color: var(--primary); background: #fff1f2; color: var(--primary); }
.btn-adm-wallet.reset { background: #fee2e2; border-color: #f87171; color: #b91c1c; }

.godmode-outcomes {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.outcome-chip {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  padding: 6px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}
.outcome-chip.four { color: #1e40af; border-color: #93c5fd; }
.outcome-chip.six { color: #7e22ce; border-color: #d8b4fe; }
.outcome-chip.wicket { color: #b91c1c; border-color: #fca5a5; }
"""

if "admin-pill" not in css:
    css += "\n" + ADMIN_CSS
    with open(STYLES_PATH, "w", encoding="utf-8") as f:
        f.write(css)
    print("styles.css updated with Admin styles!")

# 3. Update app.js
with open(APP_PATH, "r", encoding="utf-8") as f:
    js = f.read()

ADMIN_JS = """
// ================= ADMIN DASHBOARD CONTROLLERS =================
function setupAdminControllers() {
  document.getElementById('btn-open-admin')?.addEventListener('click', openAdminDashboard);
  document.getElementById('menu-item-admin')?.addEventListener('click', openAdminDashboard);
  document.getElementById('btn-back-from-admin')?.addEventListener('click', () => switchView('view-home'));
  document.getElementById('btn-exit-admin')?.addEventListener('click', () => switchView('view-home'));

  // Admin sub-tabs
  document.querySelectorAll('#admin-sub-tabs .sub-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('#admin-sub-tabs .sub-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.admintab;
      document.getElementById('admin-tab-contests').classList.toggle('hidden', target !== 'contests');
      document.getElementById('admin-tab-matches').classList.toggle('hidden', target !== 'matches');
      document.getElementById('admin-tab-wallet').classList.toggle('hidden', target !== 'wallet');
      document.getElementById('admin-tab-godmode').classList.toggle('hidden', target !== 'godmode');
    });
  });

  // Contest creation form
  document.getElementById('form-create-contest')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('adm-c-name').value,
      type: document.getElementById('adm-c-type').value,
      badge: document.getElementById('adm-c-badge').value,
      totalPrize: document.getElementById('adm-c-prize').value,
      firstPrize: document.getElementById('adm-c-first-prize').value,
      entryFee: parseInt(document.getElementById('adm-c-fee').value) || 0,
      totalSpots: parseInt(document.getElementById('adm-c-spots').value) || 1000,
    };
    const res = await fetchAPI('/api/admin/contests/create', 'POST', payload);
    if (res && res.success) {
      state.contests = res.contests;
      renderAdminContestsList();
      renderContestsList();
      showToast(`🏆 Contest '${payload.name}' published successfully!`, 'success');
    }
  });

  // Match creation form
  document.getElementById('form-create-match')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const t1Parts = document.getElementById('adm-m-t1').value.split(',').map(s => s.trim());
    const t2Parts = document.getElementById('adm-m-t2').value.split(',').map(s => s.trim());
    const payload = {
      title: document.getElementById('adm-m-title').value,
      series: document.getElementById('adm-m-series').value,
      venue: document.getElementById('adm-m-venue').value,
      team1: { name: t1Parts[0] || 'Team 1', shortName: t1Parts[1] || 'T1', logo: t1Parts[2] || '🏏', color: '#1e40af' },
      team2: { name: t2Parts[0] || 'Team 2', shortName: t2Parts[1] || 'T2', logo: t2Parts[2] || '⚡', color: '#ca8a04' },
      megaPrize: document.getElementById('adm-m-prize').value,
      entryFee: parseInt(document.getElementById('adm-m-fee').value) || 49
    };
    const res = await fetchAPI('/api/admin/matches/create', 'POST', payload);
    if (res && res.success) {
      state.matches = res.matches;
      renderAdminMatchesList();
      renderMatches();
      showToast(`🏏 Match '${payload.title}' added to schedule!`, 'success');
    }
  });

  // Quick wallet adjustments
  document.querySelectorAll('.btn-adm-wallet').forEach(btn => {
    btn.addEventListener('click', async () => {
      const act = btn.dataset.action;
      const val = parseInt(btn.dataset.val) || 0;
      let payload = {};
      if (act === 'add-dep') payload = { deposited: (state.user.wallet.deposited || 0) + val };
      else if (act === 'add-win') payload = { winnings: (state.user.wallet.winnings || 0) + val };
      else if (act === 'add-bon') payload = { bonus: (state.user.wallet.bonus || 0) + val };
      else if (act === 'reset') payload = { deposited: 500, winnings: 650, bonus: 350 };

      const res = await fetchAPI('/api/admin/wallet/adjust', 'POST', payload);
      if (res && res.success) {
        state.user.wallet = res.wallet;
        updateUserHeader();
        syncAdminWalletInputs();
        showToast('💰 Wallet adjusted successfully by Admin!', 'success');
      }
    });
  });

  document.getElementById('btn-adm-save-wallet')?.addEventListener('click', async () => {
    const payload = {
      deposited: parseInt(document.getElementById('adm-w-dep').value) || 0,
      winnings: parseInt(document.getElementById('adm-w-win').value) || 0,
      bonus: parseInt(document.getElementById('adm-w-bon').value) || 0
    };
    const res = await fetchAPI('/api/admin/wallet/adjust', 'POST', payload);
    if (res && res.success) {
      state.user.wallet = res.wallet;
      updateUserHeader();
      showToast('💰 Custom balance saved!', 'success');
    }
  });

  // God Mode outcomes radio change
  document.querySelectorAll('input[name="gm-outcome"]').forEach(r => {
    r.addEventListener('change', () => {
      document.getElementById('adm-gm-wtype-group').style.display = (r.value === 'w') ? 'block' : 'none';
    });
  });

  // God Mode custom delivery
  document.getElementById('form-adm-godmode')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const outcome = document.querySelector('input[name="gm-outcome"]:checked').value;
    const isWicket = (outcome === 'w');
    const runs = isWicket ? 0 : parseInt(outcome);
    const payload = {
      batsman: document.getElementById('adm-gm-bat').value,
      bowler: document.getElementById('adm-gm-bowl').value,
      runs: runs,
      isWicket: isWicket,
      wicketType: isWicket ? document.getElementById('adm-gm-wtype').value : null,
      comment: document.getElementById('adm-gm-comment').value
    };

    const res = await fetchAPI('/api/admin/live/custom-ball', 'POST', payload);
    if (res && res.success) {
      state.simState = res.state;
      showToast('⚡ Custom ball delivered! Points & Leaderboard updated!', 'success');
      startLiveMatchSimulation();
    }
  });
}

function openAdminDashboard() {
  renderAdminContestsList();
  renderAdminMatchesList();
  syncAdminWalletInputs();
  switchView('view-admin');
}

function syncAdminWalletInputs() {
  if (!state.user) return;
  document.getElementById('adm-w-dep').value = state.user.wallet.deposited || 0;
  document.getElementById('adm-w-win').value = state.user.wallet.winnings || 0;
  document.getElementById('adm-w-bon').value = state.user.wallet.bonus || 0;
}

function renderAdminContestsList() {
  const container = document.getElementById('admin-contests-list');
  if (!container) return;
  container.innerHTML = '';
  document.getElementById('admin-contest-count').textContent = state.contests.length;

  state.contests.forEach(c => {
    const row = document.createElement('div');
    row.className = 'admin-item-row';
    row.innerHTML = `
      <div>
        <strong>${c.name}</strong> (${c.badge})
        <div style="font-size:11px; color:var(--text-muted)">Prize: ${c.totalPrize} • Entry: ₹${c.entryFee} • Spots: ${c.totalSpots.toLocaleString('en-IN')}</div>
      </div>
      <button class="btn-delete-item" data-del-cid="${c.id}">🗑️ Delete</button>
    `;
    row.querySelector('[data-del-cid]').addEventListener('click', async () => {
      const res = await fetchAPI('/api/admin/contests/delete', 'POST', { contestId: c.id });
      if (res && res.success) {
        state.contests = res.contests;
        renderAdminContestsList();
        renderContestsList();
        showToast(`Contest '${c.name}' deleted!`, 'success');
      }
    });
    container.appendChild(row);
  });
}

function renderAdminMatchesList() {
  const container = document.getElementById('admin-matches-list');
  if (!container) return;
  container.innerHTML = '';

  state.matches.forEach(m => {
    const row = document.createElement('div');
    row.className = 'admin-item-row';
    row.innerHTML = `
      <div>
        <strong>${m.team1.logo} ${m.team1.shortName} vs ${m.team2.shortName} ${m.team2.logo}</strong>
        <div style="font-size:11px; color:var(--text-muted)">${m.series} • ${m.venue}</div>
      </div>
      <span style="font-size:10px; background:#dcfce7; color:#15803d; font-weight:700; padding:2px 8px; border-radius:10px">Active</span>
    `;
    container.appendChild(row);
  });
}
"""

if "setupAdminControllers" not in js:
    # Append admin controllers and call setupAdminControllers in initApp
    js = js.replace("setupEventListeners();", "setupEventListeners();\n  setupAdminControllers();")
    js += "\n" + ADMIN_JS
    with open(APP_PATH, "w", encoding="utf-8") as f:
        f.write(js)
    print("app.js updated with Admin controllers!")
