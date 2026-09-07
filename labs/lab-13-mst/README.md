# Lab 13 — Configure Multiple Spanning Tree (MST)

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify common Spanning Tree Protocols — MST (ENCOR 3.1.c).

## Scenario

The campus carries 200 VLANs, and running one spanning tree per VLAN is consuming switch CPU and making troubleshooting impractical. As the engineer you consolidate them onto two MST instances, load-balancing the VLANs across two roots, and confirm all switches join the same MST region — which requires name, revision and VLAN map to match exactly.

## What You'll Build

A three-switch MST region named CAMPUS with VLANs mapped to instances 1 and 2, S1 root for instance 1 and S2 root for instance 2, giving true load distribution.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-13-mst.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| MST Instance | VLAN Range | Root Switch | Secondary | Notes |
| --- | --- | --- | --- | --- |
| Instance 0 (IST) | Unmapped VLANs | S1 | S2 | The internal spanning tree |
| Instance 1 | 1-100 | S1 | S2 | First half of the campus VLANs |
| Instance 2 | 101-200 | S2 | S1 | Second half — load distribution |

## Steps

1. Open lab-13-mst/lab-13-mst.pkt and count how many spanning tree instances are running today

   ```text
   S1# show spanning-tree summary
   ```

2. Change the spanning tree mode to MST on S1

   ```text
   S1(config)# spanning-tree mode mst
   ```

3. Enter MST configuration mode to define the region

   ```text
   S1(config)# spanning-tree mst configuration
   ```

4. Name the region — this must match character for character on every switch

   ```text
   S1(config-mst)# name CAMPUS
   ```

5. Set the revision number, which must also match exactly

   ```text
   S1(config-mst)# revision 1
   ```

6. Map the first half of the VLANs to instance 1

   ```text
   S1(config-mst)# instance 1 vlan 1-100
   ```

7. Map the second half to instance 2

   ```text
   S1(config-mst)# instance 2 vlan 101-200
   ```

8. Review the pending configuration before you commit it

   ```text
   S1(config-mst)# show pending
   ```

9. Apply the identical region configuration to S2 and S3

   ```text
   S2(config-mst)# name CAMPUS
   ```

10. Make S1 the root for instance 1

   ```text
   S1(config)# spanning-tree mst 1 root primary
   ```

11. Make S2 the root for instance 2 so the two instances take different paths

   ```text
   S2(config)# spanning-tree mst 2 root primary
   ```

12. Verify the region name, revision and the configuration digest all match across switches

   ```text
   S1# show spanning-tree mst configuration
   ```

13. Confirm both instances are running with the intended roots

   ```text
   S1# show spanning-tree mst
   ```

14. Tune an MST port cost on one instance to influence its path independently

   ```text
   S3(config-if)# spanning-tree mst 1 cost 100000
   ```


## Validation

'show spanning-tree mst configuration' returns the same region name CAMPUS, revision 1 and identical configuration digest on all three switches, and 'show spanning-tree mst' shows S1 root for instance 1 and S2 root for instance 2.

## Checkpoint Questions

1. Which three values must match exactly for switches to be in the same MST region?
1. Why does mapping 200 VLANs onto 2 instances reduce switch CPU?
1. How do you achieve load distribution with MST?
1. What is instance 0 called, and what does it carry?

## Exam Focus

Name, revision number and VLAN-to-instance map must match EXACTLY or the switches are in different MST regions. Load-balance by making different switches root for different instances.
