import json

data = {
    "user": {
        "name": "Dream Champion",
        "username": "champion_xi",
        "avatar": "🏏",
        "level": 34,
        "wallet": {
            "deposited": 500,
            "winnings": 650,
            "bonus": 150
        },
        "stats": {
            "matchesPlayed": 42,
            "contestsWon": 27,
            "winRate": "64.3%",
            "totalWinnings": "₹18,450"
        }
    },
    "matches": [
        {
            "id": "ind-aus-t20",
            "title": "India vs Australia",
            "series": "Australia tour of India 2026 - 1st T20I",
            "venue": "Wankhede Stadium, Mumbai",
            "team1": {
                "name": "India",
                "shortName": "IND",
                "color": "#1e40af",
                "secondaryColor": "#3b82f6",
                "logo": "🇮🇳"
            },
            "team2": {
                "name": "Australia",
                "shortName": "AUS",
                "color": "#eab308",
                "secondaryColor": "#ca8a04",
                "logo": "🇦🇺"
            },
            "status": "upcoming",
            "lineupsOut": True,
            "startTime": "Today, 7:30 PM",
            "timeLeftSeconds": 1420,
            "megaPrize": "₹50 Crores",
            "entryFee": 49,
            "pitchReport": "Batting friendly surface with good carry. Dew expected in 2nd innings.",
            "players": [
                {"id": "ind_1", "name": "Rishabh Pant", "team": "IND", "role": "WK", "credits": 9.0, "points": 342, "selectedBy": "84.2%", "isPlaying": True, "cBy": "14.2%", "vcBy": "11.5%"},
                {"id": "ind_2", "name": "Sanju Samson", "team": "IND", "role": "WK", "credits": 8.5, "points": 280, "selectedBy": "52.8%", "isPlaying": True, "cBy": "6.1%", "vcBy": "8.0%"},
                {"id": "aus_1", "name": "Josh Inglis", "team": "AUS", "role": "WK", "credits": 8.5, "points": 298, "selectedBy": "61.5%", "isPlaying": True, "cBy": "5.4%", "vcBy": "7.2%"},
                {"id": "aus_2", "name": "Matthew Wade", "team": "AUS", "role": "WK", "credits": 8.0, "points": 175, "selectedBy": "22.1%", "isPlaying": False, "cBy": "1.2%", "vcBy": "2.1%"},
                
                {"id": "ind_3", "name": "Rohit Sharma", "team": "IND", "role": "BAT", "credits": 10.0, "points": 485, "selectedBy": "91.4%", "isPlaying": True, "cBy": "24.5%", "vcBy": "18.2%"},
                {"id": "ind_4", "name": "Virat Kohli", "team": "IND", "role": "BAT", "credits": 10.5, "points": 560, "selectedBy": "94.8%", "isPlaying": True, "cBy": "32.1%", "vcBy": "21.6%"},
                {"id": "ind_5", "name": "Suryakumar Yadav", "team": "IND", "role": "BAT", "credits": 9.5, "points": 430, "selectedBy": "87.3%", "isPlaying": True, "cBy": "18.4%", "vcBy": "15.9%"},
                {"id": "ind_6", "name": "Yashasvi Jaiswal", "team": "IND", "role": "BAT", "credits": 9.0, "points": 395, "selectedBy": "76.0%", "isPlaying": True, "cBy": "10.2%", "vcBy": "12.4%"},
                {"id": "aus_3", "name": "Travis Head", "team": "AUS", "role": "BAT", "credits": 9.5, "points": 472, "selectedBy": "88.9%", "isPlaying": True, "cBy": "22.3%", "vcBy": "16.8%"},
                {"id": "aus_4", "name": "Mitchell Marsh", "team": "AUS", "role": "BAT", "credits": 9.0, "points": 380, "selectedBy": "72.4%", "isPlaying": True, "cBy": "8.7%", "vcBy": "11.1%"},
                {"id": "aus_5", "name": "David Warner", "team": "AUS", "role": "BAT", "credits": 9.0, "points": 410, "selectedBy": "79.1%", "isPlaying": True, "cBy": "12.0%", "vcBy": "14.3%"},
                {"id": "aus_6", "name": "Tim David", "team": "AUS", "role": "BAT", "credits": 8.0, "points": 215, "selectedBy": "34.5%", "isPlaying": True, "cBy": "2.8%", "vcBy": "4.5%"},
                
                {"id": "ind_7", "name": "Hardik Pandya", "team": "IND", "role": "AR", "credits": 9.5, "points": 490, "selectedBy": "89.6%", "isPlaying": True, "cBy": "20.1%", "vcBy": "19.5%"},
                {"id": "ind_8", "name": "Ravindra Jadeja", "team": "IND", "role": "AR", "credits": 9.0, "points": 365, "selectedBy": "68.2%", "isPlaying": True, "cBy": "7.5%", "vcBy": "10.4%"},
                {"id": "ind_9", "name": "Axar Patel", "team": "IND", "role": "AR", "credits": 8.5, "points": 320, "selectedBy": "58.7%", "isPlaying": True, "cBy": "4.9%", "vcBy": "7.8%"},
                {"id": "aus_7", "name": "Glenn Maxwell", "team": "AUS", "role": "AR", "credits": 9.5, "points": 450, "selectedBy": "86.4%", "isPlaying": True, "cBy": "16.7%", "vcBy": "15.2%"},
                {"id": "aus_8", "name": "Marcus Stoinis", "team": "AUS", "role": "AR", "credits": 8.5, "points": 310, "selectedBy": "64.1%", "isPlaying": True, "cBy": "5.3%", "vcBy": "8.6%"},
                
                {"id": "ind_10", "name": "Jasprit Bumrah", "team": "IND", "role": "BOWL", "credits": 10.0, "points": 520, "selectedBy": "93.5%", "isPlaying": True, "cBy": "21.0%", "vcBy": "18.0%"},
                {"id": "ind_11", "name": "Arshdeep Singh", "team": "IND", "role": "BOWL", "credits": 8.5, "points": 340, "selectedBy": "63.8%", "isPlaying": True, "cBy": "4.1%", "vcBy": "6.9%"},
                {"id": "ind_12", "name": "Kuldeep Yadav", "team": "IND", "role": "BOWL", "credits": 9.0, "points": 385, "selectedBy": "71.2%", "isPlaying": True, "cBy": "6.5%", "vcBy": "9.4%"},
                {"id": "ind_13", "name": "Mohammed Siraj", "team": "IND", "role": "BOWL", "credits": 8.5, "points": 305, "selectedBy": "55.0%", "isPlaying": True, "cBy": "3.8%", "vcBy": "5.7%"},
                {"id": "aus_9", "name": "Pat Cummins", "team": "AUS", "role": "BOWL", "credits": 9.5, "points": 460, "selectedBy": "85.0%", "isPlaying": True, "cBy": "11.4%", "vcBy": "13.2%"},
                {"id": "aus_10", "name": "Mitchell Starc", "team": "AUS", "role": "BOWL", "credits": 9.0, "points": 415, "selectedBy": "78.4%", "isPlaying": True, "cBy": "9.1%", "vcBy": "11.7%"},
                {"id": "aus_11", "name": "Adam Zampa", "team": "AUS", "role": "BOWL", "credits": 8.5, "points": 350, "selectedBy": "67.0%", "isPlaying": True, "cBy": "4.5%", "vcBy": "7.3%"},
                {"id": "aus_12", "name": "Josh Hazlewood", "team": "AUS", "role": "BOWL", "credits": 8.5, "points": 330, "selectedBy": "60.3%", "isPlaying": True, "cBy": "3.9%", "vcBy": "6.1%"}
            ]
        },
        {
            "id": "csk-mi-ipl",
            "title": "Chennai Super Kings vs Mumbai Indians",
            "series": "Tata Indian Premier League 2026 - Match 14",
            "venue": "MA Chidambaram Stadium, Chepauk, Chennai",
            "team1": {
                "name": "Chennai Super Kings",
                "shortName": "CSK",
                "color": "#facc15",
                "secondaryColor": "#ca8a04",
                "logo": "🦁"
            },
            "team2": {
                "name": "Mumbai Indians",
                "shortName": "MI",
                "color": "#2563eb",
                "secondaryColor": "#1d4ed8",
                "logo": "⚡"
            },
            "status": "upcoming",
            "lineupsOut": True,
            "startTime": "Tomorrow, 7:30 PM",
            "timeLeftSeconds": 86400,
            "megaPrize": "₹45 Crores",
            "entryFee": 39,
            "pitchReport": "Classic Chepauk track. Spinners will get grip and turn in middle overs.",
            "players": [
                {"id": "csk_1", "name": "MS Dhoni", "team": "CSK", "role": "WK", "credits": 8.5, "points": 310, "selectedBy": "82.5%", "isPlaying": True, "cBy": "15.0%", "vcBy": "14.2%"},
                {"id": "mi_1", "name": "Ishan Kishan", "team": "MI", "role": "WK", "credits": 9.0, "points": 360, "selectedBy": "74.8%", "isPlaying": True, "cBy": "9.4%", "vcBy": "11.8%"},
                {"id": "csk_2", "name": "Ruturaj Gaikwad", "team": "CSK", "role": "BAT", "credits": 9.5, "points": 470, "selectedBy": "88.2%", "isPlaying": True, "cBy": "21.3%", "vcBy": "18.5%"},
                {"id": "csk_3", "name": "Shivam Dube", "team": "CSK", "role": "BAT", "credits": 9.0, "points": 420, "selectedBy": "81.0%", "isPlaying": True, "cBy": "14.2%", "vcBy": "15.0%"},
                {"id": "mi_2", "name": "Rohit Sharma", "team": "MI", "role": "BAT", "credits": 10.0, "points": 495, "selectedBy": "92.0%", "isPlaying": True, "cBy": "26.0%", "vcBy": "19.5%"},
                {"id": "mi_3", "name": "Suryakumar Yadav", "team": "MI", "role": "BAT", "credits": 9.5, "points": 445, "selectedBy": "86.5%", "isPlaying": True, "cBy": "18.0%", "vcBy": "16.1%"},
                {"id": "mi_4", "name": "Tilak Varma", "team": "MI", "role": "BAT", "credits": 8.5, "points": 330, "selectedBy": "61.0%", "isPlaying": True, "cBy": "5.1%", "vcBy": "7.5%"},
                {"id": "csk_4", "name": "Ravindra Jadeja", "team": "CSK", "role": "AR", "credits": 9.5, "points": 465, "selectedBy": "87.0%", "isPlaying": True, "cBy": "19.0%", "vcBy": "17.4%"},
                {"id": "csk_5", "name": "Moeen Ali", "team": "CSK", "role": "AR", "credits": 8.5, "points": 315, "selectedBy": "58.4%", "isPlaying": True, "cBy": "6.2%", "vcBy": "8.9%"},
                {"id": "mi_5", "name": "Hardik Pandya", "team": "MI", "role": "AR", "credits": 9.5, "points": 480, "selectedBy": "90.1%", "isPlaying": True, "cBy": "22.5%", "vcBy": "18.8%"},
                {"id": "csk_6", "name": "Matheesha Pathirana", "team": "CSK", "role": "BOWL", "credits": 9.0, "points": 435, "selectedBy": "83.4%", "isPlaying": True, "cBy": "12.1%", "vcBy": "13.6%"},
                {"id": "csk_7", "name": "Deepak Chahar", "team": "CSK", "role": "BOWL", "credits": 8.5, "points": 290, "selectedBy": "51.0%", "isPlaying": True, "cBy": "4.2%", "vcBy": "6.3%"},
                {"id": "mi_6", "name": "Jasprit Bumrah", "team": "MI", "role": "BOWL", "credits": 10.0, "points": 540, "selectedBy": "95.2%", "isPlaying": True, "cBy": "25.4%", "vcBy": "19.8%"},
                {"id": "mi_7", "name": "Gerald Coetzee", "team": "MI", "role": "BOWL", "credits": 8.5, "points": 320, "selectedBy": "59.0%", "isPlaying": True, "cBy": "4.8%", "vcBy": "7.1%"}
            ]
        },
        {
            "id": "rcb-kkr-ipl",
            "title": "Royal Challengers Bengaluru vs Kolkata Knight Riders",
            "series": "Tata Indian Premier League 2026 - Match 15",
            "venue": "M. Chinnaswamy Stadium, Bengaluru",
            "team1": {
                "name": "Royal Challengers Bengaluru",
                "shortName": "RCB",
                "color": "#dc2626",
                "secondaryColor": "#991b1b",
                "logo": "🔴"
            },
            "team2": {
                "name": "Kolkata Knight Riders",
                "shortName": "KKR",
                "color": "#7e22ce",
                "secondaryColor": "#581c87",
                "logo": "🟣"
            },
            "status": "upcoming",
            "lineupsOut": True,
            "startTime": "In 2 days, 7:30 PM",
            "timeLeftSeconds": 172800,
            "megaPrize": "₹35 Crores",
            "entryFee": 29,
            "pitchReport": "High-scoring paradise with short boundaries. Expect 200+ runs.",
            "players": [
                {"id": "rcb_1", "name": "Dinesh Karthik", "team": "RCB", "role": "WK", "credits": 8.5, "points": 340, "selectedBy": "65.0%", "isPlaying": True, "cBy": "6.0%", "vcBy": "8.0%"},
                {"id": "kkr_1", "name": "Philip Salt", "team": "KKR", "role": "WK", "credits": 9.0, "points": 430, "selectedBy": "82.0%", "isPlaying": True, "cBy": "15.0%", "vcBy": "14.0%"},
                {"id": "rcb_2", "name": "Virat Kohli", "team": "RCB", "role": "BAT", "credits": 10.5, "points": 580, "selectedBy": "96.0%", "isPlaying": True, "cBy": "38.0%", "vcBy": "22.0%"},
                {"id": "rcb_3", "name": "Faf du Plessis", "team": "RCB", "role": "BAT", "credits": 9.5, "points": 440, "selectedBy": "80.0%", "isPlaying": True, "cBy": "14.0%", "vcBy": "16.0%"},
                {"id": "kkr_2", "name": "Shreyas Iyer", "team": "KKR", "role": "BAT", "credits": 9.0, "points": 390, "selectedBy": "72.0%", "isPlaying": True, "cBy": "9.0%", "vcBy": "11.0%"},
                {"id": "kkr_3", "name": "Rinku Singh", "team": "KKR", "role": "BAT", "credits": 8.5, "points": 350, "selectedBy": "68.0%", "isPlaying": True, "cBy": "7.0%", "vcBy": "10.0%"},
                {"id": "rcb_4", "name": "Glenn Maxwell", "team": "RCB", "role": "AR", "credits": 9.5, "points": 430, "selectedBy": "81.0%", "isPlaying": True, "cBy": "16.0%", "vcBy": "15.0%"},
                {"id": "kkr_4", "name": "Sunil Narine", "team": "KKR", "role": "AR", "credits": 10.0, "points": 520, "selectedBy": "92.0%", "isPlaying": True, "cBy": "28.0%", "vcBy": "19.0%"},
                {"id": "kkr_5", "name": "Andre Russell", "team": "KKR", "role": "AR", "credits": 9.5, "points": 470, "selectedBy": "89.0%", "isPlaying": True, "cBy": "22.0%", "vcBy": "18.0%"},
                {"id": "rcb_5", "name": "Mohammed Siraj", "team": "RCB", "role": "BOWL", "credits": 9.0, "points": 370, "selectedBy": "70.0%", "isPlaying": True, "cBy": "6.0%", "vcBy": "8.0%"},
                {"id": "kkr_6", "name": "Mitchell Starc", "team": "KKR", "role": "BOWL", "credits": 9.0, "points": 410, "selectedBy": "76.0%", "isPlaying": True, "cBy": "8.0%", "vcBy": "11.0%"},
                {"id": "kkr_7", "name": "Varun Chakaravarthy", "team": "KKR", "role": "BOWL", "credits": 8.5, "points": 360, "selectedBy": "67.0%", "isPlaying": True, "cBy": "5.0%", "vcBy": "7.0%"}
            ]
        }
    ],
    "contests": [
        {
            "id": "c-mega-50cr",
            "name": "Mega Contest",
            "badge": "MEGA",
            "tag": "Guaranteed",
            "totalPrize": "₹50 Crores",
            "prizeNum": 500000000,
            "firstPrize": "₹2 Crores + Luxury SUV",
            "entryFee": 49,
            "originalFee": 49,
            "discountFee": 29,
            "totalSpots": 1000000,
            "spotsLeft": 784320,
            "winnersPercent": "65%",
            "maxTeams": 20,
            "type": "mega",
            "breakup": [
                {"rank": "1st", "prize": "₹2,00,00,000 + Luxury SUV"},
                {"rank": "2nd", "prize": "₹50,00,000"},
                {"rank": "3rd", "prize": "₹25,00,000"},
                {"rank": "4th - 5th", "prize": "₹10,00,000"},
                {"rank": "6th - 10th", "prize": "₹5,00,000"},
                {"rank": "11th - 50th", "prize": "₹1,00,000"},
                {"rank": "51st - 500th", "prize": "₹10,000"},
                {"rank": "501st - 5,000th", "prize": "₹1,000"},
                {"rank": "5,001st - 650,000th", "prize": "₹59 - ₹100"}
            ]
        },
        {
            "id": "c-h2h-10k",
            "name": "Head-to-Head (1 vs 1)",
            "badge": "H2H",
            "tag": "Winner Takes All",
            "totalPrize": "₹10,000",
            "prizeNum": 10000,
            "firstPrize": "₹10,000",
            "entryFee": 5750,
            "originalFee": 5750,
            "discountFee": 5750,
            "totalSpots": 2,
            "spotsLeft": 1,
            "winnersPercent": "50%",
            "maxTeams": 1,
            "type": "h2h",
            "breakup": [
                {"rank": "1st", "prize": "₹10,000"},
                {"rank": "2nd", "prize": "Better luck next time"}
            ]
        },
        {
            "id": "c-winner-3spots",
            "name": "3 Spots - Winner Takes All",
            "badge": "HOT",
            "tag": "High Returns",
            "totalPrize": "₹1,000",
            "prizeNum": 1000,
            "firstPrize": "₹1,000",
            "entryFee": 380,
            "originalFee": 380,
            "discountFee": 380,
            "totalSpots": 3,
            "spotsLeft": 2,
            "winnersPercent": "33%",
            "maxTeams": 1,
            "type": "wta",
            "breakup": [
                {"rank": "1st", "prize": "₹1,000"},
                {"rank": "2nd - 3rd", "prize": "₹0"}
            ]
        },
        {
            "id": "c-popular-25l",
            "name": "Popular League",
            "badge": "POPULAR",
            "tag": "Safe Play",
            "totalPrize": "₹25 Lakhs",
            "prizeNum": 2500000,
            "firstPrize": "₹2,50,000",
            "entryFee": 19,
            "originalFee": 19,
            "discountFee": 14,
            "totalSpots": 150000,
            "spotsLeft": 98200,
            "winnersPercent": "58%",
            "maxTeams": 10,
            "type": "popular",
            "breakup": [
                {"rank": "1st", "prize": "₹2,50,000"},
                {"rank": "2nd", "prize": "₹75,000"},
                {"rank": "3rd", "prize": "₹35,000"},
                {"rank": "4th - 10th", "prize": "₹10,000"},
                {"rank": "11th - 87,000th", "prize": "₹25 - ₹500"}
            ]
        },
        {
            "id": "c-practice-free",
            "name": "Practice Contest",
            "badge": "FREE",
            "tag": "Skill Builder",
            "totalPrize": "₹0",
            "prizeNum": 0,
            "firstPrize": "Leaderboard Glory",
            "entryFee": 0,
            "originalFee": 0,
            "discountFee": 0,
            "totalSpots": 5000,
            "spotsLeft": 4120,
            "winnersPercent": "100%",
            "maxTeams": 3,
            "type": "practice",
            "breakup": [
                {"rank": "1st - 5000th", "prize": "Bragging Rights & Dream Badges"}
            ]
        }
    ],
    "simulationScript": [
        {"ball": "0.1", "batsman": "Travis Head", "bowler": "Jasprit Bumrah", "runs": 0, "isWicket": False, "comment": "Bumrah starts with a blistering 145km/h in-swinger, Head leaves carefully to keeper."},
        {"ball": "0.2", "batsman": "Travis Head", "bowler": "Jasprit Bumrah", "runs": 4, "isWicket": False, "comment": "FOUR! Slashed through backward point! Travis Head opens his account in style! (+4 runs, +1 boundary bonus)"},
        {"ball": "0.3", "batsman": "Travis Head", "bowler": "Jasprit Bumrah", "runs": 0, "isWicket": False, "comment": "Beaten! Gorgeous seam movement from Bumrah, beats Head's outside edge."},
        {"ball": "0.4", "batsman": "Travis Head", "bowler": "Jasprit Bumrah", "runs": 0, "isWicket": True, "wicketType": "bowled", "fielder": None, "comment": "OUT! TIMBERRR! Jasprit Bumrah knocks the off-stump out of the ground! Golden strike! (+25 pts for Bumrah +8 pts bowled bonus)"},
        {"ball": "0.5", "batsman": "Mitchell Marsh", "bowler": "Jasprit Bumrah", "runs": 1, "isWicket": False, "comment": "Marsh tucks it to deep mid-wicket for a quick single, gets off the mark."},
        {"ball": "0.6", "batsman": "David Warner", "bowler": "Jasprit Bumrah", "runs": 1, "isWicket": False, "comment": "Steered towards third man for one. AUS: 6/1 after 1 over."},
        {"ball": "1.1", "batsman": "David Warner", "bowler": "Mohammed Siraj", "runs": 6, "isWicket": False, "comment": "SIX! BOOM! Warner picks the length early and pulls it deep into the Wankhede stands! (+6 runs, +2 six bonus)"},
        {"ball": "1.2", "batsman": "David Warner", "bowler": "Mohammed Siraj", "runs": 4, "isWicket": False, "comment": "FOUR! Back-to-back boundaries! Warner drives crisply through extra cover!"},
        {"ball": "1.3", "batsman": "David Warner", "bowler": "Mohammed Siraj", "runs": 2, "isWicket": False, "comment": "Punched down the ground, excellent running between the wickets."},
        {"ball": "1.4", "batsman": "David Warner", "bowler": "Mohammed Siraj", "runs": 0, "isWicket": True, "wicketType": "caught", "fielder": "Hardik Pandya", "comment": "OUT! CAUGHT! Siraj has the last laugh! Warner slices high in the air, Hardik takes a stunner at mid-off! (+25 pts Siraj, +8 pts Hardik)"},
        {"ball": "1.5", "batsman": "Glenn Maxwell", "bowler": "Mohammed Siraj", "runs": 4, "isWicket": False, "comment": "FOUR! The Big Show arrives! Reverse sweep straight to the third-man boundary!"},
        {"ball": "1.6", "batsman": "Glenn Maxwell", "bowler": "Mohammed Siraj", "runs": 1, "isWicket": False, "comment": "Tapped towards covers for a single. End of Over 2. AUS: 23/2."},
        {"ball": "2.1", "batsman": "Mitchell Marsh", "bowler": "Hardik Pandya", "runs": 6, "isWicket": False, "comment": "SIX! Mitchell Marsh launches Pandya straight back over the bowler's head!"},
        {"ball": "2.2", "batsman": "Mitchell Marsh", "bowler": "Hardik Pandya", "runs": 4, "isWicket": False, "comment": "FOUR! Cut away behind point! Wankhede is on fire tonight!"},
        {"ball": "2.3", "batsman": "Mitchell Marsh", "bowler": "Hardik Pandya", "runs": 1, "isWicket": False, "comment": "Worked into the leg side for a single."},
        {"ball": "2.4", "batsman": "Glenn Maxwell", "bowler": "Hardik Pandya", "runs": 6, "isWicket": False, "comment": "SIX! Switch hit into the second tier! Maxwell is putting on an absolute masterclass!"},
        {"ball": "2.5", "batsman": "Glenn Maxwell", "bowler": "Hardik Pandya", "runs": 0, "isWicket": True, "wicketType": "caught", "fielder": "Virat Kohli", "comment": "OUT! IN THE AIR AND TAKEN! Virat Kohli sprints from long-on and dives forward to grab a sensational catch! (+25 pts Pandya, +8 pts Kohli)"},
        {"ball": "2.6", "batsman": "Marcus Stoinis", "bowler": "Hardik Pandya", "runs": 2, "isWicket": False, "comment": "Stoinis pushes into gaps for a couple. End of Over 3. AUS: 42/3."},
        {"ball": "3.1", "batsman": "Marcus Stoinis", "bowler": "Ravindra Jadeja", "runs": 0, "isWicket": False, "comment": "Jadeja darts in a quick arm ball, defended stoutly."},
        {"ball": "3.2", "batsman": "Marcus Stoinis", "bowler": "Ravindra Jadeja", "runs": 0, "isWicket": True, "wicketType": "lbw", "fielder": None, "comment": "OUT! LBW! Jadeja strikes on his second ball! Trapped plumb in front! (+25 pts Jadeja + 8 pts LBW/Bowled bonus)"},
        {"ball": "3.3", "batsman": "Josh Inglis", "bowler": "Ravindra Jadeja", "runs": 4, "isWicket": False, "comment": "FOUR! Swept firmly through square leg by Josh Inglis!"},
        {"ball": "3.4", "batsman": "Josh Inglis", "bowler": "Ravindra Jadeja", "runs": 1, "isWicket": False, "comment": "Nudged towards long-on for one."},
        {"ball": "3.5", "batsman": "Mitchell Marsh", "bowler": "Ravindra Jadeja", "runs": 6, "isWicket": False, "comment": "SIX! Marsh clears his front leg and sends it into orbit over deep midwicket!"},
        {"ball": "3.6", "batsman": "Mitchell Marsh", "bowler": "Ravindra Jadeja", "runs": 0, "isWicket": True, "wicketType": "stumped", "fielder": "Rishabh Pant", "comment": "OUT! STUMPED! Jadeja drags the length back, Pant whips the bails off in a flash! Lightning hands! (+25 pts Jadeja, +12 pts Pant Stumping)"}
    ],
    "pointsSystem": {
        "batting": [
            {"action": "Run", "points": "+1"},
            {"action": "Boundary Bonus (4s)", "points": "+1"},
            {"action": "Six Bonus (6s)", "points": "+2"},
            {"action": "30 Run Bonus", "points": "+4"},
            {"action": "Half-Century (50 Runs)", "points": "+8"},
            {"action": "Century (100 Runs)", "points": "+16"},
            {"action": "Dismissal for Duck (BAT/WK/AR)", "points": "-2"}
        ],
        "bowling": [
            {"action": "Wicket (Excluding Run Out)", "points": "+25"},
            {"action": "Bonus (LBW / Bowled)", "points": "+8"},
            {"action": "3 Wicket Bonus", "points": "+4"},
            {"action": "4 Wicket Bonus", "points": "+8"},
            {"action": "5 Wicket Bonus", "points": "+16"},
            {"action": "Maiden Over", "points": "+12"}
        ],
        "fielding": [
            {"action": "Catch", "points": "+8"},
            {"action": "3 Catch Bonus", "points": "+4"},
            {"action": "Stumping", "points": "+12"},
            {"action": "Run Out (Direct Hit)", "points": "+12"},
            {"action": "Run Out (Thrower / Catcher)", "points": "+6 / +6"}
        ],
        "multipliers": [
            {"action": "Captain (C)", "points": "2X Points"},
            {"action": "Vice-Captain (VC)", "points": "1.5X Points"}
        ]
    }
}

with open(r'C:\Users\MY WORLD\.gemini\antigravity\scratch\dream11-fantasy-app\data\fantasy_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('fantasy_data.json successfully written!')
