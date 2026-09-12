import random
import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
DATA_FILE = os.path.join(BASE_DIR, "data", "fantasy_data.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    INITIAL_DATA = json.load(f)


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

STATE = {
    "user": INITIAL_DATA["user"],
    "matches": INITIAL_DATA["matches"],
    "contests": INITIAL_DATA["contests"],
    "pointsSystem": INITIAL_DATA["pointsSystem"],
    "simulationScript": INITIAL_DATA["simulationScript"],
    "userTeams": [],
    "joinedContests": [],
    "privateContests": {},
    "transactions": list(INITIAL_TRANSACTIONS),
    "simState": {
        "matchId": "ind-aus-t20",
        "currentBallIndex": 0,
        "isLive": False,
        "score": {"team": "AUS", "runs": 0, "wickets": 0, "overs": "0.0"},
        "playerLivePoints": {},
        "commentary": [],
        "leaderboard": []
    }
}

COMPETITORS = [
    {"name": "RohitHitman_45", "captain": "ind_3", "viceCaptain": "ind_10", "basePoints": 420, "avatar": "🏏"},
    {"name": "KingKohli_Fan", "captain": "ind_4", "viceCaptain": "aus_7", "basePoints": 405, "avatar": "👑"},
    {"name": "BumrahYorker_93", "captain": "ind_10", "viceCaptain": "ind_4", "basePoints": 395, "avatar": "⚡"},
    {"name": "WankhedeMaster", "captain": "aus_3", "viceCaptain": "ind_7", "basePoints": 380, "avatar": "🏆"},
    {"name": "CricketGuru99", "captain": "ind_7", "viceCaptain": "aus_3", "basePoints": 370, "avatar": "🎯"},
    {"name": "AussieStriker", "captain": "aus_4", "viceCaptain": "aus_10", "basePoints": 355, "avatar": "🦘"},
    {"name": "DhoniFinisher_07", "captain": "ind_1", "viceCaptain": "ind_8", "basePoints": 340, "avatar": "🧤"},
    {"name": "MaxwellSwitchHit", "captain": "aus_7", "viceCaptain": "ind_5", "basePoints": 330, "avatar": "🔥"}
]

def init_sim_player_points():
    match = STATE["matches"][0]
    pts = {}
    for p in match["players"]:
        pts[p["id"]] = {
            "runs": 0, "fours": 0, "sixes": 0, "wickets": 0,
            "bowled_lbw": 0, "catches": 0, "stumpings": 0,
            "maidens": 0, "total": 0
        }
    return pts

STATE["simState"]["playerLivePoints"] = init_sim_player_points()

def calculate_player_points(p_stats):
    total = 0
    total += p_stats["runs"] * 1
    total += p_stats["fours"] * 1
    total += p_stats["sixes"] * 2
    if p_stats["runs"] >= 100: total += 16
    elif p_stats["runs"] >= 50: total += 8
    elif p_stats["runs"] >= 30: total += 4
    total += p_stats["wickets"] * 25
    total += p_stats["bowled_lbw"] * 8
    if p_stats["wickets"] >= 5: total += 16
    elif p_stats["wickets"] >= 4: total += 8
    elif p_stats["wickets"] >= 3: total += 4
    total += p_stats["maidens"] * 12
    total += p_stats["catches"] * 8
    total += p_stats["stumpings"] * 12
    return total

def update_sim_step():
    sim = STATE["simState"]
    script = STATE["simulationScript"]
    idx = sim["currentBallIndex"]
    if idx >= len(script):
        sim["isLive"] = False
        return False
    
    event = script[idx]
    process_sim_event(event)
    sim["currentBallIndex"] += 1
    sim["isLive"] = (sim["currentBallIndex"] < len(script))
    update_leaderboard()
    return True

def process_sim_event(event):
    sim = STATE["simState"]
    sim["commentary"].insert(0, event)
    sim["score"]["runs"] += event.get("runs", 0)
    if event.get("isWicket"):
        sim["score"]["wickets"] += 1
    sim["score"]["overs"] = str(event.get("ball", "0.0"))
    
    match = STATE["matches"][0]
    batsman = next((p for p in match["players"] if p["name"] == event.get("batsman")), None)
    bowler = next((p for p in match["players"] if p["name"] == event.get("bowler")), None)
    
    if batsman and batsman["id"] in sim["playerLivePoints"]:
        b_pts = sim["playerLivePoints"][batsman["id"]]
        b_pts["runs"] += event.get("runs", 0)
        if event.get("runs") == 4: b_pts["fours"] += 1
        elif event.get("runs") == 6: b_pts["sixes"] += 1
        b_pts["total"] = calculate_player_points(b_pts)
        
    if bowler and bowler["id"] in sim["playerLivePoints"]:
        bw_pts = sim["playerLivePoints"][bowler["id"]]
        if event.get("isWicket") and event.get("wicketType") != "runout":
            bw_pts["wickets"] += 1
            if event.get("wicketType") in ["bowled", "lbw"]:
                bw_pts["bowled_lbw"] += 1
        bw_pts["total"] = calculate_player_points(bw_pts)
        
    if event.get("fielder"):
        fielder = next((p for p in match["players"] if p["name"] == event.get("fielder")), None)
        if fielder and fielder["id"] in sim["playerLivePoints"]:
            f_pts = sim["playerLivePoints"][fielder["id"]]
            if event.get("wicketType") == "caught": f_pts["catches"] += 1
            elif event.get("wicketType") == "stumped": f_pts["stumpings"] += 1
            f_pts["total"] = calculate_player_points(f_pts)

def update_leaderboard():
    sim = STATE["simState"]
    pts_map = sim["playerLivePoints"]
    lb = []
    
    for team in STATE["userTeams"]:
        u_pts = 0
        for pid in team["players"]:
            base = pts_map.get(pid, {}).get("total", 0)
            if pid == team["captain"]: u_pts += base * 2
            elif pid == team["viceCaptain"]: u_pts += int(base * 1.5)
            else: u_pts += base
        lb.append({
            "name": f"{STATE['user']['name']} ({team['name']})",
            "points": u_pts,
            "isUser": True,
            "avatar": STATE["user"]["avatar"],
            "captain": team.get("captainName", "C"),
            "viceCaptain": team.get("viceCaptainName", "VC")
        })
        
    progress_factor = (sim["currentBallIndex"] / max(1, len(STATE["simulationScript"])))
    for comp in COMPETITORS:
        c_base = int(comp["basePoints"] * progress_factor)
        cap_pts = pts_map.get(comp["captain"], {}).get("total", 0) * 2
        vc_pts = int(pts_map.get(comp["viceCaptain"], {}).get("total", 0) * 1.5)
        c_total = c_base + cap_pts + vc_pts
        lb.append({
            "name": comp["name"],
            "points": c_total,
            "isUser": False,
            "avatar": comp["avatar"]
        })
        
    lb.sort(key=lambda x: x["points"], reverse=True)
    for rank, entry in enumerate(lb, start=1):
        entry["rank"] = rank
    sim["leaderboard"] = lb

class Fantasy11Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == "/api/data":
            self.send_json(STATE)
        elif path == "/api/user":
            self.send_json(STATE["user"])
        elif path == "/api/matches":
            self.send_json(STATE["matches"])
        elif path == "/api/contests/private":
            self.send_json(list(STATE.get("privateContests", {}).values()))
        elif path.startswith("/api/contests/private/"):
            code = path.split("/")[-1].upper()
            p_contest = STATE.get("privateContests", {}).get(code)
            if p_contest:
                self.send_json({"success": True, "contest": p_contest})
            else:
                self.send_json({"success": False, "message": "Private contest not found"}, status=404)
        elif path == "/api/user/transactions":
            self.send_json(STATE.get("transactions", []))
        elif path == "/api/contests":
            self.send_json(STATE["contests"])
        elif path == "/api/user/teams":
            self.send_json(STATE["userTeams"])
        elif path == "/api/user/contests":
            self.send_json(STATE["joinedContests"])
        elif path == "/api/simulation/state":
            self.send_json(STATE["simState"])
        else:
            return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {}

        if path == "/api/user/wallet/deposit-upi":
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

        elif path == "/api/user/wallet/add":
            amount = payload.get("amount", 100)
            STATE["user"]["wallet"]["deposited"] += amount
            self.send_json({"success": True, "wallet": STATE["user"]["wallet"]})
        elif path == "/api/user/teams":
            team_id = f"T{len(STATE['userTeams']) + 1}"
            team_obj = {
                "id": team_id,
                "name": payload.get("name", f"Team {len(STATE['userTeams']) + 1}"),
                "matchId": payload.get("matchId", "ind-aus-t20"),
                "players": payload.get("players", []),
                "captain": payload.get("captain"),
                "viceCaptain": payload.get("viceCaptain"),
                "captainName": payload.get("captainName"),
                "viceCaptainName": payload.get("viceCaptainName"),
                "creditsUsed": payload.get("creditsUsed", 0),
                "createdAt": "Just now"
            }
            STATE["userTeams"].append(team_obj)
            update_leaderboard()
            self.send_json({"success": True, "team": team_obj, "teams": STATE["userTeams"]})
        elif path == "/api/user/contests/join":
            contest_id = payload.get("contestId")
            team_id = payload.get("teamId")
            contest = next((c for c in STATE["contests"] if c["id"] == contest_id), None)
            if not contest:
                self.send_json({"success": False, "message": "Contest not found"}, status=400)
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
            
            contest["spotsLeft"] = max(0, contest["spotsLeft"] - 1)
            join_record = {
                "id": f"JC_{len(STATE['joinedContests']) + 1}",
                "contestId": contest_id,
                "contest": contest,
                "teamId": team_id,
                "entryFeePaid": entry_fee,
                "joinedAt": "Just now"
            }
            STATE["joinedContests"].append(join_record)
            self.send_json({"success": True, "joined": join_record, "wallet": wallet})
        elif path == "/api/contests/private/create":
            code = f"F11-{random.randint(100, 999)}"
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
        elif path == "/api/simulation/step":
            has_more = update_sim_step()
            self.send_json({"success": True, "hasMore": has_more, "state": STATE["simState"]})
        elif path == "/api/simulation/reset":
            STATE["simState"]["currentBallIndex"] = 0
            STATE["simState"]["score"] = {"team": "AUS", "runs": 0, "wickets": 0, "overs": "0.0"}
            STATE["simState"]["commentary"] = []
            STATE["simState"]["playerLivePoints"] = init_sim_player_points()
            STATE["simState"]["isLive"] = False
            update_leaderboard()
            self.send_json({"success": True, "state": STATE["simState"]})
        # ================= ADMIN APIS =================
        elif path == "/api/admin/contests/create":
            cid = f"c-custom-{len(STATE['contests']) + 1}"
            new_c = {
                "id": cid,
                "name": payload.get("name", "Custom Contest"),
                "badge": payload.get("badge", "SPECIAL"),
                "tag": payload.get("tag", "Guaranteed"),
                "totalPrize": payload.get("totalPrize", "₹1 Crore"),
                "prizeNum": int(payload.get("prizeNum", 10000000)),
                "firstPrize": payload.get("firstPrize", "₹25 Lakhs"),
                "entryFee": int(payload.get("entryFee", 49)),
                "originalFee": int(payload.get("entryFee", 49)),
                "discountFee": int(payload.get("entryFee", 49)),
                "totalSpots": int(payload.get("totalSpots", 10000)),
                "spotsLeft": int(payload.get("totalSpots", 10000)),
                "winnersPercent": payload.get("winnersPercent", "60%"),
                "maxTeams": int(payload.get("maxTeams", 10)),
                "type": payload.get("type", "mega"),
                "breakup": [
                    {"rank": "1st", "prize": payload.get("firstPrize", "₹25 Lakhs")},
                    {"rank": "2nd - 100th", "prize": "Cash Multipliers"}
                ]
            }
            STATE["contests"].insert(0, new_c)
            self.send_json({"success": True, "contest": new_c, "contests": STATE["contests"]})
        elif path == "/api/admin/contests/delete":
            cid = payload.get("contestId")
            STATE["contests"] = [c for c in STATE["contests"] if c["id"] != cid]
            self.send_json({"success": True, "contests": STATE["contests"]})
        elif path == "/api/admin/matches/create":
            mid = f"custom-match-{len(STATE['matches']) + 1}"
            new_m = {
                "id": mid,
                "title": payload.get("title", "India vs Pakistan"),
                "series": payload.get("series", "T20 Super League 2026"),
                "venue": payload.get("venue", "Melbourne Cricket Ground"),
                "team1": payload.get("team1", {"name": "India", "shortName": "IND", "color": "#1e40af", "logo": "🇮🇳"}),
                "team2": payload.get("team2", {"name": "Pakistan", "shortName": "PAK", "color": "#15803d", "logo": "🇵🇰"}),
                "status": "upcoming",
                "lineupsOut": True,
                "startTime": payload.get("startTime", "Tomorrow, 7:30 PM"),
                "timeLeftSeconds": 86400,
                "megaPrize": payload.get("megaPrize", "₹50 Crores"),
                "entryFee": int(payload.get("entryFee", 49)),
                "pitchReport": payload.get("pitchReport", "Hard bouncy pitch offering pace and true bounce."),
                "players": STATE["matches"][0]["players"]
            }
            STATE["matches"].insert(0, new_m)
            self.send_json({"success": True, "match": new_m, "matches": STATE["matches"]})
        elif path == "/api/admin/wallet/adjust":
            if "deposited" in payload: STATE["user"]["wallet"]["deposited"] = int(payload["deposited"])
            if "winnings" in payload: STATE["user"]["wallet"]["winnings"] = int(payload["winnings"])
            if "bonus" in payload: STATE["user"]["wallet"]["bonus"] = int(payload["bonus"])
            self.send_json({"success": True, "wallet": STATE["user"]["wallet"]})
        elif path == "/api/admin/live/custom-ball":
            event = {
                "ball": payload.get("ball", f"Live.{len(STATE['simState']['commentary']) + 1}"),
                "batsman": payload.get("batsman", "Travis Head"),
                "bowler": payload.get("bowler", "Jasprit Bumrah"),
                "runs": int(payload.get("runs", 4)),
                "isWicket": bool(payload.get("isWicket", False)),
                "wicketType": payload.get("wicketType"),
                "fielder": payload.get("fielder"),
                "comment": payload.get("comment", "ADMIN EVENT: Tremendous shot sent racing to the fence!")
            }
            process_sim_event(event)
            update_leaderboard()
            self.send_json({"success": True, "state": STATE["simState"]})
        else:
            self.send_json({"error": "Endpoint not found"}, status=404)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("", PORT), Fantasy11Handler)
    server.allow_reuse_address = True
    print(f"Fantasy11 Server running on http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
