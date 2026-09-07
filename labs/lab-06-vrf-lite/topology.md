# Lab 6 Topology — Configure and Verify VRF-Lite

```text
                    +----------------+
   CORP-PC -------- | G0/0  VRF CORP |
 192.168.1.10       |                |   R1 — one router, two routing tables
   GUEST-PC ------- | G0/1  VRF GUEST|
 192.168.1.10       +----------------+
   (identical addresses — isolated because they are in different VRFs)
```
