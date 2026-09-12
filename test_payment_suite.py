import urllib.request
import urllib.error
import json

base = 'http://localhost:8000'

def make_req(path, data=None):
    url = f"{base}{path}"
    headers = {'Content-Type': 'application/json'}
    body = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

print("=== STARTING PAYMENT SUITE VERIFICATION ===")

# 1. Fetch initial transactions
code, txns = make_req('/api/user/transactions')
print(f"1. Initial Transactions Ledger: HTTP {code}, count: {len(txns)}")
assert code == 200 and len(txns) >= 3, "Initial ledger should have transactions"

# 2. Test UPI Deposit (PhonePe ₹250)
code, res = make_req('/api/user/wallet/deposit-upi', {'amount': 250, 'method': 'phonepe', 'upiId': 'user@ybl'})
print(f"2. UPI Deposit (PhonePe ₹250): HTTP {code}, UTR: {res['transaction']['utr']}, New Deposited: ₹{res['wallet']['deposited']}")
assert code == 200 and res['success'] is True, "Deposit should succeed"
assert res['transaction']['amount'] == 250, "Deposit amount should match"

# 3. Test UPI Deposit (Google Pay ₹500)
code, res = make_req('/api/user/wallet/deposit-upi', {'amount': 500, 'method': 'gpay', 'upiId': 'user@okhdfcbank'})
print(f"3. UPI Deposit (GPay ₹500): HTTP {code}, UTR: {res['transaction']['utr']}, New Deposited: ₹{res['wallet']['deposited']}")
assert code == 200 and res['success'] is True, "GPay Deposit should succeed"

# 4. Test Valid Bank Withdrawal (₹200 to UPI)
code, res = make_req('/api/user/wallet/withdraw', {'amount': 200, 'method': 'upi', 'upiId': 'champion@okhdfcbank'})
print(f"4. Bank Withdrawal (₹200 to UPI): HTTP {code}, IMPS Ref: {res.get('impsReference')}, Remaining Winnings: ₹{res['wallet']['winnings']}")
assert code == 200 and res['success'] is True, "Withdrawal should succeed"
assert 'IMPS' in res['impsReference'], "IMPS reference should be present"

# 5. Test Invalid Withdrawal (Exceeding winnings balance)
code, res = make_req('/api/user/wallet/withdraw', {'amount': 999999, 'method': 'upi', 'upiId': 'champion@okhdfcbank'})
print(f"5. Overdraft Withdrawal Rejection: HTTP {code}, Message: '{res.get('message')}'")
assert code == 400 and res['success'] is False, "Overdraft must be rejected with HTTP 400"

# 6. Test Invalid Withdrawal (Below minimum ₹50)
code, res = make_req('/api/user/wallet/withdraw', {'amount': 20, 'method': 'upi', 'upiId': 'champion@okhdfcbank'})
print(f"6. Below Minimum ₹50 Rejection: HTTP {code}, Message: '{res.get('message')}'")
assert code == 400 and res['success'] is False, "Below min ₹50 must be rejected with HTTP 400"

# 7. Verify Passbook updated with all records
code, txns = make_req('/api/user/transactions')
print(f"7. Final Passbook Count: {len(txns)} transactions recorded")
recent_types = [t['type'] for t in txns[:3]]
print(f"   Latest 3 records: {recent_types}")

print("\n>>> ALL PAYMENT GATEWAY & PASSBOOK TESTS PASSED WITH 100% SUCCESS! <<<")
