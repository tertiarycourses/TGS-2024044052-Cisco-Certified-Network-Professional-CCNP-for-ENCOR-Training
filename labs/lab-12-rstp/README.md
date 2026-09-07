# Lab 12 — Configure RSTP and Tune the Spanning Tree

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify common Spanning Tree Protocols — RSTP — and Spanning Tree enhancements (ENCOR 3.1.c).

## Scenario

The spanning tree in the distribution block elected an access switch as root, so traffic between two distribution switches is taking a suboptimal path through the wiring closet. As the engineer you deterministically move the root where it belongs, tune the port costs, migrate the network from legacy PVST+ to Rapid PVST+, and measure the convergence improvement.

## What You'll Build

A spanning tree with S1 as the deterministic root bridge and S2 as the secondary, running Rapid PVST+, with a measured convergence time on link failure.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches, PC-A.

## Topology

```text
                 [  S1  ]  <- should be ROOT (priority 4096)
                 /        \
          Gi0/1 /          \ Gi0/2
        [  S2  ] ---------- [  S3  ]  <- currently root (WRONG)
          secondary root      access switch
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-12-rstp.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Bridge Priority | MAC Address | Role Before | Role After | Notes |
| --- | --- | --- | --- | --- | --- |
| S1 | 32769 | 0001.aaaa.1111 | Non-root | ROOT (priority 4096) | Intended root bridge |
| S2 | 32769 | 0002.bbbb.2222 | Non-root | Secondary root (28672) | Intended backup root |
| S3 | 32769 | 0003.cccc.3333 | ROOT (wrong) | Non-root | Access switch, wrongly root |
| PC-A | N/A | 000c.dddd.4444 | N/A | N/A | Used to time convergence |

## Steps

1. Open lab-12-rstp/lab-12-rstp.pkt and identify which switch is currently root for VLAN 1

   ```text
   S1# show spanning-tree vlan 1
   ```

2. Note the root bridge ID and compare it with each switch's own bridge ID

   ```text
   S1# show spanning-tree vlan 1 | include Root ID|Bridge ID
   ```

3. Record which ports are root, designated and blocking across the three switches

   ```text
   S1# show spanning-tree vlan 1 | include Desg|Root|Altn
   ```

4. Make S1 the primary root using the macro, which sets a priority below the current root

   ```text
   S1(config)# spanning-tree vlan 1 root primary
   ```

5. Make S2 the secondary root so failover is also deterministic

   ```text
   S2(config)# spanning-tree vlan 1 root secondary
   ```

6. Verify S1 now reports 'This bridge is the root'

   ```text
   S1# show spanning-tree vlan 1
   ```

7. Set an exact priority instead of the macro to see the increments of 4096

   ```text
   S1(config)# spanning-tree vlan 1 priority 4096
   ```

8. Examine the port cost on the root port before you change it

   ```text
   S3# show spanning-tree vlan 1 interface FastEthernet0/1 cost
   ```

9. Manipulate the path by raising the cost on one link so the other becomes preferred

   ```text
   S3(config-if)# spanning-tree cost 100
   ```

10. Confirm the root port moved to the lower-cost path

   ```text
   S3# show spanning-tree vlan 1
   ```

11. Migrate all three switches from PVST+ to Rapid PVST+

   ```text
   S1(config)# spanning-tree mode rapid-pvst
   ```

12. Verify the protocol is now rstp and note the alternate and backup port roles

   ```text
   S1# show spanning-tree vlan 1 | include protocol
   ```

13. Shut the root port on S3 and time how long the alternate port takes to forward

   ```text
   S3(config-if)# shutdown
   ```

14. Bring the port back and record the convergence figures for both protocols

   ```text
   S3(config-if)# no shutdown
   ```


## Validation

'show spanning-tree vlan 1' on S1 states 'This bridge is the root' with priority 4096, all switches report protocol rstp, and your recorded convergence after the link failure is seconds rather than the 30–50 seconds of legacy STP.

## Checkpoint Questions

1. What two values make up the bridge ID, and which is compared first?
1. In what increments must STP priority be set, and why?
1. What are the two new port roles RSTP adds over legacy STP?
1. Roughly how long does legacy STP take to converge, and RSTP?

## Exam Focus

Lowest bridge ID wins the root election, and priority is compared before MAC. Priority must be a multiple of 4096. RSTP converges in seconds because proposal/agreement and alternate ports are pre-computed.
