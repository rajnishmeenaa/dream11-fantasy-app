/**
 * VIP Rewards Manager
 */
const VipManager = {
  currentTierIndex: 2, // VIP 3 (Gold)
  currentPoints: 34250,
  nextTierPoints: 100000,
  dailyBonusClaimed: false,

  init() {
    this.updateUI();
    document.getElementById("claim-vip-daily-btn")?.addEventListener("click", () => this.claimDailyBonus());
  },

  updateUI() {
    const tier = window.BRAND_CONFIG?.vipTiers?.[this.currentTierIndex] || { name: "Gold", level: 3, cashback: "7%" };
    
    document.querySelectorAll(".vip-tier-name").forEach(el => el.textContent = `VIP ${tier.level} (${tier.name})`);
    document.querySelectorAll(".vip-tier-badge").forEach(el => el.textContent = `VIP ${tier.level}`);
    document.querySelectorAll(".vip-cashback-rate").forEach(el => el.textContent = tier.cashback);

    const ptsEl = document.getElementById("vip-current-points");
    if (ptsEl) ptsEl.textContent = `${this.currentPoints.toLocaleString('en-IN')} / ${this.nextTierPoints.toLocaleString('en-IN')} pts`;

    const bar = document.getElementById("vip-progress-bar");
    if (bar) {
      const pct = Math.min(100, Math.round((this.currentPoints / this.nextTierPoints) * 100));
      bar.style.width = pct + "%";
    }
  },

  claimDailyBonus() {
    if (this.dailyBonusClaimed) {
      if (window.Toast) window.Toast.info("Daily VIP bonus already claimed today! Check back tomorrow.");
      return;
    }

    const bonus = 250;
    this.dailyBonusClaimed = true;

    if (window.UserManager) {
      window.UserManager.addBalance(bonus, "VIP 3 Daily Loyalty Bonus");
    }

    const btn = document.getElementById("claim-vip-daily-btn");
    if (btn) {
      btn.textContent = "Claimed Today ✓";
      btn.classList.add("opacity-50", "pointer-events-none");
    }

    if (window.Toast) {
      window.Toast.success(`👑 Claimed ₹${bonus} VIP Gold Daily Bonus! Credited to your wallet.`);
    }
  }
};

window.VipManager = VipManager;
