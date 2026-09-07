# Lab 7 Topology — Configure and Verify a GRE Tunnel

```text
  PCA                RA                              RB                PCB
192.168.1.2 --- G0/0    S0/0/0 --- [ internet ] --- S0/0/0    G0/0 --- 192.168.2.2
            192.168.1.1  64.103.211.2          209.165.122.2  192.168.2.1
                          \                                  /
                           Tunnel0 10.10.10.1 -- 10.10.10.2 (GRE)
```
