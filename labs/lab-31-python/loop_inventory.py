"""Loop the inventory and print one line per device."""
from devices import DEVICES

for d in DEVICES:
    print(f"{d['hostname']:<10} {d['ip']:<12} {d['platform']}")
