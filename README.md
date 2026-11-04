# TechVerse-Monitor

### Network User Monitoring & Upload Bandwidth Analytics System

## About the Project

TechVerse-Monitor is a Python-based network monitoring system that tracks users across a network and analyzes their upload bandwidth usage.

It collects user-wise bandwidth information through an API and generates statistics to understand network usage.

## Features

- **User Monitoring:** Tracks users detected across the network.
- **Upload Bandwidth Tracking:** Monitors individual users' upload speeds in Mbps.
- **User Statistics:** Maintains frequency, maximum speed, and last seen time.
- **Continuous Monitoring:** Fetches network data at regular intervals.
- **Final Report:** Generates a user-wise report with bandwidth statistics.

## Technologies Used

- Python
- Requests Library
- HTTP API
- JSON
- Datetime
- Collections (Defaultdict)

## Project Structure

```text
TechVerse-Monitor/
│
├── network_monitor.py
├── network_server.py
├── requirements.txt
└── README.md
```

## Installation & Setup

**1. Clone the repository**

```bash
git clone YOUR_REPOSITORY_URL
cd TechVerse-Monitor
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Start the network server**

```bash
python network_server.py
```

**4. Configure your API endpoint**

Set your private API endpoint in `network_monitor.py`.

**5. Run the monitoring script**

```bash
python network_monitor.py
```

Press `CTRL + C` to stop monitoring and generate the final report.

## How It Works

1. The network server provides user-wise upload bandwidth data.
2. The monitoring script fetches data through an API.
3. User information and upload speeds are processed.
4. Individual user statistics are updated continuously.
5. A final report is generated when monitoring stops.

## Future Scope

- Real-time monitoring dashboard.
- Historical bandwidth analysis.
- Database integration.
- Bandwidth usage alerts.
- Graphical representation of network statistics.

## Author

**Himani Chhangani**

B.Tech | Computer Science & Engineering
