// Fantasy11 Admin Console - Core Logic & Live Orchestrator

const state = {
  contests: [],
  matches: [],
  user: null,
  transactions: [],
  simState: {
    score: { team: 'AUS', runs: 0, wickets: 0, overs: '0.0' },
    commentary: [],
    leaderboard: []
  }
};

// Web Audio API Sound Synthesizer for Admin Feedback
class AdminAudioEngine {
  constructor() {
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) this.ctx = new AudioContext();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }
  playTone(freq, type = 'sine', duration = 0.15, gainVal = 0.1) {
    this.init();
    if (!this.ctx) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      console.warn('Audio tone failed', e);
    }
  }
  playCheer() {
    this.playTone(523.25, 'triangle', 0.1, 0.12);
    setTimeout(() => this.playTone(659.25, 'triangle', 0.12, 0.12), 100);
    setTimeout(() => this.playTone(783.99, 'triangle', 0.25, 0.15), 220);
  }
  playWicketSiren() {
    this.playTone(880, 'sawtooth', 0.12, 0.15);
    setTimeout(() => this.playTone(440, 'sawtooth', 0.2, 0.2), 120);
    setTimeout(() => this.playTone(220, 'sawtooth', 0.35, 0.25), 300);
  }
  playClick() {
    this.playTone(800, 'sine', 0.05, 0.04);
  }
}

const audio = new AdminAudioEngine();

// API Helper
async function apiCall(endpoint, method = 'GET', data = null) {
  try {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' }
    };
    if (data && method !== 'GET') {
      opts.body = JSON.stringify(data);
    }
    const res = await fetch(endpoint, opts);
    return await res.json();
  } catch (err) {
    console.error(`API Call to ${endpoint} failed:`, err);
    showToast('Network error connecting to backend server', 'error');
    return null;
  }
}

// Toast Helper
function showToast(msg, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  container.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateY(-10px)';
    t.style.transition = 'all 0.3s';
    setTimeout(() => t.remove(), 300);
  }, 3200);
}

// Initialize Admin App
document.addEventListener('DOMContentLoaded', async () => {
  setupTabs();
  setupFormHandlers();
  setupWalletHandlers();
  setupGodModeHandlers();
  await fetchFreshState();
  await fetchTransactions();

  // Poll for simulation & state every 4 seconds
  setInterval(async () => {
    const simRes = await apiCall('/api/simulation/state');
    if (simRes) {
      state.simState = simRes;
      updateScoreboardUI();
      updateTelemetryBar();
      renderCommentaryFeed();
      renderLeaderboardFeed();
    }
  }, 4000);
});

// Setup Tab Navigation
function setupTabs() {
  const tabs = document.querySelectorAll('.adm-tab-btn');
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      audio.playClick();
      const target = btn.dataset.tab;
      tabs.forEach(t => t.classList.remove('active'));
      btn.classList.add('active');

      document.querySelectorAll('.adm-view').forEach(v => v.classList.remove('active'));
      const activeView = document.getElementById(`adm-view-${target}`);
      if (activeView) activeView.classList.add('active');
    });
  });

  document.getElementById('btn-refresh-state')?.addEventListener('click', async () => {
    audio.playClick();
    await fetchFreshState();
    await fetchTransactions();
    showToast('⚡ Live server state synchronized!', 'success');
  });

  document.getElementById('btn-refresh-ledger')?.addEventListener('click', async () => {
    audio.playClick();
    await fetchTransactions();
    showToast('Passbook ledger refreshed!', 'success');
  });
}

// Fetch State from Server
async function fetchFreshState() {
  const data = await apiCall('/api/data');
  if (!data) return;

  state.contests = data.contests || [];
  state.matches = data.matches || [];
  state.user = data.user || null;
  state.transactions = data.transactions || [];
  if (data.simState) state.simState = data.simState;

  updateTelemetryBar();
  renderContestsList();
  renderMatchesList();
  syncWalletInputs();
  renderLedgerList();
  updateScoreboardUI();
  renderCommentaryFeed();
  renderLeaderboardFeed();
}

async function fetchTransactions() {
  const txns = await apiCall('/api/user/transactions');
  if (Array.isArray(txns)) {
    state.transactions = txns;
    renderLedgerList();
  }
}

// Update Telemetry Bar
function updateTelemetryBar() {
  document.getElementById('telem-contests').textContent = state.contests.length;
  document.getElementById('telem-matches').textContent = state.matches.length;

  if (state.user && state.user.wallet) {
    const w = state.user.wallet;
    const total = (w.deposited || 0) + (w.winnings || 0) + (w.bonus || 0);
    document.getElementById('telem-wallet').textContent = `₹${total.toLocaleString('en-IN')}`;
  }

  if (state.simState && state.simState.score) {
    const sc = state.simState.score;
    document.getElementById('telem-score').textContent = `${sc.team} ${sc.runs}/${sc.wickets} (${sc.overs})`;
  }
}

// Setup Form Handlers (Contests & Matches)
function setupFormHandlers() {
  // Create Contest
  document.getElementById('form-create-contest')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    audio.playClick();

    const payload = {
      name: document.getElementById('adm-c-name').value.trim(),
      type: document.getElementById('adm-c-type').value,
      badge: document.getElementById('adm-c-badge').value.trim().toUpperCase(),
      totalPrize: document.getElementById('adm-c-prize').value.trim(),
      firstPrize: document.getElementById('adm-c-first-prize').value.trim(),
      entryFee: parseInt(document.getElementById('adm-c-fee').value) || 0,
      totalSpots: parseInt(document.getElementById('adm-c-spots').value) || 1000,
      maxTeams: parseInt(document.getElementById('adm-c-maxteams').value) || 10
    };

    const res = await apiCall('/api/admin/contests/create', 'POST', payload);
    if (res && res.success) {
      state.contests = res.contests;
      renderContestsList();
      updateTelemetryBar();
      showToast(`🏆 Contest "${payload.name}" published to lobby!`, 'success');
      audio.playCheer();
    }
  });

  // Create Match Fixture
  document.getElementById('form-create-match')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    audio.playClick();

    const t1Parts = document.getElementById('adm-m-t1').value.split(',').map(s => s.trim());
    const t2Parts = document.getElementById('adm-m-t2').value.split(',').map(s => s.trim());
    const sport = document.getElementById('adm-m-sport').value;

    const payload = {
      title: document.getElementById('adm-m-title').value.trim(),
      sport: sport,
      series: document.getElementById('adm-m-series').value.trim(),
      venue: document.getElementById('adm-m-venue').value.trim(),
      team1: {
        name: t1Parts[0] || 'Team 1',
        shortName: t1Parts[1] || 'T1',
        logo: t1Parts[2] || (sport === 'football' ? '⚽' : sport === 'kabaddi' ? '🤼' : '🏏'),
        color: '#1e40af'
      },
      team2: {
        name: t2Parts[0] || 'Team 2',
        shortName: t2Parts[1] || 'T2',
        logo: t2Parts[2] || '⚡',
        color: '#ca8a04'
      },
      megaPrize: document.getElementById('adm-m-prize').value.trim(),
      entryFee: parseInt(document.getElementById('adm-m-fee').value) || 49
    };

    const res = await apiCall('/api/admin/matches/create', 'POST', payload);
    if (res && res.success) {
      state.matches = res.matches;
      renderMatchesList();
      updateTelemetryBar();
      showToast(`🏏 Match "${payload.title}" added to schedule!`, 'success');
      audio.playCheer();
    }
  });
}

// Render Contests
function renderContestsList() {
  const container = document.getElementById('adm-contests-list');
  const countBadge = document.getElementById('contests-count-badge');
  if (countBadge) countBadge.textContent = state.contests.length;
  if (!container) return;

  container.innerHTML = '';
  if (state.contests.length === 0) {
    container.innerHTML = '<div style="color:var(--text-muted); font-size:13px; text-align:center; padding:20px;">No active contests</div>';
    return;
  }

  state.contests.forEach(c => {
    const card = document.createElement('div');
    card.className = 'adm-item-card';
    card.innerHTML = `
      <div class="item-info-col">
        <h4>${c.name}</h4>
        <div class="item-meta">
          <span class="meta-chip" style="color:#f59e0b">${c.badge || 'MEGA'}</span>
          <span class="meta-chip">Prize: ${c.totalPrize}</span>
          <span class="meta-chip">1st: ${c.firstPrize || 'Cash'}</span>
          <span class="meta-chip">Fee: ₹${c.entryFee}</span>
          <span class="meta-chip">Spots: ${(c.spotsLeft || c.totalSpots).toLocaleString('en-IN')} / ${c.totalSpots.toLocaleString('en-IN')}</span>
        </div>
      </div>
      <button class="btn-delete-chip" data-cid="${c.id}">🗑️ Delete</button>
    `;

    card.querySelector('[data-cid]').addEventListener('click', async () => {
      audio.playTone(400, 'sine', 0.1, 0.08);
      if (confirm(`Are you sure you want to delete "${c.name}"?`)) {
        const res = await apiCall('/api/admin/contests/delete', 'POST', { contestId: c.id });
        if (res && res.success) {
          state.contests = res.contests;
          renderContestsList();
          updateTelemetryBar();
          showToast(`Contest "${c.name}" deleted from lobby`, 'info');
        }
      }
    });

    container.appendChild(card);
  });
}

// Render Matches
function renderMatchesList() {
  const container = document.getElementById('adm-matches-list');
  if (!container) return;
  container.innerHTML = '';

  state.matches.forEach(m => {
    const card = document.createElement('div');
    card.className = 'adm-item-card';
    card.innerHTML = `
      <div class="item-info-col">
        <h4>${m.team1.logo} ${m.team1.shortName} vs ${m.team2.shortName} ${m.team2.logo} • ${m.title}</h4>
        <div class="item-meta">
          <span class="meta-chip" style="color:#38bdf8">${m.series}</span>
          <span class="meta-chip">${m.venue}</span>
          <span class="meta-chip">Mega: ${m.megaPrize || '₹10 Cr'}</span>
          <span class="meta-chip">Entry: ₹${m.entryFee || 49}</span>
        </div>
      </div>
      <span class="meta-chip" style="background:#064e3b; color:#34d399; font-weight:800">ACTIVE</span>
    `;
    container.appendChild(card);
  });
}

// Setup Wallet Controllers
function setupWalletHandlers() {
  // Quick Adjust Buttons
  document.querySelectorAll('.btn-wallet-quick').forEach(btn => {
    btn.addEventListener('click', async () => {
      audio.playClick();
      const action = btn.dataset.action;
      const val = parseInt(btn.dataset.val) || 0;
      let payload = {};

      const current = state.user?.wallet || { deposited: 500, winnings: 650, bonus: 350 };
      if (action === 'add-dep') payload = { deposited: (current.deposited || 0) + val };
      else if (action === 'add-win') payload = { winnings: (current.winnings || 0) + val };
      else if (action === 'add-bon') payload = { bonus: (current.bonus || 0) + val };
      else if (action === 'reset') payload = { deposited: 500, winnings: 650, bonus: 350 };

      const res = await apiCall('/api/admin/wallet/adjust', 'POST', payload);
      if (res && res.success) {
        if (!state.user) state.user = {};
        state.user.wallet = res.wallet;
        syncWalletInputs();
        updateTelemetryBar();
        await fetchTransactions();
        showToast('💰 User wallet balance updated!', 'success');
        audio.playCheer();
      }
    });
  });

  // Manual Balance Calibration Save Button
  document.getElementById('btn-save-wallet-custom')?.addEventListener('click', async () => {
    audio.playClick();
    const payload = {
      deposited: parseInt(document.getElementById('adm-w-dep').value) || 0,
      winnings: parseInt(document.getElementById('adm-w-win').value) || 0,
      bonus: parseInt(document.getElementById('adm-w-bon').value) || 0
    };

    const res = await apiCall('/api/admin/wallet/adjust', 'POST', payload);
    if (res && res.success) {
      if (!state.user) state.user = {};
      state.user.wallet = res.wallet;
      updateTelemetryBar();
      showToast('Custom wallet balance calibrated successfully!', 'success');
      audio.playCheer();
    }
  });
}

function syncWalletInputs() {
  if (!state.user || !state.user.wallet) return;
  const w = state.user.wallet;
  const depEl = document.getElementById('adm-w-dep');
  const winEl = document.getElementById('adm-w-win');
  const bonEl = document.getElementById('adm-w-bon');
  if (depEl) depEl.value = w.deposited || 0;
  if (winEl) winEl.value = w.winnings || 0;
  if (bonEl) bonEl.value = w.bonus || 0;
}

// Render Transaction Audit Ledger
function renderLedgerList() {
  const container = document.getElementById('adm-ledger-list');
  if (!container) return;
  container.innerHTML = '';

  if (!state.transactions || state.transactions.length === 0) {
    container.innerHTML = '<div style="color:var(--text-muted); font-size:12px; text-align:center; padding:15px">No transactions recorded yet</div>';
    return;
  }

  state.transactions.slice(0, 15).forEach(t => {
    const row = document.createElement('div');
    row.className = 'ledger-row';
    const isCredit = t.isCredit;
    row.innerHTML = `
      <div class="ledger-main">
        <span class="ledger-title">${t.title || 'Transaction'}</span>
        <span class="ledger-sub">${t.method || 'Transfer'} • Ref: ${t.utr || t.id} • ${t.date || 'Today'}</span>
      </div>
      <span class="ledger-amount ${isCredit ? 'credit' : 'debit'}">
        ${isCredit ? '+' : '-'} ₹${t.amount.toLocaleString('en-IN')}
      </span>
    `;
    container.appendChild(row);
  });
}

// Setup Live God Mode Handlers
function setupGodModeHandlers() {
  // Toggle dismissal type selector on Wicket outcome
  document.querySelectorAll('input[name="gm-outcome"]').forEach(radio => {
    radio.addEventListener('change', () => {
      audio.playClick();
      const isWicket = radio.value === 'w';
      const wtypeGroup = document.getElementById('adm-gm-wtype-group');
      if (wtypeGroup) wtypeGroup.style.display = isWicket ? 'block' : 'none';
      
      const commentInput = document.getElementById('adm-gm-comment');
      if (commentInput) {
        if (isWicket) {
          commentInput.value = 'OUT! Clean bowled! The middle stump is sent cartwheeling out of the ground!';
        } else if (radio.value === '6') {
          commentInput.value = 'MAXIMUM! Smoked into the second tier of the grandstand for a colossal SIX!';
        } else if (radio.value === '4') {
          commentInput.value = 'CRACKING SHOT! Travis Head carves it through covers with laser precision for FOUR!';
        } else if (radio.value === '0') {
          commentInput.value = 'Beaten for pace! Excellent length delivery whizzing past the outside edge.';
        } else {
          commentInput.value = 'Nudged into the gap on the on-side for a brisk single.';
        }
      }
    });
  });

  // Inject Custom Ball Form
  document.getElementById('form-adm-godmode')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    audio.init();

    const outcomeVal = document.querySelector('input[name="gm-outcome"]:checked')?.value || '4';
    const isWicket = (outcomeVal === 'w');
    const runs = isWicket ? 0 : parseInt(outcomeVal);

    const payload = {
      batsman: document.getElementById('adm-gm-bat').value.trim(),
      bowler: document.getElementById('adm-gm-bowl').value.trim(),
      runs: runs,
      isWicket: isWicket,
      wicketType: isWicket ? document.getElementById('adm-gm-wtype').value : null,
      comment: document.getElementById('adm-gm-comment').value.trim()
    };

    const res = await apiCall('/api/admin/live/custom-ball', 'POST', payload);
    if (res && res.success) {
      state.simState = res.state;
      updateScoreboardUI();
      updateTelemetryBar();
      renderCommentaryFeed();
      renderLeaderboardFeed();

      if (isWicket) {
        audio.playWicketSiren();
        showToast('⚡ WICKET INJECTED! Points updated across all leagues!', 'error');
      } else if (runs >= 4) {
        audio.playCheer();
        showToast(`⚡ BOUNDARY (${runs}) DELIVERED! Live leaderboard updated!`, 'success');
      } else {
        audio.playClick();
        showToast(`Ball delivered: ${runs} run(s)`, 'info');
      }
    }
  });

  // Step Auto Simulation
  document.getElementById('btn-gm-step-sim')?.addEventListener('click', async () => {
    audio.playClick();
    const res = await apiCall('/api/simulation/step', 'POST');
    if (res && res.success) {
      state.simState = res.state;
      updateScoreboardUI();
      updateTelemetryBar();
      renderCommentaryFeed();
      renderLeaderboardFeed();
      showToast('▶️ Simulation stepped 1 ball forward!', 'info');
    }
  });

  // Reset Match Simulation
  document.getElementById('btn-gm-reset-sim')?.addEventListener('click', async () => {
    audio.playTone(300, 'sawtooth', 0.15, 0.1);
    if (confirm('Reset match score and points back to 0.0 overs?')) {
      const res = await apiCall('/api/simulation/reset', 'POST');
      if (res && res.success) {
        state.simState = res.state;
        updateScoreboardUI();
        updateTelemetryBar();
        renderCommentaryFeed();
        renderLeaderboardFeed();
        showToast('🔄 Match reset to 0.0 overs', 'info');
      }
    }
  });
}

// Update Scoreboard UI
function updateScoreboardUI() {
  if (!state.simState || !state.simState.score) return;
  const sc = state.simState.score;
  const teamEl = document.getElementById('gm-team-name');
  const scoreEl = document.getElementById('gm-runs-wickets');
  const oversEl = document.getElementById('gm-overs-display');

  if (teamEl) teamEl.textContent = sc.team;
  if (scoreEl) scoreEl.textContent = `${sc.runs}/${sc.wickets}`;
  if (oversEl) oversEl.textContent = `${sc.overs} / 20`;
}

// Render Commentary Feed
function renderCommentaryFeed() {
  const container = document.getElementById('adm-commentary-feed');
  if (!container) return;
  container.innerHTML = '';

  const commentary = state.simState?.commentary || [];
  if (commentary.length === 0) {
    container.innerHTML = '<div style="color:var(--text-muted); font-size:12px; text-align:center; padding:12px">No live ball events yet</div>';
    return;
  }

  // Show top 8 recent balls
  commentary.slice(0, 8).forEach(c => {
    const line = document.createElement('div');
    const isW = c.isWicket;
    const is6 = c.runs === 6;
    const is4 = c.runs === 4;
    const typeClass = isW ? 'wicket' : is6 ? 'six' : is4 ? 'four' : '';

    line.className = `comm-line ${typeClass}`;
    line.innerHTML = `
      <span class="comm-ball">${c.ball || '•'}</span>
      <span class="comm-text">
        <strong>${c.bowler || 'Bowler'}</strong> to <strong>${c.batsman || 'Batsman'}</strong>: 
        ${c.comment || (isW ? 'WICKET!' : `${c.runs} runs`)}
      </span>
    `;
    container.appendChild(line);
  });
}

// Render Leaderboard Feed
function renderLeaderboardFeed() {
  const container = document.getElementById('adm-leaderboard-feed');
  if (!container) return;
  container.innerHTML = '';

  const lb = state.simState?.leaderboard || [];
  if (lb.length === 0) {
    container.innerHTML = '<div style="color:var(--text-muted); font-size:12px; text-align:center; padding:12px">No leaderboard scores available yet</div>';
    return;
  }

  lb.slice(0, 6).forEach(entry => {
    const row = document.createElement('div');
    row.className = 'lb-row';
    row.innerHTML = `
      <span class="lb-rank">#${entry.rank}</span>
      <span class="lb-name ${entry.isUser ? 'user' : ''}">
        ${entry.avatar || '🏏'} ${entry.name} ${entry.isUser ? '⭐ (You)' : ''}
      </span>
      <span class="lb-pts">${entry.points} pts</span>
    `;
    container.appendChild(row);
  });
}
