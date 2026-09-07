# Lab 10 Topology — Troubleshoot 802.1Q Trunking and DTP

```text
        PC1 (VLAN 20 - AFFECTED)      Server (VLAN 20)
              |                              |
   [  S1  ] =========== trunk =========== [  S2  ]
      |  Gi0/1        (802.1Q)        Gi0/1  |
   [  S3  ]                                  PC0/PC2
   Native VLAN 99 must match on both ends; VLANs 10, 20, 99 must be allowed.
```
