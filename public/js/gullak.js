/**
 * Gullak Cash (Piggy Bank) Module
 */
const GullakManager = {
  currentCash: 148.50,
  maxCash: 500.00,
  accumulationRate: 0.15, // Adds ₹0.15 every 3 seconds
  intervalId: null,

  init() {
    this.updateUI();

    // Start accumulation timer
    this.intervalId = setInterval(() => {
      if (this.currentCash < this.maxCash) {
        this.currentCash = Math.min(this.maxCash, this.currentCash + this.accumulationRate);
        this.updateUI();
      }
    }, 3000);

    // Bind claim button
    const claimBtn = document.getElementById("gullak-claim-btn");
    if (claimBtn) {
      claimBtn.addEventListener("click", () => this.claimCash());
    }
  },

  updateUI() {
    const el = document.getElementById("gullak-amount");
    if (el) {
      el.textContent = "₹" + this.currentCash.toFixed(2);
    }
    const bar = document.getElementById("gullak-progress-bar");
    if (bar) {
      const pct = Math.min(100, (this.currentCash / this.maxCash) * 100);
      bar.style.width = pct + "%";
    }
    const btn = document.getElementById("gullak-claim-btn");
    if (btn) {
      if (this.currentCash <= 0) {
        btn.disabled = true;
        btn.classList.add("opacity-50", "pointer-events-none");
      } else {
        btn.disabled = false;
        btn.classList.remove("opacity-50", "pointer-events-none");
      }
    }
  },

  claimCash() {
    if (this.currentCash <= 0) return;

    const claimed = this.currentCash;
    this.currentCash = 0.00;
    this.updateUI();

    // Trigger celebratory coin explosion
    this.spawnCoinParticles();

    // Credit to User Wallet
    if (window.UserManager) {
      window.UserManager.addBalance(claimed, `Claimed Gullak Cash (₹${claimed.toFixed(2)})`);
    }

    if (window.Toast) {
      window.Toast.success(`🎉 Successfully claimed ₹${claimed.toFixed(2)} from your Gullak Piggy Bank!`);
    }
  },

  spawnCoinParticles() {
    const sourceBtn = document.getElementById("gullak-claim-btn");
    const walletEl = document.getElementById("nav-wallet-balance");
    if (!sourceBtn || !walletEl) return;

    const sRect = sourceBtn.getBoundingClientRect();
    const wRect = walletEl.getBoundingClientRect();

    const startX = sRect.left + sRect.width / 2;
    const startY = sRect.top + sRect.height / 2;
    const endX = wRect.left + wRect.width / 2;
    const endY = wRect.top + wRect.height / 2;

    for (let i = 0; i < 15; i++) {
      setTimeout(() => {
        const coin = document.createElement("div");
        coin.className = "coin-particle";
        coin.textContent = "🪙";
        coin.style.left = startX + "px";
        coin.style.top = startY + "px";

        // Add random scatter path
        const midX = (startX + endX) / 2 + (Math.random() * 120 - 60);
        const midY = Math.min(startY, endY) - (50 + Math.random() * 80);

        coin.style.setProperty("--tx-mid", `${midX - startX}px`);
        coin.style.setProperty("--ty-mid", `${midY - startY}px`);
        coin.style.setProperty("--tx-end", `${endX - startX}px`);
        coin.style.setProperty("--ty-end", `${endY - startY}px`);

        document.body.appendChild(coin);

        setTimeout(() => coin.remove(), 850);
      }, i * 40);
    }
  }
};

window.GullakManager = GullakManager;
