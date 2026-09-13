/**
 * Lucky Spin Wheel Game
 */
const WheelGame = {
  canvas: null,
  ctx: null,
  isSpinning: false,
  currentAngle: 0,
  prizes: [
    { label: "₹50 Cash", value: 50, type: "cash", color: "#F59E0B" },
    { label: "Free Contest", value: 49, type: "ticket", color: "#00BBFF" },
    { label: "₹100 Cash", value: 100, type: "cash", color: "#10B981" },
    { label: "₹20 Cash", value: 20, type: "cash", color: "#8B5CF6" },
    { label: "iPhone Ticket", value: 0, type: "special", color: "#EC4899" },
    { label: "₹500 Jackpot", value: 500, type: "cash", color: "#EF4444" },
    { label: "Try Tomorrow", value: 0, type: "none", color: "#64748B" },
    { label: "2x Bonus Code", value: 0, type: "bonus", color: "#F97316" }
  ],

  init() {
    this.canvas = document.getElementById("wheel-canvas");
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");

    this.drawWheel();
    document.getElementById("wheel-spin-btn")?.addEventListener("click", () => this.spin());
  },

  drawWheel() {
    if (!this.ctx) return;
    const w = this.canvas.width;
    const h = this.canvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const radius = w / 2 - 12;
    const count = this.prizes.length;
    const arc = (Math.PI * 2) / count;

    this.ctx.clearRect(0, 0, w, h);

    this.ctx.save();
    this.ctx.translate(cx, cy);
    this.ctx.rotate(this.currentAngle);

    for (let i = 0; i < count; i++) {
      const angle = i * arc;
      this.ctx.beginPath();
      this.ctx.fillStyle = this.prizes[i].color;
      this.ctx.moveTo(0, 0);
      this.ctx.arc(0, 0, radius, angle, angle + arc);
      this.ctx.lineTo(0, 0);
      this.ctx.fill();

      // Border between segments
      this.ctx.strokeStyle = "#101218";
      this.ctx.lineWidth = 2;
      this.ctx.stroke();

      // Text label
      this.ctx.save();
      this.ctx.rotate(angle + arc / 2);
      this.ctx.textAlign = "right";
      this.ctx.fillStyle = "#FFFFFF";
      this.ctx.font = "bold 12px Montserrat, sans-serif";
      this.ctx.shadowColor = "rgba(0,0,0,0.8)";
      this.ctx.shadowBlur = 4;
      this.ctx.fillText(this.prizes[i].label, radius - 18, 5);
      this.ctx.restore();
    }

    // Center peg
    this.ctx.beginPath();
    this.ctx.arc(0, 0, 24, 0, Math.PI * 2);
    this.ctx.fillStyle = "#101218";
    this.ctx.fill();
    this.ctx.strokeStyle = "#FFD156";
    this.ctx.lineWidth = 3;
    this.ctx.stroke();

    this.ctx.restore();
  },

  spin() {
    if (this.isSpinning) return;

    this.isSpinning = true;
    const btn = document.getElementById("wheel-spin-btn");
    if (btn) {
      btn.disabled = true;
      btn.classList.add("opacity-50", "pointer-events-none");
    }

    const count = this.prizes.length;
    const arc = (Math.PI * 2) / count;

    // Pick a random prize index (weigh towards cash wins)
    const winningIdx = Math.floor(Math.random() * count);
    const prize = this.prizes[winningIdx];

    // Total rotations + angle offset to stop on target segment (pointer is at top 3*PI/2)
    const extraRounds = 5 + Math.floor(Math.random() * 3);
    const targetAngle = (extraRounds * Math.PI * 2) + ((count - winningIdx - 0.5) * arc) - (Math.PI / 2);

    const startTime = performance.now();
    const duration = 4000;
    const startAngle = this.currentAngle;

    const animate = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(1, elapsed / duration);

      // Ease out cubic
      const easeOut = 1 - Math.pow(1 - progress, 3);
      this.currentAngle = startAngle + (targetAngle - startAngle) * easeOut;

      this.drawWheel();

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        this.isSpinning = false;
        if (btn) {
          btn.disabled = false;
          btn.classList.remove("opacity-50", "pointer-events-none");
        }
        this.reward(prize);
      }
    };

    requestAnimationFrame(animate);
  },

  reward(prize) {
    if (prize.type === "cash") {
      if (window.UserManager) window.UserManager.addBalance(prize.value, `Lucky Wheel: ${prize.label}`);
      if (window.Toast) window.Toast.success(`🎉 Congratulations! You won ${prize.label}! Credited to your wallet.`);
    } else if (prize.type === "ticket") {
      if (window.Toast) window.Toast.success(`🎟️ Woohoo! You won a Free ₹49 Contest Ticket!`);
    } else if (prize.type === "special") {
      if (window.Toast) window.Toast.success(`📱 Lucky Entry! Your iPhone 16 Pro Mega Draw Ticket has been registered.`);
    } else if (prize.type === "bonus") {
      if (window.Toast) window.Toast.success(`🔥 Bonus code 'WIN2X' unlocked for your next deposit!`);
    } else {
      if (window.Toast) window.Toast.info(`Better luck tomorrow! Come back every day for free spins.`);
    }
  }
};

window.WheelGame = WheelGame;
