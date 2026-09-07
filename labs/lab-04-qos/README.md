# Lab 4 — Interpret Wired and Wireless QoS Configurations

**Topic 01: Enterprise Architecture** · 15% of the exam · Skills Framework K1, A1 (ICT-DIT-3009-1.1)

## Exam Objective

Interpret wired and wireless QoS configurations, including QoS components and QoS policy (ENCOR 1.5).

## Scenario

Voice calls on the campus wireless network are breaking up during busy periods. As the network engineer you trace the QoS treatment of a voice packet end to end: you read the classification and marking at the wired trust boundary, examine the queuing policy, then check how DSCP maps to the 802.11e WMM access category on the wireless side — where the mismatch usually is.

## What You'll Build

A documented end-to-end QoS policy showing the class map, policy map and service policy, plus the DSCP-to-WMM mapping table that explains the voice degradation.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1 router, SW-1 switch, WLC.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-04-qos.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `qos-policy-map.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Notes |
| --- | --- | --- | --- | --- |
| R1 | G0/0 | 192.168.1.1 | 255.255.255.0 | LAN with IP phones |
| R1 | S0/0/0 | 10.1.1.1 | 255.255.255.252 | WAN, QoS applied outbound |
| SW-1 | VLAN 1 | 192.168.1.2 | 255.255.255.0 | Access switch, trust boundary |
| IP Phone | NIC | 192.168.100.10 | 255.255.255.0 | Voice VLAN 100, marks DSCP EF |
| PC-A | NIC | 192.168.1.10 | 255.255.255.0 | Data VLAN 1, behind the phone |
| WLC-1 | Management | 192.168.200.254 | 255.255.255.0 | Wireless QoS / WMM mapping |

## Steps

1. Open lab-04-qos/lab-04-qos.pkt and locate the IP phone, the access switch and the WAN router
2. Display the class maps that classify traffic into voice, video and best effort

   ```text
   R1# show class-map
   ```

3. Display the policy map that assigns bandwidth and priority to each class

   ```text
   R1# show policy-map
   ```

4. Identify the low-latency queue reserved for voice — the strict-priority queue

   ```text
   R1# show policy-map interface Serial0/0/0
   ```

5. Read the marking: voice should carry DSCP EF (46), call signalling CS3 (24), video AF41 (34)

   ```text
   R1# show policy-map interface | include dscp
   ```

6. Check the trust boundary on the access port where the phone connects

   ```text
   SW-1# show mls qos interface FastEthernet0/1
   ```

7. Confirm the switch trusts the DSCP the phone marks rather than remarking it

   ```text
   SW-1# show mls qos interface FastEthernet0/1 | include trust
   ```

8. Inspect the queuing and drop behaviour under congestion

   ```text
   R1# show policy-map interface Serial0/0/0 | include drops
   ```

9. Record the DSCP to 802.11e user-priority mapping — EF should map to WMM Voice (UP 6)
10. Identify in qos-policy-map.csv which class is mismarked and explain the audio symptom it causes

## Validation

You can trace a voice packet from the phone's EF marking, through the trusted access port, into the priority queue on the WAN interface, and state which DSCP-to-WMM mapping is wrong and why calls break up.

## Checkpoint Questions

1. Which DSCP value should voice bearer traffic carry, and what is its decimal value?
1. What does 'trust boundary' mean, and where should it normally be?
1. What is the difference between policing and shaping?
1. Why does a DSCP-to-WMM mismatch degrade voice over Wi-Fi but not over the wire?

## Exam Focus

Voice is DSCP EF (46). Mark once at the trust boundary and act everywhere else. Policing drops, shaping buffers — shape towards your provider, police traffic coming from them.
