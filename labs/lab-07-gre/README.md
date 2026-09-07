# Lab 7 — Configure and Verify a GRE Tunnel

**Topic 02: Virtualization Technologies** · 10% of the exam · Skills Framework K2, A2 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify data path virtualization technologies — GRE tunneling (ENCOR 2.2.b).

## Scenario

Head office and the branch are connected only across the public internet, but the routing protocol and multicast traffic they need to exchange cannot cross it. As the WAN engineer you build a GRE tunnel that carries those private networks over the public path, then demonstrate the critical limitation the exam always tests: GRE gives you transport, not confidentiality.

## What You'll Build

A working GRE tunnel between RA (64.103.211.2) and RB (209.165.122.2) carrying 192.168.1.0/24 and 192.168.2.0/24, verified up/up with traffic passing.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, RA and RB routers, PCA and PCB.

## Topology

```text
  PCA                RA                              RB                PCB
192.168.1.2 --- G0/0    S0/0/0 --- [ internet ] --- S0/0/0    G0/0 --- 192.168.2.2
            192.168.1.1  64.103.211.2          209.165.122.2  192.168.2.1
                          \                                  /
                           Tunnel0 10.10.10.1 -- 10.10.10.2 (GRE)
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-07-gre.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Notes |
| --- | --- | --- | --- | --- | --- |
| RA | G0/0 | 192.168.1.1 | 255.255.255.0 | N/A | Head office LAN |
| RA | S0/0/0 | 64.103.211.2 | 255.255.255.252 | N/A | Public, tunnel source |
| RA | Tunnel0 | 10.10.10.1 | 255.255.255.252 | N/A | GRE tunnel |
| RB | G0/0 | 192.168.2.1 | 255.255.255.0 | N/A | Branch LAN |
| RB | S0/0/0 | 209.165.122.2 | 255.255.255.252 | N/A | Public, tunnel source |
| RB | Tunnel0 | 10.10.10.2 | 255.255.255.252 | N/A | GRE tunnel |
| PCA | NIC | 192.168.1.2 | 255.255.255.0 | 192.168.1.1 | Head office host |
| PCB | NIC | 192.168.2.2 | 255.255.255.0 | 192.168.2.1 | Branch host |

## Steps

1. Open lab-07-gre/lab-07-gre.pkt and confirm RA and RB can reach each other over their public addresses

   ```text
   RA# ping 209.165.122.2
   ```

2. Create the tunnel interface on RA

   ```text
   RA(config)# interface Tunnel0
   ```

3. Give the tunnel its own private address in the 10.10.10.0/30 transit range

   ```text
   RA(config-if)# ip address 10.10.10.1 255.255.255.252
   ```

4. Set the tunnel source to RA's public interface

   ```text
   RA(config-if)# tunnel source Serial0/0/0
   ```

5. Set the tunnel destination to RB's public address

   ```text
   RA(config-if)# tunnel destination 209.165.122.2
   ```

6. Confirm the mode is GRE over IP, which is the IOS default

   ```text
   RA(config-if)# tunnel mode gre ip
   ```

7. Repeat on RB with the mirrored addresses

   ```text
   RB(config-if)# ip address 10.10.10.2 255.255.255.252
   ```

8. Set RB's tunnel source and destination back towards RA

   ```text
   RB(config-if)# tunnel destination 64.103.211.2
   ```

9. Add a static route on RA sending the remote LAN through the tunnel

   ```text
   RA(config)# ip route 192.168.2.0 255.255.255.0 10.10.10.2
   ```

10. Add the mirrored static route on RB

   ```text
   RB(config)# ip route 192.168.1.0 255.255.255.0 10.10.10.1
   ```

11. Verify the tunnel interface state and its source and destination

   ```text
   RA# show interfaces Tunnel0
   ```

12. Confirm the tunnel is up and carrying the right networks

   ```text
   RA# show ip interface brief | include Tunnel
   ```

13. Ping across the tunnel from PCA to PCB

   ```text
   C:\> ping 192.168.2.2
   ```

14. Note the GRE overhead of 24 bytes and why tunnel MTU is usually set to 1476

## Validation

'show interfaces Tunnel0' reports Tunnel0 up, line protocol up with the correct source and destination, PCA pings PCB successfully, and you can state that GRE adds no encryption, authentication or integrity.

## Checkpoint Questions

1. What security does GRE provide?
1. Why is the tunnel MTU usually set to 1476?
1. What are the two commands that define where a GRE tunnel goes?
1. Why would you choose GRE over IPsec alone for a site-to-site link carrying OSPF?

## Exam Focus

GRE provides NO confidentiality, integrity or authentication. It does carry routing protocols and multicast, which plain IPsec cannot — which is why GRE over IPsec is the classic enterprise answer.
