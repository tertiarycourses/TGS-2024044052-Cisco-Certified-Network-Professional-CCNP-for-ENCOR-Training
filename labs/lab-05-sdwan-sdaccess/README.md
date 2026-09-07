# Lab 5 — Explore SD-WAN and SD-Access Architecture

**Topic 01: Enterprise Architecture** · 15% of the exam · Skills Framework K1, A1 (ICT-DIT-3009-1.1)

## Exam Objective

Explain the working principles of the Cisco SD-WAN and SD-Access solutions and their control and data plane elements (ENCOR 1.3, 1.4).

## Scenario

Your organisation is evaluating both Cisco SD-WAN for its branch WAN and SD-Access for its campus. As the architect you must be able to name every plane element and say what breaks if it fails. You map the four SD-WAN planes and the SD-Access LISP/VXLAN/TrustSec stack, then work through failure scenarios that the exam poses as 'what happens if…' questions.

## What You'll Build

Two completed architecture maps — SD-WAN's four planes and SD-Access's control/data/policy planes — plus a failure-impact table for each component.

## Tools and Devices

Cisco Packet Tracer, architecture worksheet, sdwan-components.csv, sdaccess-components.csv.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-05-sdwan-sdaccess.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `failure-impact.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Component | Plane | Address | Solution | Notes |
| --- | --- | --- | --- | --- |
| vBond-1 | Orchestration | 203.0.113.10 | SD-WAN | Must be publicly reachable |
| vSmart-1 | Control | 10.200.0.11 | SD-WAN | Distributes OMP routes and policy |
| vManage-1 | Management | 10.200.0.10 | SD-WAN | GUI, API and templates |
| cEdge-BR1 | Data | 10.201.1.1 | SD-WAN | Branch 1 router |
| cEdge-BR2 | Data | 10.201.2.1 | SD-WAN | Branch 2 router |
| DNAC-1 | Management | 10.100.0.10 | SD-Access | Cisco DNA Center |
| CP-Node-1 | Control | 10.100.1.1 | SD-Access | LISP map server / map resolver |
| Border-1 | Border | 10.100.1.2 | SD-Access | Fabric border node |
| Edge-1 | Edge | 10.100.1.11 | SD-Access | Fabric edge node |

## Steps

1. Open lab-05-sdwan-sdaccess/ and read the two topology diagrams provided
2. Map the SD-WAN orchestration plane to vBond and state what it does — authenticates and introduces devices
3. Map the control plane to vSmart and note it distributes routes and policy over OMP, never carrying data
4. Map the management plane to vManage — the GUI, API and configuration templates
5. Map the data plane to the vEdge/cEdge routers that build the IPsec fabric between sites
6. Answer the failure question: if vSmart fails, existing data plane tunnels keep forwarding but no new routes are learned
7. Move to SD-Access and identify the underlay — any routed IP network providing reachability
8. Identify the overlay data plane as VXLAN and note the VNI replaces the VLAN as the segment identifier
9. Identify the control plane as LISP, with the map server and map resolver resolving EID to RLOC
10. Identify the policy plane as TrustSec, carrying SGTs enforced as SGACLs at egress
11. Name the fabric roles: control plane node, border node, edge node and wireless LAN controller
12. Complete the failure-impact table for each component in both architectures

## Validation

You can name all four SD-WAN planes with their controller, state that a vSmart outage stops new route learning but not existing forwarding, and correctly identify LISP as the SD-Access control plane and VXLAN as its data plane.

## Checkpoint Questions

1. Which SD-WAN component must be publicly reachable, and why?
1. If vSmart fails, does existing traffic keep flowing? Explain.
1. What is the SD-Access control plane protocol, and what is its data plane?
1. What is the difference between an EID and an RLOC?

## Exam Focus

Keep SD-WAN and SD-Access apart: SD-WAN is the WAN with OMP/vSmart and IPsec; SD-Access is the campus with LISP and VXLAN. Both appear in domain 1 and questions rely on you confusing them.
