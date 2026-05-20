import urllib.request
import urllib.parse
import json

BASE = "http://localhost:8080"

def call(endpoint, params=None):
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{BASE}{endpoint}?{query}"
    else:
        url = f"{BASE}{endpoint}"

    with urllib.request.urlopen(url) as response:
        data = response.read().decode()
        return json.loads(data)

print("\n--- TEST 1: Set Home Page ---")
print(call("/setHome", {"url": "index.html"}))

print("\n--- TEST 2: Visit Club Page 1 ---")
print(call("/visit", {"url": "club.html?id=1"}))

print("\n--- TEST 3: Visit Club Page 2 ---")
print(call("/visit", {"url": "club.html?id=2"}))

print("\n--- TEST 4: Visit Club Page 1 Again (should move to front, no duplicate) ---")
print(call("/visit", {"url": "club.html?id=1"}))

print("\n--- TEST 5: Visit Home Page (should be ignored if you added ignore rule) ---")
print(call("/visit", {"url": "index.html"}))

print("\n--- TEST 6: Get History ---")
print(call("/history"))

print("\n--- TEST 7: Remove Most Recent Entry ---")
remove_result = call("/remove")
print("REMOVE RESULT:", remove_result)

print("\n--- TEST 8: History After Removal ---")
history_after = call("/history")
print("UPDATED HISTORY:", history_after)