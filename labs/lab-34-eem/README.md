# Lab 34 — Construct an EEM Applet to Automate Response

**Topic 06: Network Automation** · 15% of the exam · Skills Framework K6, A5 (ICT-DIT-3009-1.1)

## Exam Objective

Construct an EEM applet to automate configuration, troubleshooting or data collection (ENCOR 6.6).

## Scenario

A critical WAN interface flaps at night and nobody captures the state before it recovers, so the cause is never found. As the engineer you make the device investigate itself: an EEM applet that triggers on the syslog message, runs the diagnostic commands, writes the output to a file and logs a summary — automation with no external server involved.

## What You'll Build

Two working EEM applets — one syslog-triggered applet that collects diagnostics on an interface down event, and one timed applet that logs a periodic health snapshot.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1 router.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-34-eem.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Applet | Event Detector | Trigger | Actions | Purpose |
| --- | --- | --- | --- | --- |
| INTERFACE-DOWN | syslog | Pattern: Serial0/0/0 changed state to down | show interfaces, show ip route, syslog msg | Capture state at the moment of failure |
| HEALTH-CHECK | timer watchdog | Every 300 seconds | show processes cpu, syslog msg | Periodic health snapshot |
| CONFIG-CHANGE | syslog | Pattern: CONFIG_I configured from | show running-config, syslog msg | Record what changed and when |
| HIGH-CPU | snmp | CPU above 80% | show processes cpu sorted, syslog msg | Catch the process responsible |

## Steps

1. Open lab-34-eem/lab-34-eem.pkt and confirm you can see the interface down syslog message

   ```text
   R1# show logging | include LINEPROTO
   ```

2. Create the applet and give it a descriptive name

   ```text
   R1(config)# event manager applet INTERFACE-DOWN
   ```

3. Define the syslog event detector matching the interface down pattern

   ```text
   R1(config-applet)# event syslog pattern "Interface Serial0/0/0, changed state to down"
   ```

4. Add the first action — enter privileged mode, since the applet starts unprivileged

   ```text
   R1(config-applet)# action 1.0 cli command "enable"
   ```

5. Collect the interface state

   ```text
   R1(config-applet)# action 2.0 cli command "show interfaces Serial0/0/0"
   ```

6. Collect the routing table at the moment of failure

   ```text
   R1(config-applet)# action 3.0 cli command "show ip route"
   ```

7. Write a syslog message recording that the applet ran

   ```text
   R1(config-applet)# action 4.0 syslog msg "EEM: Serial0/0/0 down - diagnostics collected"
   ```

8. Note the numbering convention — 1.0, 2.0, 3.0 sorts lexically, whereas 1, 2, 10 does not
9. Trigger the applet by shutting the interface

   ```text
   R1(config-if)# shutdown
   ```

10. Read the log and confirm the applet's message appears

   ```text
   R1# show logging | include EEM
   ```

11. Verify the applet registered and check its run count

   ```text
   R1# show event manager policy registered
   ```

12. Check the statistics for how many times it has fired

   ```text
   R1# show event manager statistics policy
   ```

13. Now create a second applet on a timer for a periodic health snapshot

   ```text
   R1(config)# event manager applet HEALTH-CHECK
   ```

14. Set the timer event to fire every 300 seconds

   ```text
   R1(config-applet)# event timer watchdog time 300
   ```

15. Add the CPU check action

   ```text
   R1(config-applet)# action 1.0 cli command "show processes cpu | include CPU"
   ```

16. Log the snapshot

   ```text
   R1(config-applet)# action 2.0 syslog msg "EEM: periodic health snapshot taken"
   ```

17. Bring the interface back and confirm both applets are registered

   ```text
   R1(config-if)# no shutdown
   ```


## Validation

'show event manager policy registered' lists both applets, shutting Serial0/0/0 produces the 'EEM: Serial0/0/0 down' syslog entry, and 'show event manager statistics policy' shows a non-zero run count for the triggered applet.

## Checkpoint Questions

1. What are the three required parts of an EEM applet?
1. Why is 1.0, 2.0, 3.0 the safe action numbering rather than 1, 2, 10?
1. Why must the first action usually be 'enable'?
1. Name three EEM event detectors.

## Exam Focus

An applet needs a name, exactly one event statement and numbered actions. Number them 1.0, 2.0, 3.0 because actions run in LEXICAL order — 10 would sort before 2.
