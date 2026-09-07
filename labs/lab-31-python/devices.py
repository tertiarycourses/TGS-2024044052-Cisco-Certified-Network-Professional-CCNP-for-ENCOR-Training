"""Device inventory used by every script in Lab 31.

This is the shape you will meet in every network automation script and in the
ENCOR exam: a LIST of DICTIONARIES, one dictionary per device.
"""

DEVICES = [
    {"hostname": "R1-CORE",  "ip": "10.1.1.1",   "platform": "ISR4451",   "status": "up",   "uptime_days": 412},
    {"hostname": "R2-EDGE",  "ip": "10.1.1.2",   "platform": "ISR4331",   "status": "up",   "uptime_days": 287},
    {"hostname": "SW1-ACC",  "ip": "10.1.2.11",  "platform": "C9200-24P", "status": "up",   "uptime_days": 198},
    {"hostname": "SW2-ACC",  "ip": "10.1.2.12",  "platform": "C9200-24P", "status": "down", "uptime_days": 0},
    {"hostname": "SW3-DIST", "ip": "10.1.2.1",   "platform": "C9300-48U", "status": "up",   "uptime_days": 365},
    {"hostname": "WLC1",     "ip": "10.1.3.1",   "platform": "C9800-CL",  "status": "up",   "uptime_days": 145},
]
