# Lab Environment and Tools

For Cisco Certified Network Professional (CCNP) for ENCOR Training (TGS-2024044052), preparing for Cisco 350-401 ENCOR v1.1.

## Required Tools

| Tool | Purpose |
| --- | --- |
| Cisco Packet Tracer 8.2+ | The primary lab environment. Every .pkt/.pka topology in labs/ opens in Packet Tracer — free from the Cisco Networking Academy. |
| Cisco IOS / IOS XE CLI | All configuration is done at the IOS CLI, so the commands transfer directly to real 9200/9300 switches and ISR/CSR routers. |
| Wireless LAN Controller (WLC) | The Packet Tracer WLC GUI is used for the WLAN, WPA2-Enterprise and wireless troubleshooting labs. |
| Python 3.10+ | Used for the automation labs — interpreting scripts, parsing JSON and calling REST APIs. |
| Postman or curl | Used to exercise the Cisco DNA Center and RESTCONF APIs and to read response codes. |
| A text editor | VS Code or any editor for writing Python scripts, JSON payloads and saved configurations. |

## Installing Cisco Packet Tracer

1. Create a free account at [netacad.com](https://www.netacad.com).
2. Enrol in the free 'Getting Started with Cisco Packet Tracer' course, which unlocks the download.
3. Download and install the release for your operating system (Windows, macOS or Linux).
4. Launch Packet Tracer and sign in with your NetAcad account — it will not open a topology until you do.
5. Open any `.pkt` file from a lab folder to confirm the install works.

## Cisco IOS CLI Quick Reference

| Mode | Prompt | How to get there | What you do here |
| --- | --- | --- | --- |
| User EXEC | `Router>` | Default on connect | Limited show commands |
| Privileged EXEC | `Router#` | `enable` | All show commands, debug, copy, reload |
| Global config | `Router(config)#` | `configure terminal` | Device-wide configuration |
| Interface config | `Router(config-if)#` | `interface g0/0` | Per-interface configuration |
| Line config | `Router(config-line)#` | `line vty 0 4` | Console, VTY and AUX settings |
| Router config | `Router(config-router)#` | `router ospf 10` | Routing protocol configuration |

## The Show Commands That Matter Most

| Command | What it proves |
| --- | --- |
| `show running-config` | What is actually configured right now |
| `show ip interface brief` | Interface addresses and up/down state — the fastest health check |
| `show ip route` | The RIB: which routes the router has chosen |
| `show ip cef` | The FIB: what CEF will actually use to forward |
| `show mac address-table` | The CAM table on a switch |
| `show interfaces trunk` | Trunk mode, native VLAN and allowed VLANs |
| `show etherchannel summary` | Bundle state and which members are bundled |
| `show spanning-tree` | Root bridge, port roles and port states |
| `show ip ospf neighbor` | OSPF adjacency state — must reach FULL |
| `show ip eigrp topology` | Successors and feasible successors |
| `show ip bgp summary` | BGP session state and prefixes received |
| `show standby brief` | HSRP active/standby and the virtual IP |
| `show ip nat translations` | Active NAT/PAT translations |
| `show crypto isakmp sa` | IKE Phase 1 state — QM_IDLE means established |
| `show crypto ipsec sa` | Phase 2 SAs and the encaps/decaps counters |
| `show flow monitor <name> cache` | The NetFlow flow cache |
| `show ip sla statistics` | IP SLA probe results and RTT |
| `show access-lists` | ACL contents and per-line match counters |
| `show policy-map control-plane` | CoPP conformed and exceeded counters |
| `show event manager policy registered` | Which EEM applets are armed |

## Safety Note

Every lab in this course runs in Cisco Packet Tracer, a simulator. When you apply these techniques to a production network, follow your organisation's change-management process. Several commands used here — clearing a MAC address table, shutting an interface, applying an ACL or a CoPP policy — will interrupt live traffic. Take a configuration backup first and have a documented rollback.
