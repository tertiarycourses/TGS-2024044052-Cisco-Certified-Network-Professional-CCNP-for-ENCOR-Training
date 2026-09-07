# Lab 10 — Troubleshoot 802.1Q Trunking and DTP

**Topic 03: Network Infrastructure** · 30% of the exam · Skills Framework K3, A3 (ICT-DIT-3009-1.1)

## Exam Objective

Troubleshoot static and dynamic 802.1q trunking protocols (ENCOR 3.1.a).

## Scenario

Users in VLAN 20 on the second floor have lost access to their file server while VLAN 10 users are unaffected. As the support engineer you work the trunk between S1 and S2: you verify the trunk formed at all, check the allowed VLAN list that is silently pruning VLAN 20, and resolve a native VLAN mismatch that CDP is already warning you about in the logs.

## What You'll Build

A repaired 802.1Q trunk carrying VLANs 10, 20 and 99 with a matching native VLAN on both ends, and DTP disabled in favour of a hard-set trunk.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches, PC0–PC5.

## Topology

```text
        PC1 (VLAN 20 - AFFECTED)      Server (VLAN 20)
              |                              |
   [  S1  ] =========== trunk =========== [  S2  ]
      |  Gi0/1        (802.1Q)        Gi0/1  |
   [  S3  ]                                  PC0/PC2
   Native VLAN 99 must match on both ends; VLANs 10, 20, 99 must be allowed.
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-10-trunking-dtp.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | VLAN | Notes |
| --- | --- | --- | --- | --- | --- |
| S1 | VLAN 99 | 192.168.99.1 | 255.255.255.0 | 99 | Management, native VLAN |
| S2 | VLAN 99 | 192.168.99.2 | 255.255.255.0 | 99 | Management, native VLAN |
| S3 | VLAN 99 | 192.168.99.3 | 255.255.255.0 | 99 | Management, native VLAN |
| PC0 | NIC | 192.168.10.1 | 255.255.255.0 | 10 | Unaffected user |
| PC1 | NIC | 192.168.20.1 | 255.255.255.0 | 20 | AFFECTED — cannot reach server |
| PC2 | NIC | 192.168.30.1 | 255.255.255.0 | 30 | Unaffected user |
| Server | NIC | 192.168.20.100 | 255.255.255.0 | 20 | File server for VLAN 20 |

## Steps

1. Open lab-10-trunking-dtp/lab-10-trunking-dtp.pkt and confirm PC1 (VLAN 20) cannot reach the server

   ```text
   C:\> ping 192.168.20.1
   ```

2. Check whether the link between S1 and S2 formed a trunk at all

   ```text
   S1# show interfaces trunk
   ```

3. Look at the switchport detail — note the administrative and operational mode differ

   ```text
   S1# show interfaces GigabitEthernet0/1 switchport
   ```

4. Read the DTP negotiation state; two 'dynamic auto' ends never form a trunk

   ```text
   S1# show dtp interface GigabitEthernet0/1
   ```

5. Hard-set the trunk on S1 rather than relying on negotiation

   ```text
   S1(config-if)# switchport mode trunk
   ```

6. Do the same on S2 so neither end depends on DTP

   ```text
   S2(config-if)# switchport mode trunk
   ```

7. Disable DTP negotiation entirely on both ends

   ```text
   S1(config-if)# switchport nonegotiate
   ```

8. Re-check the trunk and read the allowed VLAN list — VLAN 20 is missing

   ```text
   S1# show interfaces trunk
   ```

9. Add VLAN 20 back to the allowed list without wiping the others

   ```text
   S1(config-if)# switchport trunk allowed vlan add 20
   ```

10. Check the console log for the CDP native VLAN mismatch warning

   ```text
   S1# show logging | include NATIVE_VLAN_MISMATCH
   ```

11. Compare the native VLAN on each end

   ```text
   S1# show interfaces trunk | include Native
   ```

12. Set the native VLAN to 99 on both ends so they match

   ```text
   S1(config-if)# switchport trunk native vlan 99
   ```

13. Verify the trunk now carries all three VLANs with a matching native VLAN

   ```text
   S1# show interfaces trunk
   ```

14. Confirm the VLAN 20 user can reach the server again

   ```text
   C:\> ping 192.168.20.1
   ```


## Validation

'show interfaces trunk' reports mode 'on' with VLANs 10, 20 and 99 allowed and native VLAN 99 on both switches, the mismatch log stops, and the VLAN 20 PC pings its server.

## Checkpoint Questions

1. What happens when both ends of a link are set to 'dynamic auto'?
1. What is the symptom of a native VLAN mismatch, and which protocol warns you?
1. Why is 'switchport nonegotiate' considered good production practice?
1. What does 'switchport trunk allowed vlan 20' do that 'add 20' does not?

## Exam Focus

Two 'dynamic auto' ends never trunk. A native VLAN mismatch causes VLAN leaking and a CDP warning. Production practice is always to hard-set the mode and add 'switchport nonegotiate'.
