# Apply payment UI to index.html and styles.css
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "public", "index.html")
STYLES_PATH = os.path.join(BASE_DIR, "public", "styles.css")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Replace #modal-wallet in index.html
wallet_start_tag = '<!-- 4. WALLET & ADD CASH MODAL -->'
wallet_end_tag = '<!-- 5. CREATE PRIVATE CONTEST MODAL -->'

new_wallet_modal = '''<!-- 4. WALLET, UPI GATEWAY & PASSBOOK MODAL -->
  <div class="modal-overlay hidden" id="modal-wallet">
    <div class="bottom-sheet-modal wallet-sheet">
      <div class="sheet-handle"></div>
      <div class="sheet-header">
        <h4>My Dream11 Wallet</h4>
        <button class="sheet-close-btn" id="btn-close-wallet">✕</button>
      </div>
      <div class="sheet-body">
        
        <!-- Wallet Navigation Tabs -->
        <div class="wallet-nav-tabs">
          <button class="w-nav-tab active" data-wtab="deposit">💳 Add Cash</button>
          <button class="w-nav-tab" data-wtab="withdraw">🏦 Withdraw</button>
          <button class="w-nav-tab" data-wtab="passbook">📜 Passbook</button>
        </div>

        <!-- TAB 1: ADD CASH / UPI DEPOSIT -->
        <div class="w-tab-content" id="wtab-deposit">
          <div class="wallet-balance-card">
            <span class="w-label">TOTAL BALANCE</span>
            <h2 id="modal-total-balance">₹1,500</h2>
          </div>

          <div class="wallet-breakdown-grid">
            <div class="w-break-item">
              <span class="w-type">Deposited Cash</span>
              <strong id="w-deposited">₹500</strong>
              <span class="w-hint">Usable in all contests</span>
            </div>
            <div class="w-break-item">
              <span class="w-type">Winnings</span>
              <strong id="w-winnings">₹650</strong>
              <button class="btn-withdraw-small" id="btn-quick-goto-withdraw">Withdraw</button>
            </div>
            <div class="w-break-item full">
              <span class="w-type">Cash Bonus</span>
              <strong id="w-bonus">₹350</strong>
              <span class="w-hint">Max 20% usable per contest</span>
            </div>
          </div>

          <div class="add-cash-section">
            <h5>Select Deposit Amount</h5>
            <div class="quick-amounts-bar">
              <button class="btn-amt" data-amt="50">+ ₹50</button>
              <button class="btn-amt active" data-amt="100">+ ₹100</button>
              <button class="btn-amt" data-amt="250">+ ₹250</button>
              <button class="btn-amt" data-amt="500">+ ₹500</button>
            </div>
            <div class="custom-amt-row">
              <span class="currency-prefix">₹</span>
              <input type="number" id="input-custom-deposit-amt" value="100" min="10" max="50000" placeholder="Enter custom amount">
            </div>

            <h5 style="margin-top:14px">Select UPI Payment Method</h5>
            <div class="upi-methods-grid">
              <div class="upi-method-card selected" data-method="gpay">
                <div class="upi-app-icon gpay">GPay</div>
                <div class="upi-app-name">Google Pay</div>
                <span class="upi-fast-badge">INSTANT</span>
              </div>
              <div class="upi-method-card" data-method="phonepe">
                <div class="upi-app-icon phonepe">Pe</div>
                <div class="upi-app-name">PhonePe</div>
                <span class="upi-fast-badge">POPULAR</span>
              </div>
              <div class="upi-method-card" data-method="paytm">
                <div class="upi-app-icon paytm">Paytm</div>
                <div class="upi-app-name">Paytm UPI</div>
              </div>
              <div class="upi-method-card" data-method="qr">
                <div class="upi-app-icon qr">🔳</div>
                <div class="upi-app-name">Scan QR Code</div>
              </div>
            </div>

            <!-- Dynamic QR Code Container (Visible when QR selected) -->
            <div id="upi-qr-container" class="upi-qr-panel hidden">
              <div class="qr-box">
                <svg class="qr-svg" viewBox="0 0 160 160" width="140" height="140">
                  <rect width="160" height="160" fill="#ffffff"/>
                  <rect x="10" y="10" width="40" height="40" fill="#0f172a"/>
                  <rect x="18" y="18" width="24" height="24" fill="#ffffff"/>
                  <rect x="24" y="24" width="12" height="12" fill="#0f172a"/>
                  <rect x="110" y="10" width="40" height="40" fill="#0f172a"/>
                  <rect x="118" y="18" width="24" height="24" fill="#ffffff"/>
                  <rect x="124" y="24" width="12" height="12" fill="#0f172a"/>
                  <rect x="10" y="110" width="40" height="40" fill="#0f172a"/>
                  <rect x="18" y="118" width="24" height="24" fill="#ffffff"/>
                  <rect x="24" y="124" width="12" height="12" fill="#0f172a"/>
                  <rect x="60" y="20" width="10" height="10" fill="#D11A2A"/>
                  <rect x="80" y="15" width="15" height="10" fill="#0f172a"/>
                  <rect x="70" y="35" width="15" height="15" fill="#0f172a"/>
                  <rect x="20" y="65" width="15" height="10" fill="#0f172a"/>
                  <rect x="45" y="70" width="10" height="20" fill="#D11A2A"/>
                  <rect x="65" y="65" width="30" height="30" fill="#D11A2A" rx="6"/>
                  <text x="80" y="86" font-size="16" font-weight="bold" fill="white" text-anchor="middle">D</text>
                  <rect x="105" y="70" width="15" height="15" fill="#0f172a"/>
                  <rect x="130" y="60" width="10" height="20" fill="#0f172a"/>
                  <rect x="60" y="115" width="20" height="10" fill="#0f172a"/>
                  <rect x="90" y="110" width="10" height="20" fill="#0f172a"/>
                  <rect x="110" y="115" width="20" height="15" fill="#0f172a"/>
                  <rect x="135" y="135" width="15" height="15" fill="#D11A2A"/>
                </svg>
              </div>
              <div class="qr-meta">
                <strong>Scan with Any UPI App</strong>
                <p style="font-size:11px; color:var(--text-muted); margin:2px 0 6px">Google Pay, PhonePe, Paytm or BHIM</p>
                <span class="upi-id-pill" id="qr-upi-id-text">dream11.pay@icici</span>
              </div>
            </div>

            <button class="btn-primary" id="btn-proceed-upi-pay" style="width:100%; margin-top:14px; padding:14px; font-size:14px; font-weight:900">
              PAY ₹100 VIA UPI →
            </button>
            <div style="text-align:center; font-size:10px; color:var(--text-muted); margin-top:8px">
              🔒 256-Bit SSL Encrypted • Powered by NPCI UPI Gateway
            </div>
          </div>
        </div>

        <!-- TAB 2: WITHDRAW WINNINGS -->
        <div class="w-tab-content hidden" id="wtab-withdraw">
          <div class="withdraw-hero-card">
            <span class="wh-label">WITHDRAWABLE WINNINGS</span>
            <h2 id="wh-winnings-amount">₹650</h2>
            <div class="wh-badge">⚡ Instant 24x7 IMPS Payout • Zero Withdrawal Fee</div>
          </div>

          <div class="admin-form" style="margin-top:14px">
            <div class="form-group">
              <div style="display:flex; justify-content:space-between; align-items:center">
                <label>Withdrawal Amount (₹)</label>
                <button type="button" class="btn-link-all" id="btn-withdraw-max">Withdraw All</button>
              </div>
              <input type="number" id="input-withdraw-amount" value="200" min="50" placeholder="Min ₹50">
              <span style="font-size:10px; color:var(--text-muted); margin-top:2px">Min: ₹50 • Max: Available Winnings</span>
            </div>

            <div class="form-group" style="margin-top:10px">
              <label>Select Transfer Destination</label>
              <div class="payout-modes-row">
                <label class="payout-mode-opt selected">
                  <input type="radio" name="payout-mode" value="upi" checked>
                  <span>⚡ Instant UPI VPA</span>
                </label>
                <label class="payout-mode-opt">
                  <input type="radio" name="payout-mode" value="bank">
                  <span>🏦 Bank Account (IMPS)</span>
                </label>
              </div>
            </div>

            <!-- UPI Destination Field -->
            <div id="payout-field-upi" class="payout-fields-box">
              <div class="form-group">
                <label>Enter UPI ID / VPA</label>
                <input type="text" id="input-payout-upi" value="champion@okhdfcbank" placeholder="e.g. yourname@oksbi">
              </div>
            </div>

            <!-- Bank Destination Fields -->
            <div id="payout-field-bank" class="payout-fields-box hidden">
              <div class="form-group">
                <label>Bank Account Number</label>
                <input type="text" id="input-payout-acc" value="987654321012" placeholder="Account Number">
              </div>
              <div class="form-group">
                <label>IFSC Code</label>
                <input type="text" id="input-payout-ifsc" value="HDFC0001234" placeholder="e.g. HDFC0001234">
              </div>
            </div>

            <button type="button" class="btn-primary" id="btn-submit-withdraw-request" style="width:100%; margin-top:14px; background:#16a34a">
              🔒 VERIFY & WITHDRAW NOW →
            </button>
          </div>
        </div>

        <!-- TAB 3: PASSBOOK STATEMENT -->
        <div class="w-tab-content hidden" id="wtab-passbook">
          <div class="passbook-header-row">
            <div>
              <h5 style="font-size:13px; font-weight:800">Account Passbook</h5>
              <span style="font-size:11px; color:var(--text-muted)">Detailed ledger of all credits & debits</span>
            </div>
            <button class="btn-refresh-small" id="btn-refresh-passbook">🔄 Refresh</button>
          </div>

          <!-- Passbook Filter Chips -->
          <div class="passbook-filters">
            <button class="pb-filter active" data-filter="all">All</button>
            <button class="pb-filter" data-filter="deposit">Deposits (+)</button>
            <button class="pb-filter" data-filter="withdrawal">Withdrawals (-)</button>
            <button class="pb-filter" data-filter="contest">Contests (-)</button>
            <button class="pb-filter" data-filter="winning">Winnings (+)</button>
          </div>

          <!-- Transactions Ledger List -->
          <div class="passbook-items-list" id="passbook-list"></div>
        </div>

      </div>
    </div>
  </div>
'''

p1 = html.find(wallet_start_tag)
p2 = html.find(wallet_end_tag)
if p1 != -1 and p2 != -1:
    html = html[:p1] + new_wallet_modal + '\n  ' + html[p2:]

# Add Simulated Payment Gateway Modal, OTP Modal, and IMPS Receipt Modal
extra_payment_modals = '''  <!-- 8. SIMULATED PAYMENT GATEWAY PROCESSING MODAL -->
  <div class="modal-overlay hidden" id="modal-payment-gateway">
    <div class="bottom-sheet-modal" style="text-align:center; padding:24px 20px">
      <!-- State 1: Processing -->
      <div id="pg-state-processing">
        <div class="gateway-spinner-wrap">
          <div class="gateway-spinner"></div>
          <div class="gateway-center-icon">🔒</div>
        </div>
        <h4 style="font-size:17px; font-weight:900; margin-top:16px" id="pg-processing-title">Connecting to Bank UPI Gateway...</h4>
        <p style="font-size:12px; color:var(--text-muted); margin-top:6px" id="pg-processing-desc">Authenticating transaction with NPCI & HDFC Bank servers</p>
        <div class="gateway-bank-pills">
          <span class="gb-pill">GPay</span>
          <span class="gb-pill">PhonePe</span>
          <span class="gb-pill">NPCI UPI</span>
        </div>
      </div>

      <!-- State 2: Success -->
      <div id="pg-state-success" class="hidden">
        <div class="success-tick-wrap">
          <div class="success-circle">✓</div>
        </div>
        <h4 style="font-size:20px; font-weight:900; color:#15803d; margin-top:14px">Payment Successful!</h4>
        <h2 style="font-size:28px; font-weight:900; margin-top:4px" id="pg-success-amount">₹100</h2>
        <p style="font-size:12px; color:var(--text-muted); margin-top:4px">Credited to your Dream11 Deposited Balance</p>
        <div class="pg-utr-box">
          <span>Transaction UTR:</span>
          <strong id="pg-success-utr">UPI/428901824901</strong>
        </div>
        <button class="btn-primary" id="btn-pg-done" style="width:100%; margin-top:16px">
          CONTINUE PLAYING ✓
        </button>
      </div>
    </div>
  </div>

  <!-- 9. SIMULATED BANK SECURITY OTP MODAL -->
  <div class="modal-overlay hidden" id="modal-bank-otp">
    <div class="bottom-sheet-modal" style="padding:20px">
      <div class="sheet-handle"></div>
      <div class="sheet-header">
        <h4>Bank Security Verification</h4>
        <button class="sheet-close-btn" id="btn-close-bank-otp">✕</button>
      </div>
      <div class="sheet-body">
        <p style="font-size:12px; color:var(--text-muted); margin-bottom:14px">
          Enter the 6-digit Bank Security OTP dispatched to your registered mobile <strong>+91 98*** **420</strong> to authenticate IMPS withdrawal:
        </p>

        <div class="otp-input-container">
          <input type="text" id="input-otp-val" maxlength="6" value="123456" placeholder="1 2 3 4 5 6" style="letter-spacing:10px; text-align:center; font-size:22px; font-weight:900; padding:12px">
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px">
          <span style="font-size:11px; color:#15803d; font-weight:700">✓ OTP Sent (Valid for 10:00m)</span>
          <button type="button" class="btn-link-all" id="btn-autofill-otp">⚡ Use Test OTP (123456)</button>
        </div>

        <button type="button" class="btn-primary" id="btn-confirm-otp-withdraw" style="width:100%; margin-top:16px; background:#16a34a">
          AUTHORIZE IMPS TRANSFER ✓
        </button>
      </div>
    </div>
  </div>

  <!-- 10. FORMAL IMPS WITHDRAWAL RECEIPT MODAL -->
  <div class="modal-overlay hidden" id="modal-withdrawal-receipt">
    <div class="bottom-sheet-modal" style="padding:20px">
      <div class="sheet-handle"></div>
      <div class="receipt-card">
        <div class="receipt-top-banner">
          <span class="rc-badge">IMPS Payout</span>
          <div class="rc-icon">✓</div>
          <h4>Transfer Successful!</h4>
          <h2 id="rc-amount">₹200</h2>
        </div>
        <div class="receipt-details">
          <div class="rc-row">
            <span>Transfer Type:</span>
            <strong>Immediate Payment Service (IMPS)</strong>
          </div>
          <div class="rc-row">
            <span>Reference UTR:</span>
            <strong id="rc-utr" style="color:var(--primary)">IMPS8910248921</strong>
          </div>
          <div class="rc-row">
            <span>Beneficiary:</span>
            <strong id="rc-dest">champion@okhdfcbank</strong>
          </div>
          <div class="rc-row">
            <span>Date & Time:</span>
            <strong id="rc-time">Just now</strong>
          </div>
          <div class="rc-row">
            <span>Status:</span>
            <strong style="color:#15803d">PROCESSED (Zero Fees)</strong>
          </div>
        </div>
        <div class="receipt-footer-stamp">
          <span>🛡️ Verified by Reserve Bank of India (RBI) / NPCI Network</span>
        </div>
      </div>
      <button class="btn-primary" id="btn-close-receipt" style="width:100%; margin-top:14px">
        DONE ✓
      </button>
    </div>
  </div>
'''

if 'modal-payment-gateway' not in html:
    html = html.replace(
        '<!-- Toast Notification Container -->',
        extra_payment_modals + '\n  <!-- Toast Notification Container -->'
    )

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("index.html upgraded with payment modals!")

# =========================================================================
# 2. UPGRADE styles.css
# =========================================================================
with open(STYLES_PATH, "r", encoding="utf-8") as f:
    css = f.read()

payment_styles = '''
/* Wallet Sub-Tabs */
.wallet-nav-tabs {
  display: flex;
  background: #f1f5f9;
  border-radius: var(--radius-full);
  padding: 4px;
  margin-bottom: 14px;
}
.w-nav-tab {
  flex: 1;
  background: transparent;
  border: none;
  padding: 8px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 800;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}
.w-nav-tab.active {
  background: #fff;
  color: var(--text-main);
  box-shadow: var(--shadow-sm);
}

/* Custom Deposit Input */
.custom-amt-row {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 4px 12px;
  margin-top: 8px;
}
.currency-prefix {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-muted);
  margin-right: 6px;
}
.custom-amt-row input {
  flex: 1;
  border: none;
  font-size: 16px;
  font-weight: 800;
  outline: none;
  color: var(--text-main);
}

/* UPI Methods Grid */
.upi-methods-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 8px;
}
.upi-method-card {
  background: #fff;
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  position: relative;
  transition: all 0.15s;
}
.upi-method-card.selected {
  border-color: var(--primary);
  background: #fff1f2;
}
.upi-app-icon {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 900;
  color: #fff;
}
.upi-app-icon.gpay { background: #1a73e8; }
.upi-app-icon.phonepe { background: #5f259f; }
.upi-app-icon.paytm { background: #00b9f1; }
.upi-app-icon.qr { background: #1e293b; font-size: 20px; }
.upi-app-name { font-size: 11px; font-weight: 700; color: var(--text-main); }
.upi-fast-badge {
  position: absolute;
  top: 4px;
  right: 6px;
  font-size: 8px;
  font-weight: 900;
  background: #dcfce7;
  color: #15803d;
  padding: 1px 5px;
  border-radius: 4px;
}

/* Dynamic QR Code Panel */
.upi-qr-panel {
  background: #f8fafc;
  border: 1.5px dashed #cbd5e1;
  border-radius: var(--radius-lg);
  padding: 16px;
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.qr-box {
  background: #fff;
  padding: 6px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.qr-meta strong { font-size: 13px; display: block; }
.upi-id-pill {
  display: inline-block;
  background: #e2e8f0;
  color: #334155;
  font-size: 10px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-full);
}

/* Withdraw Section Styles */
.withdraw-hero-card {
  background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
  color: #fff;
  border-radius: var(--radius-lg);
  padding: 16px;
  text-align: center;
}
.wh-label { font-size: 11px; color: #a7f3d0; font-weight: 700; letter-spacing: 0.5px; }
.withdraw-hero-card h2 { font-size: 30px; font-weight: 900; color: #fde047; margin: 4px 0; }
.wh-badge { font-size: 10px; color: #d1fae5; font-weight: 600; }
.btn-link-all { background: transparent; border: none; color: var(--primary); font-size: 11px; font-weight: 800; cursor: pointer; }

.payout-modes-row {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}
.payout-mode-opt {
  flex: 1;
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 11px;
  font-weight: 700;
}
.payout-mode-opt.selected {
  border-color: #16a34a;
  background: #f0fdf4;
  color: #166534;
}
.payout-fields-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: var(--radius-md);
  padding: 12px;
  margin-top: 8px;
}

/* Passbook Styles */
.passbook-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.btn-refresh-small {
  background: #f1f5f9;
  border: none;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  cursor: pointer;
}
.passbook-filters {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  scrollbar-width: none;
  margin-bottom: 12px;
}
.passbook-filters::-webkit-scrollbar { display: none; }
.pb-filter {
  background: #f8fafc;
  border: 1px solid var(--border-light);
  font-size: 11px;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  cursor: pointer;
  white-space: nowrap;
  color: var(--text-muted);
}
.pb-filter.active {
  background: #1e293b;
  color: #fff;
  border-color: #1e293b;
}

.passbook-items-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 420px;
  overflow-y: auto;
}
.pb-txn-card {
  background: #fff;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.15s;
}
.pb-txn-card:hover { border-color: var(--primary); transform: translateY(-1px); }
.pb-txn-left { display: flex; align-items: center; gap: 10px; }
.pb-txn-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}
.pb-txn-icon.credit { background: #dcfce7; color: #15803d; }
.pb-txn-icon.debit { background: #fee2e2; color: #b91c1c; }
.pb-txn-meta strong { font-size: 12px; color: var(--text-main); display: block; }
.pb-txn-sub { font-size: 10px; color: var(--text-muted); }
.pb-txn-right { text-align: right; }
.pb-txn-amt { font-size: 14px; font-weight: 900; }
.pb-txn-amt.credit { color: #15803d; }
.pb-txn-amt.debit { color: #b91c1c; }
.pb-txn-status { font-size: 9px; font-weight: 800; padding: 1px 6px; border-radius: 4px; background: #dcfce7; color: #15803d; display: inline-block; }

/* Gateway Processing Spinner */
.gateway-spinner-wrap {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 10px auto;
}
.gateway-spinner {
  width: 80px;
  height: 80px;
  border: 4px solid #e2e8f0;
  border-top-color: #1a73e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { 100% { transform: rotate(360deg); } }
.gateway-center-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 26px;
}
.gateway-bank-pills {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 14px;
}
.gb-pill {
  background: #f1f5f9;
  font-size: 10px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  color: var(--text-muted);
}
.success-tick-wrap {
  width: 70px;
  height: 70px;
  background: #dcfce7;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}
.success-circle { font-size: 36px; font-weight: 900; color: #15803d; }
.pg-utr-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: var(--radius-md);
  padding: 10px;
  margin-top: 12px;
  font-size: 11px;
}

/* Formal Receipt Card */
.receipt-card {
  background: #fff;
  border: 1px solid #cbd5e1;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
.receipt-top-banner {
  background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
  color: #fff;
  padding: 16px;
  text-align: center;
  position: relative;
}
.rc-badge {
  position: absolute;
  top: 10px;
  left: 12px;
  background: rgba(255,255,255,0.2);
  font-size: 9px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: var(--radius-full);
}
.rc-icon {
  width: 42px;
  height: 42px;
  background: #fff;
  color: #047857;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 900;
  margin: 0 auto 6px;
}
.receipt-details {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 12px;
  border-bottom: 1px dashed #cbd5e1;
}
.rc-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.rc-row span { color: var(--text-muted); }
.receipt-footer-stamp {
  padding: 10px;
  background: #f8fafc;
  text-align: center;
  font-size: 10px;
  color: #64748b;
  font-weight: 600;
}
'''

if 'wallet-nav-tabs' not in css:
    css += payment_styles

with open(STYLES_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("styles.css upgraded with payment and passbook styles!")
