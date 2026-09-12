import urllib.request
import json

tests = [
    ("User App", "http://localhost:8000/index.html"),
    ("Admin App", "http://localhost:8000/admin.html"),
    ("Admin Manifest", "http://localhost:8000/manifest-admin.json"),
    ("API Data", "http://localhost:8000/api/data")
]

for name, url in tests:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as res:
            data = res.read()
            print(f"[PASS] {name} ({url}) -> Status: {res.status}, Size: {len(data)} bytes")
    except Exception as e:
        print(f"[FAIL] {name} ({url}) -> {e}")
