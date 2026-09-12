# Apply Features 2, 3, 4, 5
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_PATH = os.path.join(BASE_DIR, "server.py")
INDEX_PATH = os.path.join(BASE_DIR, "public", "index.html")
STYLES_PATH = os.path.join(BASE_DIR, "public", "styles.css")
APP_PATH = os.path.join(BASE_DIR, "public", "app.js")

# ----------------------------------------------------
# 1. UPGRADE server.py
# ----------------------------------------------------
with open(SERVER_PATH, "r", encoding="utf-8") as f:
    server_code = f.read()

# Add random import if not present
if "import random" not in server_code:
    server_code = "import random\n" + server_code

# Add privateContests to STATE if not present
if '"privateContests"' not in server_code:
    server_code = server_code.replace(
        '"joinedContests": [],',
        '"joinedContests": [],\n    "privateContests": {},'
    )

# Add GET endpoints for private contests
get_private_code = '''        elif path == "/api/contests/private":
            self.send_json(list(STATE.get("privateContests", {}).values()))
        elif path.startswith("/api/contests/private/"):
            code = path.split("/")[-1].upper()
            p_contest = STATE.get("privateContests", {}).get(code)
            if p_contest:
                self.send_json({"success": True, "contest": p_contest})
            else:
                self.send_json({"success": False, "message": "Private contest not found"}, status=404)
        elif path == "/api/contests":'''

if 'path == "/api/contests/private"' not in server_code:
    server_code = server_code.replace('        elif path == "/api/contests":', get_private_code)

# Add POST endpoints for private contest create and join
post_private_code = '''        elif path == "/api/contests/private/create":
            code = f"D11-{random.randint(100, 999)}"
            name = payload.get("name", "Friends Fantasy League")
            match_id = payload.get("matchId", "ind-aus-t20")
            entry_fee = int(payload.get("entryFee", 50))
            total_spots = int(payload.get("totalSpots", 10))
            prize_pool = int(payload.get("prizePool", entry_fee * total_spots))
            team_id = payload.get("teamId", "T1")
            host_name = payload.get("hostName", STATE["user"]["name"])

            wallet = STATE["user"]["wallet"]
            total_cash = wallet["deposited"] + wallet["winnings"] + wallet["bonus"]
            if total_cash < entry_fee:
                self.send_json({"success": False, "message": "Insufficient balance to create private contest"}, status=400)
                return

            bonus_usable = min(wallet["bonus"], int(entry_fee * 0.2))
            remaining = entry_fee - bonus_usable
            wallet["bonus"] -= bonus_usable
            dep_usable = min(wallet["deposited"], remaining)
            wallet["deposited"] -= dep_usable
            remaining -= dep_usable
            wallet["winnings"] -= remaining

            cid = f"priv-{code.lower()}"
            first_prize = f"₹{int(prize_pool * 0.6):,}" if total_spots > 2 else f"₹{int(prize_pool * 0.9):,}"
            priv_contest = {
                "id": cid,
                "code": code,
                "name": name,
                "matchId": match_id,
                "badge": "PRIVATE",
                "tag": "Friends League",
                "totalPrize": f"₹{prize_pool:,}",
                "prizeNum": prize_pool,
                "firstPrize": first_prize,
                "entryFee": entry_fee,
                "originalFee": entry_fee,
                "discountFee": entry_fee,
                "totalSpots": total_spots,
                "spotsLeft": total_spots - 1,
                "winnersPercent": "50%",
                "maxTeams": 1,
                "type": "private",
                "isPrivate": True,
                "hostName": host_name,
                "participants": [
                    {
                        "name": host_name,
                        "teamId": team_id,
                        "avatar": STATE["user"]["avatar"],
                        "isHost": True,
                        "points": 0,
                        "rank": 1
                    }
                ],
                "breakup": [
                    {"rank": "1st", "prize": first_prize},
                    {"rank": "2nd", "prize": f"₹{int(prize_pool * 0.3):,}"}
                ]
            }
            if "privateContests" not in STATE: STATE["privateContests"] = {}
            STATE["privateContests"][code] = priv_contest
            STATE["contests"].insert(0, priv_contest)

            join_record = {
                "id": f"JC_PRIV_{code}",
                "contestId": cid,
                "contest": priv_contest,
                "teamId": team_id,
                "entryFeePaid": entry_fee,
                "joinedAt": "Just now"
            }
            STATE["joinedContests"].append(join_record)
            self.send_json({"success": True, "contest": priv_contest, "code": code, "wallet": wallet})

        elif path == "/api/contests/private/join":
            code = payload.get("code", "").strip().upper()
            team_id = payload.get("teamId", "T1")
            user_name = payload.get("userName", STATE["user"]["name"])

            if "privateContests" not in STATE or code not in STATE["privateContests"]:
                self.send_json({"success": False, "message": f"Contest with code '{code}' not found!"}, status=404)
                return

            contest = STATE["privateContests"][code]
            if contest["spotsLeft"] <= 0:
                self.send_json({"success": False, "message": "This private contest is already full!"}, status=400)
                return

            entry_fee = contest["entryFee"]
            wallet = STATE["user"]["wallet"]
            total_cash = wallet["deposited"] + wallet["winnings"] + wallet["bonus"]
            if total_cash < entry_fee:
                self.send_json({"success": False, "message": "Insufficient balance. Please add cash."}, status=400)
                return

            bonus_usable = min(wallet["bonus"], int(entry_fee * 0.2))
            remaining = entry_fee - bonus_usable
            wallet["bonus"] -= bonus_usable
            dep_usable = min(wallet["deposited"], remaining)
            wallet["deposited"] -= dep_usable
            remaining -= dep_usable
            wallet["winnings"] -= remaining

            contest["spotsLeft"] -= 1
            contest["participants"].append({
                "name": user_name,
                "teamId": team_id,
                "avatar": STATE["user"]["avatar"],
                "isHost": False,
                "points": 0,
                "rank": len(contest["participants"]) + 1
            })

            for c in STATE["contests"]:
                if c.get("code") == code:
                    c["spotsLeft"] = contest["spotsLeft"]

            join_record = {
                "id": f"JC_PRIV_{code}_{len(contest['participants'])}",
                "contestId": contest["id"],
                "contest": contest,
                "teamId": team_id,
                "entryFeePaid": entry_fee,
                "joinedAt": "Just now"
            }
            STATE["joinedContests"].append(join_record)
            self.send_json({"success": True, "contest": contest, "wallet": wallet})
'''

if 'path == "/api/contests/private/create"' not in server_code:
    server_code = server_code.replace('        elif path == "/api/simulation/step":', post_private_code + '        elif path == "/api/simulation/step":')

with open(SERVER_PATH, "w", encoding="utf-8") as f:
    f.write(server_code)

print("server.py updated with Private Contest endpoints!")
