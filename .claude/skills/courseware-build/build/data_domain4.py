"""
Domain 4 — Network Assurance (ENCOR 4.0, 10%).  Labs 22–25.
"""

DOMAIN4 = [
    dict(
        num=22, topic=4,
        title="Diagnose Network Problems with Ping, Traceroute and Conditional Debug",
        objective="Diagnose network problems using tools such as debugs, conditional debugs, traceroute, ping, SNMP and syslog (ENCOR 4.1).",
        desc=(
            "A user reports the application server is 'sometimes slow and sometimes down'. As the engineer "
            "you work the problem methodically from the bottom of the stack up: extended ping from the right "
            "source with the right size, traceroute to locate where the path breaks, then a conditional debug "
            "scoped to one host so you can safely watch the control plane on a production router."
        ),
        build="A completed diagnostic record locating the failure to a specific hop, with an extended ping result set, a traceroute trace and safely-scoped conditional debug output.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC-A",
        steps=[
            ("Open lab-22-diagnostics/lab-22-diagnostics.pkt and confirm the reported symptom from PC-A", "C:\\> ping 192.168.3.3"),
            ("Run a basic ping from the router to establish reachability", "R1# ping 192.168.3.3"),
            ("Run an extended ping sourced from the LAN interface — the source is what usually matters", "R1# ping 192.168.3.3 source GigabitEthernet0/1"),
            ("Test with a large packet and the do-not-fragment bit to expose an MTU problem", "R1# ping 192.168.3.3 size 1500 df-bit"),
            ("Sweep a range of packet sizes to find exactly where it breaks", "R1# ping 192.168.3.3 size 1400 repeat 5"),
            ("Trace the path to identify the last responding hop", "R1# traceroute 192.168.3.3"),
            ("Read the asterisks in the traceroute output and interpret what they mean", ""),
            ("Check whether the route even exists before blaming the far end", "R1# show ip route 192.168.3.0"),
            ("Verify the interface counters for errors and drops", "R1# show interfaces Serial0/0/0 | include error|drop"),
            ("Set up a conditional debug so you only see traffic for the one affected host", "R1# debug platform condition ipv4 192.168.3.3/32 both"),
            ("Start the condition so the filter takes effect", "R1# debug platform condition start"),
            ("Enable the ICMP debug now that it is safely scoped", "R1# debug ip icmp"),
            ("Reproduce the problem and read the scoped output", "C:\\> ping 192.168.3.3"),
            ("Turn every debug off — never leave a debug running", "R1# undebug all"),
            ("Record the failing hop and the root cause in diagnostic-log.csv", ""),
        ],
        test="Your diagnostic record names the exact hop where the path fails, the sweep identifies the largest packet size that succeeds, and 'undebug all' confirms no debug is left running on the device.",
    ),
    dict(
        num=23, topic=4,
        title="Configure Syslog, SNMP and Flexible NetFlow",
        objective="Configure and verify Flexible NetFlow, and use SNMP and syslog for diagnosis (ENCOR 4.1, 4.2).",
        desc=(
            "The network has no visibility: when something breaks, nobody can say what changed or who was "
            "using the bandwidth. As the engineer you fix that in three layers — syslog to a central "
            "collector with accurate timestamps, SNMPv3 for polled state, and Flexible NetFlow to answer who "
            "talked to whom, how much and for how long."
        ),
        build="A router logging to a syslog collector at severity informational, an SNMPv3 user with authentication and encryption, and a Flexible NetFlow monitor applied to an interface producing a populated flow cache.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2 routers, syslog server, SNMP server",
        steps=[
            ("Open lab-23-netflow-syslog/lab-23-netflow-syslog.pkt and locate the syslog and SNMP servers", ""),
            ("Ensure the clock is right first — logs without accurate time are almost useless", "R1(config)# ntp server 209.165.200.226"),
            ("Turn on millisecond timestamps for both logs and debugs", "R1(config)# service timestamps log datetime msec"),
            ("Point syslog at the collector", "R1(config)# logging host 192.168.1.100"),
            ("Set the trap severity so you capture informational and above", "R1(config)# logging trap informational"),
            ("Set a consistent source interface so the collector sees one address per device", "R1(config)# logging source-interface GigabitEthernet0/0"),
            ("Verify the logging configuration and the message counts", "R1# show logging"),
            ("Now configure SNMPv3 — create the group with authentication and privacy required", "R1(config)# snmp-server group NETOPS v3 priv"),
            ("Create the user with SHA authentication and AES encryption", "R1(config)# snmp-server user monitor NETOPS v3 auth sha Auth123! priv aes 128 Priv123!"),
            ("Verify the SNMP user and group", "R1# show snmp user"),
            ("Start Flexible NetFlow by defining the flow record — the key and non-key fields", "R1(config)# flow record NETFLOW-RECORD"),
            ("Match the source address as a key field", "R1(config-flow-record)# match ipv4 source address"),
            ("Match the destination address as a key field", "R1(config-flow-record)# match ipv4 destination address"),
            ("Collect the byte and packet counters as non-key fields", "R1(config-flow-record)# collect counter bytes"),
            ("Define the exporter that sends the flows to the collector", "R1(config)# flow exporter NETFLOW-EXPORT"),
            ("Set the exporter destination and UDP port", "R1(config-flow-exporter)# destination 192.168.1.100"),
            ("Bind the record and exporter into a flow monitor", "R1(config)# flow monitor NETFLOW-MONITOR"),
            ("Apply the monitor to the interface in the input direction", "R1(config-if)# ip flow monitor NETFLOW-MONITOR input"),
            ("Generate traffic, then read the flow cache", "R1# show flow monitor NETFLOW-MONITOR cache"),
        ],
        test="'show logging' confirms messages are being sent to 192.168.1.100 at informational severity, 'show snmp user' lists the v3 user with SHA and AES, and 'show flow monitor NETFLOW-MONITOR cache' displays flow entries with source, destination and byte counts.",
    ),
    dict(
        num=24, topic=4,
        title="Configure SPAN, RSPAN and IP SLA",
        objective="Configure SPAN/RSPAN/ERSPAN and configure and verify IPSLA (ENCOR 4.3, 4.4).",
        desc=(
            "Security has asked for a packet capture of one server's traffic, and the WAN team wants to know "
            "when a path degrades before users complain. As the engineer you deliver both: SPAN to mirror the "
            "server port to an analyser, RSPAN to carry a copy to an analyser on another switch, and an IP SLA "
            "probe with a tracked object that withdraws a static route when the path fails."
        ),
        build="A working local SPAN session mirroring the server port, an RSPAN session across a dedicated VLAN, and an IP SLA ICMP echo operation with a tracked object driving a static route.",
        services="Cisco Packet Tracer, Cisco IOS CLI, S1/S2 switches, R1/R2 routers, analyser PC",
        steps=[
            ("Open lab-24-span-ipsla/lab-24-span-ipsla.pkt and identify the server port and the analyser port", ""),
            ("Create a local SPAN session with the server port as the source", "S1(config)# monitor session 1 source interface FastEthernet0/1 both"),
            ("Set the analyser port as the destination", "S1(config)# monitor session 1 destination interface FastEthernet0/24"),
            ("Verify the SPAN session is active and note the source and destination", "S1# show monitor session 1"),
            ("Now build RSPAN — first create the dedicated RSPAN VLAN", "S1(config)# vlan 199"),
            ("Flag the VLAN as an RSPAN VLAN", "S1(config-vlan)# remote-span"),
            ("On the source switch, send the mirrored traffic into the RSPAN VLAN", "S1(config)# monitor session 2 destination remote vlan 199"),
            ("On the destination switch, take the RSPAN VLAN as the source", "S2(config)# monitor session 2 source remote vlan 199"),
            ("Send it to the local analyser port on that switch", "S2(config)# monitor session 2 destination interface FastEthernet0/24"),
            ("Verify the RSPAN session on both switches", "S2# show monitor session 2"),
            ("Move to IP SLA and create an ICMP echo operation to the remote path", "R1(config)# ip sla 1"),
            ("Define the echo target and the source interface", "R1(config-ip-sla)# icmp-echo 209.165.200.226 source-interface Serial0/0/0"),
            ("Set the probe frequency in seconds", "R1(config-ip-sla-echo)# frequency 10"),
            ("Schedule the operation to run now and run forever", "R1(config)# ip sla schedule 1 life forever start-time now"),
            ("Create a tracked object that follows the SLA's reachability", "R1(config)# track 1 ip sla 1 reachability"),
            ("Attach the tracked object to a static route so it withdraws on failure", "R1(config)# ip route 0.0.0.0 0.0.0.0 209.165.200.226 track 1"),
            ("Verify the SLA statistics and the round-trip time", "R1# show ip sla statistics"),
            ("Verify the tracked object is Up and the route is in the table", "R1# show track 1"),
        ],
        test="'show monitor session 1' shows an active local SPAN, the RSPAN session appears on both switches using VLAN 199, 'show ip sla statistics' reports successful probes with an RTT, and 'show track 1' reports the object Up with the default route present.",
    ),
    dict(
        num=25, topic=4,
        title="Configure NETCONF and RESTCONF and Explore DNA Center Workflows",
        objective="Configure and verify NETCONF and RESTCONF, and describe Cisco DNA Center workflows (ENCOR 4.5, 4.6).",
        desc=(
            "Your team is moving from CLI-by-hand to programmatic configuration. As the automation engineer "
            "you enable NETCONF and RESTCONF on the router, retrieve configuration through each, and compare "
            "them honestly: NETCONF's transactional datastores against RESTCONF's simpler REST verbs. You then "
            "map the four DNA Center workflows onto the tasks your team does manually today."
        ),
        build="A router with NETCONF-YANG on port 830 and RESTCONF on 443 both enabled and verified, a retrieved interface configuration through each protocol, and a completed DNA Center workflow mapping.",
        services="Cisco Packet Tracer, Cisco IOS XE CLI, Python 3, curl or Postman",
        steps=[
            ("Open lab-25-netconf-restconf/ and confirm the router has an IP-reachable management interface", ""),
            ("Create the privileged user the API will authenticate as", "R1(config)# username apiuser privilege 15 secret Api123!"),
            ("Generate the RSA key pair that SSH and HTTPS both require", "R1(config)# crypto key generate rsa modulus 2048"),
            ("Enable NETCONF-YANG", "R1(config)# netconf-yang"),
            ("Enable the HTTPS server that RESTCONF runs on", "R1(config)# ip http secure-server"),
            ("Enable RESTCONF", "R1(config)# restconf"),
            ("Point HTTP authentication at the local user database", "R1(config)# ip http authentication local"),
            ("Verify NETCONF-YANG is running and listening on port 830", "R1# show netconf-yang sessions"),
            ("Confirm the SSH subsystem for netconf is available", "R1# show platform software yang-management process"),
            ("Retrieve the interface configuration over RESTCONF with curl", "curl -k -u apiuser:Api123! https://192.168.1.1/restconf/data/ietf-interfaces:interfaces -H 'Accept: application/yang-data+json'"),
            ("Read the JSON response and locate the interface name and IP address", ""),
            ("Run the provided Python script that does the same over NETCONF with ncclient", "python3 netconf_get_config.py"),
            ("Compare the XML NETCONF returns with the JSON RESTCONF returned", ""),
            ("Note the key difference: NETCONF has candidate/running datastores and transactional commit", ""),
            ("Map DNA Center's Design workflow onto how you record site settings today", ""),
            ("Map Policy, Provision and Assurance the same way and complete dnac-workflows.csv", ""),
        ],
        test="'show netconf-yang sessions' confirms the service is running, the curl call returns HTTP 200 with a JSON interface list, the Python NETCONF script returns the equivalent XML, and dnac-workflows.csv maps all four DNA Center workflows to real tasks.",
    ),
]
