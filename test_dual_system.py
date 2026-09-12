import os
import json
import urllib.request

print("==================================================")
print("  FANTASY11 DUAL SYSTEM COMPREHENSIVE VERIFICATION")
print("==================================================")

BASE = os.path.dirname(os.path.abspath(__file__))

# 1. Verify User App HTML
with open(os.path.join(BASE, "public", "index.html"), "r", encoding="utf-8") as f:
    idx_content = f.read()
assert "btn-open-admin" not in idx_content, "Admin button still in index.html!"
assert "menu-item-admin" not in idx_content, "Admin menu still in index.html!"
assert "Fantasy11" in idx_content, "Fantasy11 branding missing in index.html!"
print("[PASS] User app HTML has zero admin buttons and clean branding.")

# 2. Verify Admin App HTML
with open(os.path.join(BASE, "public", "admin.html"), "r", encoding="utf-8") as f:
    adm_content = f.read()
assert "adm-view-contests" in adm_content, "Contests tab missing in admin.html!"
assert "adm-view-fixtures" in adm_content, "Fixtures tab missing in admin.html!"
assert "adm-view-wallet" in adm_content, "Wallet tab missing in admin.html!"
assert "adm-view-godmode" in adm_content, "God Mode tab missing in admin.html!"
print("[PASS] Admin app HTML has all 4 executive management tabs.")

# 3. Verify Admin Manifest
with open(os.path.join(BASE, "public", "manifest-admin.json"), "r", encoding="utf-8") as f:
    m_adm = json.load(f)
assert m_adm["start_url"] == "/admin.html", "Wrong start_url in manifest-admin.json!"
print(f"[PASS] Admin Manifest is valid (App Name: {m_adm['name']}, start_url: {m_adm['start_url']}).")

# 4. Verify User Android Project
u_files = [
    "android/fantasy11-user-app/build.gradle",
    "android/fantasy11-user-app/settings.gradle",
    "android/fantasy11-user-app/app/build.gradle",
    "android/fantasy11-user-app/app/src/main/AndroidManifest.xml",
    "android/fantasy11-user-app/app/src/main/java/com/fantasy11/app/MainActivity.java",
    "android/fantasy11-user-app/app/src/main/res/layout/activity_main.xml"
]
for p in u_files:
    assert os.path.isfile(os.path.join(BASE, p)), f"Missing file: {p}"
print("[PASS] Fantasy11 User Android Studio Project (com.fantasy11.app) verified.")

# 5. Verify Admin Android Project
a_files = [
    "android/fantasy11-admin-app/build.gradle",
    "android/fantasy11-admin-app/settings.gradle",
    "android/fantasy11-admin-app/app/build.gradle",
    "android/fantasy11-admin-app/app/src/main/AndroidManifest.xml",
    "android/fantasy11-admin-app/app/src/main/java/com/fantasy11/admin/AdminActivity.java",
    "android/fantasy11-admin-app/app/src/main/res/layout/activity_admin.xml"
]
for p in a_files:
    assert os.path.isfile(os.path.join(BASE, p)), f"Missing file: {p}"
print("[PASS] Fantasy11 Admin Android Studio Project (com.fantasy11.admin) verified.")

# 6. Test Live Server Endpoints
def post_json(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        return json.loads(res.read().decode("utf-8"))

# Test God Mode Custom Ball Injection
res_gm = post_json("http://localhost:8000/api/admin/live/custom-ball", {
    "batsman": "Travis Head",
    "bowler": "Jasprit Bumrah",
    "runs": 6,
    "isWicket": False,
    "comment": "VERIFICATION SIX! Smashed high over long-on!"
})
assert res_gm["success"] is True, "God mode ball injection failed!"
print(f"[PASS] God Mode Ball Injection API works (Live score: {res_gm['state']['score']}).")

# Test Wallet Adjustment
res_w = post_json("http://localhost:8000/api/admin/wallet/adjust", {
    "deposited": 750,
    "winnings": 1200,
    "bonus": 400
})
assert res_w["success"] is True, "Wallet adjust API failed!"
assert res_w["wallet"]["winnings"] == 1200, "Wallet value did not update!"
print(f"[PASS] Admin Wallet Adjustment API works (New Wallet: {res_w['wallet']}).")

# Test Create Contest
res_c = post_json("http://localhost:8000/api/admin/contests/create", {
    "name": "Verification Mega Grand League",
    "badge": "EXCLUSIVE",
    "totalPrize": "₹20 Crores",
    "firstPrize": "₹2 Crores + Ferrari",
    "entryFee": 49,
    "totalSpots": 500000
})
assert res_c["success"] is True, "Contest create API failed!"
print(f"[PASS] Admin Contest Creation API works (Total active contests: {len(res_c['contests'])}).")

print("==================================================")
print("  ALL 10 DUAL SYSTEM VERIFICATION CHECKS PASSED!  ")
print("==================================================")
