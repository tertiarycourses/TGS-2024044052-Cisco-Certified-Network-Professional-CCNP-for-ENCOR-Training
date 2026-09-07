# Lab 27 — Implement Local and Server-Based AAA

**Topic 05: Network Security** · 20% of the exam · Skills Framework K4, A6 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify device access control — authentication and authorization using AAA (ENCOR 5.1.b).

## Scenario

Managing local accounts on 200 devices does not scale, and when an administrator leaves nobody can be sure every account is gone. As the engineer you centralise authentication on TACACS+ and RADIUS with AAA — and you deliberately keep a local fallback, because the classic AAA disaster is locking the whole team out when the server is unreachable.

## What You'll Build

Routers authenticating administrators against TACACS+ (192.168.2.2) and RADIUS (192.168.3.2) with a working local fallback, plus authorization and accounting enabled.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, TACACS+ server, RADIUS server.

## Topology

```text
   PC-A --- [ R1 ] --- [ R2 ] --- [ R3 ] --- PC-C
             TACACS+       |         RADIUS
             client        |         client
                    TACACS+ Server   RADIUS Server
                    192.168.2.2      192.168.3.2
   Always configure the LOCAL fallback before 'aaa new-model'.
```

## Lab Files

| File | What it is |
| --- | --- |
| `lab-27-aaa.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Role | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/1 | 192.168.1.1 | 255.255.255.0 | TACACS+ client | aaa authentication via TACACS+ |
| R1 | S0/0/0 | 10.1.1.2 | 255.255.255.252 | Transit | To R2 |
| R2 | G0/0 | 192.168.2.1 | 255.255.255.0 | Transit | TACACS+ server segment |
| R3 | G0/1 | 192.168.3.1 | 255.255.255.0 | RADIUS client | aaa authentication via RADIUS |
| TACACS+ Server | NIC | 192.168.2.2 | 255.255.255.0 | AAA server | Key TacacsKey123, TCP 49 |
| RADIUS Server | NIC | 192.168.3.2 | 255.255.255.0 | AAA server | Key RadiusKey123, UDP 1645/1646 |
| PC-A | NIC | 192.168.1.3 | 255.255.255.0 | Admin host | Tests the login |

## Steps

1. Open lab-27-aaa/lab-27-aaa.pkt and note the TACACS+ server at 192.168.2.2 and RADIUS at 192.168.3.2
2. Create the local fallback account BEFORE you enable AAA — this is what saves you

   ```text
   R1(config)# username admin privilege 15 secret Adm1n!Pass
   ```

3. Enable the AAA subsystem

   ```text
   R1(config)# aaa new-model
   ```

4. Define the TACACS+ server

   ```text
   R1(config)# tacacs server TAC-SRV
   ```

5. Set its address

   ```text
   R1(config-server-tacacs)# address ipv4 192.168.2.2
   ```

6. Set the shared secret, which must match the server exactly

   ```text
   R1(config-server-tacacs)# key TacacsKey123
   ```

7. Set the login authentication method list with the local fallback last

   ```text
   R1(config)# aaa authentication login default group tacacs+ local
   ```

8. Add authorization so the server also decides what the user may run

   ```text
   R1(config)# aaa authorization exec default group tacacs+ local
   ```

9. Add accounting so every command is recorded

   ```text
   R1(config)# aaa accounting exec default start-stop group tacacs+
   ```

10. Now configure RADIUS on R3 for comparison

   ```text
   R3(config)# radius server RAD-SRV
   ```

11. Set the RADIUS address and its authentication and accounting ports

   ```text
   R3(config-server-radius)# address ipv4 192.168.3.2 auth-port 1645 acct-port 1646
   ```

12. Set the RADIUS shared secret

   ```text
   R3(config-server-radius)# key RadiusKey123
   ```

13. Point R3's login authentication at RADIUS with a local fallback

   ```text
   R3(config)# aaa authentication login default group radius local
   ```

14. Test authentication against the server without dropping your session

   ```text
   R1# test aaa group tacacs+ admin Adm1n!Pass legacy
   ```

15. Verify the server is reachable and its statistics

   ```text
   R1# show tacacs
   ```

16. Shut the server link and confirm the local fallback still lets you in

   ```text
   R1(config-if)# shutdown
   ```

17. Record which protocol you would use for device administration and which for network access, and why

## Validation

'test aaa group tacacs+' returns a successful authentication, 'show tacacs' shows the server reachable, and with the server link shut you can still log in with the local admin account — proving the fallback works.

## Checkpoint Questions

1. Why must the local fallback user exist before you enable 'aaa new-model'?
1. Name three differences between TACACS+ and RADIUS.
1. Which protocol is preferred for device administration, and which for network access?
1. What does the 'local' keyword at the end of a method list do?

## Exam Focus

Create the local fallback user BEFORE 'aaa new-model'. TACACS+ = TCP 49, encrypts the whole payload, separates authn from authz, used for device admin. RADIUS = UDP, encrypts only the password, used for network access.
