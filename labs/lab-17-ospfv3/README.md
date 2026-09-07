# Lab 17 — Configure Multiarea OSPFv3 for IPv6

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Configure simple OSPFv3 environments including multiple normal areas (ENCOR 3.2.b).

## Scenario

The organisation is dual-stacking, and IPv6 needs its own routing. As the engineer you configure OSPFv3 across three routers, working with the differences that catch people out: OSPFv3 is enabled per interface rather than with network statements, it still needs a 32-bit router ID even though it routes IPv6, and adjacencies form over link-local addresses.

## What You'll Build

A multiarea OSPFv3 domain with RA in area 1, RB in area 0 and RC in area 2, full adjacencies over link-local addresses, and end-to-end IPv6 reachability.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, RA/RB/RC routers.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-17-ospfv3.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IPv6 Address | Link-Local | OSPFv3 Area | Router ID |
| --- | --- | --- | --- | --- | --- |
| RA | G0/0 | 2001:db8:1:a1::1/64 | fe80::a | 1 | 1.1.1.1 |
| RA | G0/1 | 2001:db8:1:a2::1/64 | fe80::a | 1 | 1.1.1.1 |
| RA | S0/0/0 | 2001:db8:1:ab::2/64 | fe80::a | 0 | 1.1.1.1 |
| RB | G0/0 | 2001:db8:1:b1::1/64 | fe80::b | 0 | 2.2.2.2 |
| RB | S0/0/0 | 2001:db8:1:ab::1/64 | fe80::b | 0 | 2.2.2.2 |
| RB | S0/0/1 | 2001:db8:1:bc::1/64 | fe80::b | 0 | 2.2.2.2 |
| RC | G0/0 | 2001:db8:1:c1::1/64 | fe80::c | 2 | 3.3.3.3 |
| RC | G0/1 | 2001:db8:1:d2::1/64 | fe80::c | 2 | 3.3.3.3 |
| RC | S0/0/1 | 2001:db8:1:bc::2/64 | fe80::c | 0 | 3.3.3.3 |

## Steps

1. Open lab-17-ospfv3/lab-17-ospfv3.pkt and note the 2001:db8:1::/64 addressing plan
2. Enable IPv6 unicast routing — nothing IPv6 works without it

   ```text
   RA(config)# ipv6 unicast-routing
   ```

3. Start the OSPFv3 process

   ```text
   RA(config)# ipv6 router ospf 10
   ```

4. Set the 32-bit router ID, still required even though this routes IPv6

   ```text
   RA(config-rtr)# router-id 1.1.1.1
   ```

5. Move to the LAN interface and enable OSPFv3 on it directly

   ```text
   RA(config-if)# ipv6 ospf 10 area 1
   ```

6. Enable OSPFv3 on the second LAN interface, also in area 1

   ```text
   RA(config-if)# ipv6 ospf 10 area 1
   ```

7. Enable OSPFv3 on the backbone link in area 0

   ```text
   RA(config-if)# ipv6 ospf 10 area 0
   ```

8. Set the link-local address explicitly so adjacencies are easy to read

   ```text
   RA(config-if)# ipv6 address fe80::a link-local
   ```

9. Repeat on RB with router ID 2.2.2.2, all interfaces in area 0

   ```text
   RB(config-rtr)# router-id 2.2.2.2
   ```

10. Repeat on RC with router ID 3.3.3.3, its LANs in area 2

   ```text
   RC(config-if)# ipv6 ospf 10 area 2
   ```

11. Verify the adjacencies formed and note they use link-local addresses

   ```text
   RA# show ipv6 ospf neighbor
   ```

12. Confirm each interface is in the intended area

   ```text
   RA# show ipv6 ospf interface brief
   ```

13. Inspect the IPv6 routing table for inter-area routes marked OI

   ```text
   RA# show ipv6 route ospf
   ```

14. Test end-to-end IPv6 reachability across all three areas

   ```text
   RA# ping 2001:db8:1:c1::1
   ```


## Validation

'show ipv6 ospf neighbor' shows all neighbours FULL with link-local addresses as the neighbour address, 'show ipv6 route ospf' contains OI inter-area routes, and RA pings RC's LAN across the backbone.

## Checkpoint Questions

1. Why does OSPFv3 still need a 32-bit router ID?
1. How is OSPFv3 enabled on an interface, and how does that differ from OSPFv2?
1. Which addresses do OSPFv3 adjacencies use?
1. What command must be enabled before any IPv6 routing works?

## Exam Focus

OSPFv3 is enabled per interface ('ipv6 ospf 10 area N'), still needs a 32-bit router ID, and forms adjacencies over link-local addresses. 'ipv6 unicast-routing' must be on first.
