# Lab 9 — Explore LISP and VXLAN Network Virtualization

**Topic 02: Virtualization Technologies** · 10% of the exam · Skills Framework K2, A2 (ICT-DIT-3009-1.1)

## Exam Objective

Describe network virtualization concepts — LISP and VXLAN (ENCOR 2.3.a, 2.3.b).

## Scenario

Your campus is moving to SD-Access, whose entire mobility story rests on LISP and whose data plane is VXLAN. As the network engineer you must be able to trace a packet through both. You walk the LISP map-request and map-reply exchange, follow an endpoint that roams between edge switches, then decode a VXLAN header field by field and calculate the encapsulation overhead.

## What You'll Build

An annotated LISP registration and lookup walkthrough, a completed VXLAN header decode with all field sizes, and a calculated MTU requirement for the underlay.

## Tools and Devices

Cisco Packet Tracer, packet-decode worksheet, vxlan-header.csv, lisp-mapping.csv.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-09-lisp-vxlan.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `vxlan-header.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Component | Role | EID / RLOC | VNI / Address | Notes |
| --- | --- | --- | --- | --- |
| Host-A | Endpoint | EID 10.10.10.10 | VNI 10001 | Roams between edge nodes |
| Edge-1 | Edge node / xTR | RLOC 10.100.1.11 | VNI 10001 | Host-A's original attachment |
| Edge-2 | Edge node / xTR | RLOC 10.100.1.12 | VNI 10001 | Host-A's attachment after the roam |
| CP-Node-1 | Map server / resolver | 10.100.1.1 | N/A | Holds the EID-to-RLOC bindings |
| Border-1 | Border node | 10.100.1.2 | N/A | Fabric exit to the rest of the network |
| Host-B | Endpoint | EID 10.10.20.20 | VNI 10002 | Different VNI, no L2 adjacency to Host-A |

## Steps

1. Open lab-09-lisp-vxlan/ and read the fabric topology showing edge nodes, border node and control plane node
2. Identify the EID — the endpoint identifier, the host's own IP address that never changes as it roams
3. Identify the RLOC — the routing locator, the address of the edge switch the host is attached to now
4. Trace registration: the edge node registers the EID-to-RLOC binding with the map server
5. Trace lookup: an ingress tunnel router sends a map-request to the map resolver
6. Trace the reply: the map server returns the RLOC, and the ITR caches it in its map cache
7. Model a roam — the host moves to a second edge node, which re-registers the same EID to a new RLOC
8. State why the host keeps its IP address across the roam, and why that is what makes fabric mobility work
9. Move to VXLAN and record the outer headers: outer MAC, outer IP, UDP with destination port 4789
10. Record the 8-byte VXLAN header carrying the 24-bit VNI
11. Calculate the total overhead — 50 bytes — and state the resulting underlay MTU of at least 1550
12. Compare the segment ceiling: 4,094 VLANs against 16,777,216 VNIs
13. Complete vxlan-header.csv with each field, its size and its purpose

## Validation

You can state the LISP lookup sequence (register, map-request, map-reply, cache), explain why an EID survives a roam, name UDP 4789 as the VXLAN port, and calculate the 50-byte overhead and the 1550-byte minimum underlay MTU.

## Checkpoint Questions

1. Which UDP port does VXLAN use?
1. How many bytes of overhead does VXLAN add, and what underlay MTU does that require?
1. How does a host keep its IP address when it roams between fabric edge nodes?
1. How many segments can a 24-bit VNI address, compared with 802.1Q VLANs?

## Exam Focus

Memorise: VXLAN is UDP 4789, 8-byte header, 24-bit VNI, 50 bytes total overhead, so the underlay needs an MTU of at least 1550. LISP separates the EID (who) from the RLOC (where).
