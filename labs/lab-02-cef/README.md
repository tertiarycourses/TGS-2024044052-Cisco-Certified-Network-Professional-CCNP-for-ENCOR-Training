# Lab 2 — Analyse Cisco Express Forwarding

**Topic 01: Enterprise Architecture** · 15% of the exam · Skills Framework K1, A1 (ICT-DIT-3009-1.1)

## Exam Objective

Describe and verify CEF, the FIB and the adjacency table, and contrast them with process and fast switching (ENCOR 1.6).

## Scenario

Continuing as the campus engineer, you now move up to Layer 3 and prove how the router forwards in hardware. You examine the RIB, then the FIB that CEF builds from it ahead of any traffic, then the adjacency table that holds the Layer 2 rewrite. You disable CEF to watch forwarding fall back to process switching, observe the CPU cost, and re-enable it.

## What You'll Build

A side-by-side record of the RIB, the FIB and the adjacency table for one destination prefix, plus measured evidence of the CPU difference when CEF is disabled.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1 and R2 routers, PC-A and PC-B.

## Topology

```text
  PC-A                R1                     R2                PC-B
192.168.10.10 --- G0/0        S0/0/0 ---- S0/0/0        G0/0 --- 192.168.20.10
              192.168.10.1  10.1.1.1    10.1.1.2   192.168.20.1
                            \____ 10.1.1.0/30 ____/
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-02-cef.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Notes |
| --- | --- | --- | --- | --- |
| R1 | G0/0 | 192.168.10.1 | 255.255.255.0 | LAN side |
| R1 | S0/0/0 | 10.1.1.1 | 255.255.255.252 | Link to R2 |
| R2 | S0/0/0 | 10.1.1.2 | 255.255.255.252 | Link to R1 |
| R2 | G0/0 | 192.168.20.1 | 255.255.255.0 | Remote LAN |
| PC-A | NIC | 192.168.10.10 | 255.255.255.0 | Gateway 192.168.10.1 |
| PC-B | NIC | 192.168.20.10 | 255.255.255.0 | Gateway 192.168.20.1 |

## Steps

1. Open lab-02-cef/lab-02-cef.pkt and confirm R1 G0/0 is 192.168.10.1 and the R1–R2 link is 10.1.1.0/30
2. Display the routing table (the RIB) — the control plane's view of the network

   ```text
   R1# show ip route
   ```

3. Display the FIB that CEF has pre-built from that RIB

   ```text
   R1# show ip cef
   ```

4. Look at one specific prefix in the FIB and note its next hop and outgoing interface

   ```text
   R1# show ip cef 192.168.20.0
   ```

5. Display the adjacency table holding the Layer 2 rewrite string for that next hop

   ```text
   R1# show adjacency detail
   ```

6. Confirm CEF is enabled globally and per interface

   ```text
   R1# show ip interface brief | include Protocol
   ```

7. Baseline the CPU before you change anything

   ```text
   R1# show processes cpu sorted | include CPU
   ```

8. Disable CEF globally to force process switching

   ```text
   R1(config)# no ip cef
   ```

9. Generate sustained traffic from PC-A to PC-B and observe the CPU climb

   ```text
   C:\> ping 192.168.20.10 -n 100
   ```

10. Re-check the CPU utilisation and record the difference

   ```text
   R1# show processes cpu sorted | include CPU
   ```

11. Re-enable CEF and confirm the FIB is repopulated

   ```text
   R1(config)# ip cef
   ```

12. Verify the FIB is back and traffic is switched in hardware again

   ```text
   R1# show ip cef summary
   ```


## Validation

'show ip cef' returns a populated FIB and 'show adjacency detail' shows a valid rewrite for the next hop; with CEF disabled you can point to a measurably higher CPU figure during the ping, and it falls again once CEF is re-enabled.

## Checkpoint Questions

1. What is the difference between the RIB and the FIB?
1. Why is CEF called 'topology-based' rather than 'traffic-driven'?
1. What did the CPU do differently when you disabled CEF?
1. Which two tables must both be populated for CEF to switch a packet in hardware?

## Exam Focus

CEF is the default and the answer to almost every 'which switching method is fastest' question. Remember the pair: the FIB holds the forwarding decision, the adjacency table holds the Layer 2 rewrite. Both are built BEFORE traffic arrives.
