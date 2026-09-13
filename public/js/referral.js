/**
 * Referral & Affiliate Manager
 */
const ReferralManager = {
  myReferralCode: "WIN99X",
  totalInvited: 28,
  totalEarned: 14850,
  claimableCommission: 1250,

  init() {
    this.updateUI();

    document.getElementById("copy-ref-code-btn")?.addEventListener("click", () => this.copyCode());
    document.getElementById("copy-ref-link-btn")?.addEventListener("click", () => this.copyLink());
    document.getElementById("claim-ref-comm-btn")?.addEventListener("click", () => this.claimCommission());
  },

  updateUI() {
    document.querySelectorAll(".ref-code-text").forEach(el => el.textContent = this.myReferralCode);
    
    const countEl = document.getElementById("ref-total-invited");
    if (countEl) countEl.textContent = this.totalInvited;

    const earnedEl = document.getElementById("ref-total-earned");
    if (earnedEl) earnedEl.textContent = "₹" + this.totalEarned.toLocaleString('en-IN');

    const commEl = document.getElementById("ref-claimable-comm");
    if (commEl) commEl.textContent = "₹" + this.claimableCommission.toLocaleString('en-IN');

    const linkInput = document.getElementById("ref-link-input");
    if (linkInput) linkInput.value = `https://${window.BRAND_CONFIG?.domain || 'winplay11.com'}/join?ref=${this.myReferralCode}`;
  },

  copyCode() {
    navigator.clipboard?.writeText(this.myReferralCode);
    if (window.Toast) window.Toast.success(`Copied Referral Code: ${this.myReferralCode}`);
  },

  copyLink() {
    const link = `https://${window.BRAND_CONFIG?.domain || 'winplay11.com'}/join?ref=${this.myReferralCode}`;
    navigator.clipboard?.writeText(link);
    if (window.Toast) window.Toast.success(`Copied Share Link! Share with friends on WhatsApp / Telegram.`);
  },

  claimCommission() {
    if (this.claimableCommission <= 0) {
      if (window.Toast) window.Toast.info("No commission available to claim right now.");
      return;
    }

    const claimed = this.claimableCommission;
    this.totalEarned += claimed;
    this.claimableCommission = 0;
    this.updateUI();

    if (window.UserManager) {
      window.UserManager.addBalance(claimed, `Referral Commission Payout (₹${claimed})`);
    }

    if (window.Toast) {
      window.Toast.success(`💰 Successfully claimed ₹${claimed.toLocaleString('en-IN')} referral commission to wallet!`);
    }
  }
};

window.ReferralManager = ReferralManager;
