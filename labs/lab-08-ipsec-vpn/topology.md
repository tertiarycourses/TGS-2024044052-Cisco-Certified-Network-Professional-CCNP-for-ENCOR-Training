# Lab 8 Topology — Configure and Verify a Site-to-Site IPsec VPN

```text
  PC-A            R1              R2 (ISP)            R3            PC-C
192.168.1.3 --- G0/0  S0/0/0 --- S0/0/0  S0/0/1 --- S0/0/1  G0/0 --- 192.168.3.3
            192.168.1.1 10.1.1.2  10.1.1.1 10.2.2.1  10.2.2.2 192.168.3.1
                        \________ IPsec tunnel (protects 192.168.1.0 <-> 192.168.3.0) ________/
```
