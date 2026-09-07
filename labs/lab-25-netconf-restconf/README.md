# Lab 25 — Configure NETCONF and RESTCONF and Explore DNA Center Workflows

**Topic 04: Network Assurance** · 10% of the exam · Skills Framework K5, A4 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify NETCONF and RESTCONF, and describe Cisco DNA Center workflows (ENCOR 4.5, 4.6).

## Scenario

Your team is moving from CLI-by-hand to programmatic configuration. As the automation engineer you enable NETCONF and RESTCONF on the router, retrieve configuration through each, and compare them honestly: NETCONF's transactional datastores against RESTCONF's simpler REST verbs. You then map the four DNA Center workflows onto the tasks your team does manually today.

## What You'll Build

A router with NETCONF-YANG on port 830 and RESTCONF on 443 both enabled and verified, a retrieved interface configuration through each protocol, and a completed DNA Center workflow mapping.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS XE CLI, Python 3, curl or Postman.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-25-netconf-restconf.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `dnac-workflows.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Protocol | Port | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | 192.168.1.1 | NETCONF | 830 | netconf-yang over SSH |
| R1 | G0/0 | 192.168.1.1 | RESTCONF | 443 | HTTPS REST, JSON or XML |
| R1 | G0/0 | 192.168.1.1 | SSH | 22 | CLI management |
| Admin PC | NIC | 192.168.1.50 | Client | N/A | Runs curl, Postman and the Python scripts |
| DNAC (sandbox) | N/A | sandboxdnac.cisco.com | HTTPS | 443 | Cisco DevNet always-on sandbox |

## Steps

1. Open lab-25-netconf-restconf/ and confirm the router has an IP-reachable management interface
2. Create the privileged user the API will authenticate as

   ```text
   R1(config)# username apiuser privilege 15 secret Api123!
   ```

3. Generate the RSA key pair that SSH and HTTPS both require

   ```text
   R1(config)# crypto key generate rsa modulus 2048
   ```

4. Enable NETCONF-YANG

   ```text
   R1(config)# netconf-yang
   ```

5. Enable the HTTPS server that RESTCONF runs on

   ```text
   R1(config)# ip http secure-server
   ```

6. Enable RESTCONF

   ```text
   R1(config)# restconf
   ```

7. Point HTTP authentication at the local user database

   ```text
   R1(config)# ip http authentication local
   ```

8. Verify NETCONF-YANG is running and listening on port 830

   ```text
   R1# show netconf-yang sessions
   ```

9. Confirm the SSH subsystem for netconf is available

   ```text
   R1# show platform software yang-management process
   ```

10. Retrieve the interface configuration over RESTCONF with curl

   ```text
   curl -k -u apiuser:Api123! https://192.168.1.1/restconf/data/ietf-interfaces:interfaces -H 'Accept: application/yang-data+json'
   ```

11. Read the JSON response and locate the interface name and IP address
12. Run the provided Python script that does the same over NETCONF with ncclient

   ```text
   python3 netconf_get_config.py
   ```

13. Compare the XML NETCONF returns with the JSON RESTCONF returned
14. Note the key difference: NETCONF has candidate/running datastores and transactional commit
15. Map DNA Center's Design workflow onto how you record site settings today
16. Map Policy, Provision and Assurance the same way and complete dnac-workflows.csv

## Validation

'show netconf-yang sessions' confirms the service is running, the curl call returns HTTP 200 with a JSON interface list, the Python NETCONF script returns the equivalent XML, and dnac-workflows.csv maps all four DNA Center workflows to real tasks.

## Checkpoint Questions

1. Which port does NETCONF use, and which does RESTCONF use?
1. What does NETCONF offer that RESTCONF does not?
1. What must be generated before either protocol will run?
1. Name the four Cisco DNA Center workflows.

## Exam Focus

NETCONF is XML over SSH 830 with candidate/running datastores and transactional commit. RESTCONF is JSON or XML over HTTPS 443 with REST verbs but no transaction. Both are driven by the same YANG models.
