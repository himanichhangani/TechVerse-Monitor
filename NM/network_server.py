"""
TechVerse-Network -- local fake bandwidth API server for TechVerse-Monitor testing.

Serves the endpoint TechVerse-Monitor polls:
    GET /api/..../..../... ->  {"data": [{"Username": "...", "Speed": "12.34Mbps"}, ...]}

Run:
    python techverse_network_server.py

Then in techverse_monitor.py (or your own script), set:
    URL = ""
 """

import json
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = ""
PORT = 8000
POOL_SIZE = 200
TOP_N = 20

PREFIXES = ["LL", "ILL-CUST"]
SURNAMES = [
    "Sharma", "Verma", "Rathore", "Jain", "Meena", "Choudhary", "Gupta", "Singh",
    "Yadav", "Agarwal", "Kumawat", "Bansal", "Pareek", "Soni", "Mishra", "Chauhan",
    "Tiwari", "Nair", "Joshi", "Kapoor", "Bhatt", "Saxena", "Rawat", "Panwar",
    "Solanki", "Purohit", "Vyas", "Goyal",
]


def build_user_pool(size):
    pool = []
    used_ids = set()
    for i in range(size):
        prefix = PREFIXES[i % len(PREFIXES)]
        while True:
            uid = random.randint(1000, 9999)
            if uid not in used_ids:
                used_ids.add(uid)
                break
        if prefix == "LL":
            sur = SURNAMES[i % len(SURNAMES)]
            pool.append(f"LL-{uid}-{sur}")
        else:
            pool.append(f"ILL-CUST-{uid}")
    return pool


USER_POOL = build_user_pool(POOL_SIZE)
BASELINE = {u: random.uniform(3, 98) for u in USER_POOL}


def generate_top20():
    online_count = random.randint(60, 160)
    online = random.sample(USER_POOL, min(online_count, len(USER_POOL)))
    scored = []
    for u in online:
        jitter = random.uniform(-9, 9)
        spike = random.uniform(0, 60) if random.random() < 0.04 else 0
        speed = max(0.5, BASELINE[u] + jitter + spike)
        scored.append({"Username": u, "Speed": f"{speed:.2f}Mbps"})
    scored.sort(key=lambda r: float(r["Speed"].replace("Mbps", "")), reverse=True)
    return scored[:TOP_N]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {fmt % args}")

    def do_GET(self):
        if self.path.startswith("/api/v1/info/top20/upload"):
            payload = {"data": generate_top20()}
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')


if __name__ == "__main__":
    print("=" * 70)
    print("TechVerse-Network -- Simulated Bandwidth API")
    print(f"Serving  : http://{HOST}:{PORT}/api/.../.../...")
    print(f"User pool: {POOL_SIZE} (top {TOP_N} returned per request)")
    print("Point TechVerse-Monitor's URL here. Press CTRL+C to stop.")
    print("=" * 70)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nTechVerse-Network stopped.")
