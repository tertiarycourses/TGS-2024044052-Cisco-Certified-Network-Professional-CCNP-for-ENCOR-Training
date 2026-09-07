"""Parse the valid JSON file and confirm it becomes a Python dictionary."""
import json

with open("devices.json") as f:
    data = json.load(f)

print("Python type of the whole document :", type(data).__name__)
print("Python type of data['devices']    :", type(data["devices"]).__name__)
print("Python type of one device         :", type(data["devices"][0]).__name__)
print()
print("Site      :", data["site"])
print("Devices   :", len(data["devices"]))
print()
for d in data["devices"]:
    print(f"  {d['hostname']:<10} {d['mgmt_ip']:<12} "
          f"enabled={d['enabled']} last_error={d['last_error']}")
print()
# Navigating a NESTED structure — chained keys and indexes
print("Second device, first interface name:",
      data["devices"][1]["interfaces"][0]["name"])
