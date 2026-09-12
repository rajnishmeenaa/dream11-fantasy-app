
// ==========================================================================
// FANTASY11 SPORTS CLIENT APPLICATION (V2 - UPGRADED)
// Features: Private Contests, Multi-Sport, Web Audio Engine, Bilingual Live Sim, PWA
// ==========================================================================

// Web Audio API Synthesizer (Works 100% offline, zero-latency, no audio files needed)
class StadiumAudioEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playBatCrack() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;

    // Wood bat strike: sharp transient attack
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(850, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(140, this.ctx.currentTime + 0.08);

    filter.type = 'bandpass';
    filter.frequency.value = 1200;
    filter.Q.value = 3;

    gain.gain.setValueAtTime(0.9, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.09);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start();
    osc.stop(this.ctx.currentTime + 0.1);
  }

  playCrowdRoar() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;

    // Simulated crowd roar using filtered noise buffer
    const bufferSize = this.ctx.sampleRate * 1.5;
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (this.ctx.sampleRate * 1.2));
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(400, this.ctx.currentTime);
    filter.frequency.linearRampToValueAtTime(1200, this.ctx.currentTime + 0.4);
    filter.frequency.exponentialRampToValueAtTime(250, this.ctx.currentTime + 1.4);

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.01, this.ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.7, this.ctx.currentTime + 0.35);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1.5);

    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.ctx.destination);

    noise.start();
  }

  playTimberCrash() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;

    // Timber! Wickets bowled: resonance + tumbling bails
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(480, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(45, this.ctx.currentTime + 0.25);

    gain.gain.setValueAtTime(0.8, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.28);

    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.3);

    // Followed by crowd gasp / cheer
    setTimeout(() => this.playCrowdRoar(), 120);
  }

  playGoalHorn() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;

    // Dual-tone football foghorn
    [220, 277].forEach(freq => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.4, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.8);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.85);
    });
  }

  playWhistle() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(2600, this.ctx.currentTime);
    osc.frequency.linearRampToValueAtTime(2900, this.ctx.currentTime + 0.08);

    gain.gain.setValueAtTime(0.4, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);

    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.22);
  }

  playWinFanfare() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;

    // Major triad: C5 (523), E5 (659), G5 (784), C6 (1046)
    const notes = [523.25, 659.25, 783.99, 1046.50];
    notes.forEach((freq, idx) => {
      setTimeout(() => {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0.4, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.4);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.45);
      }, idx * 110);
    });
  }
}

const audio = new StadiumAudioEngine();

// Application Global State
const state = {
  data: null,
  user: null,
  matches: [],
  contests: [],
  selectedMatch: null,
  activeSport: 'cricket',
  activeView: 'view-home',
  
  // Audio & Language
  soundEnabled: true,
  commentaryLang: 'en', // 'en' | 'hi'

  // Team creation draft
  currentTeam: {
    players: [],
    captain: null,
    viceCaptain: null,
    roleCounts: {},
    teamCounts: {},
    creditsUsed: 0
  },
  activeRoleTab: 'WK',
  
  // Contest Lobby
  activeContestTab: 'all-contests',
  contestFilter: 'all',
  
  // User data
  userTeams: [],
  joinedContests: [],
  selectedContestForJoin: null,
  selectedTeamForJoin: null,
  
  // Private Contests
  privateContestToJoin: null,

  // Simulation
  simState: null,
  simTimer: null,
  simSpeed: 1500,
  activeLiveTab: 'commentary',

  // PWA
  deferredPrompt: null
};

// API Client
async function fetchAPI(endpoint, method = 'GET', body = null) {
  try {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(endpoint, opts);
    return await res.json();
  } catch (err) {
    console.error('API Error:', err);
    showToast('Network error, working in offline mode', 'error');
    return null;
  }
}

// Toast Notifications
function showToast(msg, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast-msg ${type}`;
  toast.innerHTML = `<span>${type === 'success' ? '✓' : '⚠️'}</span> <span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// View Navigation
function switchView(viewId) {
  document.querySelectorAll('.app-view').forEach(v => v.classList.remove('active'));
  const target = document.getElementById(viewId);
  if (target) {
    target.classList.add('active');
    state.activeView = viewId;
    document.getElementById('main-content').scrollTop = 0;
  }

  document.querySelectorAll('.app-bottom-nav .nav-item').forEach(item => {
    if (item.dataset.target === viewId) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
}

// Initialize Application
async function initApp() {
  // PWA Service Worker Registration
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').then(reg => {
      console.log('Fantasy11 ServiceWorker registered with scope:', reg.scope);
    }).catch(err => console.log('SW registration error:', err));
  }

  // Listen for PWA installation prompt
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    state.deferredPrompt = e;
    const installBtn = document.getElementById('btn-pwa-install');
    if (installBtn) installBtn.classList.remove('hidden');
  });

  const data = await fetchAPI('/api/data');
  if (data) {
    state.data = data;
    state.user = data.user;
    state.matches = data.matches;
    state.contests = data.contests;
    state.userTeams = data.userTeams || [];
    state.joinedContests = data.joinedContests || [];
    state.selectedMatch = state.matches[0];
  }

  updateUserHeader();
  renderMatches();
  renderContestLobby();
  setupEventListeners();
  setupPrivateContestControllers();
  setupPaymentControllers();
  startCountdownTimer();
}

// Update User Header Info

// Dream11 Left Sliding Profile Drawer Controls
function openDrawer() {
  const drawer = document.getElementById('side-drawer');
  const overlay = document.getElementById('drawer-overlay');
  if (drawer) drawer.classList.add('open');
  if (overlay) {
    overlay.classList.remove('hidden');
    overlay.classList.add('open');
  }
  updateDrawerUser();
}

function closeDrawer() {
  const drawer = document.getElementById('side-drawer');
  const overlay = document.getElementById('drawer-overlay');
  if (drawer) drawer.classList.remove('open');
  if (overlay) {
    overlay.classList.remove('open');
    setTimeout(() => overlay.classList.add('hidden'), 300);
  }
}

function updateDrawerUser() {
  if (!state.user) return;
  const totalBalance = (state.user.wallet.deposited || 0) + (state.user.wallet.winnings || 0) + (state.user.wallet.bonus || 0);
  const dWalletAmt = document.getElementById('drawer-wallet-amount');
  if (dWalletAmt) dWalletAmt.textContent = `₹${totalBalance.toLocaleString('en-IN')}`;
  const dWin = document.getElementById('drawer-w-winnings');
  if (dWin) dWin.textContent = `₹${(state.user.wallet.winnings || 0).toLocaleString('en-IN')}`;
  const dDep = document.getElementById('drawer-w-deposited');
  if (dDep) dDep.textContent = `₹${(state.user.wallet.deposited || 0).toLocaleString('en-IN')}`;
  const dBon = document.getElementById('drawer-w-bonus');
  if (dBon) dBon.textContent = `₹${(state.user.wallet.bonus || 0).toLocaleString('en-IN')}`;
}

function updateUserHeader() {
  updateDrawerUser();
  if (!state.user) return;
  const totalBalance = (state.user.wallet.deposited || 0) + (state.user.wallet.winnings || 0) + (state.user.wallet.bonus || 0);
  document.getElementById('header-wallet-amount').textContent = `₹${totalBalance.toLocaleString('en-IN')}`;
  document.getElementById('modal-total-balance').textContent = `₹${totalBalance.toLocaleString('en-IN')}`;
  document.getElementById('w-deposited').textContent = `₹${(state.user.wallet.deposited || 0).toLocaleString('en-IN')}`;
  document.getElementById('w-winnings').textContent = `₹${(state.user.wallet.winnings || 0).toLocaleString('en-IN')}`;
  document.getElementById('w-bonus').textContent = `₹${(state.user.wallet.bonus || 0).toLocaleString('en-IN')}`;
}

// Render Matches List on Home View (Sport filter aware)
function renderMatches(filter = 'all') {
  const container = document.getElementById('matches-container');
  if (!container) return;
  container.innerHTML = '';

  let filtered = state.matches.filter(m => {
    const sport = m.sport || 'cricket';
    return sport === state.activeSport;
  });

  if (filter === 'lineups') {
    filtered = filtered.filter(m => m.lineupsOut);
  } else if (filter === 'mega') {
    filtered = filtered.filter(m => m.entryFee >= 35);
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:40px 16px; color:var(--text-muted)">
        <div style="font-size:36px; margin-bottom:8px">🏆</div>
        <h4>No upcoming matches right now in ${state.activeSport.toUpperCase()}</h4>
        <p style="font-size:12px; margin-top:4px">Check back shortly or switch sports tab!</p>
      </div>
    `;
    document.getElementById('match-count-badge').textContent = '0 Matches';
    return;
  }

  filtered.forEach(match => {
    const card = document.createElement('div');
    card.className = 'match-card';
    card.innerHTML = `
      <div class="match-card-header">
        <span class="match-series-name">${match.series}</span>
        ${match.lineupsOut ? '<span class="lineup-badge"><span class="dot"></span> Lineups Out</span>' : ''}
      </div>
      <div class="match-card-body">
        <div class="team-col">
          <div class="team-logo-circle">${match.team1.logo}</div>
          <div class="team-meta">
            <span class="team-short">${match.team1.shortName}</span>
            <span class="team-full">${match.team1.name}</span>
          </div>
        </div>
        <div class="match-center-col">
          <span class="match-timer-pill" data-match-id="${match.id}">14m 20s</span>
          <span class="match-start-time">${match.startTime}</span>
        </div>
        <div class="team-col right">
          <div class="team-meta">
            <span class="team-short">${match.team2.shortName}</span>
            <span class="team-full">${match.team2.name}</span>
          </div>
          <div class="team-logo-circle">${match.team2.logo}</div>
        </div>
      </div>
      <div class="match-card-footer">
        <span class="mega-prize-tag">🏆 Mega ${match.megaPrize}</span>
        <span class="entry-pill">Entry ₹${match.entryFee}</span>
      </div>
    `;

    card.addEventListener('click', () => {
      selectMatch(match.id);
    });
    container.appendChild(card);
  });

  document.getElementById('match-count-badge').textContent = `${filtered.length} Matches`;
}

// Match Selection
function selectMatch(matchId) {
  const match = state.matches.find(m => m.id === matchId);
  if (!match) return;
  state.selectedMatch = match;
  state.activeSport = match.sport || 'cricket';
  renderContestLobby();
  switchView('view-contests');
}

// Render Contest Lobby for Selected Match
function renderContestLobby() {
  const match = state.selectedMatch;
  if (!match) return;

  document.getElementById('contest-match-title').textContent = `${match.team1.shortName} vs ${match.team2.shortName}`;
  document.getElementById('contest-match-timer').textContent = '14m 20s left';
  document.getElementById('team-match-timer').textContent = '14m left';

  const infoCard = document.getElementById('contest-match-card');
  infoCard.innerHTML = `
    <div class="mic-row">
      <div class="mic-team">
        <span>${match.team1.logo}</span>
        <span>${match.team1.name}</span>
      </div>
      <span style="font-size:12px; font-weight:800; color:var(--text-muted)">VS</span>
      <div class="mic-team">
        <span>${match.team2.name}</span>
        <span>${match.team2.logo}</span>
      </div>
    </div>
    <div class="mic-pitch-report">
      <span>🏟️ ${match.venue}</span> • <span>🌱 ${match.pitchReport}</span>
    </div>
  `;

  renderContestsList();
  renderMyTeamsTab();
  renderMyContestsTab();
}

// Render Contests by category
function renderContestsList() {
  const container = document.getElementById('contests-container');
  if (!container) return;
  container.innerHTML = '';

  let filtered = state.contests;
  if (state.contestFilter === 'private') {
    filtered = filtered.filter(c => c.isPrivate || c.type === 'private');
  } else if (state.contestFilter !== 'all') {
    filtered = filtered.filter(c => c.type === state.contestFilter);
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:30px 16px; color:var(--text-muted)">
        <h4>No contests found in this category</h4>
        <p style="font-size:12px; margin-top:4px">Try switching filters or create your own private contest above!</p>
      </div>
    `;
    return;
  }

  filtered.forEach(c => {
    const card = document.createElement('div');
    card.className = 'contest-card';
    const percentFilled = Math.min(100, Math.round(((c.totalSpots - c.spotsLeft) / c.totalSpots) * 100));

    card.innerHTML = `
      <div class="contest-card-top">
        <div class="c-pool-row">
          <div class="c-pool-meta">
            <span class="c-type-badge ${c.isPrivate ? 'style="background:#4f46e5;color:#fff"' : ''}">${c.badge}</span>
            ${c.code ? `<span style="font-size:10px; background:#e0e7ff; color:#3730a3; padding:1px 6px; border-radius:4px; font-weight:800; margin-left:6px">CODE: ${c.code}</span>` : ''}
            <h3>${c.totalPrize}</h3>
            <span style="font-size:11px; color:var(--text-muted)">Prize Pool</span>
          </div>
          <button class="btn-join-contest ${c.entryFee === 0 ? 'free' : ''}" data-cid="${c.id}">
            ${c.entryFee === 0 ? 'JOIN FREE' : `₹${c.entryFee}`}
          </button>
        </div>
        <div class="spots-bar-container">
          <div class="spots-progress-track">
            <div class="spots-progress-fill" style="width: ${percentFilled}%"></div>
          </div>
          <div class="spots-labels-row">
            <span style="color:#ef4444">${c.spotsLeft.toLocaleString('en-IN')} spots left</span>
            <span>${c.totalSpots.toLocaleString('en-IN')} spots</span>
          </div>
        </div>
      </div>
      <div class="contest-card-footer">
        <span class="first-prize-tag">🥇 ${c.firstPrize}</span>
        <span>👥 Max ${c.maxTeams} Teams</span>
        <span class="guaranteed-tag">${c.tag}</span>
      </div>
    `;

    card.querySelector('.contest-card-top').addEventListener('click', (e) => {
      if (e.target.tagName !== 'BUTTON') {
        openPrizeBreakupModal(c);
      }
    });

    card.querySelector('.btn-join-contest').addEventListener('click', (e) => {
      e.stopPropagation();
      openJoinContestModal(c);
    });

    container.appendChild(card);
  });
}

// Open Prize Breakup Modal
function openPrizeBreakupModal(contest) {
  document.getElementById('pb-contest-name').textContent = contest.name;
  document.getElementById('pb-total-prize').textContent = `Prize Pool: ${contest.totalPrize}`;
  document.getElementById('pb-entry-fee').textContent = `₹${contest.entryFee}`;
  document.getElementById('pb-total-spots').textContent = contest.totalSpots.toLocaleString('en-IN');
  document.getElementById('pb-winners').textContent = contest.winnersPercent || '60%';

  const table = document.getElementById('pb-table-rows');
  table.innerHTML = '';
  const breakup = contest.breakup || [
    { rank: '1st', prize: contest.firstPrize },
    { rank: '2nd - 10th', prize: '₹1 Lakh' }
  ];

  breakup.forEach(row => {
    const div = document.createElement('div');
    div.className = 'pb-row';
    div.innerHTML = `<span>Rank ${row.rank}</span><strong>${row.prize}</strong>`;
    table.appendChild(div);
  });

  document.getElementById('modal-prize-breakup').classList.remove('hidden');
}

// Open Join Contest Modal
function openJoinContestModal(contest) {
  state.selectedContestForJoin = contest;
  const matchTeams = state.userTeams.filter(t => t.matchId === state.selectedMatch.id);

  if (matchTeams.length === 0) {
    showToast('Please create a fantasy team first before joining!', 'error');
    startTeamCreation();
    return;
  }

  document.getElementById('join-contest-summary-box').innerHTML = `
    <div style="font-size:13px; font-weight:800">${contest.name}</div>
    <div style="font-size:11px; color:var(--text-muted); margin-top:2px">Prize Pool: ${contest.totalPrize} • 1st: ${contest.firstPrize}</div>
  `;

  const picker = document.getElementById('join-team-picker-list');
  picker.innerHTML = '';
  state.selectedTeamForJoin = matchTeams[0].id;

  matchTeams.forEach((team, idx) => {
    const opt = document.createElement('div');
    opt.className = `team-picker-option ${idx === 0 ? 'selected' : ''}`;
    opt.innerHTML = `
      <div>
        <strong>${team.name}</strong>
        <div style="font-size:11px; color:var(--text-muted)">C: ${team.captainName || 'C'} • VC: ${team.viceCaptainName || 'VC'}</div>
      </div>
      <input type="radio" name="join-team-choice" value="${team.id}" ${idx === 0 ? 'checked' : ''}>
    `;

    opt.addEventListener('click', () => {
      picker.querySelectorAll('.team-picker-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input').checked = true;
      state.selectedTeamForJoin = team.id;
    });

    picker.appendChild(opt);
  });

  const entryFee = contest.entryFee;
  const usableBonus = Math.min(state.user.wallet.bonus || 0, Math.floor(entryFee * 0.2));
  const finalPay = Math.max(0, entryFee - usableBonus);

  document.getElementById('pay-entry-fee').textContent = `₹${entryFee}`;
  document.getElementById('pay-bonus-deduct').textContent = `-₹${usableBonus}`;
  document.getElementById('pay-final-amount').textContent = `₹${finalPay}`;

  document.getElementById('modal-join-contest').classList.remove('hidden');
}

// Confirm Pay and Join
async function confirmPayAndJoin() {
  const contest = state.selectedContestForJoin;
  const teamId = state.selectedTeamForJoin;
  if (!contest || !teamId) return;

  const res = await fetchAPI('/api/user/contests/join', 'POST', {
    contestId: contest.id,
    teamId: teamId
  });

  if (res && res.success) {
    state.user.wallet = res.wallet;
    state.joinedContests.push(res.joined);
    updateUserHeader();
    document.getElementById('modal-join-contest').classList.add('hidden');
    audio.playWinFanfare();
    showToast(`🎉 Joined ${contest.name}! All the best Champion!`, 'success');
    
    const badge = document.getElementById('nav-joined-badge');
    if (badge) {
      badge.style.display = 'flex';
      badge.textContent = state.joinedContests.length;
    }

    renderContestsList();
    renderMyContestsTab();
  } else {
    showToast(res ? res.message : 'Failed to join contest', 'error');
  }
}

// SPORT CONFIGURATION
function getSportConfig(sport = 'cricket') {
  if (sport === 'football') {
    return {
      name: 'Football',
      squadSize: 11,
      maxPerTeam: 7,
      roles: ['GK', 'DEF', 'MID', 'FWD'],
      roleNames: { GK: 'Goalkeeper', DEF: 'Defender', MID: 'Midfielder', FWD: 'Forward' },
      roleRules: { GK: [1, 1], DEF: [3, 5], MID: [3, 5], FWD: [1, 3] },
      guideText: {
        GK: 'Pick 1 Goalkeeper (GK)',
        DEF: 'Pick 3 to 5 Defenders (DEF)',
        MID: 'Pick 3 to 5 Midfielders (MID)',
        FWD: 'Pick 1 to 3 Forwards (FWD)'
      }
    };
  } else if (sport === 'kabaddi') {
    return {
      name: 'Kabaddi',
      squadSize: 7,
      maxPerTeam: 5,
      roles: ['DEF', 'RAI', 'ALL'],
      roleNames: { DEF: 'Defenders', RAI: 'Raiders', ALL: 'All-Rounders' },
      roleRules: { DEF: [2, 4], RAI: [1, 3], ALL: [1, 2] },
      guideText: {
        DEF: 'Pick 2 to 4 Defenders (DEF)',
        RAI: 'Pick 1 to 3 Raiders (RAI)',
        ALL: 'Pick 1 to 2 All-Rounders (ALL)'
      }
    };
  } else {
    return {
      name: 'Cricket',
      squadSize: 11,
      maxPerTeam: 7,
      roles: ['WK', 'BAT', 'AR', 'BOWL'],
      roleNames: { WK: 'Wicket-Keeper', BAT: 'Batsman', AR: 'All-Rounder', BOWL: 'Bowler' },
      roleRules: { WK: [1, 8], BAT: [1, 8], AR: [1, 8], BOWL: [1, 8] },
      guideText: {
        WK: 'Pick 1 to 8 Wicket-Keepers (WK)',
        BAT: 'Pick 1 to 8 Batsmen (BAT)',
        AR: 'Pick 1 to 8 All-Rounders (AR)',
        BOWL: 'Pick 1 to 8 Bowlers (BOWL)'
      }
    };
  }
}

// Start Team Creation
function startTeamCreation() {
  const match = state.selectedMatch;
  if (!match) return;
  const cfg = getSportConfig(match.sport);

  state.currentTeam = {
    players: [],
    captain: null,
    viceCaptain: null,
    roleCounts: {},
    teamCounts: { [match.team1.shortName]: 0, [match.team2.shortName]: 0 },
    creditsUsed: 0
  };
  cfg.roles.forEach(r => state.currentTeam.roleCounts[r] = 0);

  document.getElementById('team-number-label').textContent = state.userTeams.length + 1;
  document.getElementById('badge-team1').textContent = match.team1.shortName;
  document.getElementById('badge-team2').textContent = match.team2.shortName;
  state.activeRoleTab = cfg.roles[0];

  renderPositionTabs(cfg);
  renderDotsProgress(cfg);
  updateTeamBuilderUI();
  renderPlayerRows();
  switchView('view-create-team');
}

// Render position tabs based on sport
function renderPositionTabs(cfg) {
  const bar = document.querySelector('.position-tabs-bar');
  if (!bar) return;
  bar.innerHTML = '';

  cfg.roles.forEach(role => {
    const tab = document.createElement('div');
    tab.className = `pos-tab ${role === state.activeRoleTab ? 'active' : ''}`;
    tab.dataset.role = role;
    tab.innerHTML = `
      ${role} (<span id="role-count-${role}">0</span>)
      <span class="pos-rule">Select ${cfg.roleRules[role][0]}-${cfg.roleRules[role][1]}</span>
    `;
    tab.addEventListener('click', () => {
      bar.querySelectorAll('.pos-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      state.activeRoleTab = role;
      renderPlayerRows();
    });
    bar.appendChild(tab);
  });
}

// Render dots progress based on squad size
function renderDotsProgress(cfg) {
  const container = document.getElementById('team-dots-container');
  if (!container) return;
  container.innerHTML = '';
  for (let i = 0; i < cfg.squadSize; i++) {
    const dot = document.createElement('span');
    dot.className = 'dot';
    container.appendChild(dot);
  }
}

// Update Team Builder UI Status
function updateTeamBuilderUI() {
  const team = state.currentTeam;
  const match = state.selectedMatch;
  const cfg = getSportConfig(match.sport);
  const count = team.players.length;
  const creditsLeft = (100.0 - team.creditsUsed).toFixed(1);

  document.getElementById('selected-count-text').textContent = count;
  const metaVal = document.querySelector('.team-meta-row .meta-val');
  if (metaVal) metaVal.innerHTML = `<strong id="selected-count-text">${count}</strong>/${cfg.squadSize}`;
  document.getElementById('credits-left-text').textContent = creditsLeft;
  document.getElementById('count-team1').textContent = team.teamCounts[match.team1.shortName] || 0;
  document.getElementById('count-team2').textContent = team.teamCounts[match.team2.shortName] || 0;

  cfg.roles.forEach(role => {
    const el = document.getElementById(`role-count-${role}`);
    if (el) el.textContent = team.roleCounts[role] || 0;
  });

  const dots = document.querySelectorAll('#team-dots-container .dot');
  dots.forEach((dot, idx) => {
    if (idx < count) dot.classList.add('active');
    else dot.classList.remove('active');
  });

  // Role validation checks
  let rolesValid = true;
  cfg.roles.forEach(role => {
    const [minR, maxR] = cfg.roleRules[role];
    const c = team.roleCounts[role] || 0;
    if (c < minR || c > maxR) rolesValid = false;
  });

  const nextBtn = document.getElementById('btn-proceed-to-cvc');
  const validComposition = (count === cfg.squadSize && team.creditsUsed <= 100.0 && rolesValid);
  nextBtn.disabled = !validComposition;
}

// Render Players for active role tab
function renderPlayerRows() {
  const container = document.getElementById('players-table-body');
  if (!container) return;
  container.innerHTML = '';

  const match = state.selectedMatch;
  const cfg = getSportConfig(match.sport);
  const role = state.activeRoleTab;
  const players = match.players.filter(p => p.role === role);

  document.getElementById('position-guide-text').textContent = cfg.guideText[role] || '';

  const getRoleIcon = (r) => {
    if (r === 'GK') return '🧤';
    if (r === 'DEF') return '🛡️';
    if (r === 'MID') return '👟';
    if (r === 'FWD') return '⚽';
    if (r === 'RAI') return '⚡';
    if (r === 'ALL') return '🤼';
    if (r === 'WK') return '🧤';
    if (r === 'BOWL') return '🎯';
    if (r === 'AR') return '⚡';
    return '🏏';
  };

  players.forEach(player => {
    const isSelected = state.currentTeam.players.includes(player.id);
    const row = document.createElement('div');
    row.className = `player-row ${isSelected ? 'selected' : ''}`;
    row.innerHTML = `
      <div class="player-cell-main">
        <div class="p-avatar">${getRoleIcon(player.role)}</div>
        <div class="p-meta">
          <span class="p-name">${player.name}</span>
          <div class="p-sub">
            <span class="p-team-badge">${player.team}</span>
            <span class="p-playing-dot">● ${player.isPlaying ? 'Playing' : 'Bench'}</span>
          </div>
        </div>
      </div>
      <div class="player-cell-stat">${player.points}</div>
      <div class="player-cell-stat">${player.selectedBy}</div>
      <div class="player-cell-credits">${player.credits.toFixed(1)}</div>
      <div class="player-cell-btn">
        <button class="btn-toggle-player">${isSelected ? '✓' : '+'}</button>
      </div>
    `;

    row.addEventListener('click', () => {
      togglePlayerSelection(player);
    });

    container.appendChild(row);
  });
}

// Toggle Player Selection
function togglePlayerSelection(player) {
  const team = state.currentTeam;
  const match = state.selectedMatch;
  const cfg = getSportConfig(match.sport);
  const isSelected = team.players.includes(player.id);

  if (isSelected) {
    team.players = team.players.filter(id => id !== player.id);
    team.roleCounts[player.role] -= 1;
    team.teamCounts[player.team] -= 1;
    team.creditsUsed -= player.credits;
    if (team.captain === player.id) team.captain = null;
    if (team.viceCaptain === player.id) team.viceCaptain = null;
    audio.playWhistle();
  } else {
    if (team.players.length >= cfg.squadSize) {
      showToast(`You can only select exactly ${cfg.squadSize} players!`, 'error');
      return;
    }
    if ((team.creditsUsed + player.credits) > 100.0) {
      showToast('Not enough credits left! Maximum budget is 100.0.', 'error');
      return;
    }
    if ((team.teamCounts[player.team] || 0) >= cfg.maxPerTeam) {
      showToast(`Maximum ${cfg.maxPerTeam} players allowed from ${player.team}!`, 'error');
      return;
    }
    const maxForRole = cfg.roleRules[player.role][1];
    if ((team.roleCounts[player.role] || 0) >= maxForRole) {
      showToast(`Maximum ${maxForRole} players allowed in ${player.role}!`, 'error');
      return;
    }

    team.players.push(player.id);
    team.roleCounts[player.role] = (team.roleCounts[player.role] || 0) + 1;
    team.teamCounts[player.team] = (team.teamCounts[player.team] || 0) + 1;
    team.creditsUsed += player.credits;
    audio.playBatCrack();
  }

  updateTeamBuilderUI();
  renderPlayerRows();
}

// Go to Choose C & VC View
function proceedToChooseCVC() {
  const team = state.currentTeam;
  const match = state.selectedMatch;
  const cfg = getSportConfig(match.sport);
  if (team.players.length !== cfg.squadSize) {
    showToast(`Please select all ${cfg.squadSize} players to proceed!`, 'error');
    return;
  }

  const container = document.getElementById('cvc-table-body');
  container.innerHTML = '';
  const selectedPlayers = match.players.filter(p => team.players.includes(p.id));

  selectedPlayers.forEach(p => {
    const row = document.createElement('div');
    row.className = 'cvc-row';
    const isCap = team.captain === p.id;
    const isVc = team.viceCaptain === p.id;

    row.innerHTML = `
      <div class="cvc-player-info">
        <div class="p-avatar" style="width:30px; height:30px; font-size:14px">👤</div>
        <div>
          <strong style="font-size:12px">${p.name}</strong>
          <div style="font-size:10px; color:var(--text-muted)">${p.team} • ${p.role} • ${p.points} pts</div>
        </div>
      </div>
      <div class="cvc-btn-cell">
        <button class="btn-cvc-toggle ${isCap ? 'active-c' : ''}" data-cap-id="${p.id}">
          2X
        </button>
      </div>
      <div class="cvc-btn-cell">
        <button class="btn-cvc-toggle ${isVc ? 'active-vc' : ''}" data-vc-id="${p.id}">
          1.5X
        </button>
      </div>
    `;

    row.querySelector('[data-cap-id]').addEventListener('click', (e) => {
      e.stopPropagation();
      if (team.viceCaptain === p.id) team.viceCaptain = null;
      team.captain = p.id;
      audio.playBatCrack();
      proceedToChooseCVC();
    });

    row.querySelector('[data-vc-id]').addEventListener('click', (e) => {
      e.stopPropagation();
      if (team.captain === p.id) team.captain = null;
      team.viceCaptain = p.id;
      audio.playBatCrack();
      proceedToChooseCVC();
    });

    container.appendChild(row);
  });

  const saveBtn = document.getElementById('btn-save-final-team');
  saveBtn.disabled = !(team.captain && team.viceCaptain);
  switchView('view-choose-cvc');
}

// Save User Team
async function saveFinalTeam() {
  const team = state.currentTeam;
  const match = state.selectedMatch;
  if (!team.captain || !team.viceCaptain) {
    showToast('Please choose both Captain (C) and Vice-Captain (VC)!', 'error');
    return;
  }

  const capPlayer = match.players.find(p => p.id === team.captain);
  const vcPlayer = match.players.find(p => p.id === team.viceCaptain);

  const teamData = {
    name: `Team ${state.userTeams.length + 1}`,
    matchId: match.id,
    players: team.players,
    captain: team.captain,
    viceCaptain: team.viceCaptain,
    captainName: capPlayer ? capPlayer.name : 'Captain',
    viceCaptainName: vcPlayer ? vcPlayer.name : 'Vice Captain',
    creditsUsed: team.creditsUsed
  };

  const res = await fetchAPI('/api/user/teams', 'POST', teamData);
  if (res && res.success) {
    state.userTeams.push(res.team);
    audio.playWinFanfare();
    showToast(`🎉 Team ${res.team.name} created successfully!`, 'success');
    renderContestLobby();
    switchView('view-contests');
  } else {
    showToast('Failed to save team', 'error');
  }
}

// Render 2D Multi-Sport Pitch Preview Modal
function renderPitchPreviewModal(customTeam = null) {
  const match = state.selectedMatch;
  const team = customTeam || state.currentTeam;
  const sport = match.sport || 'cricket';
  const selectedPlayers = match.players.filter(p => team.players.includes(p.id));

  document.getElementById('pitch-team-name-title').textContent = customTeam ? customTeam.name : `Team ${state.userTeams.length + 1} Preview`;
  document.getElementById('pitch-summary-subtitle').textContent = `${match.team1.shortName}: ${team.teamCounts ? (team.teamCounts[match.team1.shortName] || 0) : ''} • Credits: ${(team.creditsUsed || 0).toFixed(1)}`;

  // Sport-specific field switcher
  const fCricket = document.getElementById('pitch-field-cricket');
  const fFootball = document.getElementById('pitch-field-football');
  const fKabaddi = document.getElementById('pitch-field-kabaddi');

  if (fCricket) fCricket.classList.toggle('hidden', sport !== 'cricket');
  if (fFootball) fFootball.classList.toggle('hidden', sport !== 'football');
  if (fKabaddi) fKabaddi.classList.toggle('hidden', sport !== 'kabaddi');

  const createPitchCard = (p) => {
    const isCap = team.captain === p.id;
    const isVc = team.viceCaptain === p.id;
    const card = document.createElement('div');
    card.className = `pitch-player-card ${p.team.toLowerCase()}`;
    card.innerHTML = `
      <div class="pitch-jersey">
        👕
        ${isCap ? '<span class="pitch-badge-c">C</span>' : ''}
        ${isVc ? '<span class="pitch-badge-vc">VC</span>' : ''}
      </div>
      <div class="pitch-p-name">${p.name.split(' ').pop()}</div>
      <span class="pitch-p-credits">${p.credits} Cr</span>
    `;
    return card;
  };

  if (sport === 'football') {
    ['gk', 'def', 'mid', 'fwd'].forEach(r => {
      const el = document.getElementById(`pitch-players-${r}`);
      if (el) el.innerHTML = '';
    });
    selectedPlayers.forEach(p => {
      const el = document.getElementById(`pitch-players-${p.role.toLowerCase()}`);
      if (el) el.appendChild(createPitchCard(p));
    });
  } else if (sport === 'kabaddi') {
    ['kdef', 'kall', 'krai'].forEach(r => {
      const el = document.getElementById(`pitch-players-${r}`);
      if (el) el.innerHTML = '';
    });
    selectedPlayers.forEach(p => {
      const key = p.role === 'DEF' ? 'kdef' : (p.role === 'ALL' ? 'kall' : 'krai');
      const el = document.getElementById(`pitch-players-${key}`);
      if (el) el.appendChild(createPitchCard(p));
    });
  } else {
    // Cricket
    ['wk', 'bat', 'ar', 'bowl'].forEach(r => {
      const el = document.getElementById(`pitch-players-${r}`);
      if (el) el.innerHTML = '';
    });
    const map = { WK: 'wk', BAT: 'bat', AR: 'ar', BOWL: 'bowl' };
    selectedPlayers.forEach(p => {
      const el = document.getElementById(`pitch-players-${map[p.role]}`);
      if (el) el.appendChild(createPitchCard(p));
    });
  }

  document.getElementById('modal-pitch-preview').classList.remove('hidden');
}

// Render My Teams Tab
function renderMyTeamsTab() {
  const container = document.getElementById('my-teams-container');
  if (!container) return;
  container.innerHTML = '';
  document.getElementById('tab-my-teams').textContent = `My Teams (${state.userTeams.length})`;

  if (state.userTeams.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:30px 16px; color:var(--text-muted)">
        <div style="font-size:36px; margin-bottom:8px">🏏</div>
        <h4>No teams created yet!</h4>
        <p style="font-size:12px; margin-top:4px">Tap '+ CREATE TEAM' below to pick your champions.</p>
      </div>
    `;
    return;
  }

  state.userTeams.forEach((team, idx) => {
    const card = document.createElement('div');
    card.className = 'match-card';
    card.style.marginBottom = '10px';
    card.innerHTML = `
      <div class="match-card-header">
        <strong>${team.name}</strong>
        <span style="font-size:11px; color:var(--text-muted)">Credits: ${(team.creditsUsed || 0).toFixed(1)}/100</span>
      </div>
      <div style="padding:12px 14px; display:flex; justify-content:space-between; align-items:center">
        <div>
          <div style="font-size:12px; font-weight:700">👑 Captain: <span style="color:var(--primary)">${team.captainName || 'C'} (2X)</span></div>
          <div style="font-size:12px; font-weight:700; margin-top:3px">⭐ Vice-Captain: <span style="color:var(--gold)">${team.viceCaptainName || 'VC'} (1.5X)</span></div>
        </div>
        <button class="pitch-btn" data-team-idx="${idx}">🌱 Preview Pitch</button>
      </div>
    `;

    card.querySelector('[data-team-idx]').addEventListener('click', () => {
      renderPitchPreviewModal(team);
    });

    container.appendChild(card);
  });
}

// Render My Contests Tab
function renderMyContestsTab() {
  const container = document.getElementById('my-contests-container');
  if (!container) return;
  container.innerHTML = '';
  document.getElementById('tab-my-contests').textContent = `My Contests (${state.joinedContests.length})`;

  if (state.joinedContests.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:30px 16px; color:var(--text-muted)">
        <div style="font-size:36px; margin-bottom:8px">🏆</div>
        <h4>You haven't joined any contest yet</h4>
        <p style="font-size:12px; margin-top:4px">Join Mega or Private contests from the Contests tab!</p>
      </div>
    `;
    return;
  }

  state.joinedContests.forEach(jc => {
    const card = document.createElement('div');
    card.className = 'contest-card';
    card.style.marginBottom = '10px';
    card.innerHTML = `
      <div class="contest-card-top">
        <div class="c-pool-row">
          <div>
            <span class="c-type-badge">${jc.contest.badge}</span>
            <h3>${jc.contest.name}</h3>
            <span style="font-size:11px; color:#16a34a; font-weight:700">✓ Joined with Team: ${jc.teamId}</span>
          </div>
          <button class="btn-join-contest" style="background:#0284c7" id="btn-goto-live-sim">
            LIVE SIM ⚡
          </button>
        </div>
      </div>
    `;

    card.querySelector('#btn-goto-live-sim').addEventListener('click', () => {
      startLiveMatchSimulation();
    });

    container.appendChild(card);
  });
}

// Render My Matches View
function renderMyMatchesView() {
  const container = document.getElementById('my-matches-list');
  if (!container) return;
  container.innerHTML = '';

  const hasJoined = state.joinedContests.length > 0;
  const match = state.selectedMatch;

  if (hasJoined) {
    const card = document.createElement('div');
    card.className = 'match-card';
    card.innerHTML = `
      <div class="match-card-header">
        <span class="match-series-name">${match.series}</span>
        <span class="lineup-badge" style="background:#fee2e2; color:#b91c1c"><span class="dot" style="background:#b91c1c"></span> LIVE SIM</span>
      </div>
      <div class="match-card-body">
        <div class="team-col">
          <div class="team-logo-circle">${match.team1.logo}</div>
          <span class="team-short">${match.team1.shortName}</span>
        </div>
        <div class="match-center-col">
          <span class="match-timer-pill" style="background:#fee2e2; color:#b91c1c">LIVE NOW</span>
          <span class="match-start-time">${state.joinedContests.length} Contests Joined</span>
        </div>
        <div class="team-col right">
          <span class="team-short">${match.team2.shortName}</span>
          <div class="team-logo-circle">${match.team2.logo}</div>
        </div>
      </div>
      <div class="match-card-footer" style="background:#f8fafc">
        <span style="font-size:12px; font-weight:700; color:#15803d">🏆 Fantasy Winnings in Play</span>
        <button class="entry-pill" style="background:#0284c7; border:none; cursor:pointer" id="btn-track-live">Track Live ⚡</button>
      </div>
    `;

    card.querySelector('#btn-track-live').addEventListener('click', () => {
      startLiveMatchSimulation();
    });

    container.appendChild(card);
  } else {
    container.innerHTML = `
      <div style="text-align:center; padding:40px 16px; color:var(--text-muted)">
        <div style="font-size:48px; margin-bottom:12px">🏏</div>
        <h4>No Active Matches</h4>
        <p style="font-size:12px; margin-top:4px">Join upcoming contests to track your live fantasy score here!</p>
        <button class="btn-primary" style="margin-top:16px; max-width:200px" id="btn-explore-matches">Explore Matches</button>
      </div>
    `;
    container.querySelector('#btn-explore-matches')?.addEventListener('click', () => {
      switchView('view-home');
    });
  }
}

// Live Match Simulation
async function startLiveMatchSimulation() {
  switchView('view-live-match');
  await refreshSimState();
}

async function refreshSimState() {
  const res = await fetchAPI('/api/simulation/state');
  if (res) {
    state.simState = res;
    updateLiveSimUI();
  }
}

// Update Live Simulation Screen (Bilingual + Audio triggered)
function updateLiveSimUI() {
  const sim = state.simState;
  if (!sim) return;

  // Scoreboard
  document.getElementById('live-aus-score').textContent = `${sim.score.runs}/${sim.score.wickets}`;
  document.getElementById('live-aus-overs').textContent = `(${sim.score.overs} ov)`;

  // Commentary Feed
  const feed = document.getElementById('live-commentary-feed');
  feed.innerHTML = '';

  if (sim.commentary.length === 0) {
    feed.innerHTML = `<div class="feed-empty-state">Click <strong>"▶ START SIMULATION"</strong> to bowl the first delivery!</div>`;
  } else {
    sim.commentary.forEach(ev => {
      const item = document.createElement('div');
      item.className = 'commentary-item';
      let badgeClass = 'single';
      let badgeText = `${ev.runs}`;
      if (ev.isWicket) {
        badgeClass = 'wicket';
        badgeText = 'W';
      } else if (ev.runs === 6) {
        badgeClass = 'six';
        badgeText = '6';
      } else if (ev.runs === 4) {
        badgeClass = 'four';
        badgeText = '4';
      } else if (ev.runs === 0) {
        badgeClass = 'dot';
        badgeText = '•';
      }

      // Bilingual text
      const commentaryText = state.commentaryLang === 'hi' ? (ev.commentHindi || ev.comment) : ev.comment;

      item.innerHTML = `
        <div class="comm-ball-badge ${badgeClass}">${badgeText}</div>
        <div class="comm-text-content">
          <div class="comm-meta">Over ${ev.ball} • ${ev.bowler} to ${ev.batsman}</div>
          <div class="comm-desc">${commentaryText}</div>
        </div>
      `;
      feed.appendChild(item);
    });
  }

  updateLiveLeaderboardUI(sim);
}

// Update Live Leaderboard UI
function updateLiveLeaderboardUI(sim) {
  const lbContainer = document.getElementById('live-leaderboard-feed');
  lbContainer.innerHTML = '';

  let userEntry = sim.leaderboard.find(e => e.isUser);
  if (!userEntry && state.userTeams.length > 0) {
    userEntry = { points: 0, rank: 1 };
  }

  if (userEntry) {
    document.getElementById('user-live-pts').innerHTML = `${userEntry.points} <span class="pts-unit">PTS</span>`;
    document.getElementById('user-live-rank').textContent = `#${userEntry.rank || 1}`;
  }

  sim.leaderboard.forEach(entry => {
    const row = document.createElement('div');
    row.className = `lb-row ${entry.isUser ? 'user-row' : ''}`;
    row.innerHTML = `
      <div class="lb-left">
        <span class="lb-rank">#${entry.rank}</span>
        <span style="font-size:18px">${entry.avatar || '🏏'}</span>
        <div>
          <strong>${entry.name}</strong>
          ${entry.captain ? `<div style="font-size:10px; color:var(--text-muted)">C: ${entry.captain} • VC: ${entry.viceCaptain}</div>` : ''}
        </div>
      </div>
      <div class="lb-pts">${entry.points} pts</div>
    `;
    lbContainer.appendChild(row);
  });

  // Render player stats tab
  const statsContainer = document.getElementById('live-player-points-feed');
  statsContainer.innerHTML = '';
  const match = state.selectedMatch;
  match.players.forEach(p => {
    const pts = sim.playerLivePoints[p.id] || { total: 0, runs: 0, wickets: 0, catches: 0 };
    const pRow = document.createElement('div');
    pRow.className = 'lb-row';
    pRow.innerHTML = `
      <div class="lb-left">
        <span>${p.team === 'IND' ? '🇮🇳' : '🇦🇺'}</span>
        <div>
          <strong>${p.name} (${p.role})</strong>
          <div style="font-size:10px; color:var(--text-muted)">Runs: ${pts.runs} • Wickets: ${pts.wickets} • Catches: ${pts.catches}</div>
        </div>
      </div>
      <div class="lb-pts" style="color:var(--primary)">${pts.total} pts</div>
    `;
    statsContainer.appendChild(pRow);
  });
}

// Trigger ball sound based on event
function playBallSound(event) {
  if (!event) return;
  if (event.isWicket) {
    audio.playTimberCrash();
  } else if (event.runs === 6) {
    audio.playBatCrack();
    setTimeout(() => audio.playCrowdRoar(), 100);
  } else if (event.runs === 4) {
    audio.playBatCrack();
    setTimeout(() => audio.playCrowdRoar(), 150);
  } else if (event.runs > 0) {
    audio.playBatCrack();
  } else {
    audio.playWhistle();
  }
}

// Toggle Live Simulation Play/Pause
function toggleSimPlay() {
  audio.init();
  const btn = document.getElementById('btn-sim-play-pause');
  if (state.simTimer) {
    clearInterval(state.simTimer);
    state.simTimer = null;
    btn.classList.remove('running');
    btn.textContent = '▶ RESUME SIMULATION';
  } else {
    btn.classList.add('running');
    btn.textContent = '⏸ PAUSE SIMULATION';
    state.simTimer = setInterval(async () => {
      const res = await fetchAPI('/api/simulation/step', 'POST');
      if (res && res.success) {
        state.simState = res.state;
        const latestEv = res.state.commentary[0];
        playBallSound(latestEv);
        updateLiveSimUI();
        if (!res.hasMore) {
          clearInterval(state.simTimer);
          state.simTimer = null;
          btn.classList.remove('running');
          btn.textContent = 'MATCH COMPLETED 🏁';
          audio.playWinFanfare();
          showToast('🏆 Match Finished! Check final rankings on leaderboard!', 'success');
        }
      }
    }, state.simSpeed);
  }
}

// Reset Match Simulation
async function resetSimMatch() {
  if (state.simTimer) {
    clearInterval(state.simTimer);
    state.simTimer = null;
  }
  const btn = document.getElementById('btn-sim-play-pause');
  btn.classList.remove('running');
  btn.textContent = '▶ START SIMULATION';

  const res = await fetchAPI('/api/simulation/reset', 'POST');
  if (res && res.success) {
    state.simState = res.state;
    updateLiveSimUI();
    showToast('Match simulation reset to ball 0.', 'success');
  }
}

// =========================================================================
// PRIVATE CONTEST CONTROLLERS (Feature 2)
// =========================================================================
function setupPrivateContestControllers() {
  // Join by code from Lobby banner
  document.getElementById('btn-submit-code-join')?.addEventListener('click', async () => {
    const code = document.getElementById('input-invite-code').value.trim().toUpperCase();
    if (!code) {
      showToast('Please enter a 6-digit invite code (e.g. F11-882)', 'error');
      return;
    }
    openJoinPrivateModal(code);
  });

  // Open Create Private Contest Modal
  document.getElementById('btn-open-create-private')?.addEventListener('click', () => {
    openCreatePrivateModal();
  });

  // Close Modals
  document.getElementById('btn-close-create-private')?.addEventListener('click', () => {
    document.getElementById('modal-create-private-contest').classList.add('hidden');
  });
  document.getElementById('btn-close-join-private')?.addEventListener('click', () => {
    document.getElementById('modal-join-private').classList.add('hidden');
  });
  document.getElementById('btn-done-share')?.addEventListener('click', () => {
    document.getElementById('modal-private-code-share').classList.add('hidden');
  });

  // Copy Code
  document.getElementById('btn-copy-share-code')?.addEventListener('click', () => {
    const code = document.getElementById('share-modal-code').textContent;
    navigator.clipboard?.writeText(code);
    showToast(`📋 Code '${code}' copied! Share with friends!`, 'success');
  });

  // WhatsApp Share
  document.getElementById('btn-share-whatsapp')?.addEventListener('click', () => {
    const code = document.getElementById('share-modal-code').textContent;
    const text = `Hey! Join my Fantasy11 Private Fantasy League! Use Invite Code: *${code}* to join the battle! 🏆🏏`;
    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
  });

  // Dynamic Prize Calculation in Create Form
  const calcPrivatePrize = () => {
    const spots = parseInt(document.getElementById('pc-spots').value) || 10;
    const fee = parseInt(document.getElementById('pc-fee').value) || 50;
    const total = spots * fee;
    const first = spots > 2 ? Math.floor(total * 0.6) : Math.floor(total * 0.9);
    document.getElementById('pc-calc-total').textContent = `₹${total.toLocaleString('en-IN')}`;
    document.getElementById('pc-calc-1st').textContent = `₹${first.toLocaleString('en-IN')}`;
  };
  document.getElementById('pc-spots')?.addEventListener('change', calcPrivatePrize);
  document.getElementById('pc-fee')?.addEventListener('input', calcPrivatePrize);

  // Submit Create Private Contest Form
  document.getElementById('form-create-private-contest')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const matchTeams = state.userTeams.filter(t => t.matchId === state.selectedMatch.id);
    if (matchTeams.length === 0) {
      showToast('Please create a fantasy team first!', 'error');
      startTeamCreation();
      return;
    }

    const selectedTeamRadio = document.querySelector('input[name="pc-team-choice"]:checked');
    const teamId = selectedTeamRadio ? selectedTeamRadio.value : matchTeams[0].id;
    const payload = {
      name: document.getElementById('pc-name').value,
      totalSpots: parseInt(document.getElementById('pc-spots').value),
      entryFee: parseInt(document.getElementById('pc-fee').value),
      matchId: state.selectedMatch.id,
      teamId: teamId
    };

    const res = await fetchAPI('/api/contests/private/create', 'POST', payload);
    if (res && res.success) {
      state.user.wallet = res.wallet;
      updateUserHeader();
      state.contests.unshift(res.contest);
      state.joinedContests.push({
        id: `JC_PRIV_${res.code}`,
        contestId: res.contest.id,
        contest: res.contest,
        teamId: teamId,
        entryFeePaid: payload.entryFee,
        joinedAt: 'Just now'
      });

      document.getElementById('modal-create-private-contest').classList.add('hidden');
      document.getElementById('share-modal-code').textContent = res.code;
      document.getElementById('modal-private-code-share').classList.remove('hidden');

      audio.playWinFanfare();
      renderContestsList();
      renderMyContestsTab();
      showToast(`🏆 Private League '${payload.name}' Created! Code: ${res.code}`, 'success');
    } else {
      showToast(res ? res.message : 'Failed to create contest', 'error');
    }
  });

  // Confirm Join Private Contest
  document.getElementById('btn-confirm-join-private')?.addEventListener('click', async () => {
    if (!state.privateContestToJoin) return;
    const selectedTeamRadio = document.querySelector('input[name="jp-team-choice"]:checked');
    if (!selectedTeamRadio) {
      showToast('Please select a team to join with', 'error');
      return;
    }

    const res = await fetchAPI('/api/contests/private/join', 'POST', {
      code: state.privateContestToJoin.code,
      teamId: selectedTeamRadio.value,
      userName: state.user.name
    });

    if (res && res.success) {
      state.user.wallet = res.wallet;
      updateUserHeader();
      state.joinedContests.push({
        id: `JC_PRIV_${state.privateContestToJoin.code}`,
        contestId: state.privateContestToJoin.id,
        contest: res.contest,
        teamId: selectedTeamRadio.value,
        entryFeePaid: state.privateContestToJoin.entryFee,
        joinedAt: 'Just now'
      });

      document.getElementById('modal-join-private').classList.add('hidden');
      audio.playWinFanfare();
      showToast(`🎉 Joined Private Contest '${res.contest.name}'!`, 'success');
      renderContestsList();
      renderMyContestsTab();
    } else {
      showToast(res ? res.message : 'Failed to join private contest', 'error');
    }
  });
}

function openCreatePrivateModal() {
  const matchTeams = state.userTeams.filter(t => t.matchId === state.selectedMatch.id);
  if (matchTeams.length === 0) {
    showToast('Please create a fantasy team first!', 'error');
    startTeamCreation();
    return;
  }

  const picker = document.getElementById('pc-team-picker');
  picker.innerHTML = '';
  matchTeams.forEach((team, idx) => {
    const opt = document.createElement('div');
    opt.className = `team-picker-option ${idx === 0 ? 'selected' : ''}`;
    opt.innerHTML = `
      <div>
        <strong>${team.name}</strong>
        <div style="font-size:11px; color:var(--text-muted)">C: ${team.captainName || 'C'} • VC: ${team.viceCaptainName || 'VC'}</div>
      </div>
      <input type="radio" name="pc-team-choice" value="${team.id}" ${idx === 0 ? 'checked' : ''}>
    `;
    opt.addEventListener('click', () => {
      picker.querySelectorAll('.team-picker-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input').checked = true;
    });
    picker.appendChild(opt);
  });

  document.getElementById('modal-create-private-contest').classList.remove('hidden');
}

async function openJoinPrivateModal(code) {
  const res = await fetchAPI(`/api/contests/private/${code}`);
  if (!res || !res.success) {
    showToast(`No private contest found with code '${code}'!`, 'error');
    return;
  }

  const contest = res.contest;
  state.privateContestToJoin = contest;

  const matchTeams = state.userTeams.filter(t => t.matchId === contest.matchId);
  if (matchTeams.length === 0) {
    showToast('Please create a fantasy team first!', 'error');
    startTeamCreation();
    return;
  }

  document.getElementById('join-private-details-box').innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center">
      <strong style="font-size:14px">${contest.name}</strong>
      <span style="font-size:10px; background:#e0e7ff; color:#3730a3; padding:2px 8px; border-radius:4px; font-weight:800">${contest.code}</span>
    </div>
    <div style="font-size:11px; color:var(--text-muted); margin-top:4px">
      Host: ${contest.hostName} • Total Prize: ${contest.totalPrize} • Spots Left: ${contest.spotsLeft}/${contest.totalSpots}
    </div>
  `;

  const picker = document.getElementById('join-private-team-picker');
  picker.innerHTML = '';
  matchTeams.forEach((team, idx) => {
    const opt = document.createElement('div');
    opt.className = `team-picker-option ${idx === 0 ? 'selected' : ''}`;
    opt.innerHTML = `
      <div>
        <strong>${team.name}</strong>
        <div style="font-size:11px; color:var(--text-muted)">C: ${team.captainName || 'C'} • VC: ${team.viceCaptainName || 'VC'}</div>
      </div>
      <input type="radio" name="jp-team-choice" value="${team.id}" ${idx === 0 ? 'checked' : ''}>
    `;
    opt.addEventListener('click', () => {
      picker.querySelectorAll('.team-picker-option').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input').checked = true;
    });
    picker.appendChild(opt);
  });

  document.getElementById('jp-entry-fee').textContent = `₹${contest.entryFee}`;
  document.getElementById('jp-final-pay').textContent = `₹${contest.entryFee}`;
  document.getElementById('modal-join-private').classList.remove('hidden');
}

// =========================================================================
// EVENT LISTENERS & NAVIGATION
// =========================================================================
function setupEventListeners() {
  // Navigation
  document.getElementById('nav-logo-home')?.addEventListener('click', () => switchView('view-home'));
  document.getElementById('btn-menu')?.addEventListener('click', openDrawer);
  document.getElementById('btn-back-to-home')?.addEventListener('click', () => switchView('view-home'));
  document.getElementById('btn-back-to-contests')?.addEventListener('click', () => switchView('view-contests'));
  document.getElementById('btn-back-to-team-create')?.addEventListener('click', () => switchView('view-create-team'));
  document.getElementById('btn-back-from-live')?.addEventListener('click', () => switchView('view-my-matches'));

  // Dream11 Left Sliding Profile Drawer Listeners
  document.getElementById('btn-close-drawer')?.addEventListener('click', closeDrawer);
  document.getElementById('drawer-overlay')?.addEventListener('click', closeDrawer);

  document.getElementById('d-menu-matches')?.addEventListener('click', () => {
    closeDrawer();
    renderMyMatchesView();
    switchView('view-my-matches');
  });

  document.getElementById('d-menu-rewards')?.addEventListener('click', () => {
    closeDrawer();
    switchView('view-rewards');
  });

  document.getElementById('d-menu-chat')?.addEventListener('click', () => {
    closeDrawer();
    switchView('view-chat-groups');
  });

  document.getElementById('d-menu-winners')?.addEventListener('click', () => {
    closeDrawer();
    switchView('view-winners');
  });

  document.getElementById('d-menu-invite')?.addEventListener('click', () => {
    closeDrawer();
    const shareModal = document.getElementById('modal-private-code-share');
    if (shareModal) {
      const codeSpan = document.getElementById('share-modal-code');
      if (codeSpan) codeSpan.textContent = 'DREAM11WIN';
      shareModal.classList.remove('hidden');
    } else {
      showToast('Invite Friends: Share code DREAM11WIN & earn ₹500 cash bonus!', 'success');
    }
  });

  document.getElementById('d-menu-champions')?.addEventListener('click', () => {
    closeDrawer();
    showToast('👑 Champions Club: VIP Level 45 Pro status active! 0% platform fee.', 'success');
  });

  document.getElementById('d-menu-points')?.addEventListener('click', () => {
    closeDrawer();
    switchView('view-rewards');
    setTimeout(() => {
      document.querySelector('.points-system-section')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  });

  document.getElementById('d-menu-fairplay')?.addEventListener('click', () => {
    closeDrawer();
    showToast('🛡️ 100% Fair Play: Certified by Supreme Court of India as Game of Skill', 'success');
  });

  document.getElementById('d-menu-settings')?.addEventListener('click', () => {
    closeDrawer();
    showToast('⚙️ Settings: Stadium Crowd Audio & Lineup Push Alerts are ON', 'success');
  });

  document.getElementById('d-menu-help')?.addEventListener('click', () => {
    closeDrawer();
    showToast('🎧 24x7 Help Desk: Connecting you to official Dream11 support...', 'success');
  });

  document.getElementById('btn-drawer-add-cash')?.addEventListener('click', () => {
    closeDrawer();
    document.getElementById('modal-wallet')?.classList.remove('hidden');
    document.querySelector('.w-nav-tab[data-wtab="deposit"]')?.click();
  });

  document.getElementById('btn-drawer-withdraw')?.addEventListener('click', () => {
    closeDrawer();
    document.getElementById('modal-wallet')?.classList.remove('hidden');
    document.querySelector('.w-nav-tab[data-wtab="withdraw"]')?.click();
  });

  // Header Bell & Help
  document.getElementById('btn-header-bell')?.addEventListener('click', () => {
    showToast('🔔 Lineups Out for MI vs CSK! Playing XI announced with toss update.', 'success');
  });

  document.getElementById('btn-header-help')?.addEventListener('click', () => {
    showToast('🎧 24x7 Dream11 Live Chat Support is online.', 'success');
  });

  // Home Banner Join
  document.getElementById('btn-home-banner-join')?.addEventListener('click', () => {
    if (state.matches && state.matches.length > 0) {
      selectMatch(state.matches[0].id);
    }
  });

  // Chat & Groups View Listeners
  document.getElementById('btn-chat-join-code')?.addEventListener('click', () => {
    const code = document.getElementById('input-chat-invite-code')?.value.trim();
    if (!code) {
      showToast('Please enter an invite code (e.g. F11-MI-CSK)', 'error');
      return;
    }
    showToast(`Successfully joined private contest with code ${code}!`, 'success');
    const inp = document.getElementById('input-chat-invite-code');
    if (inp) inp.value = '';
    renderMyMatchesView();
    switchView('view-my-matches');
  });

  document.getElementById('btn-chat-create-private')?.addEventListener('click', () => {
    document.getElementById('modal-create-private-contest')?.classList.remove('hidden');
  });

  // Live Fan Chat Sender
  const sendChatMsg = () => {
    const input = document.getElementById('input-chat-send');
    const container = document.getElementById('chat-messages-container');
    if (!input || !container) return;
    const txt = input.value.trim();
    if (!txt) return;

    const msgEl = document.createElement('div');
    msgEl.className = 'chat-msg user-msg';
    msgEl.innerHTML = `
      <span class="chat-user">You:</span>
      <span class="chat-bubble">${txt}</span>
    `;
    container.appendChild(msgEl);
    input.value = '';
    container.scrollTop = container.scrollHeight;

    setTimeout(() => {
      const respEl = document.createElement('div');
      respEl.className = 'chat-msg';
      const answers = [
        "Boom! 🔥 Great fantasy prediction!",
        "Agreed, captain pick is crucial today! 🏏",
        "Lineups just confirmed bowling first, bowlers get extra swing!",
        "Let's win the Mega Contest! 🏆"
      ];
      const randomAns = answers[Math.floor(Math.random() * answers.length)];
      respEl.innerHTML = `
        <span class="chat-user">@expert_kunal:</span>
        <span class="chat-bubble">${randomAns}</span>
      `;
      container.appendChild(respEl);
      container.scrollTop = container.scrollHeight;
    }, 1200);
  };

  document.getElementById('btn-chat-send')?.addEventListener('click', sendChatMsg);
  document.getElementById('input-chat-send')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendChatMsg();
  });


  // Bottom Nav items
  document.querySelectorAll('.app-bottom-nav .nav-item').forEach(item => {
    item.addEventListener('click', () => {
      const target = item.dataset.target;
      if (target === 'view-my-matches') renderMyMatchesView();
      switchView(target);
    });
  });

  // Sports Switcher (Multi-sport expansion!)
  document.querySelectorAll('.sports-nav .sport-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      audio.playWhistle();
      document.querySelectorAll('.sports-nav .sport-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const sport = tab.dataset.sport;
      state.activeSport = sport;

      const firstSportMatch = state.matches.find(m => (m.sport || 'cricket') === sport);
      if (firstSportMatch) {
        state.selectedMatch = firstSportMatch;
      }
      renderMatches();
      showToast(`Switched to ${tab.querySelector('.sport-name').textContent}!`, 'success');
    });
  });

  // Quick Filters
  document.querySelectorAll('.quick-filters .filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.quick-filters .filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      renderMatches(chip.dataset.filter);
    });
  });

  // Contest Lobby Sub-tabs
  document.querySelectorAll('.sub-tabs-bar .sub-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const parent = tab.parentElement;
      parent.querySelectorAll('.sub-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      if (tab.dataset.subtab) {
        const sub = tab.dataset.subtab;
        document.getElementById('contests-container').classList.toggle('hidden', sub !== 'all-contests');
        document.getElementById('contest-category-bar').classList.toggle('hidden', sub !== 'all-contests');
        document.getElementById('my-contests-container').classList.toggle('hidden', sub !== 'my-contests');
        document.getElementById('my-teams-container').classList.toggle('hidden', sub !== 'my-teams');
      } else if (tab.dataset.mystat) {
        renderMyMatchesView();
      } else if (tab.dataset.livesub) {
        const lsub = tab.dataset.livesub;
        document.getElementById('live-commentary-feed').classList.toggle('hidden', lsub !== 'commentary');
        document.getElementById('live-leaderboard-feed').classList.toggle('hidden', lsub !== 'leaderboard');
        document.getElementById('live-player-points-feed').classList.toggle('hidden', lsub !== 'player-stats');
      }
    });
  });

  // Contest Category Pills
  document.querySelectorAll('.contest-type-pills .type-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      document.querySelectorAll('.contest-type-pills .type-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      state.contestFilter = pill.dataset.type;
      renderContestsList();
    });
  });

  // Team Builder: Start Team Create
  document.getElementById('btn-start-team-create')?.addEventListener('click', startTeamCreation);
  document.getElementById('btn-proceed-to-cvc')?.addEventListener('click', proceedToChooseCVC);
  document.getElementById('btn-save-final-team')?.addEventListener('click', saveFinalTeam);

  // Pitch Previews
  document.getElementById('btn-quick-preview-pitch')?.addEventListener('click', () => renderPitchPreviewModal());
  document.getElementById('btn-view-pitch-from-builder')?.addEventListener('click', () => renderPitchPreviewModal());
  document.getElementById('btn-pitch-preview-from-cvc')?.addEventListener('click', () => renderPitchPreviewModal());
  document.getElementById('btn-pitch-from-cvc-bottom')?.addEventListener('click', () => renderPitchPreviewModal());
  document.getElementById('btn-close-pitch')?.addEventListener('click', () => document.getElementById('modal-pitch-preview').classList.add('hidden'));
  document.getElementById('btn-edit-from-pitch')?.addEventListener('click', () => {
    document.getElementById('modal-pitch-preview').classList.add('hidden');
    switchView('view-create-team');
  });

  // Modals Close buttons
  document.getElementById('btn-close-breakup')?.addEventListener('click', () => document.getElementById('modal-prize-breakup').classList.add('hidden'));
  document.getElementById('btn-close-join')?.addEventListener('click', () => document.getElementById('modal-join-contest').classList.add('hidden'));
  document.getElementById('btn-close-wallet')?.addEventListener('click', () => document.getElementById('modal-wallet').classList.add('hidden'));
  document.getElementById('btn-confirm-pay-join')?.addEventListener('click', confirmPayAndJoin);

  // Wallet Modal Open
  document.getElementById('btn-open-wallet')?.addEventListener('click', () => document.getElementById('modal-wallet').classList.remove('hidden'));
  document.getElementById('menu-item-wallet')?.addEventListener('click', () => document.getElementById('modal-wallet').classList.remove('hidden'));
  document.getElementById('menu-item-rules')?.addEventListener('click', () => switchView('view-rewards'));
  document.getElementById('btn-open-points-system')?.addEventListener('click', () => switchView('view-rewards'));

  // Quick Add Cash
  let selectedAddAmt = 100;
  document.querySelectorAll('.quick-amounts-bar .btn-amt').forEach(b => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.quick-amounts-bar .btn-amt').forEach(el => el.classList.remove('active'));
      b.classList.add('active');
      selectedAddAmt = parseInt(b.dataset.amt);
      document.getElementById('btn-submit-add-cash').textContent = `ADD ₹${selectedAddAmt} TO WALLET`;
    });
  });

  document.getElementById('btn-submit-add-cash')?.addEventListener('click', async () => {
    const res = await fetchAPI('/api/user/wallet/add', 'POST', { amount: selectedAddAmt });
    if (res && res.success) {
      state.user.wallet = res.wallet;
      updateUserHeader();
      audio.playWinFanfare();
      showToast(`💰 ₹${selectedAddAmt} added successfully to your wallet!`, 'success');
      document.getElementById('modal-wallet').classList.add('hidden');
    }
  });

  // Daily Bonus Claim
  document.getElementById('btn-claim-daily-bonus')?.addEventListener('click', async () => {
    const res = await fetchAPI('/api/user/wallet/add', 'POST', { amount: 50 });
    if (res && res.success) {
      state.user.wallet = res.wallet;
      updateUserHeader();
      audio.playWinFanfare();
      showToast('🎁 Daily Bonus Claimed! ₹50 added to your Cash Bonus!', 'success');
    }
  });

  // Simulation Controls
  document.getElementById('btn-sim-play-pause')?.addEventListener('click', toggleSimPlay);
  document.getElementById('btn-sim-next-ball')?.addEventListener('click', async () => {
    audio.init();
    const res = await fetchAPI('/api/simulation/step', 'POST');
    if (res && res.success) {
      state.simState = res.state;
      const ev = res.state.commentary[0];
      playBallSound(ev);
      updateLiveSimUI();
    }
  });
  document.getElementById('btn-sim-reset')?.addEventListener('click', resetSimMatch);

  // Speed chips
  document.querySelectorAll('.speed-selector .speed-chip').forEach(sc => {
    sc.addEventListener('click', () => {
      document.querySelectorAll('.speed-selector .speed-chip').forEach(c => c.classList.remove('active'));
      sc.classList.add('active');
      state.simSpeed = parseInt(sc.dataset.speed);
      if (state.simTimer) {
        clearInterval(state.simTimer);
        state.simTimer = null;
        toggleSimPlay();
      }
    });
  });

  // Audio Toggle Button
  document.getElementById('btn-toggle-sound')?.addEventListener('click', () => {
    state.soundEnabled = !state.soundEnabled;
    audio.enabled = state.soundEnabled;
    const btn = document.getElementById('btn-toggle-sound');
    btn.classList.toggle('active', state.soundEnabled);
    document.getElementById('sound-icon').textContent = state.soundEnabled ? '🔊' : '🔇';
    document.getElementById('sound-text').textContent = state.soundEnabled ? 'Sound ON' : 'Sound OFF';
    showToast(state.soundEnabled ? '🔊 Stadium sound effects ON' : '🔇 Sound effects muted', 'success');
  });

  // Language Toggle Button (English <-> Hindi)
  document.getElementById('btn-toggle-lang')?.addEventListener('click', () => {
    state.commentaryLang = (state.commentaryLang === 'en') ? 'hi' : 'en';
    const isHi = state.commentaryLang === 'hi';
    document.getElementById('lang-text').textContent = isHi ? 'Commentary: हिंदी' : 'Commentary: English';
    showToast(isHi ? '🌐 कमेंट्री हिंदी में सेट की गई!' : '🌐 Commentary switched to English!', 'success');
    if (state.simState) updateLiveSimUI();
  });

  // PWA Install Button
  document.getElementById('btn-pwa-install')?.addEventListener('click', async () => {
    if (state.deferredPrompt) {
      state.deferredPrompt.prompt();
      const { outcome } = await state.deferredPrompt.userChoice;
      if (outcome === 'accepted') {
        showToast('📱 Fantasy11 installed to home screen!', 'success');
      }
      state.deferredPrompt = null;
      document.getElementById('btn-pwa-install').classList.add('hidden');
    } else {
      showToast('📱 Add to Home Screen from your browser menu!', 'success');
    }
  });
}

// Live Countdown Timer
function startCountdownTimer() {
  let seconds = 860;
  setInterval(() => {
    seconds--;
    if (seconds < 0) seconds = 860;
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    const txt = `${m}m ${s < 10 ? '0' : ''}${s}s`;
    document.querySelectorAll('.match-timer-pill, #contest-match-timer').forEach(el => {
      el.textContent = `${txt} left`;
    });
  }, 1000);
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);

let otpCountdownTimer = null;

function triggerNewOTPGeneration() {
  // Generate random 6-digit OTP
  state.currentGeneratedOTP = String(Math.floor(100000 + Math.random() * 900000));

  // Clear 6 boxes
  const boxes = document.querySelectorAll('.otp-six-boxes-wrapper .otp-box');
  boxes.forEach(b => {
    b.value = '';
    b.classList.remove('filled');
  });
  if (boxes[0]) boxes[0].focus();

  // Show Simulated SMS Banner
  const smsBanner = document.getElementById('sms-push-banner');
  const smsCodeDisplay = document.getElementById('sms-otp-display');
  if (smsCodeDisplay) smsCodeDisplay.textContent = state.currentGeneratedOTP;
  if (smsBanner) {
    smsBanner.classList.remove('hidden');
    audio.playWhistle();
    // Auto-hide SMS banner after 8 seconds
    setTimeout(() => {
      smsBanner.classList.add('hidden');
    }, 8000);
  }

  // Start 60-second countdown
  let seconds = 59;
  const statusEl = document.getElementById('otp-timer-status');
  const timerSec = document.getElementById('otp-timer-seconds');
  const resendBtn = document.getElementById('btn-resend-otp');

  if (resendBtn) resendBtn.classList.add('hidden');
  if (statusEl) statusEl.classList.remove('hidden');

  if (otpCountdownTimer) clearInterval(otpCountdownTimer);

  otpCountdownTimer = setInterval(() => {
    seconds--;
    if (timerSec) timerSec.textContent = `00:${seconds < 10 ? '0' : ''}${seconds}`;
    if (seconds <= 0) {
      clearInterval(otpCountdownTimer);
      if (statusEl) statusEl.classList.add('hidden');
      if (resendBtn) resendBtn.classList.remove('hidden');
    }
  }, 1000);
}
