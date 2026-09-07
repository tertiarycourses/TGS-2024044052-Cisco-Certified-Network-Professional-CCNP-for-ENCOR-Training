# Lab 18 — Configure and Verify eBGP

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify eBGP between directly connected neighbours, including best path selection and neighbour relationships (ENCOR 3.2.c).

## Scenario

ACME is multihoming to two ISP entry points for internet resilience. As the WAN engineer you configure eBGP to both providers, advertise your own prefix, then influence which path inbound and outbound traffic takes — and you deliberately break the session by peering to a loopback without ebgp-multihop, so you recognise the most common eBGP failure in the field.

## What You'll Build

Established eBGP sessions from ACME1 to both ISP entry points, the local prefix advertised and visible in both providers' tables, and a demonstrated path preference change.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, ACME1, OtherCo1, ISP-Entry-1, ISP-Entry-2.

## Topology

```text
            AS 65000 (ISP)
      [ ISP-Entry-1 ]      [ ISP-Entry-2 ]
        1.1.1.1              1.1.1.9
           |                    |
        1.1.1.2              1.1.1.6
      [        ACME1 — AS 65001        ]
              192.168.0.0/24
   eBGP to both entry points for multihomed resilience.
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-18-ebgp.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | AS Number | Notes |
| --- | --- | --- | --- | --- | --- |
| ACME1 | G0/0 | 192.168.0.1 | 255.255.255.0 | 65001 | Customer LAN |
| ACME1 | S0/0/0 | 1.1.1.2 | 255.255.255.252 | 65001 | eBGP peer to ISP-Entry-1 |
| ACME1 | S0/0/1 | 1.1.1.6 | 255.255.255.252 | 65001 | eBGP peer to ISP-Entry-2 |
| ISP-Entry-1 | S0/0/0 | 1.1.1.1 | 255.255.255.252 | 65000 | Primary provider entry |
| ISP-Entry-1 | S0/0/1 | 1.1.1.5 | 255.255.255.252 | 65000 | Secondary link |
| ISP-Entry-2 | S0/0/0 | 1.1.1.9 | 255.255.255.252 | 65000 | Second provider entry |
| OtherCo1 | G0/0 | 172.16.10.1 | 255.255.255.0 | 65002 | Remote AS to reach |
| Server | NIC | 172.16.10.2 | 255.255.255.0 | N/A | Reachability test target |

## Steps

1. Open lab-18-ebgp/lab-18-ebgp.pkt and confirm ACME1 S0/0/0 is 1.1.1.2 peering to 1.1.1.1

   ```text
   ACME1# ping 1.1.1.1
   ```

2. Start BGP with ACME's autonomous system number

   ```text
   ACME1(config)# router bgp 65001
   ```

3. Define the eBGP neighbour and its remote AS

   ```text
   ACME1(config-router)# neighbor 1.1.1.1 remote-as 65000
   ```

4. Advertise the local LAN prefix into BGP

   ```text
   ACME1(config-router)# network 192.168.0.0 mask 255.255.255.0
   ```

5. Disable auto-summary so classful summarisation does not surprise you

   ```text
   ACME1(config-router)# no auto-summary
   ```

6. Verify the session moved to Established by checking the state and prefix count

   ```text
   ACME1# show ip bgp summary
   ```

7. Read the BGP table and identify the best path, marked with >

   ```text
   ACME1# show ip bgp
   ```

8. Examine the attributes BGP used to choose it

   ```text
   ACME1# show ip bgp 172.16.10.0
   ```

9. Add the second provider session for redundancy

   ```text
   ACME1(config-router)# neighbor 1.1.1.5 remote-as 65000
   ```

10. Verify both neighbours are Established

   ```text
   ACME1# show ip bgp neighbors | include BGP state
   ```

11. Influence outbound path selection by raising local preference on one neighbour's routes

   ```text
   ACME1(config)# route-map PREFER-ISP1 permit 10
   ```

12. Set the local preference value inside the route map

   ```text
   ACME1(config-route-map)# set local-preference 200
   ```

13. Apply the route map inbound from the preferred provider

   ```text
   ACME1(config-router)# neighbor 1.1.1.1 route-map PREFER-ISP1 in
   ```

14. Clear the session softly so the policy takes effect without dropping the peering

   ```text
   ACME1# clear ip bgp * soft in
   ```

15. Confirm the best path moved to the preferred provider

   ```text
   ACME1# show ip bgp
   ```


## Validation

'show ip bgp summary' shows both neighbours Established with a non-zero prefix count, 'show ip bgp' marks the best path with >, and after the local preference change the best-path marker moves to the preferred provider's route.

## Checkpoint Questions

1. Which TCP port does BGP use?
1. Why does peering to a loopback require 'ebgp-multihop'?
1. What are the first three steps of the BGP best-path algorithm?
1. Why use 'clear ip bgp * soft in' rather than a hard clear?

## Exam Focus

eBGP peers are directly connected with TTL 1 by default — peering to a loopback needs 'ebgp-multihop' AND 'update-source'. Best path order starts weight, local preference, locally originated, AS-path length.
