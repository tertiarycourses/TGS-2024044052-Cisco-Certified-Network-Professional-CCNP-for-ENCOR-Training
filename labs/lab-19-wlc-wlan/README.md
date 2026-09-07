# Lab 19 — Configure a Basic WLAN and WPA2-Enterprise on the WLC

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Describe AP discovery and join, wireless segmentation with groups, profiles and tags, and configure wireless security features (ENCOR 3.3.c, 3.3.f, 5.4).

## Scenario

The office is deploying its first controller-based wireless network. As the wireless engineer you build the WLC configuration end to end through the GUI: interfaces and VLANs, a PSK guest WLAN, then a WPA2-Enterprise corporate WLAN backed by RADIUS. You watch the AP complete its CAPWAP discovery and join, and confirm clients land in the right VLAN.

## What You'll Build

A WLC with a management interface on 192.168.200.254, a joined LAP, a PSK guest WLAN and a WPA2-Enterprise corporate WLAN authenticating against the RADIUS server at 172.31.1.254.

## Tools and Devices

Cisco Packet Tracer, WLC-1 GUI, LAP-1, R1, SW1, RADIUS server, wireless hosts.

## Topology

```text
  Wireless Host ~~~ [ LAP-1 ] --- [ SW-1 ] --- [ R-1 ] --- RADIUS 172.31.1.254
        (VLAN 5)          CAPWAP        VLAN 200      |
                          5246 ctrl                   |
                          5247 data              [ WLC-1 ]
                                              192.168.200.254
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-19-wlc-wlan.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | VLAN | Notes |
| --- | --- | --- | --- | --- |
| R-1 | G0/0/1.5 | 192.168.5.1/24 | 5 | Wireless client VLAN gateway |
| R-1 | G0/0/1.200 | 192.168.200.1/24 | 200 | Management VLAN gateway |
| R-1 | G0/0/0 | 172.31.1.1/24 | N/A | Server VLAN gateway |
| SW-1 | VLAN 200 | 192.168.200.100/24 | 200 | Access switch management |
| WLC-1 | Management | 192.168.200.254/24 | 200 | Controller management interface |
| WLC-1 | Dynamic (VLAN 5) | 192.168.5.254/24 | 5 | Wireless client interface |
| LAP-1 | G0 | DHCP | 200 | Joins the WLC over CAPWAP |
| RADIUS Server | NIC | 172.31.1.254/24 | N/A | WPA2-Enterprise authentication |
| Admin PC | NIC | 192.168.200.200/24 | 200 | Runs the WLC GUI |
| Wireless Host | Wireless NIC | DHCP | 5 | Guest and corporate test client |

## Steps

1. Open lab-19-wlc-wlan/lab-19-wlc-wlan.pkt and browse to the WLC at https://192.168.200.254 from the Admin PC
2. Log in to the WLC GUI and review the Monitor summary page
3. Under Controller > Interfaces, create the VLAN 5 dynamic interface for wireless clients
4. Set the interface IP as 192.168.5.254/24 with gateway 192.168.5.1 and the DHCP server address
5. Confirm the AP has completed CAPWAP discovery and joined under Wireless > All APs
6. Note the CAPWAP control tunnel on UDP 5246 and the data tunnel on UDP 5247
7. Under WLANs, create the guest WLAN and set its SSID and profile name
8. Map the guest WLAN to the VLAN 5 dynamic interface
9. On the Security tab, set Layer 2 security to WPA2 with PSK and enter the pre-shared key
10. Enable the WLAN under General and verify it appears in the WLAN list
11. Now create the corporate WLAN for WPA2-Enterprise
12. Under Security > AAA Servers, add the RADIUS server 172.31.1.254 with its shared secret
13. Set the corporate WLAN's Layer 2 security to WPA2 with 802.1X and select that RADIUS server
14. Connect a wireless host to the guest SSID and confirm it receives a VLAN 5 address

   ```text
   C:\> ipconfig
   ```

15. Connect a second host to the corporate SSID with a RADIUS username and password
16. Verify both clients under Monitor > Clients showing their SSID, VLAN and policy

## Validation

The LAP shows as joined and associated in Wireless > All APs, both WLANs appear enabled in the WLAN list, the guest client receives a 192.168.5.x address, and the corporate client authenticates against RADIUS and appears under Monitor > Clients.

## Checkpoint Questions

1. Which two UDP ports does CAPWAP use, and what does each carry?
1. Name four ways an AP can discover a controller.
1. What is the difference between WPA2-Personal and WPA2-Enterprise?
1. What does the dynamic interface on a WLC do?

## Exam Focus

CAPWAP: UDP 5246 control (DTLS-encrypted), UDP 5247 data. AP discovery order: broadcast, DHCP option 43, DNS, previously learnt list. 'The AP will not join' is usually option 43, DNS or a certificate mismatch.
