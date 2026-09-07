# Lab 29 Topology — Configure Control Plane Policing

```text
              control plane (CPU)
                     ^
                     |  service-policy input COPP-POLICY
              +------+------+
   OSPF ----> | COPP-CRITICAL | 512k  transmit  (never starve routing)
   SSH  ----> | COPP-MANAGEMENT| 256k drop
   ICMP ----> | COPP-ICMP      |  64k drop      (the flood vector)
              +---------------+
```
