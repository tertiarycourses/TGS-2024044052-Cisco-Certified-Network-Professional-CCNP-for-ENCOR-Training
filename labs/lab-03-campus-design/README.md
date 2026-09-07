# Lab 3 — Compare Two-Tier and Three-Tier Campus Designs

**Topic 01: Enterprise Architecture** · 15% of the exam · Skills Framework K1, A1 (ICT-DIT-3009-1.1)

## Exam Objective

Explain enterprise design principles including 2-tier, 3-tier, fabric and cloud designs (ENCOR 1.1.a).

## Scenario

A 400-staff company on one campus is merging with a 2,000-staff company across four buildings. As the design engineer you must recommend a campus architecture for the merged organisation. You document the current 2-tier collapsed-core design, model the merged requirement, and justify whether a dedicated core layer is now warranted — the exact judgement the exam tests.

## What You'll Build

A completed design comparison table and a one-page written recommendation stating whether to move to a 3-tier design, with the trigger conditions that justify it.

## Tools and Devices

Cisco Packet Tracer, network diagram, design decision worksheet.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-03-campus-design.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `design-comparison.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Role | Management IP | Subnet Mask | Building | Notes |
| --- | --- | --- | --- | --- | --- |
| SW-ACC-1 | Access | 10.10.1.11 | 255.255.255.0 | A | 24 x PoE edge ports |
| SW-ACC-2 | Access | 10.10.1.12 | 255.255.255.0 | A | 24 x PoE edge ports |
| SW-DIST-1 | Distribution | 10.10.1.1 | 255.255.255.0 | A | L2/L3 boundary, HSRP active |
| SW-DIST-2 | Distribution | 10.10.1.2 | 255.255.255.0 | A | L2/L3 boundary, HSRP standby |
| SW-ACC-3 | Access | 10.10.2.11 | 255.255.255.0 | B | Merged company |
| SW-DIST-3 | Distribution | 10.10.2.1 | 255.255.255.0 | B | Merged company |

## Steps

1. Open lab-03-campus-design/lab-03-campus-design.pkt and identify which switches are access and which are distribution
2. Record what each layer is doing today — port security and PoE at access, routing at distribution

   ```text
   SW-DIST-1# show ip route
   ```

3. Confirm the distribution layer is the Layer 2 to Layer 3 boundary by checking the SVIs

   ```text
   SW-DIST-1# show ip interface brief | include Vlan
   ```

4. Count the distribution blocks the merged network will need (one per building)
5. Apply the design rule: a dedicated core is justified beyond roughly three distribution blocks
6. Calculate the full-mesh link count without a core — n(n-1)/2 for four blocks
7. Complete the comparison table in design-comparison.csv for cost, cabling, convergence and scalability
8. Document where high availability belongs — redundant supervisors, links, FHRP and SSO/NSF
9. State which layer must never carry policy, and why the core stays simple and fast
10. Write your recommendation with the trigger conditions that would justify the change

## Validation

Your recommendation names 3-tier for the merged network, shows the full-mesh link count that falls from six inter-block links to four uplinks once a core is added, and states that the core layer carries no ACLs or policy.

## Checkpoint Questions

1. What is the trigger that justifies a dedicated core layer?
1. How many inter-block links does a full mesh of six distribution blocks need?
1. Which layer must never carry ACLs or policy, and why?
1. Where does the Layer 2 to Layer 3 boundary sit in a traditional campus design?

## Exam Focus

The trigger for a dedicated core is roughly three distribution blocks, not a user count. Be ready to justify it with the link maths: a full mesh grows as n(n-1)/2, a core grows linearly.
