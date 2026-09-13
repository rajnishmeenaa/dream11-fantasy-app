/**
 * Fantasy Sports Engine & Team Builder
 */
const FantasyManager = {
  matches: [
    {
      id: "m-ipl-01",
      tournament: "TATA IPL 2026",
      team1: { name: "Mumbai Indians", code: "MI", flag: "🔵" },
      team2: { name: "Chennai Super Kings", code: "CSK", flag: "🟡" },
      timeText: "Starts in 02h 15m",
      megaPrize: "₹15 Crore",
      firstPrize: "₹1.5 Crore + iPhone 16 Pro",
      entryFee: 1,
      origEntryFee: 49,
      totalSpots: 1000000,
      filledSpots: 842190,
      isLive: false,
      players: [
        { id: "p1", name: "Rohit Sharma", team: "MI", role: "BAT", credits: 9.5, pts: 142 },
        { id: "p2", name: "Suryakumar Yadav", team: "MI", role: "BAT", credits: 9.0, pts: 188 },
        { id: "p3", name: "Hardik Pandya", team: "MI", role: "AR", credits: 9.0, pts: 165 },
        { id: "p4", name: "Jasprit Bumrah", team: "MI", role: "BOWL", credits: 9.5, pts: 210 },
        { id: "p5", name: "Ishan Kishan", team: "MI", role: "WK", credits: 8.5, pts: 120 },
        { id: "p6", name: "Tilak Varma", team: "MI", role: "BAT", credits: 8.5, pts: 130 },
        { id: "p7", name: "Ruturaj Gaikwad", team: "CSK", role: "BAT", credits: 9.5, pts: 175 },
        { id: "p8", name: "MS Dhoni", team: "CSK", role: "WK", credits: 8.5, pts: 110 },
        { id: "p9", name: "Ravindra Jadeja", team: "CSK", role: "AR", credits: 9.0, pts: 195 },
        { id: "p10", name: "Shivam Dube", team: "CSK", role: "AR", credits: 8.5, pts: 154 },
        { id: "p11", name: "Matheesha Pathirana", team: "CSK", role: "BOWL", credits: 9.0, pts: 170 },
        { id: "p12", name: "Deepak Chahar", team: "CSK", role: "BOWL", credits: 8.0, pts: 95 },
        { id: "p13", name: "Gerald Coetzee", team: "MI", role: "BOWL", credits: 8.5, pts: 115 },
        { id: "p14", name: "Daryl Mitchell", team: "CSK", role: "AR", credits: 8.5, pts: 105 }
      ]
    },
    {
      id: "m-ipl-02",
      tournament: "TATA IPL 2026",
      team1: { name: "Royal Challengers", code: "RCB", flag: "🔴" },
      team2: { name: "Kolkata Knight Riders", code: "KKR", flag: "🟣" },
      timeText: "Starts in 05h 40m",
      megaPrize: "₹10 Crore",
      firstPrize: "₹1 Crore",
      entryFee: 1,
      origEntryFee: 49,
      totalSpots: 750000,
      filledSpots: 590120,
      isLive: false,
      players: [
        { id: "p20", name: "Virat Kohli", team: "RCB", role: "BAT", credits: 9.5, pts: 220 },
        { id: "p21", name: "Faf du Plessis", team: "RCB", role: "BAT", credits: 9.0, pts: 160 },
        { id: "p22", name: "Glenn Maxwell", team: "RCB", role: "AR", credits: 9.0, pts: 145 },
        { id: "p23", name: "Mohammed Siraj", team: "RCB", role: "BOWL", credits: 8.5, pts: 130 },
        { id: "p24", name: "Dinesh Karthik", team: "RCB", role: "WK", credits: 8.0, pts: 95 },
        { id: "p25", name: "Shreyas Iyer", team: "KKR", role: "BAT", credits: 9.0, pts: 170 },
        { id: "p26", name: "Andre Russell", team: "KKR", role: "AR", credits: 9.5, pts: 215 },
        { id: "p27", name: "Sunil Narine", team: "KKR", role: "AR", credits: 9.5, pts: 240 },
        { id: "p28", name: "Rinku Singh", team: "KKR", role: "BAT", credits: 8.5, pts: 140 },
        { id: "p29", name: "Mitchell Starc", team: "KKR", role: "BOWL", credits: 9.0, pts: 155 },
        { id: "p30", name: "Phil Salt", team: "KKR", role: "WK", credits: 8.5, pts: 160 },
        { id: "p31", name: "Varun Chakaravarthy", team: "KKR", role: "BOWL", credits: 8.5, pts: 145 }
      ]
    },
    {
      id: "m-ipl-03",
      tournament: "TATA IPL 2026",
      team1: { name: "Gujarat Titans", code: "GT", flag: "🔵" },
      team2: { name: "Rajasthan Royals", code: "RR", flag: "💖" },
      timeText: "Tomorrow at 07:30 PM",
      megaPrize: "₹5 Crore",
      firstPrize: "₹50 Lakh",
      entryFee: 19,
      origEntryFee: 39,
      totalSpots: 400000,
      filledSpots: 210400,
      isLive: false,
      players: []
    }
  ],

  currentMatch: null,
  selectedPlayers: new Set(),
  captainId: null,
  viceCaptainId: null,
  currentContestFee: 1,

  init() {
    this.renderMatches();
    this.bindEvents();
  },

  renderMatches() {
    const grid = document.getElementById("fantasy-matches-grid");
    if (!grid) return;

    grid.innerHTML = this.matches.map(m => {
      const fillPct = Math.round((m.filledSpots / m.totalSpots) * 100);
      return `
        <div class="card-gradient p-4 flex flex-col justify-between hover:border-sky-500/50 transition duration-200">
          <div>
            <!-- Header -->
            <div class="flex items-center justify-between text-xs pb-3 border-b border-slate-700/60">
              <span class="text-slate-400 font-medium">${m.tournament}</span>
              <span class="inline-flex items-center gap-1.5 bg-sky-500/10 text-sky-400 font-semibold px-2 py-0.5 rounded-full">
                <span class="pulse-dot"></span> ${m.timeText}
              </span>
            </div>

            <!-- Teams -->
            <div class="flex items-center justify-between my-4 px-2">
              <div class="flex items-center gap-2">
                <span class="text-2xl">${m.team1.flag}</span>
                <div>
                  <h4 class="font-bold text-white text-base">${m.team1.code}</h4>
                  <p class="text-[11px] text-slate-400">${m.team1.name}</p>
                </div>
              </div>

              <div class="text-xs font-black text-slate-500 bg-slate-800/80 px-2 py-1 rounded">VS</div>

              <div class="flex items-center gap-2 text-right">
                <div>
                  <h4 class="font-bold text-white text-base">${m.team2.code}</h4>
                  <p class="text-[11px] text-slate-400">${m.team2.name}</p>
                </div>
                <span class="text-2xl">${m.team2.flag}</span>
              </div>
            </div>

            <!-- Prize Details -->
            <div class="bg-[#121622] rounded-lg p-3 my-2 border border-slate-800 flex justify-between items-center">
              <div>
                <p class="text-[10px] text-slate-400 uppercase font-semibold">Mega Prize Pool</p>
                <p class="text-lg font-black text-amber-400 num-font">${m.megaPrize}</p>
              </div>
              <div class="text-right">
                <p class="text-[10px] text-slate-400 uppercase font-semibold">1st Prize</p>
                <p class="text-xs font-bold text-emerald-400">${m.firstPrize}</p>
              </div>
            </div>

            <!-- Spots Fill Bar -->
            <div class="mt-3">
              <div class="flex justify-between text-[11px] text-slate-400 mb-1">
                <span>${(m.filledSpots).toLocaleString('en-IN')} spots filled</span>
                <span class="font-semibold text-slate-300">${(m.totalSpots - m.filledSpots).toLocaleString('en-IN')} left</span>
              </div>
              <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="bg-gradient-to-r from-amber-500 to-red-500 h-full rounded-full" style="width: ${fillPct}%"></div>
              </div>
            </div>
          </div>

          <!-- Action Footer -->
          <div class="flex items-center justify-between pt-4 mt-3 border-t border-slate-800">
            <div class="flex items-baseline gap-1.5">
              <span class="text-xs text-slate-400">Entry:</span>
              <span class="text-lg font-black text-emerald-400 num-font">₹${m.entryFee}</span>
              ${m.origEntryFee ? `<span class="text-xs text-slate-500 line-through">₹${m.origEntryFee}</span>` : ''}
              <span class="text-[10px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 rounded font-bold">98% OFF</span>
            </div>
            <button onclick="FantasyManager.openTeamBuilder('${m.id}')" class="btn-primary text-xs px-4 py-2 font-bold shadow-md hover:shadow-sky-500/20">
              Join Contest
            </button>
          </div>
        </div>
      `;
    }).join('');
  },

  bindEvents() {
    const modal = document.getElementById("team-builder-modal");
    if (!modal) return;

    document.getElementById("close-team-builder")?.addEventListener("click", () => {
      modal.classList.remove("active");
    });
  },

  openTeamBuilder(matchId) {
    const match = this.matches.find(m => m.id === matchId);
    if (!match) return;

    this.currentMatch = match;
    this.selectedPlayers.clear();
    this.captainId = null;
    this.viceCaptainId = null;
    this.currentContestFee = match.entryFee;

    const modal = document.getElementById("team-builder-modal");
    if (!modal) return;

    document.getElementById("tb-match-title").textContent = `${match.team1.code} vs ${match.team2.code} (Mega Contest ₹${match.entryFee})`;
    this.renderPlayerList(match.players || []);
    this.updateTeamStats();
    modal.classList.add("active");
  },

  renderPlayerList(players) {
    const container = document.getElementById("tb-player-list");
    if (!container) return;

    if (!players || players.length === 0) {
      container.innerHTML = `<div class="p-6 text-center text-slate-400 text-sm">Squad announcement pending for this match. Check back soon!</div>`;
      return;
    }

    container.innerHTML = players.map(p => {
      const isSelected = this.selectedPlayers.has(p.id);
      const isC = this.captainId === p.id;
      const isVC = this.viceCaptainId === p.id;

      return `
        <div id="player-row-${p.id}" class="flex items-center justify-between p-3 rounded-lg border transition ${isSelected ? 'bg-sky-950/40 border-sky-500/60' : 'bg-[#121622] border-slate-800'}">
          <div class="flex items-center gap-3">
            <button onclick="FantasyManager.togglePlayer('${p.id}')" class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs transition ${isSelected ? 'bg-red-500 text-white' : 'bg-sky-500 text-white'}">
              ${isSelected ? '✕' : '+'}
            </button>
            <div>
              <h5 class="font-bold text-white text-sm">${p.name}</h5>
              <div class="flex items-center gap-2 text-[11px] text-slate-400">
                <span class="font-semibold text-sky-400">${p.team}</span>
                <span>•</span>
                <span class="bg-slate-800 px-1.5 py-0.5 rounded text-[10px]">${p.role}</span>
                <span>•</span>
                <span>${p.pts} pts</span>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <span class="text-sm font-bold text-amber-400 num-font">${p.credits} Cr</span>
            
            ${isSelected ? `
              <div class="flex items-center gap-1.5">
                <button onclick="FantasyManager.setCaptain('${p.id}')" class="px-2 py-1 text-[10px] rounded font-bold transition ${isC ? 'bg-amber-400 text-black font-black' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}">
                  2x C
                </button>
                <button onclick="FantasyManager.setViceCaptain('${p.id}')" class="px-2 py-1 text-[10px] rounded font-bold transition ${isVC ? 'bg-sky-400 text-black font-black' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}">
                  1.5x VC
                </button>
              </div>
            ` : ''}
          </div>
        </div>
      `;
    }).join('');
  },

  togglePlayer(id) {
    if (this.selectedPlayers.has(id)) {
      this.selectedPlayers.delete(id);
      if (this.captainId === id) this.captainId = null;
      if (this.viceCaptainId === id) this.viceCaptainId = null;
    } else {
      if (this.selectedPlayers.size >= 11) {
        if (window.Toast) window.Toast.error("You can select maximum 11 players!");
        return;
      }
      this.selectedPlayers.add(id);
    }
    this.renderPlayerList(this.currentMatch.players);
    this.updateTeamStats();
  },

  setCaptain(id) {
    if (this.viceCaptainId === id) this.viceCaptainId = null;
    this.captainId = id;
    this.renderPlayerList(this.currentMatch.players);
    this.updateTeamStats();
  },

  setViceCaptain(id) {
    if (this.captainId === id) this.captainId = null;
    this.viceCaptainId = id;
    this.renderPlayerList(this.currentMatch.players);
    this.updateTeamStats();
  },

  updateTeamStats() {
    const countEl = document.getElementById("tb-selected-count");
    const creditsEl = document.getElementById("tb-credits-left");
    const cInfo = document.getElementById("tb-c-vc-status");
    const joinBtn = document.getElementById("tb-join-btn");

    let totalCreditsUsed = 0;
    this.currentMatch?.players?.forEach(p => {
      if (this.selectedPlayers.has(p.id)) totalCreditsUsed += p.credits;
    });
    const creditsLeft = Math.max(0, 100 - totalCreditsUsed);

    if (countEl) countEl.textContent = `${this.selectedPlayers.size}/11`;
    if (creditsEl) creditsEl.textContent = `${creditsLeft.toFixed(1)} Cr`;

    if (cInfo) {
      const c = this.currentMatch?.players?.find(p => p.id === this.captainId);
      const vc = this.currentMatch?.players?.find(p => p.id === this.viceCaptainId);
      cInfo.textContent = `Captain (2x): ${c ? c.name : 'None'} | VC (1.5x): ${vc ? vc.name : 'None'}`;
    }

    if (joinBtn) {
      const isValid = this.selectedPlayers.size === 11 && this.captainId && this.viceCaptainId && creditsLeft >= 0;
      joinBtn.disabled = !isValid;
      if (isValid) {
        joinBtn.classList.remove("opacity-50", "pointer-events-none");
      } else {
        joinBtn.classList.add("opacity-50", "pointer-events-none");
      }
    }
  },

  submitTeam() {
    if (this.selectedPlayers.size !== 11) {
      if (window.Toast) window.Toast.error("Please pick exactly 11 players for your team!");
      return;
    }
    if (!this.captainId || !this.viceCaptainId) {
      if (window.Toast) window.Toast.error("Please assign Captain (2x) and Vice-Captain (1.5x)!");
      return;
    }

    // Check user balance
    if (window.UserManager && !window.UserManager.hasBalance(this.currentContestFee)) {
      if (window.Toast) window.Toast.error("Insufficient wallet balance! Please deposit to join.");
      if (window.WalletManager) window.WalletManager.openDepositModal();
      return;
    }

    // Deduct entry fee
    if (window.UserManager) {
      window.UserManager.deductBalance(this.currentContestFee, `Contest Entry: ${this.currentMatch.tournament} (${this.currentMatch.team1.code} vs ${this.currentMatch.team2.code})`);
    }

    document.getElementById("team-builder-modal")?.classList.remove("active");

    if (window.Toast) {
      window.Toast.success(`🏆 Team Created! Contest entry confirmed for ₹${this.currentContestFee}. Good luck!`);
    }
  }
};

window.FantasyManager = FantasyManager;
