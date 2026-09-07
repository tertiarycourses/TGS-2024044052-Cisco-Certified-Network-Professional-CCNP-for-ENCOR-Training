# Lab 21 Topology — Configure NTP, NAT/PAT and HSRP

```text
     PC-A (gateway 192.168.1.254 — the HSRP virtual IP)
             |
       [  S1  ]
        /      \
   [ R1 ]      [ R3 ]        R1: priority 110, preempt -> ACTIVE
  ACTIVE       STANDBY       R3: priority 100          -> STANDBY
     |
  S0/0/0 209.165.200.226  (NTP master, NAT outside)
```
