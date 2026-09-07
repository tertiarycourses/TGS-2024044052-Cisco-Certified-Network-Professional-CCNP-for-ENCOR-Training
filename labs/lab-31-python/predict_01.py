"""Predict the output BEFORE you run this. Write your answer down first."""
from devices import DEVICES

print(len(DEVICES))
print(DEVICES[0]["hostname"])
print(DEVICES[-1]["ip"])
print(DEVICES[2]["platform"][:6])
