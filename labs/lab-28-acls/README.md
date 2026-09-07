# Lab 28 — Configure Extended ACLs to Mitigate Attacks

**Topic 05: Network Security** · 20% of the exam · Skills Framework K4, A6 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify infrastructure security features — ACLs (ENCOR 5.2.a).

## Scenario

The security team wants the branch to permit only what the business needs and to block the traffic patterns behind the last incident: spoofed private source addresses arriving from the internet and unsolicited inbound ICMP. As the engineer you write named extended ACLs, place them correctly, and confirm the implicit deny is not silently dropping something you needed.

## What You'll Build

Named extended ACLs permitting only required services, blocking spoofed RFC 1918 sources inbound and unsolicited ICMP, applied in the correct direction with verified hit counters.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC-A, PC-C, servers.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-28-acls.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `acl-test-matrix.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | 172.22.34.65 | 255.255.255.224 | N/A | User segment 1 |
| R1 | G0/1 | 172.22.34.97 | 255.255.255.240 | N/A | User segment 2 |
| R1 | G0/2 | 172.22.34.1 | 255.255.255.192 | N/A | Server segment |
| R1 | S0/0/0 | 209.165.200.226 | 255.255.255.224 | N/A | Internet edge — ACL applied inbound |
| Server | NIC | 172.22.34.62 | 255.255.255.192 | 172.22.34.1 | Web server, HTTP/HTTPS permitted |
| PC1 | NIC | 172.22.34.66 | 255.255.255.224 | 172.22.34.65 | Internal user |
| PC2 | NIC | 172.22.34.98 | 255.255.255.240 | 172.22.34.97 | Internal user |

## Steps

1. Open lab-28-acls/lab-28-acls.pkt and confirm PC1 can currently reach every service on the server

   ```text
   C:\> ping 172.22.34.62
   ```

2. Create a named extended ACL for the inbound internet edge

   ```text
   R1(config)# ip access-list extended INTERNET-IN
   ```

3. Block spoofed RFC 1918 sources arriving from outside

   ```text
   R1(config-ext-nacl)# deny ip 10.0.0.0 0.255.255.255 any
   ```

4. Block the 172.16.0.0/12 private range as a spoofed source

   ```text
   R1(config-ext-nacl)# deny ip 172.16.0.0 0.15.255.255 any
   ```

5. Block the 192.168.0.0/16 private range as a spoofed source

   ```text
   R1(config-ext-nacl)# deny ip 192.168.0.0 0.0.255.255 any
   ```

6. Permit only the web traffic the business needs to the server

   ```text
   R1(config-ext-nacl)# permit tcp any host 172.22.34.62 eq 80
   ```

7. Permit HTTPS to the same server

   ```text
   R1(config-ext-nacl)# permit tcp any host 172.22.34.62 eq 443
   ```

8. Permit return traffic for sessions your users established

   ```text
   R1(config-ext-nacl)# permit tcp any any established
   ```

9. Block unsolicited inbound ICMP echo but allow the replies your pings need

   ```text
   R1(config-ext-nacl)# deny icmp any any echo
   ```

10. Add an explicit deny with logging so you can see what the implicit deny would have dropped

   ```text
   R1(config-ext-nacl)# deny ip any any log
   ```

11. Apply the ACL inbound on the outside interface — extended ACLs go close to the source

   ```text
   R1(config-if)# ip access-group INTERNET-IN in
   ```

12. Verify the ACL contents and the order of the entries

   ```text
   R1# show access-lists INTERNET-IN
   ```

13. Generate test traffic and watch the match counters increment on the right lines

   ```text
   R1# show access-lists INTERNET-IN | include matches
   ```

14. Check the log for what the final deny caught

   ```text
   R1# show logging | include list INTERNET-IN
   ```

15. Test that permitted web traffic still works after the ACL is applied

   ```text
   C:\> ping 172.22.34.62
   ```


## Validation

'show access-lists INTERNET-IN' shows the entries in the intended order with match counters incrementing on the permit lines, spoofed private-source traffic is denied, permitted HTTP/HTTPS still reaches the server, and the logged deny shows what the implicit deny would have dropped.

## Checkpoint Questions

1. Where should a standard ACL be placed, and where an extended ACL?
1. What is the implicit last line of every ACL?
1. Why add an explicit 'deny ip any any log' when the implicit deny already exists?
1. What does the 'established' keyword match?

## Exam Focus

Standard ACLs match source only and go near the destination; extended ACLs match everything and go near the source. Every ACL ends in an implicit deny — that is the most common self-inflicted outage.
