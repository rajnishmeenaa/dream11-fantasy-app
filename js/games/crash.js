/**
 * Interactive Crash / Limbo Game
 */
const CrashGame = {
  canvas: null,
  ctx: null,
  state: "IDLE", // IDLE, RUNNING, CRASHED
  currentMultiplier: 1.00,
  crashPoint: 1.00,
  betAmount: 50,
  hasBet: false,
  cashedOut: false,
  autoCashout: 2.00,
  history: [1.85, 4.20, 1.25, 14.50, 2.10, 1.10, 7.80],
  animationId: null,
  startTime: null,

  init() {
    this.canvas = document.getElementById("crash-canvas");
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");

    this.resizeCanvas();
    window.addEventListener("resize", () => this.resizeCanvas());

    this.renderHistory();
    this.drawIdle();
    this.bindEvents();
  },

  resizeCanvas() {
    if (!this.canvas) return;
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = 240;
    if (this.state === "IDLE") this.drawIdle();
  },

  renderHistory() {
    const list = document.getElementById("crash-history");
    if (!list) return;

    list.innerHTML = this.history.slice(-8).map(m => {
      const isHigh = m >= 2.0;
      const isMega = m >= 10.0;
      const color = isMega ? 'bg-amber-500/20 text-amber-400 border-amber-500/40' : (isHigh ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40' : 'bg-slate-800 text-slate-400 border-slate-700');
      return `<span class="px-2 py-0.5 text-[11px] font-bold rounded-full border ${color} num-font">${m.toFixed(2)}x</span>`;
    }).join('');
  },

  bindEvents() {
    document.getElementById("crash-bet-btn")?.addEventListener("click", () => this.handleAction());

    // Preset Bet buttons
    document.querySelectorAll(".crash-bet-quick").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const val = e.target.getAttribute("data-val");
        const input = document.getElementById("crash-bet-input");
        if (!input) return;

        if (val === "2x") this.betAmount = Math.min(10000, this.betAmount * 2);
        else if (val === "/2") this.betAmount = Math.max(10, Math.floor(this.betAmount / 2));
        else if (val === "min") this.betAmount = 10;
        else if (val === "max") this.betAmount = Math.min(10000, window.UserManager ? window.UserManager.balance : 1000);
        else this.betAmount = parseInt(val, 10) || 50;

        input.value = this.betAmount;
      });
    });

    document.getElementById("crash-bet-input")?.addEventListener("input", (e) => {
      this.betAmount = Math.max(10, parseInt(e.target.value, 10) || 10);
    });

    document.getElementById("crash-autocashout-input")?.addEventListener("input", (e) => {
      this.autoCashout = parseFloat(e.target.value) || 2.0;
    });
  },

  handleAction() {
    if (this.state === "IDLE" || this.state === "CRASHED") {
      this.startRound();
    } else if (this.state === "RUNNING" && this.hasBet && !this.cashedOut) {
      this.cashOut();
    }
  },

  startRound() {
    if (window.UserManager && !window.UserManager.hasBalance(this.betAmount)) {
      if (window.Toast) window.Toast.error("Insufficient balance to place bet!");
      if (window.WalletManager) window.WalletManager.openDepositModal();
      return;
    }

    if (window.UserManager) {
      window.UserManager.deductBalance(this.betAmount, `Crash Bet (₹${this.betAmount})`);
    }

    this.state = "RUNNING";
    this.hasBet = true;
    this.cashedOut = false;
    this.currentMultiplier = 1.00;

    // Determine random crash point based on standard provably fair curve
    const r = Math.random();
    if (r < 0.04) {
      this.crashPoint = 1.00; // Instant crash 4% of the time
    } else {
      this.crashPoint = Math.max(1.01, +(0.98 / (1 - r)).toFixed(2));
    }

    this.startTime = performance.now();
    this.updateButtonUI();

    if (this.animationId) cancelAnimationFrame(this.animationId);
    this.loop();
  },

  loop() {
    const elapsed = (performance.now() - this.startTime) / 1000;
    // Multiplier grows exponentially over time: e^(0.06 * t)
    this.currentMultiplier = +(Math.pow(Math.E, 0.07 * elapsed * 2)).toFixed(2);

    // Check Auto-Cashout
    if (this.hasBet && !this.cashedOut && this.autoCashout && this.currentMultiplier >= this.autoCashout) {
      this.cashOut();
    }

    // Check Crash
    if (this.currentMultiplier >= this.crashPoint) {
      this.triggerCrash();
      return;
    }

    this.drawChart();
    this.updateDisplay();
    this.animationId = requestAnimationFrame(() => this.loop());
  },

  cashOut() {
    this.cashedOut = true;
    const winAmount = Math.floor(this.betAmount * this.currentMultiplier);

    if (window.UserManager) {
      window.UserManager.addBalance(winAmount, `Crash Win (${this.currentMultiplier.toFixed(2)}x)`);
    }

    if (window.Toast) {
      window.Toast.success(`🚀 Cashed Out at ${this.currentMultiplier.toFixed(2)}x! Won ₹${winAmount.toLocaleString('en-IN')}`);
    }

    this.updateButtonUI();
  },

  triggerCrash() {
    this.state = "CRASHED";
    this.currentMultiplier = this.crashPoint;

    this.history.push(this.crashPoint);
    this.renderHistory();

    this.drawCrashed();
    this.updateDisplay();
    this.updateButtonUI();

    if (this.hasBet && !this.cashedOut) {
      if (window.Toast) window.Toast.error(`💥 Crashed at ${this.crashPoint.toFixed(2)}x! Better luck next round.`);
    }

    setTimeout(() => {
      this.state = "IDLE";
      this.hasBet = false;
      this.cashedOut = false;
      this.updateButtonUI();
      this.drawIdle();
    }, 2800);
  },

  updateDisplay() {
    const el = document.getElementById("crash-multiplier-text");
    if (!el) return;

    el.textContent = `${this.currentMultiplier.toFixed(2)}x`;
    if (this.state === "CRASHED") {
      el.className = "text-5xl md:text-6xl font-black text-rose-500 text-glow-red num-font transition";
    } else if (this.state === "RUNNING") {
      el.className = "text-5xl md:text-6xl font-black text-sky-400 text-glow-blue num-font transition";
    } else {
      el.className = "text-5xl md:text-6xl font-black text-slate-400 num-font transition";
    }
  },

  updateButtonUI() {
    const btn = document.getElementById("crash-bet-btn");
    if (!btn) return;

    if (this.state === "RUNNING") {
      if (this.hasBet && !this.cashedOut) {
        const potentialProfit = Math.floor(this.betAmount * this.currentMultiplier);
        btn.className = "btn-gold w-full py-3 text-base font-black";
        btn.textContent = `Cash Out ₹${potentialProfit} (${this.currentMultiplier.toFixed(2)}x)`;
      } else {
        btn.className = "btn-outline w-full py-3 text-base font-bold opacity-50 pointer-events-none";
        btn.textContent = `Round In Progress...`;
      }
    } else if (this.state === "CRASHED") {
      btn.className = "btn-outline w-full py-3 text-base font-bold opacity-50 pointer-events-none";
      btn.textContent = `Crashed! Preparing next...`;
    } else {
      btn.className = "btn-success w-full py-3 text-base font-black";
      btn.textContent = `Place Bet (₹${this.betAmount})`;
    }
  },

  drawIdle() {
    if (!this.ctx) return;
    const w = this.canvas.width;
    const h = this.canvas.height;
    this.ctx.clearRect(0, 0, w, h);

    // Draw Grid
    this.ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
    this.ctx.lineWidth = 1;
    for (let x = 40; x < w; x += 60) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, h);
      this.ctx.stroke();
    }
    for (let y = 30; y < h; y += 40) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(w, y);
      this.ctx.stroke();
    }

    const mText = document.getElementById("crash-multiplier-text");
    if (mText) mText.textContent = "1.00x";
  },

  drawChart() {
    if (!this.ctx) return;
    const w = this.canvas.width;
    const h = this.canvas.height;
    this.ctx.clearRect(0, 0, w, h);

    // Draw Grid Lines
    this.ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
    for (let y = 30; y < h; y += 40) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(w, y);
      this.ctx.stroke();
    }

    // Rocket curve
    const progress = Math.min(1, (this.currentMultiplier - 1) / Math.max(3, this.crashPoint * 0.8));
    const startX = 40;
    const startY = h - 30;
    const endX = startX + (w - 100) * progress;
    const endY = startY - (h - 70) * Math.pow(progress, 0.85);

    // Fill under curve
    const grad = this.ctx.createLinearGradient(0, endY, 0, h);
    grad.addColorStop(0, "rgba(0, 187, 255, 0.35)");
    grad.addColorStop(1, "rgba(0, 187, 255, 0.0)");

    this.ctx.fillStyle = grad;
    this.ctx.beginPath();
    this.ctx.moveTo(startX, startY);
    this.ctx.quadraticCurveTo((startX + endX) / 2, startY, endX, endY);
    this.ctx.lineTo(endX, startY);
    this.ctx.closePath();
    this.ctx.fill();

    // Curve line
    this.ctx.strokeStyle = "#00BBFF";
    this.ctx.lineWidth = 4;
    this.ctx.shadowColor = "#00BBFF";
    this.ctx.shadowBlur = 12;
    this.ctx.beginPath();
    this.ctx.moveTo(startX, startY);
    this.ctx.quadraticCurveTo((startX + endX) / 2, startY, endX, endY);
    this.ctx.stroke();
    this.ctx.shadowBlur = 0;

    // Rocket icon/circle
    this.ctx.fillStyle = "#FFD156";
    this.ctx.beginPath();
    this.ctx.arc(endX, endY, 6, 0, Math.PI * 2);
    this.ctx.fill();
  },

  drawCrashed() {
    if (!this.ctx) return;
    const w = this.canvas.width;
    const h = this.canvas.height;

    this.ctx.fillStyle = "rgba(244, 63, 94, 0.15)";
    this.ctx.fillRect(0, 0, w, h);
  }
};

window.CrashGame = CrashGame;
