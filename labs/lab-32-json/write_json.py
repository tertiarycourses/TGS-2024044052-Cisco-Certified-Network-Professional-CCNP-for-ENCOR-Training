"""Serialise a Python dictionary back out to JSON."""
import json

new_device = {
    "hostname": "R3-BRANCH",
    "mgmt_ip": "10.1.1.3",
    "platform": "ISR4331",
    "uptime_days": 12,
    "enabled": True,          # Python True  -> JSON true
    "last_error": None,       # Python None  -> JSON null
    "interfaces": [
        {"name": "GigabitEthernet0/0/0", "ip": "10.1.1.3", "status": "up"}
    ],
}

# indent= makes it human readable; without it you get one long line
text = json.dumps(new_device, indent=2)
print(text)

with open("new_device.json", "w") as f:
    f.write(text)
print("\nWritten to new_device.json - validate it with: python3 -m json.tool new_device.json")
