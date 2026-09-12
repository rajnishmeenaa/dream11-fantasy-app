# Upgrade OTP System: 6-Box Auto-Advance Input + Realistic Mobile Push SMS Notification Banner
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "public", "index.html")
STYLES_PATH = os.path.join(BASE_DIR, "public", "styles.css")
APP_PATH = os.path.join(BASE_DIR, "public", "app.js")

# =========================================================================
# 1. UPGRADE index.html
# =========================================================================
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Add Floating SMS Push Banner right inside .mobile-frame
sms_banner_html = '''      <!-- Floating Simulated Mobile Push SMS Banner -->
      <div class="sms-push-banner hidden" id="sms-push-banner">
        <div class="sms-banner-top">
          <div class="sms-app-badge">💬 MESSAGES • DREAM11 OTP</div>
          <button class="sms-dismiss-btn" id="btn-dismiss-sms">✕</button>
        </div>
        <div class="sms-content">
          Your Dream11 Bank Withdrawal OTP is <strong id="sms-otp-display">849201</strong>. Valid for 10 minutes. Do not share with anyone.
        </div>
        <div class="sms-actions">
          <button id="btn-sms-tap-autofill" class="btn-sms-action">⚡ Tap to Auto-Fill 6 Boxes</button>
        </div>
      </div>
'''

if 'sms-push-banner' not in html:
    html = html.replace(
        '<header class="app-header">',
        sms_banner_html + '\n      <header class="app-header">'
    )

# Replace the single input in #modal-bank-otp with 6-box inputs
old_otp_block = '''        <div class="otp-input-container">
          <input type="text" id="input-otp-val" maxlength="6" value="123456" placeholder="1 2 3 4 5 6" style="letter-spacing:10px; text-align:center; font-size:22px; font-weight:900; padding:12px">
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px">
          <span style="font-size:11px; color:#15803d; font-weight:700">✓ OTP Sent (Valid for 10:00m)</span>
          <button type="button" class="btn-link-all" id="btn-autofill-otp">⚡ Use Test OTP (123456)</button>
        </div>'''

new_otp_block = '''        <!-- 6-Box Auto-Advance Fintech Input -->
        <div class="otp-six-boxes-wrapper" id="otp-six-boxes">
          <input type="tel" inputmode="numeric" maxlength="1" class="otp-box" data-idx="0" autocomplete="off" autofocus>
          <input type="tel" inputmode="numeric" maxlength="1" class="otp-box" data-idx="1" autocomplete="off">
          <input type="tel" inputmode="numeric" maxlength="1" class="otp-box" data-idx="2" autocomplete="off">
          <input type="tel" inputmode="numeric" maxlength="1" class="otp-box" data-idx="3" autocomplete="off">
          <input type="tel" inputmode="numeric" maxlength="1" class="otp-box" data-idx="4" autocomplete="off">
          <input type="tel" inputmode="numeric" maxlength="1" class="otp-box" data-idx="5" autocomplete="off">
        </div>

        <div class="otp-timer-action-row">
          <span class="otp-countdown-text" id="otp-timer-status">Resend code in <strong id="otp-timer-seconds">00:59</strong></span>
          <button type="button" class="btn-link-all hidden" id="btn-resend-otp">🔄 Resend OTP</button>
          <button type="button" class="btn-link-all" id="btn-autofill-otp">⚡ Auto-Fill Code</button>
        </div>'''

if old_otp_block in html:
    html = html.replace(old_otp_block, new_otp_block)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("index.html upgraded with 6-box input and SMS push banner!")

# =========================================================================
# 2. UPGRADE styles.css
# =========================================================================
with open(STYLES_PATH, "r", encoding="utf-8") as f:
    css = f.read()

six_box_styles = '''
/* 6-Box OTP Input Styles */
.otp-six-boxes-wrapper {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 18px 0;
}
.otp-box {
  width: 48px;
  height: 56px;
  border: 2px solid #cbd5e1;
  border-radius: 12px;
  background: #f8fafc;
  font-size: 24px;
  font-weight: 900;
  color: #0f172a;
  text-align: center;
  outline: none;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.03);
}
.otp-box:focus {
  border-color: #16a34a;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.2);
  transform: translateY(-2px);
}
.otp-box.filled {
  border-color: #15803d;
  background: #f0fdf4;
  color: #166534;
}
.otp-box.shake {
  animation: shakeBox 0.3s ease-in-out;
  border-color: #b91c1c;
  background: #fee2e2;
}
@keyframes shakeBox {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-4px); }
  40%, 80% { transform: translateX(4px); }
}

.otp-timer-action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
  margin-top: 8px;
}
.otp-countdown-text {
  color: #64748b;
  font-weight: 600;
}

/* Floating Simulated Mobile Push SMS Banner */
.sms-push-banner {
  position: absolute;
  top: 14px;
  left: 12px;
  right: 12px;
  background: rgba(15, 23, 42, 0.96);
  backdrop-filter: blur(14px);
  color: #ffffff;
  border-radius: 18px;
  padding: 12px 16px;
  z-index: 150;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  animation: slideDownSms 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideDownSms {
  from { transform: translateY(-120%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.sms-banner-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}
.sms-app-badge {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  color: #94a3b8;
}
.sms-dismiss-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 14px;
  cursor: pointer;
}
.sms-content {
  font-size: 12px;
  line-height: 1.4;
  color: #f1f5f9;
}
.sms-content strong {
  color: #facc15;
  font-size: 15px;
  letter-spacing: 1.5px;
}
.sms-actions {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
}
.btn-sms-action {
  background: #16a34a;
  color: #ffffff;
  border: none;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.4);
  transition: transform 0.15s;
}
.btn-sms-action:hover {
  transform: scale(1.04);
}
'''

if 'otp-six-boxes-wrapper' not in css:
    css += six_box_styles

with open(STYLES_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("styles.css upgraded with 6-box and SMS push styles!")

# =========================================================================
# 3. UPGRADE public/app.js
# =========================================================================
with open(APP_PATH, "r", encoding="utf-8") as f:
    app_js = f.read()

# Replace the OTP handling in setupPaymentControllers
old_otp_controller = '''  // Auto-fill Test OTP
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
  });'''

new_otp_controller = '''  // --- 6-Box Auto-Advance Input & Dynamic OTP Engine ---
  const otpBoxes = document.querySelectorAll('.otp-six-boxes-wrapper .otp-box');

  otpBoxes.forEach((box, idx) => {
    box.addEventListener('input', (e) => {
      const val = e.target.value.replace(/[^0-9]/g, '');
      e.target.value = val ? val[0] : '';
      e.target.classList.toggle('filled', !!e.target.value);
      audio.playWhistle();

      if (e.target.value && idx < 5) {
        otpBoxes[idx + 1].focus();
        otpBoxes[idx + 1].select();
      }
    });

    box.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace') {
        if (!box.value && idx > 0) {
          otpBoxes[idx - 1].focus();
          otpBoxes[idx - 1].value = '';
          otpBoxes[idx - 1].classList.remove('filled');
        } else {
          box.value = '';
          box.classList.remove('filled');
        }
      } else if (e.key === 'ArrowLeft' && idx > 0) {
        otpBoxes[idx - 1].focus();
      } else if (e.key === 'ArrowRight' && idx < 5) {
        otpBoxes[idx + 1].focus();
      }
    });

    box.addEventListener('paste', (e) => {
      e.preventDefault();
      const pasted = (e.clipboardData || window.clipboardData).getData('text').replace(/[^0-9]/g, '');
      if (pasted) {
        pasted.split('').slice(0, 6).forEach((digit, i) => {
          if (otpBoxes[i]) {
            otpBoxes[i].value = digit;
            otpBoxes[i].classList.add('filled');
          }
        });
        const targetIdx = Math.min(5, pasted.length - 1);
        otpBoxes[targetIdx]?.focus();
        audio.playBatCrack();
        showToast('6-digit code pasted into boxes ✓', 'success');
      }
    });
  });

  // Auto-Fill function for 6 boxes
  const autoFillSixBoxes = (code) => {
    code = String(code);
    code.split('').slice(0, 6).forEach((digit, i) => {
      setTimeout(() => {
        if (otpBoxes[i]) {
          otpBoxes[i].value = digit;
          otpBoxes[i].classList.add('filled');
          audio.playBatCrack();
        }
      }, i * 60);
    });
  };

  document.getElementById('btn-autofill-otp')?.addEventListener('click', () => {
    autoFillSixBoxes(state.currentGeneratedOTP || '123456');
  });

  document.getElementById('btn-sms-tap-autofill')?.addEventListener('click', () => {
    autoFillSixBoxes(state.currentGeneratedOTP || '123456');
    document.getElementById('sms-push-banner').classList.add('hidden');
  });

  document.getElementById('btn-dismiss-sms')?.addEventListener('click', () => {
    document.getElementById('sms-push-banner').classList.add('hidden');
  });

  document.getElementById('btn-resend-otp')?.addEventListener('click', () => {
    triggerNewOTPGeneration();
    showToast('New OTP dispatched to mobile!', 'success');
  });

  // Confirm OTP & Authorize IMPS
  document.getElementById('btn-confirm-otp-withdraw')?.addEventListener('click', async () => {
    const otp = Array.from(otpBoxes).map(b => b.value.trim()).join('');

    if (otp.length !== 6) {
      otpBoxes.forEach(b => {
        b.classList.add('shake');
        setTimeout(() => b.classList.remove('shake'), 400);
      });
      showToast('Please enter all 6 digits of the OTP!', 'error');
      return;
    }

    if (otp !== state.currentGeneratedOTP && otp !== '123456') {
      otpBoxes.forEach(b => {
        b.classList.add('shake');
        setTimeout(() => b.classList.remove('shake'), 400);
      });
      showToast('Invalid OTP! Please check the SMS banner or resend.', 'error');
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
      document.getElementById('sms-push-banner').classList.add('hidden');

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
  });'''

if old_otp_controller in app_js:
    app_js = app_js.replace(old_otp_controller, new_otp_controller)

# Also update the submit withdraw click to trigger triggerNewOTPGeneration()
old_submit_wd = '''    pendingWithdrawalData = { amount, method: mode, upiId, bankAccount: bankAcc, ifsc };
    document.getElementById('modal-bank-otp').classList.remove('hidden');'''

new_submit_wd = '''    pendingWithdrawalData = { amount, method: mode, upiId, bankAccount: bankAcc, ifsc };
    document.getElementById('modal-bank-otp').classList.remove('hidden');
    triggerNewOTPGeneration();'''

if old_submit_wd in app_js:
    app_js = app_js.replace(old_submit_wd, new_submit_wd)

# Add triggerNewOTPGeneration function to app.js
otp_helper_func = '''
let otpCountdownTimer = null;

function triggerNewOTPGeneration() {
  // Generate random 6-digit OTP
  state.currentGeneratedOTP = String(Math.floor(100000 + Math.random() * 900000));

  // Clear 6 boxes
  const boxes = document.querySelectorAll('.otp-six-boxes-wrapper .otp-box');
  boxes.forEach(b => {
    b.value = '';
    b.classList.remove('filled');
  });
  if (boxes[0]) boxes[0].focus();

  // Show Simulated SMS Banner
  const smsBanner = document.getElementById('sms-push-banner');
  const smsCodeDisplay = document.getElementById('sms-otp-display');
  if (smsCodeDisplay) smsCodeDisplay.textContent = state.currentGeneratedOTP;
  if (smsBanner) {
    smsBanner.classList.remove('hidden');
    audio.playWhistle();
    // Auto-hide SMS banner after 8 seconds
    setTimeout(() => {
      smsBanner.classList.add('hidden');
    }, 8000);
  }

  // Start 60-second countdown
  let seconds = 59;
  const statusEl = document.getElementById('otp-timer-status');
  const timerSec = document.getElementById('otp-timer-seconds');
  const resendBtn = document.getElementById('btn-resend-otp');

  if (resendBtn) resendBtn.classList.add('hidden');
  if (statusEl) statusEl.classList.remove('hidden');

  if (otpCountdownTimer) clearInterval(otpCountdownTimer);

  otpCountdownTimer = setInterval(() => {
    seconds--;
    if (timerSec) timerSec.textContent = `00:${seconds < 10 ? '0' : ''}${seconds}`;
    if (seconds <= 0) {
      clearInterval(otpCountdownTimer);
      if (statusEl) statusEl.classList.add('hidden');
      if (resendBtn) resendBtn.classList.remove('hidden');
    }
  }, 1000);
}
'''

if 'function triggerNewOTPGeneration' not in app_js:
    app_js += '\n' + otp_helper_func

with open(APP_PATH, "w", encoding="utf-8") as f:
    f.write(app_js)

print("public/app.js upgraded with 6-box auto-advance & SMS banner logic!")
