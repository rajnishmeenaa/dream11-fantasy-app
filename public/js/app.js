/**
 * Main Application Orchestrator & State Manager
 */

// Toast Notifications System
const Toast = {
  container: null,

  init() {
    this.container = document.getElementById("toast-box");
    if (!this.container) {
      this.container = document.createElement("div");
      this.container.id = "toast-box";
      document.body.appendChild(this.container);
    }
  },

  show(message, type = "info") {
    if (!this.container) this.init();

    const toast = document.createElement("div");
    toast.className = `toast-msg ${type}`;
    
    let icon = "ℹ️";
    if (type === "success") icon = "✅";
    if (type === "error") icon = "⚠️";

    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    this.container.appendChild(toast);

    setTimeout(() => {
      toast.style.transition = "all 0.3s ease";
      toast.style.opacity = "0";
      toast.style.transform = "translateY(20px)";
      setTimeout(() => toast.remove(), 300);
    }, 3800);
  },

  success(msg) { this.show(msg, "success"); },
  error(msg) { this.show(msg, "error"); },
  info(msg) { this.show(msg, "info"); }
};
window.Toast = Toast;

// User & Wallet State Manager
const UserManager = {
  username: "Player_77",
  phone: "+91 98765 43210",
  balance: 2450.00,
  bonusBalance: 500.00,
  transactions: [
    { id: "TXN10982", desc: "Welcome Signup Bonus", amount: "+₹500.00", status: "Success", time: "Yesterday" },
    { id: "TXN10981", desc: "UPI Deposit (GPay)", amount: "+₹1,000.00", status: "Success", time: "Yesterday" },
    { id: "TXN10980", desc: "Won Crash Game (4.2x)", amount: "+₹950.00", status: "Success", time: "2 days ago" }
  ],

  init() {
    // Load from localStorage if present
    const saved = localStorage.getItem("winplay11_user");
    if (saved) {
      try {
        const d = JSON.parse(saved);
        this.balance = d.balance ?? this.balance;
        this.bonusBalance = d.bonusBalance ?? this.bonusBalance;
        this.transactions = d.transactions ?? this.transactions;
      } catch (e) {}
    }
    this.updateUI();
  },

  save() {
    localStorage.setItem("winplay11_user", JSON.stringify({
      balance: this.balance,
      bonusBalance: this.bonusBalance,
      transactions: this.transactions
    }));
  },

  hasBalance(amount) {
    return this.balance >= amount;
  },

  deductBalance(amount, reason = "Bet placed") {
    if (this.balance < amount) return false;
    this.balance -= amount;
    this.transactions.unshift({
      id: "TXN" + Math.floor(10000 + Math.random() * 90000),
      desc: reason,
      amount: `-₹${amount.toLocaleString('en-IN')}`,
      status: "Success",
      time: "Just now"
    });
    this.updateUI();
    this.save();
    return true;
  },

  addBalance(amount, reason = "Winnings") {
    this.balance += amount;
    this.transactions.unshift({
      id: "TXN" + Math.floor(10000 + Math.random() * 90000),
      desc: reason,
      amount: `+₹${amount.toLocaleString('en-IN')}`,
      status: "Success",
      time: "Just now"
    });
    this.updateUI();
    this.save();
  },

  updateUI() {
    const el = document.getElementById("nav-wallet-balance");
    if (el) {
      el.textContent = "₹" + this.balance.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    const bonusEl = document.getElementById("nav-bonus-balance");
    if (bonusEl) {
      bonusEl.textContent = "₹" + this.bonusBalance.toLocaleString('en-IN');
    }
    this.renderTransactions();
  },

  renderTransactions() {
    const container = document.getElementById("tx-history-list");
    if (!container) return;

    container.innerHTML = this.transactions.slice(0, 10).map(t => {
      const isCredit = t.amount.startsWith("+");
      return `
        <div class="flex items-center justify-between p-3 border-b border-slate-800 text-xs">
          <div>
            <p class="font-bold text-white">${t.desc}</p>
            <p class="text-slate-500 text-[10px]">${t.time} • ${t.id}</p>
          </div>
          <div class="text-right">
            <span class="font-black ${isCredit ? 'text-emerald-400' : 'text-rose-400'} num-font text-sm">${t.amount}</span>
            <p class="text-[10px] text-slate-400 font-semibold">${t.status}</p>
          </div>
        </div>
      `;
    }).join('');
  }
};
window.UserManager = UserManager;

// Main App Controller
const App = {
  currentTab: "fantasy", // fantasy, crash, mines, wheel, leaderboard, vip, referral
  heroCurrentSlide: 0,
  heroTotalSlides: 3,
  heroInterval: null,

  init() {
    Toast.init();
    UserManager.init();

    // Init submodules
    if (window.TickerManager) window.TickerManager.init();
    if (window.GullakManager) window.GullakManager.init();
    if (window.FantasyManager) window.FantasyManager.init();
    if (window.CrashGame) window.CrashGame.init();
    if (window.MinesGame) window.MinesGame.init();
    if (window.WheelGame) window.WheelGame.init();
    if (window.WalletManager) window.WalletManager.init();
    if (window.VipManager) window.VipManager.init();
    if (window.ReferralManager) window.ReferralManager.init();

    this.bindNavigation();
    this.initHeroCarousel();
    this.bindModals();
    this.renderLeaderboard();
  },

  bindNavigation() {
    // Top & Mobile Category Tabs
    document.querySelectorAll(".nav-category-tab").forEach(tab => {
      tab.addEventListener("click", (e) => {
        const targetView = e.currentTarget.getAttribute("data-tab");
        this.switchTab(targetView);
      });
    });

    // Mobile Bottom Bar Navigation
    document.querySelectorAll(".mobile-nav-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const targetView = e.currentTarget.getAttribute("data-tab");
        this.switchTab(targetView);
      });
    });
  },

  switchTab(tabId) {
    this.currentTab = tabId;

    // Update active tab styles
    document.querySelectorAll(".nav-category-tab").forEach(t => {
      const isMatch = t.getAttribute("data-tab") === tabId;
      if (isMatch) {
        t.className = "nav-category-tab px-4 py-2 rounded-xl text-sm font-bold bg-sky-500 text-white shadow-lg shadow-sky-500/25 flex items-center gap-2 whitespace-nowrap cursor-pointer transition";
      } else {
        t.className = "nav-category-tab px-4 py-2 rounded-xl text-sm font-semibold bg-[#171F33] text-slate-300 hover:text-white hover:bg-[#1E283D] flex items-center gap-2 whitespace-nowrap cursor-pointer transition";
      }
    });

    // Hide all view sections
    document.querySelectorAll(".view-section").forEach(sec => sec.classList.add("hidden"));

    // Show target section
    const targetEl = document.getElementById(`view-${tabId}`);
    if (targetEl) {
      targetEl.classList.remove("hidden");
      targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // Resize canvas if needed
    if (tabId === "crash" && window.CrashGame) {
      window.CrashGame.resizeCanvas();
    }
  },

  initHeroCarousel() {
    const slides = document.querySelectorAll(".hero-slide");
    const dots = document.querySelectorAll(".hero-carousel-dot");
    if (!slides.length) return;

    const showSlide = (idx) => {
      this.heroCurrentSlide = (idx + slides.length) % slides.length;
      slides.forEach((s, i) => {
        s.style.transform = `translateX(${(i - this.heroCurrentSlide) * 100}%)`;
      });
      dots.forEach((d, i) => {
        d.className = i === this.heroCurrentSlide 
          ? "hero-carousel-dot w-6 h-2 rounded-full bg-sky-400 transition-all duration-300"
          : "hero-carousel-dot w-2 h-2 rounded-full bg-slate-600 transition-all duration-300";
      });
    };

    showSlide(0);

    // Auto rotate
    this.heroInterval = setInterval(() => {
      showSlide(this.heroCurrentSlide + 1);
    }, 5000);

    document.getElementById("hero-prev-btn")?.addEventListener("click", () => {
      clearInterval(this.heroInterval);
      showSlide(this.heroCurrentSlide - 1);
    });
    document.getElementById("hero-next-btn")?.addEventListener("click", () => {
      clearInterval(this.heroInterval);
      showSlide(this.heroCurrentSlide + 1);
    });
    dots.forEach((dot, idx) => {
      dot.addEventListener("click", () => {
        clearInterval(this.heroInterval);
        showSlide(idx);
      });
    });
  },

  bindModals() {
    // Auth Modal
    const authModal = document.getElementById("auth-modal");
    document.getElementById("nav-login-btn")?.addEventListener("click", () => {
      authModal?.classList.add("active");
    });
    document.getElementById("close-auth-modal")?.addEventListener("click", () => {
      authModal?.classList.remove("active");
    });
    document.getElementById("auth-send-otp-btn")?.addEventListener("click", () => {
      const phone = document.getElementById("auth-phone-input")?.value;
      if (!phone || phone.length < 10) {
        Toast.error("Please enter a valid 10-digit mobile number");
        return;
      }
      Toast.success(`Verification code sent to +91 ${phone}! (Code: 1234)`);
      document.getElementById("auth-otp-section")?.classList.remove("hidden");
    });
    document.getElementById("auth-login-submit-btn")?.addEventListener("click", () => {
      Toast.success("Welcome back! Logged in successfully.");
      authModal?.classList.remove("active");
    });

    // Profile Dropdown
    const profileBtn = document.getElementById("nav-profile-btn");
    const profileDropdown = document.getElementById("profile-dropdown");
    if (profileBtn && profileDropdown) {
      profileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        profileDropdown.classList.toggle("hidden");
      });
      document.addEventListener("click", () => {
        profileDropdown.classList.add("hidden");
      });
    }

    // Transaction History Modal
    const txModal = document.getElementById("tx-history-modal");
    document.getElementById("open-tx-history-btn")?.addEventListener("click", () => {
      profileDropdown?.classList.add("hidden");
      txModal?.classList.add("active");
    });
    document.getElementById("close-tx-modal")?.addEventListener("click", () => {
      txModal?.classList.remove("active");
    });

    // Support Chat Modal
    const supportModal = document.getElementById("support-modal");
    document.querySelectorAll(".open-support-btn").forEach(btn => {
      btn.addEventListener("click", () => supportModal?.classList.add("active"));
    });
    document.getElementById("close-support-modal")?.addEventListener("click", () => {
      supportModal?.classList.remove("active");
    });
    document.getElementById("send-support-msg-btn")?.addEventListener("click", () => {
      const inp = document.getElementById("support-msg-input");
      if (!inp || !inp.value.trim()) return;
      const text = inp.value.trim();
      inp.value = "";

      const box = document.getElementById("support-chat-box");
      if (box) {
        box.innerHTML += `
          <div class="flex justify-end my-2">
            <div class="bg-sky-500 text-white text-xs px-3 py-2 rounded-xl rounded-tr-none max-w-[80%]">${text}</div>
          </div>
        `;
        setTimeout(() => {
          box.innerHTML += `
            <div class="flex justify-start my-2">
              <div class="bg-slate-800 border border-slate-700 text-slate-200 text-xs px-3 py-2 rounded-xl rounded-tl-none max-w-[80%]">
                Hello! Our agent is reviewing your query: "${text}". We're available 24/7 to resolve deposit, withdrawal, or fantasy contest questions!
              </div>
            </div>
          `;
          box.scrollTop = box.scrollHeight;
        }, 800);
      }
    });
  },

  renderLeaderboard() {
    const list = document.getElementById("leaderboard-list");
    if (!list) return;

    const ranks = [
      { rank: 1, name: "Kishore_King", badge: "🥇", points: "4,820 pts", prize: "₹1,50,000" },
      { rank: 2, name: "CricketGod_10", badge: "🥈", points: "4,510 pts", prize: "₹75,000" },
      { rank: 3, name: "BumrahBoom", badge: "🥉", points: "4,190 pts", prize: "₹35,000" },
      { rank: 4, name: "ThunderStriker", badge: "#4", points: "3,890 pts", prize: "₹15,000" },
      { rank: 5, name: "SuperStar_Raj", badge: "#5", points: "3,650 pts", prize: "₹10,000" },
      { rank: 6, name: "ApexRider", badge: "#6", points: "3,420 pts", prize: "₹5,000" },
      { rank: 7, name: "PlayMaster99", badge: "#7", points: "3,110 pts", prize: "₹3,000" },
      { rank: 8, name: "RanchiCaptain", badge: "#8", points: "2,980 pts", prize: "₹2,000" }
    ];

    list.innerHTML = ranks.map(r => `
      <div class="flex items-center justify-between p-3 rounded-xl bg-[#121622] border border-slate-800 hover:border-slate-700 transition">
        <div class="flex items-center gap-3">
          <span class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-sm ${r.rank <= 3 ? 'bg-amber-400/20 text-amber-300' : 'bg-slate-800 text-slate-400'}">${r.badge}</span>
          <div>
            <h5 class="font-bold text-white text-xs">${r.name}</h5>
            <span class="text-[10px] text-slate-400">${r.points}</span>
          </div>
        </div>
        <div class="text-right">
          <span class="font-black text-amber-400 num-font text-sm">${r.prize}</span>
          <p class="text-[10px] text-emerald-400 font-semibold">Prize</p>
        </div>
      </div>
    `).join('');
  }
};

window.App = App;
document.addEventListener("DOMContentLoaded", () => App.init());
