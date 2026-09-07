# Lab 11 — Troubleshoot Static and Dynamic EtherChannels

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Troubleshoot static and dynamic EtherChannels — PAgP and LACP (ENCOR 3.1.b).

## Scenario

Three EtherChannel bundles were configured across the distribution layer over the weekend and only one came up. As the engineer on duty you diagnose each: one has both ends passive so LACP never initiates, one has a speed and duplex mismatch that suspends a member port, and one mixes PAgP on one end with LACP on the other — a combination that can never negotiate.

## What You'll Build

Three working EtherChannel bundles — Po1 with PAgP, Po2 with LACP and Po3 negotiated LACP — all showing SU (in use) with every member port bundled.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-11-etherchannel.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `etherchannel-faults.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Channel Group | Switches | Member Ports | Protocol | Expected Mode | Fault Injected |
| --- | --- | --- | --- | --- | --- |
| Po1 | S1 – S3 | F0/21, F0/22 | PAgP | desirable / auto | Speed and duplex mismatch on F0/22 |
| Po2 | S1 – S2 | G0/1, G0/2 | LACP | active / passive | Both ends left passive |
| Po3 | S2 – S3 | F0/23, F0/24 | LACP | active / active | PAgP on one end, LACP on the other |

## Steps

1. Open lab-11-etherchannel/lab-11-etherchannel.pkt and check the state of all three port channels

   ```text
   S1# show etherchannel summary
   ```

2. Read the flags column — SU means in use, SD means down, and (s) means suspended
3. Investigate Po2 where both ends were left passive

   ```text
   S1# show etherchannel 2 port-channel
   ```

4. Set S1's end of Po2 to LACP active so one side initiates

   ```text
   S1(config-if-range)# channel-group 2 mode active
   ```

5. Confirm the S2 end stays passive — active-to-passive is a valid LACP pairing

   ```text
   S2# show etherchannel summary
   ```

6. Investigate the suspended member port on Po1

   ```text
   S1# show interfaces FastEthernet0/22 | include duplex
   ```

7. Compare the two member ports and find the speed and duplex mismatch

   ```text
   S1# show interfaces status | include Fa0/21|Fa0/22
   ```

8. Correct the mismatched port so both members match

   ```text
   S1(config-if)# duplex full
   ```

9. Set the matching speed on the same port

   ```text
   S1(config-if)# speed 100
   ```

10. Investigate Po3, which mixes protocols across the two ends

   ```text
   S3# show etherchannel 3 detail | include protocol
   ```

11. Remove the PAgP configuration from the mismatched end

   ```text
   S3(config-if-range)# no channel-group 3 mode desirable
   ```

12. Re-apply the same protocol both ends use — LACP active

   ```text
   S3(config-if-range)# channel-group 3 mode active
   ```

13. Verify all three bundles are now SU with every member bundled

   ```text
   S1# show etherchannel summary
   ```

14. Confirm the load-balancing method the switch is using

   ```text
   S1# show etherchannel load-balance
   ```


## Validation

'show etherchannel summary' shows Po1, Po2 and Po3 all with flags (SU) and every member port marked (P) for bundled — no (s) suspended and no (D) down ports remain.

## Checkpoint Questions

1. Which two LACP mode combinations will NOT form a bundle?
1. Name three parameters that must match across EtherChannel member ports.
1. What do the flags (SU), (SD) and (s) mean in 'show etherchannel summary'?
1. Can you mix PAgP on one end and LACP on the other? Why?

## Exam Focus

Two passive LACP ends or two auto PAgP ends will never bundle — at least one side must initiate. Members must match on speed, duplex, trunk mode, allowed VLANs and native VLAN.
