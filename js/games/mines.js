/**
 * Interactive 5x5 Mines Game
 */
const MinesGame = {
  gridSize: 25,
  mineCount: 3,
  betAmount: 50,
  isPlaying: false,
  grid: [], // array of { isMine: bool, isRevealed: bool }
  revealedGems: 0,
  currentMultiplier: 1.00,

  init() {
    this.renderEmptyGrid();
    this.bindEvents();
  },

  renderEmptyGrid() {
    const container = document.getElementById("mines-grid-container");
    if (!container) return;

    container.innerHTML = "";
    for (let i = 0; i < this.gridSize; i++) {
      const tile = document.createElement("div");
      tile.className = "mine-tile opacity-80 cursor-not-allowed";
      tile.id = `mine-tile-${i}`;
      tile.textContent = "❓";
      container.appendChild(tile);
    }
  },

  bindEvents() {
    document.getElementById("mines-start-btn")?.addEventListener("click", () => this.handleAction());

    const mineSelect = document.getElementById("mines-count-select");
    if (mineSelect) {
      mineSelect.addEventListener("change", (e) => {
        this.mineCount = parseInt(e.target.value, 10);
      });
    }

    document.getElementById("mines-bet-input")?.addEventListener("input", (e) => {
      this.betAmount = Math.max(10, parseInt(e.target.value, 10) || 10);
    });

    document.querySelectorAll(".mines-bet-quick").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const val = e.target.getAttribute("data-val");
        const input = document.getElementById("mines-bet-input");
        if (!input) return;

        if (val === "2x") this.betAmount = Math.min(10000, this.betAmount * 2);
        else if (val === "/2") this.betAmount = Math.max(10, Math.floor(this.betAmount / 2));
        else if (val === "min") this.betAmount = 10;
        else if (val === "max") this.betAmount = Math.min(10000, window.UserManager ? window.UserManager.balance : 1000);
        else this.betAmount = parseInt(val, 10) || 50;

        input.value = this.betAmount;
      });
    });
  },

  handleAction() {
    if (!this.isPlaying) {
      this.startGame();
    } else {
      this.cashOut();
    }
  },

  startGame() {
    if (window.UserManager && !window.UserManager.hasBalance(this.betAmount)) {
      if (window.Toast) window.Toast.error("Insufficient balance to place bet!");
      if (window.WalletManager) window.WalletManager.openDepositModal();
      return;
    }

    if (window.UserManager) {
      window.UserManager.deductBalance(this.betAmount, `Mines Bet (₹${this.betAmount})`);
    }

    this.isPlaying = true;
    this.revealedGems = 0;
    this.currentMultiplier = 1.00;

    // Generate Mines
    this.grid = Array(this.gridSize).fill(null).map(() => ({ isMine: false, isRevealed: false }));
    let planted = 0;
    while (planted < this.mineCount) {
      const idx = Math.floor(Math.random() * this.gridSize);
      if (!this.grid[idx].isMine) {
        this.grid[idx].isMine = true;
        planted++;
      }
    }

    this.renderActiveGrid();
    this.updateButtonUI();
    this.updateMultiplierUI();
  },

  renderActiveGrid() {
    const container = document.getElementById("mines-grid-container");
    if (!container) return;

    container.innerHTML = "";
    for (let i = 0; i < this.gridSize; i++) {
      const tile = document.createElement("div");
      tile.className = "mine-tile";
      tile.id = `mine-tile-${i}`;
      tile.innerHTML = `<span class="opacity-30">⭐</span>`;
      tile.addEventListener("click", () => this.revealTile(i));
      container.appendChild(tile);
    }
  },

  revealTile(idx) {
    if (!this.isPlaying || this.grid[idx].isRevealed) return;

    this.grid[idx].isRevealed = true;
    const tile = document.getElementById(`mine-tile-${idx}`);
    if (!tile) return;

    if (this.grid[idx].isMine) {
      // Hit a mine!
      tile.className = "mine-tile revealed-bomb";
      tile.innerHTML = "💣";
      this.gameOver(false);
    } else {
      // Found a gem!
      tile.className = "mine-tile revealed-gem";
      tile.innerHTML = "💎";
      this.revealedGems++;

      // Multiplier formula: 0.98 * (25 choose revealed) / ((25 - mines) choose revealed)
      this.currentMultiplier = this.calculateMultiplier(this.revealedGems, this.mineCount);
      this.updateMultiplierUI();
      this.updateButtonUI();

      // If all gems found
      if (this.revealedGems === (this.gridSize - this.mineCount)) {
        this.cashOut();
      }
    }
  },

  calculateMultiplier(revealed, mines) {
    let prob = 1.0;
    for (let i = 0; i < revealed; i++) {
      prob *= (25 - mines - i) / (25 - i);
    }
    const mult = 0.98 / prob;
    return +mult.toFixed(2);
  },

  updateMultiplierUI() {
    const el = document.getElementById("mines-current-mult");
    if (el) el.textContent = `${this.currentMultiplier.toFixed(2)}x`;
  },

  updateButtonUI() {
    const btn = document.getElementById("mines-start-btn");
    if (!btn) return;

    if (this.isPlaying) {
      const win = Math.floor(this.betAmount * this.currentMultiplier);
      if (this.revealedGems > 0) {
        btn.className = "btn-gold w-full py-3 text-base font-black";
        btn.textContent = `Cash Out ₹${win.toLocaleString('en-IN')} (${this.currentMultiplier.toFixed(2)}x)`;
      } else {
        btn.className = "btn-outline w-full py-3 text-base font-bold";
        btn.textContent = `Pick a tile to start`;
      }
    } else {
      btn.className = "btn-success w-full py-3 text-base font-black";
      btn.textContent = `Start Game (₹${this.betAmount})`;
    }
  },

  cashOut() {
    if (!this.isPlaying || this.revealedGems === 0) return;

    const winAmount = Math.floor(this.betAmount * this.currentMultiplier);
    this.gameOver(true, winAmount);
  },

  gameOver(won, winAmount = 0) {
    this.isPlaying = false;

    // Reveal rest of grid
    for (let i = 0; i < this.gridSize; i++) {
      const tile = document.getElementById(`mine-tile-${i}`);
      if (!tile || this.grid[i].isRevealed) continue;

      if (this.grid[i].isMine) {
        tile.className = "mine-tile opacity-60 bg-red-950/40 border border-red-500/30";
        tile.innerHTML = "💣";
      } else {
        tile.className = "mine-tile opacity-40 bg-emerald-950/30";
        tile.innerHTML = "💎";
      }
    }

    if (won) {
      if (window.UserManager) {
        window.UserManager.addBalance(winAmount, `Mines Win (${this.currentMultiplier.toFixed(2)}x)`);
      }
      if (window.Toast) {
        window.Toast.success(`💎 Brilliant! Cashed out ₹${winAmount.toLocaleString('en-IN')} (${this.currentMultiplier.toFixed(2)}x)!`);
      }
    } else {
      if (window.Toast) {
        window.Toast.error(`💥 Boom! You stepped on a mine. Try again!`);
      }
    }

    this.updateButtonUI();
  }
};

window.MinesGame = MinesGame;
