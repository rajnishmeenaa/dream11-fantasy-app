/**
 * Live Win & Contest Marquee Ticker
 */
const TickerManager = {
  events: [
    { user: "Rajesh***42", game: "Crash", win: "₹14,850", mult: "14.85x", time: "Just now" },
    { user: "Sunil***99", game: "IPL Mega", win: "₹1,50,000", rank: "Rank #1", time: "1m ago" },
    { user: "Vikram***18", game: "Mines", win: "₹4,600", mult: "9.20x", time: "2m ago" },
    { user: "Amit***07", game: "Cricket Contest", win: "₹25,000", rank: "Rank #3", time: "2m ago" },
    { user: "Pooja***55", game: "Limbo", win: "₹8,400", mult: "21.00x", time: "3m ago" },
    { user: "Karan***31", game: "Gullak Cash", win: "₹500", mult: "Daily Cash", time: "4m ago" },
    { user: "Rohit***88", game: "Crash", win: "₹32,200", mult: "32.20x", time: "4m ago" },
    { user: "Deepak***12", game: "IPL Mega", win: "₹75,000", rank: "Rank #2", time: "5m ago" },
    { user: "Ananya***29", game: "Lucky Wheel", win: "₹1,000", mult: "Jackpot", time: "6m ago" }
  ],

  init() {
    const track = document.getElementById("live-ticker-track");
    if (!track) return;

    this.render(track);

    // Periodically push fresh win
    setInterval(() => {
      this.pushRandomWin();
    }, 4500);
  },

  render(track) {
    const html = this.events.map(ev => `
      <div class="inline-flex items-center gap-2 bg-[#171F33] border border-[#2B3952] rounded-full px-3 py-1 text-xs text-slate-300 mr-4 shadow-sm">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="font-semibold text-white">${ev.user}</span>
        <span class="text-slate-400">won</span>
        <span class="font-bold text-amber-400">${ev.win}</span>
        <span class="text-slate-500">in</span>
        <span class="text-sky-400 font-medium">${ev.game}</span>
        ${ev.mult ? `<span class="bg-sky-950 text-sky-300 px-1.5 py-0.5 rounded text-[10px] font-bold">${ev.mult}</span>` : ''}
      </div>
    `).join('');

    // Duplicate for seamless infinite scrolling
    track.innerHTML = html + html;
  },

  pushRandomWin() {
    const names = ["Aarav", "Pawan", "Sneha", "Kunal", "Rakesh", "Suresh", "Manoj", "Harsh", "Divya"];
    const games = ["Crash", "Mines", "IPL Mega", "Limbo", "Cricket Contest"];
    const randomUser = names[Math.floor(Math.random() * names.length)] + "***" + Math.floor(10 + Math.random() * 89);
    const randomGame = games[Math.floor(Math.random() * games.length)];
    const randomMult = (1.5 + Math.random() * 25).toFixed(2) + "x";
    const randomWin = "₹" + (Math.floor(200 + Math.random() * 45000)).toLocaleString('en-IN');

    this.events.unshift({
      user: randomUser,
      game: randomGame,
      win: randomWin,
      mult: randomMult,
      time: "Just now"
    });
    if (this.events.length > 20) this.events.pop();

    const track = document.getElementById("live-ticker-track");
    if (track) this.render(track);
  }
};

window.TickerManager = TickerManager;
