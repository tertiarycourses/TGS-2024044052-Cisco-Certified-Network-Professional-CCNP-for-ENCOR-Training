# Lab 16 Topology — Configure Multiarea OSPFv2 with Summarization and Filtering

```text
   Area 1              Area 0 (backbone)             Area 2
  172.16.1.0/24                                     192.168.1.0/24
      |                                                   |
    [ R1 ] ==== 172.16.3.0/30 ==== [ R2 ]                 |
    ABR          \                                       |
                  \____ 192.168.10.4/30 ____ [ R3 ] -----+
                                              ABR / stub
```
