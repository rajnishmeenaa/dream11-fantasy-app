# Append and configure payment suite logic in public/app.js
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.join(BASE_DIR, "public", "app.js")

with open(APP_PATH, "r", encoding="utf-8") as f:
    app_js = f.read()

# Check if setupPaymentControllers is already called in initApp
if 'setupPaymentControllers();' not in app_js:
    app_js = app_js.replace(
        'setupPrivateContestControllers();',
        'setupPrivateContestControllers();\n  setupPaymentControllers();'
    )

payment_js_code = r'''
// =========================================================================
// SIMULATED UPI & PAYMENT GATEWAY CONTROLLERS (Feature Suite 3)
// =========================================================================

let selectedDepositMethod = 'gpay';
let selectedDepositAmount = 100;
let pendingWithdrawalData = null;
let activePassbookFilter = 'all';

function setupPaymentControllers() {
  // 1. Wallet Sub-Tabs Switcher
  document.querySelectorAll('.wallet-nav-tabs .w-nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.wallet-nav-tabs .w-nav-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.wtab;
      document.getElementById('wtab-deposit').classList.toggle('hidden', target !== 'deposit');
      document.getElementById('wtab-withdraw').classList.toggle('hidden', target !== 'withdraw');
      document.getElementById('wtab-passbook').classList.toggle('hidden', target !== 'passbook');

      if (target === 'withdraw') syncWithdrawalUI();
      if (target === 'passbook') loadPassbookStatement();
    });
  });

  // Quick link from wallet breakdown to withdraw tab
  document.getElementById('btn-quick-goto-withdraw')?.addEventListener('click', () => {
    const withdrawTab = document.querySelector('.w-nav-tab[data-wtab="withdraw"]');
    if (withdrawTab) withdrawTab.click();
  });

  // 2. Deposit Amount Chips
  document.querySelectorAll('.quick-amounts-bar .btn-amt').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.quick-amounts-bar .btn-amt').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedDepositAmount = parseInt(btn.dataset.amt) || 100;
      const customInput = document.getElementById('input-custom-deposit-amt');
      if (customInput) customInput.value = selectedDepositAmount;
      updateDepositPayButton();
    });
  });

  // Custom deposit input change
  document.getElementById('input-custom-deposit-amt')?.addEventListener('input', (e) => {
    const val = parseInt(e.target.value) || 0;
    selectedDepositAmount = val;
    document.querySelectorAll('.quick-amounts-bar .btn-amt').forEach(b => {
      b.classList.toggle('active', parseInt(b.dataset.amt) === val);
    });
    updateDepositPayButton();
  });

  // 3. UPI Method Selection
  document.querySelectorAll('.upi-method-card').forEach(card => {
    card.addEventListener('click', () => {
      document.querySelectorAll('.upi-method-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      selectedDepositMethod = card.dataset.method;

      // Toggle QR panel
      const qrPanel = document.getElementById('upi-qr-container');
      if (qrPanel) qrPanel.classList.toggle('hidden', selectedDepositMethod !== 'qr');

      updateDepositPayButton();
    });
  });

  // 4. Pay via UPI Button
  document.getElementById('btn-proceed-upi-pay')?.addEventListener('click', () => {
    if (selectedDepositAmount < 10) {
      showToast('Minimum deposit amount is ₹10', 'error');
      return;
    }
    startUPIPaymentSimulation(selectedDepositAmount, selectedDepositMethod);
  });

  // Payment Gateway Done button
  document.getElementById('btn-pg-done')?.addEventListener('click', () => {
    document.getElementById('modal-payment-gateway').classList.add('hidden');
    document.getElementById('modal-wallet').classList.remove('hidden');
  });

  // 5. Withdrawal Logic
  document.getElementById('btn-withdraw-max')?.addEventListener('click', () => {
    const winnings = state.user?.wallet?.winnings || 0;
    document.getElementById('input-withdraw-amount').value = winnings;
  });

  // Payout mode radio toggle
  document.querySelectorAll('input[name="payout-mode"]').forEach(r => {
    r.addEventListener('change', () => {
      document.querySelectorAll('.payout-mode-opt').forEach(opt => opt.classList.remove('selected'));
      r.closest('.payout-mode-opt')?.classList.add('selected');
      const isBank = (r.value === 'bank');
      document.getElementById('payout-field-bank').classList.toggle('hidden', !isBank);
      document.getElementById('payout-field-upi').classList.toggle('hidden', isBank);
    });
  });

  // Submit Withdraw Request -> opens OTP
  document.getElementById('btn-submit-withdraw-request')?.addEventListener('click', () => {
    const amount = parseInt(document.getElementById('input-withdraw-amount').value) || 0;
    const winnings = state.user?.wallet?.winnings || 0;
    if (amount < 50) {
      showToast('Minimum withdrawal amount is ₹50', 'error');
      return;
    }
    if (amount > winnings) {
      showToast(`Insufficient winnings! Available: ₹${winnings}`, 'error');
      return;
    }

    const mode = document.querySelector('input[name="payout-mode"]:checked').value;
    const upiId = document.getElementById('input-payout-upi').value.trim();
    const bankAcc = document.getElementById('input-payout-acc').value.trim();
    const ifsc = document.getElementById('input-payout-ifsc').value.trim();

    pendingWithdrawalData = { amount, method: mode, upiId, bankAccount: bankAcc, ifsc };
    document.getElementById('modal-bank-otp').classList.remove('hidden');
  });

  // Close OTP Modal
  document.getElementById('btn-close-bank-otp')?.addEventListener('click', () => {
    document.getElementById('modal-bank-otp').classList.add('hidden');
  });

  // Auto-fill Test OTP
  document.getElementById('btn-autofill-otp')?.addEventListener('click', () => {
    document.getElementById('input-otp-val').value = '123456';
  });

  // Confirm OTP & Authorize IMPS
  document.getElementById('btn-confirm-otp-withdraw')?.addEventListener('click', async () => {
    const otp = document.getElementById('input-otp-val').value.trim();
    if (otp !== '123456' && otp.length !== 6) {
      showToast('Invalid Bank OTP! Please enter test OTP: 123456', 'error');
      return;
    }

    if (!pendingWithdrawalData) return;
    const payload = { ...pendingWithdrawalData, otp };
    const res = await fetchAPI('/api/user/wallet/withdraw', 'POST', payload);

    if (res && res.success) {
      state.user.wallet = res.wallet;
      updateUserHeader();
      syncWithdrawalUI();

      document.getElementById('modal-bank-otp').classList.add('hidden');

      // Populate Receipt Modal
      document.getElementById('rc-amount').textContent = `₹${payload.amount.toLocaleString('en-IN')}`;
      document.getElementById('rc-utr').textContent = res.impsReference;
      document.getElementById('rc-dest').textContent = payload.method === 'upi' ? payload.upiId : `Bank A/C ...${payload.bankAccount.slice(-4)}`;
      document.getElementById('rc-time').textContent = 'Just now';
      document.getElementById('modal-withdrawal-receipt').classList.remove('hidden');

      audio.playWinFanfare();
      showToast(`⚡ IMPS Transfer of ₹${payload.amount} processed instantly!`, 'success');
      pendingWithdrawalData = null;
    } else {
      showToast(res ? res.message : 'Withdrawal failed', 'error');
    }
  });

  // Close IMPS Receipt
  document.getElementById('btn-close-receipt')?.addEventListener('click', () => {
    document.getElementById('modal-withdrawal-receipt').classList.add('hidden');
  });

  // 6. Passbook Filters
  document.querySelectorAll('.passbook-filters .pb-filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.passbook-filters .pb-filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activePassbookFilter = btn.dataset.filter;
      renderPassbookList();
    });
  });

  document.getElementById('btn-refresh-passbook')?.addEventListener('click', () => {
    loadPassbookStatement();
    showToast('Passbook refreshed ✓', 'success');
  });
}

function updateDepositPayButton() {
  const btn = document.getElementById('btn-proceed-upi-pay');
  if (!btn) return;
  const labels = {
    gpay: 'Google Pay',
    phonepe: 'PhonePe',
    paytm: 'Paytm',
    qr: 'UPI QR'
  };
  const methodName = labels[selectedDepositMethod] || 'UPI';
  btn.textContent = `PAY ₹${selectedDepositAmount} VIA ${methodName.toUpperCase()} →`;
}

function syncWithdrawalUI() {
  const winnings = state.user?.wallet?.winnings || 0;
  const el = document.getElementById('wh-winnings-amount');
  if (el) el.textContent = `₹${winnings.toLocaleString('en-IN')}`;
  const input = document.getElementById('input-withdraw-amount');
  if (input) input.max = winnings;
}

// Simulated UPI Gateway Flow
function startUPIPaymentSimulation(amount, method) {
  audio.init();
  document.getElementById('modal-wallet').classList.add('hidden');
  const pgModal = document.getElementById('modal-payment-gateway');
  const pState = document.getElementById('pg-state-processing');
  const sState = document.getElementById('pg-state-success');

  pState.classList.remove('hidden');
  sState.classList.add('hidden');
  pgModal.classList.remove('hidden');

  const methodNames = {
    gpay: 'Google Pay',
    phonepe: 'PhonePe',
    paytm: 'Paytm UPI',
    qr: 'UPI QR'
  };
  document.getElementById('pg-processing-title').textContent = `Opening ${methodNames[method] || 'Bank UPI'} Gateway...`;

  // Simulate bank processing
  setTimeout(async () => {
    const res = await fetchAPI('/api/user/wallet/deposit-upi', 'POST', {
      amount: amount,
      method: method
    });

    if (res && res.success) {
      state.user.wallet = res.wallet;
      updateUserHeader();

      // Show success state
      pState.classList.add('hidden');
      sState.classList.remove('hidden');
      document.getElementById('pg-success-amount').textContent = `₹${amount.toLocaleString('en-IN')}`;
      document.getElementById('pg-success-utr').textContent = res.transaction.utr;

      audio.playWinFanfare();
      showToast(`💰 ₹${amount} deposited successfully via UPI!`, 'success');
    } else {
      pgModal.classList.add('hidden');
      showToast('Payment failed, please try again', 'error');
    }
  }, 1600);
}

// Passbook Management
let cachedTransactions = [];

async function loadPassbookStatement() {
  const res = await fetchAPI('/api/user/transactions');
  if (res) {
    cachedTransactions = res;
    renderPassbookList();
  }
}

function renderPassbookList() {
  const container = document.getElementById('passbook-list');
  if (!container) return;
  container.innerHTML = '';

  let filtered = cachedTransactions;
  if (activePassbookFilter !== 'all') {
    filtered = filtered.filter(t => t.type === activePassbookFilter);
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:30px 16px; color:var(--text-muted)">
        <div style="font-size:32px; margin-bottom:6px">📜</div>
        <p style="font-size:12px">No transactions in this category</p>
      </div>
    `;
    return;
  }

  filtered.forEach(txn => {
    const card = document.createElement('div');
    card.className = 'pb-txn-card';
    const isCredit = txn.isCredit;

    card.innerHTML = `
      <div class="pb-txn-left">
        <div class="pb-txn-icon ${isCredit ? 'credit' : 'debit'}">
          ${isCredit ? '↓' : '↑'}
        </div>
        <div class="pb-txn-meta">
          <strong>${txn.title}</strong>
          <span class="pb-txn-sub">${txn.date} • ${txn.utr}</span>
        </div>
      </div>
      <div class="pb-txn-right">
        <div class="pb-txn-amt ${isCredit ? 'credit' : 'debit'}">
          ${isCredit ? '+' : '-'}₹${txn.amount.toLocaleString('en-IN')}
        </div>
        <span class="pb-txn-status">${txn.status}</span>
      </div>
    `;

    card.addEventListener('click', () => {
      showToast(`Ref: ${txn.utr} | Method: ${txn.method || 'Dream11 Wallet'}`, 'success');
    });

    container.appendChild(card);
  });
}
'''

if 'setupPaymentControllers' not in app_js:
    app_js += '\n' + payment_js_code

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(app_js)

print("public/app.js upgraded with full payment suite logic!")
