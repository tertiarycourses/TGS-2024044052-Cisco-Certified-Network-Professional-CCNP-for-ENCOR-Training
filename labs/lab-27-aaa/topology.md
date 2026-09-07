# Lab 27 Topology — Implement Local and Server-Based AAA

```text
   PC-A --- [ R1 ] --- [ R2 ] --- [ R3 ] --- PC-C
             TACACS+       |         RADIUS
             client        |         client
                    TACACS+ Server   RADIUS Server
                    192.168.2.2      192.168.3.2
   Always configure the LOCAL fallback before 'aaa new-model'.
```
