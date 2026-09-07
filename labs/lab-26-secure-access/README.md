# Lab 26 — Configure Secure Device Access with SSH and Strong Passwords

**Topic 05: Network Security** · 20% of the exam · Skills Framework K4, A6 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify device access control — lines and local user authentication (ENCOR 5.1.a).

## Scenario

An audit found the branch routers reachable by Telnet with a type 7 password that anyone can decode in seconds. As the engineer you harden device access: strong hashed local credentials, SSH version 2 only, Telnet removed from the VTY lines, an exec timeout, and login blocking so brute force attempts are throttled.

## What You'll Build

A router and switch reachable only by SSHv2 with type 9 hashed local credentials, Telnet disabled, an exec timeout set and login-attempt throttling armed.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, RTA router, SW1 switch, PCA.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-26-secure-access.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Default Gateway | Notes |
| --- | --- | --- | --- | --- | --- |
| RTA | G0/0 | 172.16.1.1 | 255.255.255.0 | N/A | Device being hardened |
| SW1 | VLAN 1 | 172.16.1.2 | 255.255.255.0 | 172.16.1.1 | Also hardened |
| PCA | NIC | 172.16.1.10 | 255.255.255.0 | 172.16.1.1 | Admin workstation |

## Steps

1. Open lab-26-secure-access/lab-26-secure-access.pkt and confirm Telnet currently works from PCA

   ```text
   C:\> telnet 172.16.1.1
   ```

2. Set the enable secret so the privileged password is hashed, not stored in the clear

   ```text
   RTA(config)# enable secret Str0ngEn@ble!
   ```

3. Create a local user with a strong hash rather than a type 7 password

   ```text
   RTA(config)# username netadmin privilege 15 algorithm-type scrypt secret Adm1n!Pass
   ```

4. Encrypt any remaining plaintext passwords in the configuration

   ```text
   RTA(config)# service password-encryption
   ```

5. Enforce a minimum password length

   ```text
   RTA(config)# security passwords min-length 10
   ```

6. Set the domain name, which SSH requires before a key can be generated

   ```text
   RTA(config)# ip domain-name tertiary.local
   ```

7. Generate the RSA key pair — 2048 bits or better

   ```text
   RTA(config)# crypto key generate rsa modulus 2048
   ```

8. Force SSH version 2 only

   ```text
   RTA(config)# ip ssh version 2
   ```

9. Restrict the VTY lines to SSH so Telnet can no longer be used

   ```text
   RTA(config-line)# transport input ssh
   ```

10. Point the VTY lines at the local user database

   ```text
   RTA(config-line)# login local
   ```

11. Set an idle timeout so abandoned sessions close

   ```text
   RTA(config-line)# exec-timeout 5 0
   ```

12. Throttle brute-force attempts by blocking after repeated failures

   ```text
   RTA(config)# login block-for 120 attempts 3 within 60
   ```

13. Add a legal banner warning against unauthorised access

   ```text
   RTA(config)# banner motd #Authorised access only. All activity is logged.#
   ```

14. Verify SSH is enabled at version 2

   ```text
   RTA# show ip ssh
   ```

15. Confirm Telnet is now refused from PCA

   ```text
   C:\> telnet 172.16.1.1
   ```

16. Confirm SSH succeeds with the new credentials

   ```text
   C:\> ssh -l netadmin 172.16.1.1
   ```


## Validation

'show ip ssh' reports SSH Enabled version 2.0, Telnet from PCA is refused, SSH with the netadmin account succeeds, and 'show running-config | include username' shows a strong hash rather than a type 7 password.

## Checkpoint Questions

1. Why is a type 7 password unacceptable?
1. What must be configured before 'crypto key generate rsa' will work?
1. What does 'transport input ssh' do?
1. What does 'login block-for 120 attempts 3 within 60' protect against?

## Exam Focus

'username … secret' hashes; 'password' stores type 7, which is trivially reversible. SSH needs a hostname, a domain name and an RSA key before it will start. 'transport input ssh' is what actually removes Telnet.
