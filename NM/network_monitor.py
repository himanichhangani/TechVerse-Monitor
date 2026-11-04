iport time
from collections import defaultdict
from datetime import datetime
import requests

# Config
URL = "api end point"  # TechVerse-Network local server
INTERVAL = 3  # seconds between poll

session = requests.Session()

# Per-user stats: how often seen, max/avg speed, last seen time
users = defaultdict(lambda: {
    "count": 0,
    "max": 0.0,
    "total": 0.0,
    "last_seen": ""
})
samples = 0
start = datetime.now()

print("=" * 90)
print("TechVerse-Monitor Started")
print("Pulling data from TechVerse-Network")
print(f"Started : {start.strftime('%d-%m-%Y %H:%M:%S')}")
print("Press CTRL+C to stop")
print("=" * 90)

try:
    while True:
        try:
            response = session.get(URL, timeout=10)
            response.raise_for_status()
            json_data = response.json()
            if "data" not in json_data:
                print("\nNo data received.")
                time.sleep(INTERVAL)
                continue

            samples += 1
            now = datetime.now().strftime("%H:%M:%S")

            for row in json_data["data"]:
                username = row["Username"]
                speed = float(row["Speed"].replace("Mbps", "").strip())
                info = users[username]
                info["count"] += 1
                info["total"] += speed
                info["last_seen"] = now
                info["max"] = max(info["max"], speed)

            print(
                f"\rSamples: {samples} | Unique Users: {len(users)} | Last Poll: {now}",
                end="",
                flush=True
            )
        except Exception as e:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ERROR -> {e}")
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    runtime = datetime.now() - start
    print("\n")
    print("=" * 155)
    print("TECHVERSE-MONITOR -- FINAL REPORT")
    print("=" * 155)
    print(f"Runtime       : {runtime}")
    print(f"Total Samples : {samples}")
    print(f"Unique Users  : {len(users)}")
    print("=" * 155)
    print(
        f"{'Rank':<5}"
        f"{'Username':<30}"
        f"{'Frequency':>10}"
        f"{'Max Mbps':>12}"
        f"{'Total MB':>14}"
        f"{'Total GB':>12}"
        f"{'Last Seen':>15}"
    )
    print("-" * 155)

    report = sorted(users.items(), key=lambda x: x[1]["count"], reverse=True)
    for rank, (username, data) in enumerate(report, start=1):
        avg = data["total"] / data["count"]  # kept for internal calc, not printed
        total_mb = data["total"]
        total_gb = total_mb / 1024
        print(
            f"{rank:<5}"
            f"{username:<30}"
            f"{data['count']:>10}"
            f"{data['max']:>12.2f}"
            f"{total_mb:>14.2f}"
            f"{total_gb:>12.4f}"
            f"{data['last_seen']:>15}"
        )
    print("=" * 155)
