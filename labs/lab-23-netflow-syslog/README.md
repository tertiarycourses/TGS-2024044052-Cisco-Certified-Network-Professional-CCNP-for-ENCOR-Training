# Lab 23 — Configure Syslog, SNMP and Flexible NetFlow

**Topic 04: Network Assurance** · 10% of the exam · Skills Framework K5, A4 (ICT-DIT-3009-1.1)

## Exam Objective

Configure and verify Flexible NetFlow, and use SNMP and syslog for diagnosis (ENCOR 4.1, 4.2).

## Scenario

The network has no visibility: when something breaks, nobody can say what changed or who was using the bandwidth. As the engineer you fix that in three layers — syslog to a central collector with accurate timestamps, SNMPv3 for polled state, and Flexible NetFlow to answer who talked to whom, how much and for how long.

## What You'll Build

A router logging to a syslog collector at severity informational, an SNMPv3 user with authentication and encryption, and a Flexible NetFlow monitor applied to an interface producing a populated flow cache.

## Tools and Devices

Cisco Packet Tracer, Cisco IOS CLI, R1/R2 routers, syslog server, SNMP server.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-23-netflow-syslog.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `netflow-cache-sample.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Interface | IP Address | Subnet Mask | Role | Notes |
| --- | --- | --- | --- | --- | --- |
| R1 | G0/0 | 192.168.1.1 | 255.255.255.0 | Monitored device | NetFlow monitor applied inbound |
| R1 | S0/0/0 | 10.1.1.1 | 255.255.255.252 | Monitored device | WAN link |
| R2 | S0/0/0 | 10.1.1.2 | 255.255.255.252 | Monitored device | Second device |
| Syslog Server | NIC | 192.168.1.100 | 255.255.255.0 | Collector | Syslog and NetFlow collector |
| SNMP Server | NIC | 192.168.1.101 | 255.255.255.0 | Collector | SNMPv3 poller |
| NTP Source | NIC | 209.165.200.226 | 255.255.255.0 | Time source | Stratum 3 master |

## Steps

1. Open lab-23-netflow-syslog/lab-23-netflow-syslog.pkt and locate the syslog and SNMP servers
2. Ensure the clock is right first — logs without accurate time are almost useless

   ```text
   R1(config)# ntp server 209.165.200.226
   ```

3. Turn on millisecond timestamps for both logs and debugs

   ```text
   R1(config)# service timestamps log datetime msec
   ```

4. Point syslog at the collector

   ```text
   R1(config)# logging host 192.168.1.100
   ```

5. Set the trap severity so you capture informational and above

   ```text
   R1(config)# logging trap informational
   ```

6. Set a consistent source interface so the collector sees one address per device

   ```text
   R1(config)# logging source-interface GigabitEthernet0/0
   ```

7. Verify the logging configuration and the message counts

   ```text
   R1# show logging
   ```

8. Now configure SNMPv3 — create the group with authentication and privacy required

   ```text
   R1(config)# snmp-server group NETOPS v3 priv
   ```

9. Create the user with SHA authentication and AES encryption

   ```text
   R1(config)# snmp-server user monitor NETOPS v3 auth sha Auth123! priv aes 128 Priv123!
   ```

10. Verify the SNMP user and group

   ```text
   R1# show snmp user
   ```

11. Start Flexible NetFlow by defining the flow record — the key and non-key fields

   ```text
   R1(config)# flow record NETFLOW-RECORD
   ```

12. Match the source address as a key field

   ```text
   R1(config-flow-record)# match ipv4 source address
   ```

13. Match the destination address as a key field

   ```text
   R1(config-flow-record)# match ipv4 destination address
   ```

14. Collect the byte and packet counters as non-key fields

   ```text
   R1(config-flow-record)# collect counter bytes
   ```

15. Define the exporter that sends the flows to the collector

   ```text
   R1(config)# flow exporter NETFLOW-EXPORT
   ```

16. Set the exporter destination and UDP port

   ```text
   R1(config-flow-exporter)# destination 192.168.1.100
   ```

17. Bind the record and exporter into a flow monitor

   ```text
   R1(config)# flow monitor NETFLOW-MONITOR
   ```

18. Apply the monitor to the interface in the input direction

   ```text
   R1(config-if)# ip flow monitor NETFLOW-MONITOR input
   ```

19. Generate traffic, then read the flow cache

   ```text
   R1# show flow monitor NETFLOW-MONITOR cache
   ```


## Validation

'show logging' confirms messages are being sent to 192.168.1.100 at informational severity, 'show snmp user' lists the v3 user with SHA and AES, and 'show flow monitor NETFLOW-MONITOR cache' displays flow entries with source, destination and byte counts.

## Checkpoint Questions

1. What are the three components of a Flexible NetFlow configuration?
1. What is the difference between a key field and a non-key field?
1. Why is SNMPv3 required in production rather than v2c?
1. What syslog severity level is 'informational', and what does trap level mean?

## Exam Focus

Flexible NetFlow has exactly three parts: record (key/non-key fields), exporter (where to send), monitor (binds them, applied to an interface). Miss any one and you get no flows.
