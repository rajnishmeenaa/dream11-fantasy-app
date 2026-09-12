# Build Payment Suite: UPI Gateway, Withdrawal with OTP, Transaction Passbook
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_PATH = os.path.join(BASE_DIR, "server.py")
INDEX_PATH = os.path.join(BASE_DIR, "public", "index.html")
STYLES_PATH = os.path.join(BASE_DIR, "public", "styles.css")
APP_PATH = os.path.join(BASE_DIR, "public", "app.js")

# =========================================================================
# 1. UPGRADE server.py
# =========================================================================
with open(SERVER_PATH, "r", encoding="utf-8") as f:
    s_code = f.read()

# Add initial transactions to STATE if not present
init_txn_code = '''
INITIAL_TRANSACTIONS = [
    {
        "id": "TXN_INIT_001",
        "type": "deposit",
        "title": "UPI Deposit - PhonePe",
        "amount": 500,
        "isCredit": True,
        "walletCategory": "Deposited",
        "method": "PhonePe UPI",
        "utr": "UPI/428901842019",
        "date": "Today, 11:20 AM",
        "status": "SUCCESS"
    },
    {
        "id": "TXN_INIT_002",
        "type": "bonus",
        "title": "Daily Login Cash Bonus",
        "amount": 350,
        "isCredit": True,
        "walletCategory": "Bonus",
        "method": "Promotional Reward",
        "utr": "REW/8910482910",
        "date": "Yesterday, 08:30 AM",
        "status": "SUCCESS"
    },
    {
        "id": "TXN_INIT_003",
        "type": "winning",
        "title": "Mega Contest 1st Rank Payout",
        "amount": 650,
        "isCredit": True,
        "walletCategory": "Winnings",
        "method": "Contest Prize Pool",
        "utr": "WIN/2910485910",
        "date": "Yesterday, 11:45 PM",
        "status": "SUCCESS"
    }
]
'''

if 'INITIAL_TRANSACTIONS' not in s_code:
    s_code = s_code.replace('STATE = {', init_txn_code + '\nSTATE = {')
    s_code = s_code.replace(
        '"privateContests": {},',
        '"privateContests": {},\n    "transactions": list(INITIAL_TRANSACTIONS),'
    )

# Add GET endpoint /api/user/transactions
if 'path == "/api/user/transactions"' not in s_code:
    s_code = s_code.replace(
        'elif path == "/api/contests":',
        'elif path == "/api/user/transactions":\n            self.send_json(STATE.get("transactions", []))\n        elif path == "/api/contests":'
    )

# Add POST endpoints: /api/user/wallet/deposit-upi and /api/user/wallet/withdraw
payment_endpoints = '''        elif path == "/api/user/wallet/deposit-upi":
            amount = int(payload.get("amount", 100))
            method = payload.get("method", "gpay")
            upi_id = payload.get("upiId", "user@upi")
            utr_num = f"UPI/{random.randint(100000000000, 999999999999)}"

            STATE["user"]["wallet"]["deposited"] += amount

            method_labels = {
                "gpay": "Google Pay (GPay)",
                "phonepe": "PhonePe UPI",
                "paytm": "Paytm UPI",
                "qr": "Dynamic UPI QR Scan",
                "custom_upi": f"UPI ({upi_id})"
            }
            method_name = method_labels.get(method, "UPI Payment")

            txn = {
                "id": f"TXN_{len(STATE['transactions']) + 1}_{random.randint(100, 999)}",
                "type": "deposit",
                "title": f"UPI Deposit - {method_name}",
                "amount": amount,
                "isCredit": True,
                "walletCategory": "Deposited",
                "method": method_name,
                "utr": utr_num,
                "date": "Just now",
                "status": "SUCCESS"
            }
            STATE["transactions"].insert(0, txn)
            self.send_json({
                "success": True,
                "wallet": STATE["user"]["wallet"],
                "transaction": txn
            })

        elif path == "/api/user/wallet/withdraw":
            amount = int(payload.get("amount", 0))
            method = payload.get("method", "upi")
            upi_id = payload.get("upiId", "user@upi")
            bank_acc = payload.get("bankAccount", "9876543210")
            ifsc = payload.get("ifsc", "HDFC0001234")

            winnings = STATE["user"]["wallet"]["winnings"]
            if amount < 50:
                self.send_json({"success": False, "message": "Minimum withdrawal amount is ₹50"}, status=400)
                return
            if amount > winnings:
                self.send_json({"success": False, "message": f"Insufficient winnings! Max withdrawable: ₹{winnings}"}, status=400)
                return

            STATE["user"]["wallet"]["winnings"] -= amount
            imps_rrn = f"IMPS{random.randint(1000000000, 9999999999)}"
            dest_label = f"UPI ({upi_id})" if method == "upi" else f"Bank A/C ...{bank_acc[-4:] if len(bank_acc) >= 4 else '1234'} ({ifsc})"

            txn = {
                "id": f"TXN_WD_{len(STATE['transactions']) + 1}_{random.randint(100, 999)}",
                "type": "withdrawal",
                "title": f"Bank Withdrawal - {dest_label}",
                "amount": amount,
                "isCredit": False,
                "walletCategory": "Winnings",
                "method": "IMPS Instant Transfer",
                "destination": dest_label,
                "utr": imps_rrn,
                "date": "Just now",
                "status": "SUCCESS"
            }
            STATE["transactions"].insert(0, txn)
            self.send_json({
                "success": True,
                "wallet": STATE["user"]["wallet"],
                "transaction": txn,
                "impsReference": imps_rrn
            })
'''

if 'path == "/api/user/wallet/deposit-upi"' not in s_code:
    s_code = s_code.replace(
        'if path == "/api/user/wallet/add":',
        payment_endpoints + '\n        if path == "/api/user/wallet/add":'
    )

with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.write(s_code)

print("server.py updated with payment & withdrawal endpoints!")
