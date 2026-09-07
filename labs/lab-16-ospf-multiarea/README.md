# Lab 16 — Configure Multiarea OSPFv2 with Summarization and Filtering

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Configure simple OSPFv2 environments including multiple normal areas, summarization and filtering (ENCOR 3.2.b).

## Scenario

The campus OSPF domain has grown to a single area carrying 400 routes, and every link flap triggers a full SPF run everywhere. As the engineer you split it into multiple areas, place the ABR correctly, summarise at the area boundary to contain the flooding, and make LAN interfaces passive so no adjacency is ever attempted towards a host.

## What You'll Build

A multiarea OSPFv2 domain with area 0 backbone plus areas 1 and 2, route summarization at the ABR, passive LAN interfaces, and a stub area that blocks external LSAs.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC1/PC2/PC3.

## Topology

```text
   Area 1              Area 0 (backbone)             Area 2
  172.16.1.0/24                                     192.168.1.0/24
      |                                                   |
    [ R1 ] ==== 172.16.3.0/30 ==== [ R2 ]                 |
    ABR          \                                       |
                  \____ 192.168.10.4/30 ____ [ R3 ] -----+
                                              ABR / stub
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-16-ospf-multiarea.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | OSPF Area | Router ID |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | 172.16.1.1 | 255.255.255.0 | 1 | 1.1.1.1 |
| R1 | S0/0/0 | 172.16.3.1 | 255.255.255.252 | 0 | 1.1.1.1 |
| R1 | S0/0/1 | 192.168.10.5 | 255.255.255.252 | 0 | 1.1.1.1 |
| R2 | G0/0 | 172.16.2.1 | 255.255.255.0 | 1 | 2.2.2.2 |
| R2 | S0/0/0 | 172.16.3.2 | 255.255.255.252 | 0 | 2.2.2.2 |
| R3 | G0/0 | 192.168.1.1 | 255.255.255.0 | 2 | 3.3.3.3 |
| R3 | S0/0/0 | 192.168.10.6 | 255.255.255.252 | 0 | 3.3.3.3 |
| PC1 | NIC | 172.16.1.10 | 255.255.255.0 | N/A | Gateway 172.16.1.1 |
| PC3 | NIC | 192.168.1.10 | 255.255.255.0 | N/A | Gateway 192.168.1.1 |

## Steps

1. Open lab-16-ospf-multiarea/lab-16-ospf-multiarea.pkt and note R1 172.16.1.1, R2 172.16.2.1, R3 192.168.1.1
2. Start OSPF process 10 on R1 and set the router ID

   ```text
   R1(config)# router ospf 10
   ```

3. Set the router ID explicitly to 1.1.1.1

   ```text
   R1(config-router)# router-id 1.1.1.1
   ```

4. Place the backbone link into area 0

   ```text
   R1(config-router)# network 172.16.3.0 0.0.0.3 area 0
   ```

5. Place the LAN into area 1

   ```text
   R1(config-router)# network 172.16.1.0 0.0.0.255 area 1
   ```

6. Make the LAN interface passive so no hello is sent towards hosts

   ```text
   R1(config-router)# passive-interface GigabitEthernet0/0
   ```

7. Repeat on R2 with router ID 2.2.2.2 and its own area

   ```text
   R2(config-router)# router-id 2.2.2.2
   ```

8. Repeat on R3 with router ID 3.3.3.3 placing its LAN in area 2

   ```text
   R3(config-router)# network 192.168.1.0 0.0.0.255 area 2
   ```

9. Verify all adjacencies reached FULL

   ```text
   R1# show ip ospf neighbor
   ```

10. Identify which router is the ABR because it has interfaces in two areas

   ```text
   R1# show ip ospf | include Area
   ```

11. Summarise area 1's prefixes at the ABR to contain flooding

   ```text
   R1(config-router)# area 1 range 172.16.0.0 255.255.0.0
   ```

12. Confirm the summary appears as a single Type 3 LSA instead of many

   ```text
   R2# show ip ospf database summary
   ```

13. Configure area 2 as a stub so external LSAs never enter it

   ```text
   R3(config-router)# area 2 stub
   ```

14. Apply the matching stub command on the ABR — both ends must agree or the adjacency drops

   ```text
   R1(config-router)# area 2 stub
   ```

15. Verify the routing tables and the LSA types present in each area

   ```text
   R3# show ip ospf database
   ```


## Validation

All OSPF neighbours are FULL, 'show ip ospf' identifies the ABR with interfaces in two areas, the area 1 prefixes appear as one summarised Type 3 LSA in the backbone, and the stub area's database contains no Type 5 external LSAs.

## Checkpoint Questions

1. What makes a router an ABR?
1. Which LSA type does area summarization produce?
1. What does a stub area block, and what does a totally stubby area additionally block?
1. Name four things that must match for two routers to form an OSPF adjacency.

## Exam Focus

Adjacency requires matching hello/dead timers, area ID, subnet mask, authentication and stub flags. Summarization at the ABR produces one Type 3 LSA. Stub areas block Type 5; totally stubby also blocks Type 3.
