# Lab 29 — Configure Control Plane Policing

**Topic 05: Network Security** · 20% of the exam · Skills Framework K4, A6 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify infrastructure security features — CoPP (ENCOR 5.2.b).

## Scenario

During the last incident a flood of ICMP and SNMP drove the router CPU to 99% and OSPF adjacencies dropped — the device stopped routing because it was too busy answering management traffic. As the engineer you build a CoPP policy that rate-limits management and ICMP traffic to the control plane while guaranteeing routing protocol traffic always gets through.

## What You'll Build

A CoPP policy applied to the control plane with separate classes for routing, management and ICMP, each policed at an appropriate rate, with verified conform and exceed counters.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2 routers.

## Topology

```text
              control plane (CPU)
                     ^
                     |  service-policy input COPP-POLICY
              +------+------+
   OSPF ----> | COPP-CRITICAL | 512k  transmit  (never starve routing)
   SSH  ----> | COPP-MANAGEMENT| 256k drop
   ICMP ----> | COPP-ICMP      |  64k drop      (the flood vector)
              +---------------+
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-29-copp.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `copp-classes.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Role | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | 192.168.1.1 | 255.255.255.0 | CoPP applied | Control plane protected |
| R1 | S0/0/0 | 10.1.1.1 | 255.255.255.252 | OSPF adjacency | Must survive the flood |
| R2 | S0/0/0 | 10.1.1.2 | 255.255.255.252 | Flood source | Generates the ICMP flood |
| R2 | G0/0 | 192.168.2.1 | 255.255.255.0 | OSPF neighbour | Adjacency under test |
| Admin PC | NIC | 192.168.1.50 | 255.255.255.0 | Management | SSH and SNMP source |

## Steps

1. Open lab-29-copp/lab-29-copp.pkt and baseline the CPU utilisation

   ```text
   R1# show processes cpu sorted | include CPU
   ```

2. Create an ACL matching routing protocol traffic that must never be dropped

   ```text
   R1(config)# access-list 120 permit ospf any any
   ```

3. Add EIGRP and BGP to the same critical ACL

   ```text
   R1(config)# access-list 120 permit tcp any any eq 179
   ```

4. Create an ACL matching management traffic

   ```text
   R1(config)# access-list 121 permit tcp any any eq 22
   ```

5. Add SNMP to the management ACL

   ```text
   R1(config)# access-list 121 permit udp any any eq 161
   ```

6. Create an ACL matching ICMP, the usual flood vector

   ```text
   R1(config)# access-list 122 permit icmp any any
   ```

7. Define the class map for critical routing traffic

   ```text
   R1(config)# class-map match-all COPP-CRITICAL
   ```

8. Match the routing ACL inside the class map

   ```text
   R1(config-cmap)# match access-group 120
   ```

9. Define the management class map the same way

   ```text
   R1(config)# class-map match-all COPP-MANAGEMENT
   ```

10. Define the ICMP class map

   ```text
   R1(config)# class-map match-all COPP-ICMP
   ```

11. Build the policy map that will govern the control plane

   ```text
   R1(config)# policy-map COPP-POLICY
   ```

12. Give routing traffic a generous rate so it is never starved

   ```text
   R1(config-pmap-c)# police 512000 conform-action transmit exceed-action transmit
   ```

13. Rate-limit management traffic and drop the excess

   ```text
   R1(config-pmap-c)# police 256000 conform-action transmit exceed-action drop
   ```

14. Rate-limit ICMP hard, since this is the flood vector

   ```text
   R1(config-pmap-c)# police 64000 conform-action transmit exceed-action drop
   ```

15. Enter control-plane configuration mode

   ```text
   R1(config)# control-plane
   ```

16. Apply the policy to the control plane in the input direction

   ```text
   R1(config-cp)# service-policy input COPP-POLICY
   ```

17. Generate an ICMP flood and verify the exceed counters climb while OSPF stays up

   ```text
   R2# ping 10.1.1.1 repeat 1000 size 1500
   ```

18. Read the policy counters for conformed and exceeded traffic

   ```text
   R1# show policy-map control-plane
   ```


## Validation

'show policy-map control-plane' shows the three classes with conformed bytes on all of them and exceeded/dropped bytes on the ICMP class during the flood, while 'show ip ospf neighbor' confirms the adjacency never dropped.

## Checkpoint Questions

1. What does CoPP protect, and from what?
1. Why must the routing class be policed with 'exceed-action transmit'?
1. In which direction is a CoPP policy applied?
1. Which show command reveals the conformed and exceeded byte counters?

## Exam Focus

CoPP applies a QoS policy to the control plane in the INPUT direction. Routing classes must use 'exceed-action transmit' — dropping routing traffic to protect the CPU defeats the purpose entirely.
