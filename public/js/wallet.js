/**
 * Wallet, Deposits & Withdrawals Manager
 */
const WalletManager = {
  selectedDepositMethod: "phonepe",
  depositAmount: 500,
  promoCode: "",
  activePromoBonus: 0,

  init() {
    this.bindEvents();
  },

  bindEvents() {
    // Deposit Method selectors
    document.querySelectorAll(".deposit-method-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".deposit-method-btn").forEach(b => b.classList.remove("border-sky-500", "bg-sky-500/10"));
        const target = e.currentTarget;
        target.classList.add("border-sky-500", "bg-sky-500/10");
        this.selectedDepositMethod = target.getAttribute("data-method");
      });
    });

    // Preset Amount buttons
    document.querySelectorAll(".deposit-amount-preset").forEach(btn => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".deposit-amount-preset").forEach(b => b.classList.remove("border-sky-400", "bg-sky-500/20", "text-sky-300"));
        const target = e.currentTarget;
        target.classList.add("border-sky-400", "bg-sky-500/20", "text-sky-300");
        const amt = parseInt(target.getAttribute("data-amount"), 10);
        this.depositAmount = amt;
        const input = document.getElementById("deposit-amount-input");
        if (input) input.value = amt;
        this.updateBonusPreview();
      });
    });

    document.getElementById("deposit-amount-input")?.addEventListener("input", (e) => {
      this.depositAmount = Math.max(10, parseInt(e.target.value, 10) || 0);
      this.updateBonusPreview();
    });

    document.getElementById("apply-promo-btn")?.addEventListener("click", () => this.applyPromo());
    document.getElementById("confirm-deposit-btn")?.addEventListener("click", () => this.processDeposit());
    document.getElementById("confirm-withdraw-btn")?.addEventListener("click", () => this.processWithdrawal());

    // Close modals
    document.getElementById("close-deposit-modal")?.addEventListener("click", () => {
      document.getElementById("deposit-modal")?.classList.remove("active");
    });
    document.getElementById("close-withdraw-modal")?.addEventListener("click", () => {
      document.getElementById("withdraw-modal")?.classList.remove("active");
    });
    document.getElementById("nav-deposit-btn")?.addEventListener("click", () => this.openDepositModal());
  },

  openDepositModal() {
    document.getElementById("deposit-modal")?.classList.add("active");
    this.updateBonusPreview();
  },

  openWithdrawModal() {
    document.getElementById("withdraw-modal")?.classList.add("active");
    const balEl = document.getElementById("withdraw-available-balance");
    if (balEl && window.UserManager) {
      balEl.textContent = "₹" + window.UserManager.balance.toLocaleString('en-IN');
    }
  },

  applyPromo() {
    const input = document.getElementById("deposit-promo-input");
    if (!input) return;
    const code = input.value.trim().toUpperCase();

    if (code === "WELCOME100" || code === "IPL2026" || code === "WIN2X") {
      this.promoCode = code;
      this.activePromoBonus = 1.0; // 100% bonus
      this.updateBonusPreview();
      if (window.Toast) window.Toast.success(`🎉 Promo code '${code}' applied! 100% bonus cash added.`);
    } else {
      if (window.Toast) window.Toast.error("Invalid promo code! Try 'WELCOME100'");
    }
  },

  updateBonusPreview() {
    const bonusBox = document.getElementById("deposit-bonus-preview");
    const totalCreditEl = document.getElementById("deposit-total-credit");
    if (!bonusBox || !totalCreditEl) return;

    const bonus = Math.floor(this.depositAmount * this.activePromoBonus);
    const total = this.depositAmount + bonus;

    if (bonus > 0) {
      bonusBox.classList.remove("hidden");
      document.getElementById("deposit-bonus-amount").textContent = `+₹${bonus.toLocaleString('en-IN')} Extra Bonus`;
    } else {
      bonusBox.classList.add("hidden");
    }

    totalCreditEl.textContent = `₹${total.toLocaleString('en-IN')}`;
  },

  processDeposit() {
    const btn = document.getElementById("confirm-deposit-btn");
    if (!btn || this.depositAmount < 100) {
      if (window.Toast) window.Toast.error("Minimum deposit amount is ₹100!");
      return;
    }

    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span class="inline-block animate-spin mr-2">⏳</span> Processing payment via UPI...`;

    setTimeout(() => {
      const bonus = Math.floor(this.depositAmount * this.activePromoBonus);
      const total = this.depositAmount + bonus;

      if (window.UserManager) {
        window.UserManager.addBalance(total, `UPI Deposit (${this.selectedDepositMethod.toUpperCase()}) + ₹${bonus} Bonus`);
      }

      btn.disabled = false;
      btn.innerHTML = originalText;
      document.getElementById("deposit-modal")?.classList.remove("active");

      if (window.Toast) {
        window.Toast.success(`✅ Deposit of ₹${this.depositAmount.toLocaleString('en-IN')} successful! ₹${total.toLocaleString('en-IN')} added to your wallet.`);
      }
    }, 1200);
  },

  processWithdrawal() {
    const input = document.getElementById("withdraw-amount-input");
    const ifscInput = document.getElementById("withdraw-ifsc-input");
    const accInput = document.getElementById("withdraw-acc-input");
    const btn = document.getElementById("confirm-withdraw-btn");

    const amount = parseInt(input?.value, 10) || 0;
    if (amount < 200) {
      if (window.Toast) window.Toast.error("Minimum withdrawal amount is ₹200!");
      return;
    }

    if (window.UserManager && !window.UserManager.hasBalance(amount)) {
      if (window.Toast) window.Toast.error("Insufficient balance for this withdrawal amount!");
      return;
    }

    if (!accInput?.value || !ifscInput?.value) {
      if (window.Toast) window.Toast.error("Please enter valid Bank Account number and IFSC code!");
      return;
    }

    btn.disabled = true;
    btn.innerHTML = `<span class="inline-block animate-spin mr-2">⏳</span> Verifying IMPS/UPI transfer...`;

    setTimeout(() => {
      if (window.UserManager) {
        window.UserManager.deductBalance(amount, `Bank Withdrawal (A/C ...${accInput.value.slice(-4)})`);
      }

      btn.disabled = false;
      btn.innerHTML = `Confirm Instant Withdrawal`;
      document.getElementById("withdraw-modal")?.classList.remove("active");

      if (window.Toast) {
        window.Toast.success(`💸 Withdrawal request of ₹${amount.toLocaleString('en-IN')} accepted! Funds will be credited to your bank account within 15 minutes.`);
      }
    }, 1500);
  }
};

window.WalletManager = WalletManager;
