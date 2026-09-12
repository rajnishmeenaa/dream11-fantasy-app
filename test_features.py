import urllib.request
import json

base = 'http://localhost:8000'

def test_url(url):
    req = urllib.request.urlopen(url)
    return req.getcode(), req.read().decode('utf-8')

# 1. Manifest
code, data = test_url(f'{base}/manifest.json')
manifest = json.loads(data)
print(f"1. Manifest: OK (name: {manifest['name']})")

# 2. Service Worker
code, data = test_url(f'{base}/sw.js')
print(f"2. Service Worker: OK ({len(data)} bytes)")

# 3. Matches
code, data = test_url(f'{base}/api/matches')
matches = json.loads(data)
sports = [m.get('sport', 'cricket') for m in matches]
print(f"3. Matches: OK ({len(matches)} matches, sports: {set(sports)})")

# 4. Create Private Contest
req = urllib.request.Request(
    f'{base}/api/contests/private/create',
    data=json.dumps({
        'name': 'Weekend UCL Derby',
        'matchId': 'rma-mci-ucl',
        'entryFee': 50,
        'totalSpots': 5,
        'teamId': 'T1',
        'hostName': 'DreamChampion'
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
code_gen = res.get('code')
print(f"4. Create Private Contest: OK (Code: {code_gen}, Contest ID: {res['contest']['id']})")

# 5. Fetch Private Contest by Code
code, data = test_url(f'{base}/api/contests/private/{code_gen}')
p_contest = json.loads(data)
print(f"5. Fetch Private Contest: OK (Found: {p_contest['contest']['name']})")

# 6. Join Private Contest
req = urllib.request.Request(
    f'{base}/api/contests/private/join',
    data=json.dumps({
        'code': code_gen,
        'teamId': 'T1',
        'userName': 'FriendGamer_77'
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res_join = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
print(f"6. Join Private Contest: OK (Spots left: {res_join['contest']['spotsLeft']}, Participants: {len(res_join['contest']['participants'])})")

# 7. Simulation State
code, data = test_url(f'{base}/api/simulation/state')
sim = json.loads(data)
print(f"7. Simulation: OK (Score: {sim['score']['runs']}/{sim['score']['wickets']})")

print("\n>>> ALL TESTS PASSED WITH 100% SUCCESS! <<<")
