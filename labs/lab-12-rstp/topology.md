# Lab 12 Topology — Configure RSTP and Tune the Spanning Tree

```text
                 [  S1  ]  <- should be ROOT (priority 4096)
                 /        \
          Gi0/1 /          \ Gi0/2
        [  S2  ] ---------- [  S3  ]  <- currently root (WRONG)
          secondary root      access switch
```
