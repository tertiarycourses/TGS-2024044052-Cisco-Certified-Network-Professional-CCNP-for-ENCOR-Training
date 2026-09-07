"""The full inventory report — the target output for Lab 31."""
from devices import DEVICES

print(f"{'HOSTNAME':<10} {'IP':<12} {'PLATFORM':<12} {'STATUS':<7} {'UPTIME':>7}")
print("-" * 52)
for d in DEVICES:
    print(f"{d['hostname']:<10} {d['ip']:<12} {d['platform']:<12} "
          f"{d['status']:<7} {d['uptime_days']:>5}d")
print("-" * 52)
up = [d for d in DEVICES if d["status"] == "up"]
print(f"{len(up)} of {len(DEVICES)} devices up "
      f"({len(up) / len(DEVICES) * 100:.0f}%)")
