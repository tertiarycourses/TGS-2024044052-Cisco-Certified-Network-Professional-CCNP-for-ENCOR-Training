# Lab 6 — Configure and Verify VRF-Lite

**Topic 02: Virtualization Technologies** · 10% of the exam · Skills Framework K2, A2 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify data path virtualization technologies — VRF (ENCOR 2.2.a).

## Scenario

Your organisation must keep guest traffic and corporate traffic completely separate on the same physical router, and the acquisition it just completed uses the same 192.168.1.0/24 range as head office. As the network engineer you solve both problems with VRF-Lite: two independent routing tables on one device, with overlapping address space and no leaking between them.

## What You'll Build

A router carrying two VRFs (CORP and GUEST) with overlapping 192.168.1.0/24 prefixes, proven isolated by a VRF-aware ping that succeeds inside a VRF and fails across VRFs.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1 router, CORP-PC and GUEST-PC.

## Topology

```text
                    +----------------+
   CORP-PC -------- | G0/0  VRF CORP |
 192.168.1.10       |                |   R1 — one router, two routing tables
   GUEST-PC ------- | G0/1  VRF GUEST|
 192.168.1.10       +----------------+
   (identical addresses — isolated because they are in different VRFs)
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-06-vrf-lite.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | VRF | IP Address | Subnet Mask | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | CORP | 192.168.1.1 | 255.255.255.0 | Overlapping prefix, corporate |
| R1 | G0/1 | GUEST | 192.168.1.1 | 255.255.255.0 | Overlapping prefix, guest |
| CORP-PC | NIC | CORP | 192.168.1.10 | 255.255.255.0 | Gateway 192.168.1.1 in CORP |
| GUEST-PC | NIC | GUEST | 192.168.1.10 | 255.255.255.0 | Gateway 192.168.1.1 in GUEST |

## Steps

1. Open lab-06-vrf-lite/lab-06-vrf-lite.pkt and note both PCs use 192.168.1.10 in different VRFs
2. Create the CORP VRF on R1

   ```text
   R1(config)# vrf definition CORP
   ```

3. Enable IPv4 address family inside the VRF

   ```text
   R1(config-vrf)# address-family ipv4
   ```

4. Create the GUEST VRF the same way

   ```text
   R1(config)# vrf definition GUEST
   ```

5. Assign G0/0 to the CORP VRF — note this clears any existing IP address

   ```text
   R1(config-if)# vrf forwarding CORP
   ```

6. Now add the address to the CORP interface

   ```text
   R1(config-if)# ip address 192.168.1.1 255.255.255.0
   ```

7. Assign G0/1 to the GUEST VRF and give it the identical address

   ```text
   R1(config-if)# vrf forwarding GUEST
   ```

8. Add the overlapping address to the GUEST interface

   ```text
   R1(config-if)# ip address 192.168.1.1 255.255.255.0
   ```

9. List the VRFs and confirm each owns its interface

   ```text
   R1# show vrf
   ```

10. Display the CORP routing table — it must be separate from the global table

   ```text
   R1# show ip route vrf CORP
   ```

11. Display the GUEST routing table and confirm the same prefix appears independently

   ```text
   R1# show ip route vrf GUEST
   ```

12. Ping inside the CORP VRF — this must succeed

   ```text
   R1# ping vrf CORP 192.168.1.10
   ```

13. Ping the same address without a VRF keyword and observe it consult the empty global table and fail

   ```text
   R1# ping 192.168.1.10
   ```


## Validation

'show vrf' lists CORP and GUEST with their interfaces, both VRF routing tables carry 192.168.1.0/24 independently, 'ping vrf CORP' succeeds, and the unqualified ping fails — proving isolation rather than a broken configuration.

## Checkpoint Questions

1. Why does a ping without the 'vrf' keyword fail even though the VRF ping succeeds?
1. What happens to an interface's IP address when you assign it to a VRF?
1. How can two interfaces on one router carry the same IP address?
1. What is the difference between VRF-Lite and full MPLS VPN?

## Exam Focus

Every show, ping and traceroute in a VRF must be qualified with the vrf keyword. An unqualified command consults the global table and looks like a failure when the configuration is actually correct.
