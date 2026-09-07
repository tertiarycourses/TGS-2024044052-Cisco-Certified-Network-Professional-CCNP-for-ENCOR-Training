"""Flag any device that is not up — a conditional inside a loop."""
from devices import DEVICES

for d in DEVICES:
    if d["status"] != "up":
        print(f"ALERT: {d['hostname']} ({d['ip']}) is {d['status'].upper()}")
    else:
        print(f"ok   : {d['hostname']}")


def devices_down(inventory):
    """Return only the devices that are down. Note what this RETURNS: a list."""
    return [d for d in inventory if d["status"] != "up"]


print()
print("Down count:", len(devices_down(DEVICES)))
