# Lab 8 — Configure and Verify a Site-to-Site IPsec VPN

**Topic 02: Virtualization Technologies** · 10% of the exam · Skills Framework K2, A2 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify data path virtualization technologies — IPsec tunneling (ENCOR 2.2.b).

## Scenario

The GRE tunnel from the previous lab carries payroll data in clear text, and the audit has flagged it. As the security-minded network engineer you now build a site-to-site IPsec VPN between R1 and R3 across the R2 ISP, working through both IKE phases and proving the tunnel only forms once interesting traffic matches on both ends.

## What You'll Build

A functioning site-to-site IPsec VPN between R1 (192.168.1.0/24) and R3 (192.168.3.0/24) with a formed ISAKMP SA, established IPsec SAs and encrypted packet counters incrementing.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC-A and PC-C.

## Topology

```text
  PC-A            R1              R2 (ISP)            R3            PC-C
192.168.1.3 --- G0/0  S0/0/0 --- S0/0/0  S0/0/1 --- S0/0/1  G0/0 --- 192.168.3.3
            192.168.1.1 10.1.1.2  10.1.1.1 10.2.2.1  10.2.2.2 192.168.3.1
                        \________ IPsec tunnel (protects 192.168.1.0 <-> 192.168.3.0) ________/
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-08-ipsec-vpn.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | 192.168.1.1 | 255.255.255.0 | N/A | Site 1 LAN |
| R1 | S0/0/0 | 10.1.1.2 | 255.255.255.252 | N/A | VPN peer interface |
| R2 | S0/0/0 | 10.1.1.1 | 255.255.255.252 | N/A | ISP, transit only |
| R2 | S0/0/1 | 10.2.2.1 | 255.255.255.252 | N/A | ISP, transit only |
| R3 | G0/0 | 192.168.3.1 | 255.255.255.0 | N/A | Site 3 LAN |
| R3 | S0/0/1 | 10.2.2.2 | 255.255.255.252 | N/A | VPN peer interface |
| PC-A | NIC | 192.168.1.3 | 255.255.255.0 | 192.168.1.1 | Interesting traffic source |
| PC-C | NIC | 192.168.3.3 | 255.255.255.0 | 192.168.3.1 | Interesting traffic destination |

## Steps

1. Open lab-08-ipsec-vpn/lab-08-ipsec-vpn.pkt and confirm R1 and R3 reach each other through R2

   ```text
   R1# ping 10.2.2.2
   ```

2. Enable the security technology package if the lab image requires it

   ```text
   R1(config)# license boot module c1900 technology-package securityk9
   ```

3. Create the IKE Phase 1 policy defining how the management tunnel is protected

   ```text
   R1(config)# crypto isakmp policy 10
   ```

4. Set AES encryption, SHA hashing, pre-shared key authentication and DH group 5

   ```text
   R1(config-isakmp)# encryption aes 256
   ```

5. Set the pre-shared key and the peer it applies to

   ```text
   R1(config)# crypto isakmp key Cisco123 address 10.2.2.2
   ```

6. Define the Phase 2 transform set that protects the actual data

   ```text
   R1(config)# crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
   ```

7. Write the interesting-traffic ACL — this must mirror exactly on the far end

   ```text
   R1(config)# access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255
   ```

8. Build the crypto map binding the peer, transform set and ACL together

   ```text
   R1(config)# crypto map VPN-MAP 10 ipsec-isakmp
   ```

9. Set the peer inside the crypto map

   ```text
   R1(config-crypto-map)# set peer 10.2.2.2
   ```

10. Apply the crypto map to the outside interface

   ```text
   R1(config-if)# crypto map VPN-MAP
   ```

11. Repeat the mirrored configuration on R3, reversing the ACL source and destination

   ```text
   R3(config)# access-list 110 permit ip 192.168.3.0 0.0.0.255 192.168.1.0 0.0.0.255
   ```

12. Generate interesting traffic from PC-A to PC-C to bring the tunnel up

   ```text
   C:\> ping 192.168.3.3
   ```

13. Verify the Phase 1 ISAKMP SA is in QM_IDLE state

   ```text
   R1# show crypto isakmp sa
   ```

14. Verify the Phase 2 IPsec SAs and confirm the encrypt and decrypt counters are climbing

   ```text
   R1# show crypto ipsec sa
   ```


## Validation

'show crypto isakmp sa' shows the peer in QM_IDLE and 'show crypto ipsec sa' shows non-zero '#pkts encaps' and '#pkts decaps' counters that increase with each ping — traffic between the two LANs is genuinely encrypted.

## Checkpoint Questions

1. What does IKE Phase 1 build, and what does Phase 2 build?
1. Why must the interesting-traffic ACL mirror exactly on both ends?
1. Which show command proves traffic is actually being encrypted?
1. What does QM_IDLE mean in 'show crypto isakmp sa'?

## Exam Focus

Phase 1 builds one bidirectional ISAKMP SA; Phase 2 builds the unidirectional IPsec SAs that carry data. A mismatched interesting-traffic ACL is the classic Phase 2 failure. Non-zero encaps/decaps counters are the proof.
