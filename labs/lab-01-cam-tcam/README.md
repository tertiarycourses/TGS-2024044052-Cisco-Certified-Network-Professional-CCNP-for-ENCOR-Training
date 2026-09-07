# Lab 1 — Investigate the CAM and TCAM Tables

**Topic 01: Enterprise Architecture** · 15% of the exam · Skills Framework K1, A1 (ICT-DIT-3009-1.1)

## Exam Objective

Describe hardware switching mechanisms such as CAM, TCAM, FIB, RIB and adjacency tables (ENCOR 1.6).

## Scenario

You take the role of a campus network engineer verifying how an access switch actually forwards a frame. You generate traffic between hosts, watch the MAC address table (CAM) populate by learning source addresses, then age an entry out and observe the switch flood the unknown unicast. You finish by inspecting how TCAM stores the masked ACL and QoS entries that CAM's exact-match lookup cannot hold.

## What You'll Build

A documented CAM table showing dynamically learned entries, one static entry you added, and a written comparison of CAM versus TCAM lookup behaviour.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, S1/S2 access switches, PC-A and PC-B.

## Topology

```text
    PC-A (192.168.10.10)          PC-B (192.168.10.20)
         |  Fa0/1                        |  Fa0/2
         +----------[  S1  ]-------------+
                       | Gi0/1 (trunk)
                    [  S2  ]
                       |
                    [  R1  ] 192.168.10.1  (default gateway)
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-01-cam-tcam.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `cam-table-baseline.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | VLAN | Notes |
| --- | --- | --- | --- | --- | --- |
| S1 | VLAN 10 | 192.168.10.2 | 255.255.255.0 | 10 | Access switch under test |
| S2 | VLAN 10 | 192.168.10.3 | 255.255.255.0 | 10 | Second access switch |
| PC-A | NIC | 192.168.10.10 | 255.255.255.0 | 10 | MAC 000c.1234.5678, port F0/1 |
| PC-B | NIC | 192.168.10.20 | 255.255.255.0 | 10 | MAC 000c.8765.4321, port F0/2 |
| R1 | G0/0 | 192.168.10.1 | 255.255.255.0 | 10 | Default gateway |

## Steps

1. Open lab-01-cam-tcam/lab-01-cam-tcam.pkt and confirm PC-A (192.168.10.10) and PC-B (192.168.10.20) are in VLAN 10
2. Clear the switch MAC address table so you start from a known empty state

   ```text
   S1# clear mac address-table dynamic
   ```

3. Display the empty table and note that only the CPU entries remain

   ```text
   S1# show mac address-table
   ```

4. From PC-A, ping PC-B to make the switch learn both source MAC addresses

   ```text
   C:\> ping 192.168.10.20
   ```

5. Display the CAM table again and record the two dynamic entries, their VLAN and their ports

   ```text
   S1# show mac address-table dynamic
   ```

6. Show the ageing time — the timer that removes an entry when a host goes quiet

   ```text
   S1# show mac address-table aging-time
   ```

7. Add a static CAM entry so PC-A's MAC is pinned to F0/1 and never ages out

   ```text
   S1(config)# mac address-table static 000c.1234.5678 vlan 10 interface FastEthernet0/1
   ```

8. Verify the static entry appears with type STATIC, not DYNAMIC

   ```text
   S1# show mac address-table static
   ```

9. Count the total entries the switch is currently holding

   ```text
   S1# show mac address-table count
   ```

10. Apply an ACL so the switch programs masked entries into TCAM rather than CAM

   ```text
   S1(config)# access-list 10 permit 192.168.10.0 0.0.0.255
   ```

11. Inspect the platform TCAM utilisation to see the ACL and QoS regions

   ```text
   S1# show platform tcam utilization
   ```

12. Write two sentences in your notes explaining why an ACL cannot live in CAM

## Validation

'show mac address-table dynamic' lists both PC MAC addresses against the correct ports and VLAN 10, 'show mac address-table static' shows your pinned entry, and you can state that CAM does exact-match on MAC while TCAM does masked match for ACL/QoS.

## Checkpoint Questions

1. Why can an ACL not be stored in CAM?
1. What happens to a frame whose destination MAC is not in the CAM table?
1. What is the default MAC address ageing time, and why does it exist?
1. Which table holds the Layer 2 rewrite information used by CEF?

## Exam Focus

Know which table answers which question: a question about a MAC address wants CAM, one about an ACL or QoS wants TCAM. CAM is exact-match; TCAM is masked (ternary), which is precisely why ACLs live there.
