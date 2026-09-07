# Lab 21 — Configure NTP, NAT/PAT and HSRP

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Interpret NTP configurations, configure NAT/PAT, and configure first hop redundancy protocols such as HSRP and VRRP (ENCOR 3.4.a, 3.4.b, 3.4.c).

## Scenario

The branch office needs three IP services before it goes live: synchronised time so logs correlate, PAT so its private hosts reach the internet through one public address, and a redundant default gateway so a router failure does not black-hole the LAN. As the branch engineer you configure all three and prove the HSRP failover actually works.

## What You'll Build

A branch router synchronised to an NTP master, PAT translating 192.168.10.0/24 out one public address, and an HSRP group with virtual IP 192.168.1.254 that fails over on preemption.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, S1/S3 switches, PC-A and PC-B.

## Topology

```text
     PC-A (gateway 192.168.1.254 — the HSRP virtual IP)
             |
       [  S1  ]
        /      \
   [ R1 ]      [ R3 ]        R1: priority 110, preempt -> ACTIVE
  ACTIVE       STANDBY       R3: priority 100          -> STANDBY
     |
  S0/0/0 209.165.200.226  (NTP master, NAT outside)
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-21-ip-services.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Service | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/1 | 192.168.1.1 | 255.255.255.0 | HSRP | Active, priority 110, preempt |
| R1 | S0/0/0 | 209.165.200.226 | 255.255.255.0 | NTP + NAT | NTP master stratum 3, NAT outside |
| R1 | G0/0 | 192.168.10.1 | 255.255.255.0 | NAT | NAT inside |
| R3 | G0/1 | 192.168.1.3 | 255.255.255.0 | HSRP | Standby, default priority 100 |
| HSRP Virtual | Virtual | 192.168.1.254 | 255.255.255.0 | HSRP | Group 1 virtual IP |
| R2 | G0/0 | 209.165.200.227 | 255.255.255.0 | NTP | NTP client of R1 |
| PC-A | NIC | 192.168.1.101 | 255.255.255.0 | N/A | Gateway 192.168.1.254 (virtual) |
| PC1 | NIC | 192.168.10.10 | 255.255.255.0 | N/A | NAT inside host |

## Steps

1. Open lab-21-ip-services/lab-21-ip-services.pkt and review the three service requirements
2. Configure R1 as the NTP master at stratum 3

   ```text
   R1(config)# ntp master 3
   ```

3. Point R2 at R1 as its NTP server

   ```text
   R2(config)# ntp server 209.165.200.226
   ```

4. Verify the clock synchronised and note the stratum

   ```text
   R2# show ntp status
   ```

5. Check the association and confirm the * marks the synchronised peer

   ```text
   R2# show ntp associations
   ```

6. Make timestamps meaningful by logging with the actual date and time

   ```text
   R2(config)# service timestamps log datetime msec
   ```

7. Now configure PAT — define which inside addresses may be translated

   ```text
   R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255
   ```

8. Mark the inside interface

   ```text
   R1(config-if)# ip nat inside
   ```

9. Mark the outside interface

   ```text
   R1(config-if)# ip nat outside
   ```

10. Create the overload translation using the outside interface address

   ```text
   R1(config)# ip nat inside source list 1 interface Serial0/0/0 overload
   ```

11. Generate traffic from PC1 and inspect the translation table

   ```text
   R1# show ip nat translations
   ```

12. Check the translation statistics for hits and misses

   ```text
   R1# show ip nat statistics
   ```

13. Now configure HSRP on R1 as the intended active router

   ```text
   R1(config-if)# standby 1 ip 192.168.1.254
   ```

14. Raise R1's priority above the default of 100

   ```text
   R1(config-if)# standby 1 priority 110
   ```

15. Enable preemption so R1 reclaims the active role after a recovery

   ```text
   R1(config-if)# standby 1 preempt
   ```

16. Configure R3 as the standby with default priority

   ```text
   R3(config-if)# standby 1 ip 192.168.1.254
   ```

17. Verify R1 is Active and R3 is Standby with the correct virtual IP and MAC

   ```text
   R1# show standby brief
   ```

18. Shut R1's LAN interface and confirm R3 takes over while PC-A keeps pinging

   ```text
   R1(config-if)# shutdown
   ```


## Validation

'show ntp status' reports the clock is synchronised, 'show ip nat translations' lists inside-local to inside-global entries with differing ports, and 'show standby brief' shows R1 Active / R3 Standby — with R3 becoming Active and PC-A's ping continuing when R1's interface is shut.

## Checkpoint Questions

1. What does the stratum number in NTP represent?
1. What makes PAT different from static NAT?
1. What is HSRP's default priority, and is preemption on or off by default?
1. How does VRRP's preemption default differ from HSRP's?

## Exam Focus

Defaults matter here: HSRP priority 100 with preemption OFF, VRRP preemption ON. Configuring a higher HSRP priority without 'standby preempt' means that router will never become active.
