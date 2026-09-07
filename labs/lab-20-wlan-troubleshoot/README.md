# Lab 20 — Troubleshoot WLAN and Wireless Client Connectivity

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Troubleshoot WLAN configuration and wireless client connectivity issues using GUI only (ENCOR 3.3.e).

## Scenario

Three separate wireless complaints arrive the same morning: one user cannot see the SSID, one associates but gets no IP address, and one authenticates but cannot reach the internal server. As the wireless support engineer you must resolve all three using the WLC GUI only — no CLI — which is exactly how the exam frames this objective.

## What You'll Build

Three resolved wireless faults with a documented root cause for each: a disabled/misbroadcast WLAN, a wrong interface-to-VLAN mapping, and a RADIUS shared-secret mismatch.

## Tools and Devices

Cisco Packet Tracer, WLC-1 GUI, LAP-1, RADIUS server, Laptop1 and Laptop2.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-20-wlan-troubleshoot.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `troubleshooting-log.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | VLAN | Fault |
| --- | --- | --- | --- | --- |
| R1 | G0/0/0.10 | 192.168.10.1/24 | 10 | — |
| R1 | G0/0/0.20 | 192.168.20.1/24 | 20 | — |
| R1 | G0/0/0.200 | 192.168.200.1/24 | 200 | — |
| R1 | G0/0/1 | 172.31.1.1/24 | N/A | — |
| SW1 | VLAN 200 | 192.168.200.100/24 | 200 | — |
| WLC-1 | Management | 192.168.200.254/24 | 200 | — |
| LAP-1 | G0 | DHCP | 200 | — |
| RADIUS Server | NIC | 172.31.1.254/24 | N/A | Fault 3: shared secret mismatch |
| Admin PC | NIC | 192.168.200.200/24 | 200 | — |
| Laptop1 | Wireless0 | DHCP | 10 | Fault 1: cannot see the SSID |
| Laptop2 | Wireless0 | DHCP | 20 | Fault 2: associates but no IP address |

## Steps

1. Open lab-20-wlan-troubleshoot/lab-20-wlan-troubleshoot.pkt and log in to the WLC GUI as the admin
2. Fault 1: the user cannot see the SSID — check whether the WLAN is enabled under WLANs
3. Check the Broadcast SSID setting on the WLAN's Advanced tab
4. Confirm the WLAN is applied to the AP group or policy tag serving that AP
5. Enable the WLAN and its SSID broadcast, then confirm the client can see it
6. Fault 2: the client associates but has no IP address — inspect the WLAN's interface mapping
7. Compare the mapped dynamic interface's VLAN with the VLAN the DHCP scope serves
8. Check the DHCP server address configured on the dynamic interface
9. Correct the interface-to-VLAN mapping and renew the client address

   ```text
   C:\> ipconfig /renew
   ```

10. Fault 3: the corporate client fails authentication — open Security > AAA > RADIUS > Authentication
11. Verify the RADIUS server IP, port 1812 and that the server is marked enabled
12. Re-enter the shared secret so it matches the one configured on the RADIUS server
13. Retry the client association and watch it succeed under Monitor > Clients
14. Record each fault, its symptom, its root cause and its fix in troubleshooting-log.csv

## Validation

All three clients reach a working state: the SSID is visible and broadcast, the DHCP client holds an address in the correct VLAN, the 802.1X client authenticates, and troubleshooting-log.csv names a distinct root cause for each fault.

## Checkpoint Questions

1. If a client associates but gets no IP address, what should you check first?
1. What is the difference between a 401-style authentication failure and a mapping error?
1. Why does the exam specify 'GUI only' for this objective?
1. Where in the WLC GUI do you verify that an AP has joined?

## Exam Focus

This objective explicitly says GUI only — the exam will not accept a CLI answer. Work the layers in order: is the WLAN enabled and broadcast, is it mapped to the right interface/VLAN, does RADIUS answer?
