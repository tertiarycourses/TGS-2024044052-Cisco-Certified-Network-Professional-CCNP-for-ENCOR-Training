"""This script has a deliberate indentation bug. Find it, fix it, and add a
comment explaining WHY Python cared."""
from devices import DEVICES

total = 0
for d in DEVICES:
    if d["status"] == "up":
        total += d["uptime_days"]
print("Total uptime of devices that are up:", total)

# The bug: the print below is indented INSIDE the loop, so it runs once per
# device instead of once at the end. Move it to column 0 to fix it.
for d in DEVICES:
    pass
    print("This line runs 6 times, but should run once.")
