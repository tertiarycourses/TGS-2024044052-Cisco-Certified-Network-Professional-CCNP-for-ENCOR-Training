# Lab 24 — Configure SPAN, RSPAN and IP SLA

**Topic 04: Network Assurance** · 10% of the exam · Skills Framework K5, A4 (ICT-DIT-3009-1.1)

## Exam Objective

Configure SPAN/RSPAN/ERSPAN and configure and verify IPSLA (ENCOR 4.3, 4.4).

## Scenario

Security has asked for a packet capture of one server's traffic, and the WAN team wants to know when a path degrades before users complain. As the engineer you deliver both: SPAN to mirror the server port to an analyser, RSPAN to carry a copy to an analyser on another switch, and an IP SLA probe with a tracked object that withdraws a static route when the path fails.

## What You'll Build

A working local SPAN session mirroring the server port, an RSPAN session across a dedicated VLAN, and an IP SLA ICMP echo operation with a tracked object driving a static route.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, S1/S2 switches, R1/R2 routers, analyser PC.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-24-span-ipsla.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Role | Notes |
| --- | --- | --- | --- | --- | --- |
| S1 | F0/1 | N/A | N/A | SPAN source | Server port being mirrored |
| S1 | F0/24 | N/A | N/A | SPAN destination | Local analyser port |
| S1 | VLAN 199 | N/A | N/A | RSPAN VLAN | Dedicated remote-span VLAN |
| S2 | F0/24 | N/A | N/A | RSPAN destination | Analyser on the second switch |
| R1 | S0/0/0 | 209.165.200.225 | 255.255.255.0 | IP SLA source | Probe source interface |
| R2 | G0/0 | 209.165.200.226 | 255.255.255.0 | IP SLA target | Echo target |
| Server | NIC | 192.168.1.100 | 255.255.255.0 | Monitored host | The capture subject |
| Analyser | NIC | 192.168.1.200 | 255.255.255.0 | Analyser | Receives the mirrored traffic |

## Steps

1. Open lab-24-span-ipsla/lab-24-span-ipsla.pkt and identify the server port and the analyser port
2. Create a local SPAN session with the server port as the source

   ```text
   S1(config)# monitor session 1 source interface FastEthernet0/1 both
   ```

3. Set the analyser port as the destination

   ```text
   S1(config)# monitor session 1 destination interface FastEthernet0/24
   ```

4. Verify the SPAN session is active and note the source and destination

   ```text
   S1# show monitor session 1
   ```

5. Now build RSPAN — first create the dedicated RSPAN VLAN

   ```text
   S1(config)# vlan 199
   ```

6. Flag the VLAN as an RSPAN VLAN

   ```text
   S1(config-vlan)# remote-span
   ```

7. On the source switch, send the mirrored traffic into the RSPAN VLAN

   ```text
   S1(config)# monitor session 2 destination remote vlan 199
   ```

8. On the destination switch, take the RSPAN VLAN as the source

   ```text
   S2(config)# monitor session 2 source remote vlan 199
   ```

9. Send it to the local analyser port on that switch

   ```text
   S2(config)# monitor session 2 destination interface FastEthernet0/24
   ```

10. Verify the RSPAN session on both switches

   ```text
   S2# show monitor session 2
   ```

11. Move to IP SLA and create an ICMP echo operation to the remote path

   ```text
   R1(config)# ip sla 1
   ```

12. Define the echo target and the source interface

   ```text
   R1(config-ip-sla)# icmp-echo 209.165.200.226 source-interface Serial0/0/0
   ```

13. Set the probe frequency in seconds

   ```text
   R1(config-ip-sla-echo)# frequency 10
   ```

14. Schedule the operation to run now and run forever

   ```text
   R1(config)# ip sla schedule 1 life forever start-time now
   ```

15. Create a tracked object that follows the SLA's reachability

   ```text
   R1(config)# track 1 ip sla 1 reachability
   ```

16. Attach the tracked object to a static route so it withdraws on failure

   ```text
   R1(config)# ip route 0.0.0.0 0.0.0.0 209.165.200.226 track 1
   ```

17. Verify the SLA statistics and the round-trip time

   ```text
   R1# show ip sla statistics
   ```

18. Verify the tracked object is Up and the route is in the table

   ```text
   R1# show track 1
   ```


## Validation

'show monitor session 1' shows an active local SPAN, the RSPAN session appears on both switches using VLAN 199, 'show ip sla statistics' reports successful probes with an RTT, and 'show track 1' reports the object Up with the default route present.

## Checkpoint Questions

1. What is the difference between SPAN, RSPAN and ERSPAN?
1. What must be configured on the VLAN used by RSPAN?
1. What does an IP SLA tracked object let you do that a raw SLA cannot?
1. Why would you use NetFlow instead of SPAN for a whole network?

## Exam Focus

SPAN is local, RSPAN crosses a dedicated VLAN that must be flagged 'remote-span', ERSPAN encapsulates in GRE to cross a routed network. IP SLA plus a tracked object is what makes a route withdraw on failure.
