# Lab 14 — Harden the Spanning Tree with PortFast, BPDU Guard and Root Guard

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify Spanning Tree enhancements such as root guard and BPDU guard (ENCOR 3.1.c).

## Scenario

A contractor plugged a personal switch into a meeting-room wall port last month and became the spanning tree root, black-holing the floor for four minutes. As the engineer you make that impossible: PortFast on edge ports so hosts get an instant link, BPDU guard to shut any edge port that receives a BPDU, and root guard on the distribution uplinks.

## What You'll Build

Edge ports running PortFast with BPDU guard globally enabled, root guard on the distribution-facing uplinks, and a demonstrated err-disable when a rogue BPDU arrives.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches, rogue switch, PC-A.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-14-stp-hardening.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Port | Switch | Role | Feature Applied | Expected Behaviour |
| --- | --- | --- | --- | --- |
| F0/1 | S1 | Access / edge | PortFast + BPDU guard | Instant forwarding; err-disable on any BPDU |
| F0/2 | S1 | Access / edge | PortFast + BPDU guard | Instant forwarding; err-disable on any BPDU |
| G0/1 | S1 | Uplink to distribution | Root guard | Root-inconsistent on a superior BPDU |
| G0/2 | S1 | Uplink to distribution | Root guard + loop guard | Protected against rogue root and unidirectional link |
| F0/24 | S1 | Rogue switch port | PortFast + BPDU guard | Test port — plug the rogue switch here |

## Steps

1. Open lab-14-stp-hardening/lab-14-stp-hardening.pkt and time how long a PC port takes to forward
2. Enable PortFast on the access port so it skips listening and learning

   ```text
   S1(config-if)# spanning-tree portfast
   ```

3. Enable PortFast by default on all non-trunking ports

   ```text
   S1(config)# spanning-tree portfast default
   ```

4. Verify PortFast is active on the interface

   ```text
   S1# show spanning-tree interface FastEthernet0/1 portfast
   ```

5. Enable BPDU guard on that specific interface

   ```text
   S1(config-if)# spanning-tree bpduguard enable
   ```

6. Enable BPDU guard globally for every PortFast-enabled port

   ```text
   S1(config)# spanning-tree portfast bpduguard default
   ```

7. Connect the rogue switch to the PortFast port and watch the port err-disable

   ```text
   S1# show interfaces status err-disabled
   ```

8. Read the log entry that names BPDU guard as the cause

   ```text
   S1# show logging | include BPDUGUARD
   ```

9. Configure automatic recovery so the port returns after five minutes

   ```text
   S1(config)# errdisable recovery cause bpduguard
   ```

10. Set the recovery interval

   ```text
   S1(config)# errdisable recovery interval 300
   ```

11. Apply root guard to the uplink so no superior BPDU can move the root

   ```text
   S1(config-if)# spanning-tree guard root
   ```

12. Verify root guard is applied and note it puts the port in root-inconsistent rather than shutting it

   ```text
   S1# show spanning-tree inconsistentports
   ```

13. Enable loop guard to cover unidirectional link failures

   ```text
   S1(config)# spanning-tree loopguard default
   ```

14. Summarise which feature defends which failure mode in your notes

   ```text
   S1# show spanning-tree summary
   ```


## Validation

The rogue switch's BPDU puts the PortFast port into err-disabled with a BPDUGUARD log entry, 'show spanning-tree inconsistentports' reports a root-inconsistent port when a superior BPDU hits the guarded uplink, and errdisable recovery is armed.

## Checkpoint Questions

1. What does BPDU guard do when a PortFast port receives a BPDU?
1. How does root guard's response differ from BPDU guard's?
1. What failure mode does loop guard defend against?
1. Why should PortFast never be enabled on a trunk to another switch?

## Exam Focus

Each feature defends a different failure: BPDU guard err-disables on any BPDU, root guard blocks a superior BPDU (root-inconsistent, not err-disabled), loop guard covers unidirectional links.
