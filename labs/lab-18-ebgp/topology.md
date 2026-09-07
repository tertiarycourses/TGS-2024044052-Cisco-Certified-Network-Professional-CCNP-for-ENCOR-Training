# Lab 18 Topology — Configure and Verify eBGP

```text
            AS 65000 (ISP)
      [ ISP-Entry-1 ]      [ ISP-Entry-2 ]
        1.1.1.1              1.1.1.9
           |                    |
        1.1.1.2              1.1.1.6
      [        ACME1 — AS 65001        ]
              192.168.0.0/24
   eBGP to both entry points for multihomed resilience.
```
