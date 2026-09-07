# Lab 15 — Compare EIGRP and OSPF Path Selection

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Compare routing concepts of EIGRP and OSPF — advanced distance vector versus link state, load balancing, path selection, metrics and area types (ENCOR 3.2.a).

## Scenario

Your network runs EIGRP in the legacy branch estate and OSPF in the new campus, and you must explain to management why the two choose different paths across the identical topology. As the engineer you configure both over the same links, compare their metrics, and demonstrate the one capability EIGRP has that OSPF does not: unequal-cost load balancing.

## What You'll Build

Both protocols running over one topology with documented metric calculations, an identified successor and feasible successor in EIGRP, and working unequal-cost load balancing via the variance command.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-15-eigrp-ospf.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Bandwidth (kbps) | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | 172.16.1.1 | 255.255.255.0 | 1000000 | LAN |
| R1 | S0/0/0 | 172.16.3.1 | 255.255.255.252 | 1544 | Slow path to R2 |
| R1 | S0/0/1 | 192.168.10.5 | 255.255.255.252 | 64 | Very slow path to R3 |
| R2 | G0/0 | 172.16.2.1 | 255.255.255.0 | 1000000 | LAN |
| R2 | S0/0/0 | 172.16.3.2 | 255.255.255.252 | 1544 | Path to R1 |
| R3 | G0/0 | 192.168.1.1 | 255.255.255.0 | 1000000 | LAN |
| R3 | S0/0/0 | 192.168.10.6 | 255.255.255.252 | 64 | Path to R1 |

## Steps

1. Open lab-15-eigrp-ospf/lab-15-eigrp-ospf.pkt and review the three-router topology with unequal-bandwidth links
2. Enable EIGRP in named mode on R1

   ```text
   R1(config)# router eigrp CAMPUS
   ```

3. Enter the IPv4 unicast address family with autonomous system 100

   ```text
   R1(config-router)# address-family ipv4 unicast autonomous-system 100
   ```

4. Advertise the connected networks

   ```text
   R1(config-router-af)# network 172.16.0.0 0.0.255.255
   ```

5. Verify the EIGRP neighbours have formed

   ```text
   R1# show ip eigrp neighbors
   ```

6. Examine the topology table and identify the successor and the feasible successor

   ```text
   R1# show ip eigrp topology
   ```

7. Read the feasibility condition — the feasible successor's reported distance must be below the feasible distance

   ```text
   R1# show ip eigrp topology all-links
   ```

8. Enable unequal-cost load balancing with variance

   ```text
   R1(config-router-af)# variance 2
   ```

9. Confirm two unequal paths now appear in the routing table

   ```text
   R1# show ip route eigrp
   ```

10. Now enable OSPF process 10 on the same routers

   ```text
   R1(config)# router ospf 10
   ```

11. Set an explicit router ID rather than letting IOS pick one

   ```text
   R1(config-router)# router-id 1.1.1.1
   ```

12. Advertise the same networks into area 0

   ```text
   R1(config-router)# network 172.16.0.0 0.0.255.255 area 0
   ```

13. Verify OSPF adjacencies reached FULL state

   ```text
   R1# show ip ospf neighbor
   ```

14. Compare the OSPF cost with the EIGRP composite metric for the same destination

   ```text
   R1# show ip route ospf
   ```

15. Record which protocol picked which path and explain why in your notes

## Validation

'show ip eigrp topology' identifies a successor and at least one feasible successor with its reported distance, the routing table shows two unequal-cost paths after variance 2, and OSPF neighbours reach FULL with a cost you can calculate from reference bandwidth over interface bandwidth.

## Checkpoint Questions

1. What is the feasibility condition, and what does it guarantee?
1. Which command enables unequal-cost load balancing in EIGRP?
1. How is OSPF cost calculated by default?
1. Name one thing EIGRP can do that OSPF cannot.

## Exam Focus

EIGRP's feasibility condition: the feasible successor's REPORTED distance must be less than the current FEASIBLE distance. Unequal-cost load balancing needs 'variance' — OSPF cannot do it at all.
