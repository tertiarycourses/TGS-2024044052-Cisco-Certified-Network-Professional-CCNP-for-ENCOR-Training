# Lab 22 — Diagnose Network Problems with Ping, Traceroute and Conditional Debug

**Topic 04: Network Assurance** · 10% of the exam · Skills Framework K5, A4 (ICT-DIT-3009-1.1)

## Exam Objective

Diagnose network problems using tools such as debugs, conditional debugs, traceroute, ping, SNMP and syslog (ENCOR 4.1).

## Scenario

A user reports the application server is 'sometimes slow and sometimes down'. As the engineer you work the problem methodically from the bottom of the stack up: extended ping from the right source with the right size, traceroute to locate where the path breaks, then a conditional debug scoped to one host so you can safely watch the control plane on a production router.

## What You'll Build

A completed diagnostic record locating the failure to a specific hop, with an extended ping result set, a traceroute trace and safely-scoped conditional debug output.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC-A.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-22-diagnostics.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `diagnostic-log.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | MTU | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/1 | 192.168.1.1 | 255.255.255.0 | 1500 | Source of the diagnostics |
| R1 | S0/0/0 | 10.1.1.1 | 255.255.255.252 | 1400 | MTU reduced — the injected fault |
| R2 | S0/0/0 | 10.1.1.2 | 255.255.255.252 | 1400 | Transit |
| R2 | S0/0/1 | 10.2.2.1 | 255.255.255.252 | 1500 | Transit |
| R3 | S0/0/1 | 10.2.2.2 | 255.255.255.252 | 1500 | Far end |
| R3 | G0/1 | 192.168.3.1 | 255.255.255.0 | 1500 | Destination LAN |
| PC-A | NIC | 192.168.1.3 | 255.255.255.0 | 1500 | Reports the symptom |
| Server | NIC | 192.168.3.3 | 255.255.255.0 | 1500 | The 'slow' application server |

## Steps

1. Open lab-22-diagnostics/lab-22-diagnostics.pkt and confirm the reported symptom from PC-A

   ```text
   C:\> ping 192.168.3.3
   ```

2. Run a basic ping from the router to establish reachability

   ```text
   R1# ping 192.168.3.3
   ```

3. Run an extended ping sourced from the LAN interface — the source is what usually matters

   ```text
   R1# ping 192.168.3.3 source GigabitEthernet0/1
   ```

4. Test with a large packet and the do-not-fragment bit to expose an MTU problem

   ```text
   R1# ping 192.168.3.3 size 1500 df-bit
   ```

5. Sweep a range of packet sizes to find exactly where it breaks

   ```text
   R1# ping 192.168.3.3 size 1400 repeat 5
   ```

6. Trace the path to identify the last responding hop

   ```text
   R1# traceroute 192.168.3.3
   ```

7. Read the asterisks in the traceroute output and interpret what they mean
8. Check whether the route even exists before blaming the far end

   ```text
   R1# show ip route 192.168.3.0
   ```

9. Verify the interface counters for errors and drops

   ```text
   R1# show interfaces Serial0/0/0 | include error|drop
   ```

10. Set up a conditional debug so you only see traffic for the one affected host

   ```text
   R1# debug platform condition ipv4 192.168.3.3/32 both
   ```

11. Start the condition so the filter takes effect

   ```text
   R1# debug platform condition start
   ```

12. Enable the ICMP debug now that it is safely scoped

   ```text
   R1# debug ip icmp
   ```

13. Reproduce the problem and read the scoped output

   ```text
   C:\> ping 192.168.3.3
   ```

14. Turn every debug off — never leave a debug running

   ```text
   R1# undebug all
   ```

15. Record the failing hop and the root cause in diagnostic-log.csv

## Validation

Your diagnostic record names the exact hop where the path fails, the sweep identifies the largest packet size that succeeds, and 'undebug all' confirms no debug is left running on the device.

## Checkpoint Questions

1. What does a large ping with the DF bit set prove when it fails?
1. What do asterisks in traceroute output mean?
1. Why must debug be scoped with a condition on a production router?
1. Which command turns off every running debug at once?

## Exam Focus

A large ping with df-bit that fails while traceroute completes points at MTU, not routing. Always scope a debug with a condition, and always 'undebug all' afterwards.
