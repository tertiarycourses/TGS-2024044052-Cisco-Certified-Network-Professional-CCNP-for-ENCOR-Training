"""What happens when a key does not exist? Predict, then run, then fix."""
from devices import DEVICES

d = DEVICES[0]
print(d["hostname"])
print(d["serial"])       # <-- this raises KeyError. Why?

# THE FIX — uncomment these two lines and comment out the line above:
# print(d.get("serial"))                  # returns None instead of raising
# print(d.get("serial", "not recorded"))  # returns your default instead
