"""
Domain 5 — Network Security (ENCOR 5.0, 20%).  Labs 26–30.
"""

DOMAIN5 = [
    dict(
        num=26, topic=5,
        title="Configure Secure Device Access with SSH and Strong Passwords",
        objective="Configure and verify device access control — lines and local user authentication (ENCOR 5.1.a).",
        desc=(
            "An audit found the branch routers reachable by Telnet with a type 7 password that anyone can "
            "decode in seconds. As the engineer you harden device access: strong hashed local credentials, "
            "SSH version 2 only, Telnet removed from the VTY lines, an exec timeout, and login blocking so "
            "brute force attempts are throttled."
        ),
        build="A router and switch reachable only by SSHv2 with type 9 hashed local credentials, Telnet disabled, an exec timeout set and login-attempt throttling armed.",
        services="Cisco Packet Tracer, Cisco IOS CLI, RTA router, SW1 switch, PCA",
        steps=[
            ("Open lab-26-secure-access/lab-26-secure-access.pkt and confirm Telnet currently works from PCA", "C:\\> telnet 172.16.1.1"),
            ("Set the enable secret so the privileged password is hashed, not stored in the clear", "RTA(config)# enable secret Str0ngEn@ble!"),
            ("Create a local user with a strong hash rather than a type 7 password", "RTA(config)# username netadmin privilege 15 algorithm-type scrypt secret Adm1n!Pass"),
            ("Encrypt any remaining plaintext passwords in the configuration", "RTA(config)# service password-encryption"),
            ("Enforce a minimum password length", "RTA(config)# security passwords min-length 10"),
            ("Set the domain name, which SSH requires before a key can be generated", "RTA(config)# ip domain-name tertiary.local"),
            ("Generate the RSA key pair — 2048 bits or better", "RTA(config)# crypto key generate rsa modulus 2048"),
            ("Force SSH version 2 only", "RTA(config)# ip ssh version 2"),
            ("Restrict the VTY lines to SSH so Telnet can no longer be used", "RTA(config-line)# transport input ssh"),
            ("Point the VTY lines at the local user database", "RTA(config-line)# login local"),
            ("Set an idle timeout so abandoned sessions close", "RTA(config-line)# exec-timeout 5 0"),
            ("Throttle brute-force attempts by blocking after repeated failures", "RTA(config)# login block-for 120 attempts 3 within 60"),
            ("Add a legal banner warning against unauthorised access", "RTA(config)# banner motd #Authorised access only. All activity is logged.#"),
            ("Verify SSH is enabled at version 2", "RTA# show ip ssh"),
            ("Confirm Telnet is now refused from PCA", "C:\\> telnet 172.16.1.1"),
            ("Confirm SSH succeeds with the new credentials", "C:\\> ssh -l netadmin 172.16.1.1"),
        ],
        test="'show ip ssh' reports SSH Enabled version 2.0, Telnet from PCA is refused, SSH with the netadmin account succeeds, and 'show running-config | include username' shows a strong hash rather than a type 7 password.",
    ),
    dict(
        num=27, topic=5,
        title="Implement Local and Server-Based AAA",
        objective="Configure and verify device access control — authentication and authorization using AAA (ENCOR 5.1.b).",
        desc=(
            "Managing local accounts on 200 devices does not scale, and when an administrator leaves nobody "
            "can be sure every account is gone. As the engineer you centralise authentication on TACACS+ and "
            "RADIUS with AAA — and you deliberately keep a local fallback, because the classic AAA disaster is "
            "locking the whole team out when the server is unreachable."
        ),
        build="Routers authenticating administrators against TACACS+ (192.168.2.2) and RADIUS (192.168.3.2) with a working local fallback, plus authorization and accounting enabled.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, TACACS+ server, RADIUS server",
        steps=[
            ("Open lab-27-aaa/lab-27-aaa.pkt and note the TACACS+ server at 192.168.2.2 and RADIUS at 192.168.3.2", ""),
            ("Create the local fallback account BEFORE you enable AAA — this is what saves you", "R1(config)# username admin privilege 15 secret Adm1n!Pass"),
            ("Enable the AAA subsystem", "R1(config)# aaa new-model"),
            ("Define the TACACS+ server", "R1(config)# tacacs server TAC-SRV"),
            ("Set its address", "R1(config-server-tacacs)# address ipv4 192.168.2.2"),
            ("Set the shared secret, which must match the server exactly", "R1(config-server-tacacs)# key TacacsKey123"),
            ("Set the login authentication method list with the local fallback last", "R1(config)# aaa authentication login default group tacacs+ local"),
            ("Add authorization so the server also decides what the user may run", "R1(config)# aaa authorization exec default group tacacs+ local"),
            ("Add accounting so every command is recorded", "R1(config)# aaa accounting exec default start-stop group tacacs+"),
            ("Now configure RADIUS on R3 for comparison", "R3(config)# radius server RAD-SRV"),
            ("Set the RADIUS address and its authentication and accounting ports", "R3(config-server-radius)# address ipv4 192.168.3.2 auth-port 1645 acct-port 1646"),
            ("Set the RADIUS shared secret", "R3(config-server-radius)# key RadiusKey123"),
            ("Point R3's login authentication at RADIUS with a local fallback", "R3(config)# aaa authentication login default group radius local"),
            ("Test authentication against the server without dropping your session", "R1# test aaa group tacacs+ admin Adm1n!Pass legacy"),
            ("Verify the server is reachable and its statistics", "R1# show tacacs"),
            ("Shut the server link and confirm the local fallback still lets you in", "R1(config-if)# shutdown"),
            ("Record which protocol you would use for device administration and which for network access, and why", ""),
        ],
        test="'test aaa group tacacs+' returns a successful authentication, 'show tacacs' shows the server reachable, and with the server link shut you can still log in with the local admin account — proving the fallback works.",
    ),
    dict(
        num=28, topic=5,
        title="Configure Extended ACLs to Mitigate Attacks",
        objective="Configure and verify infrastructure security features — ACLs (ENCOR 5.2.a).",
        desc=(
            "The security team wants the branch to permit only what the business needs and to block the "
            "traffic patterns behind the last incident: spoofed private source addresses arriving from the "
            "internet and unsolicited inbound ICMP. As the engineer you write named extended ACLs, place them "
            "correctly, and confirm the implicit deny is not silently dropping something you needed."
        ),
        build="Named extended ACLs permitting only required services, blocking spoofed RFC 1918 sources inbound and unsolicited ICMP, applied in the correct direction with verified hit counters.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC-A, PC-C, servers",
        steps=[
            ("Open lab-28-acls/lab-28-acls.pkt and confirm PC1 can currently reach every service on the server", "C:\\> ping 172.22.34.62"),
            ("Create a named extended ACL for the inbound internet edge", "R1(config)# ip access-list extended INTERNET-IN"),
            ("Block spoofed RFC 1918 sources arriving from outside", "R1(config-ext-nacl)# deny ip 10.0.0.0 0.255.255.255 any"),
            ("Block the 172.16.0.0/12 private range as a spoofed source", "R1(config-ext-nacl)# deny ip 172.16.0.0 0.15.255.255 any"),
            ("Block the 192.168.0.0/16 private range as a spoofed source", "R1(config-ext-nacl)# deny ip 192.168.0.0 0.0.255.255 any"),
            ("Permit only the web traffic the business needs to the server", "R1(config-ext-nacl)# permit tcp any host 172.22.34.62 eq 80"),
            ("Permit HTTPS to the same server", "R1(config-ext-nacl)# permit tcp any host 172.22.34.62 eq 443"),
            ("Permit return traffic for sessions your users established", "R1(config-ext-nacl)# permit tcp any any established"),
            ("Block unsolicited inbound ICMP echo but allow the replies your pings need", "R1(config-ext-nacl)# deny icmp any any echo"),
            ("Add an explicit deny with logging so you can see what the implicit deny would have dropped", "R1(config-ext-nacl)# deny ip any any log"),
            ("Apply the ACL inbound on the outside interface — extended ACLs go close to the source", "R1(config-if)# ip access-group INTERNET-IN in"),
            ("Verify the ACL contents and the order of the entries", "R1# show access-lists INTERNET-IN"),
            ("Generate test traffic and watch the match counters increment on the right lines", "R1# show access-lists INTERNET-IN | include matches"),
            ("Check the log for what the final deny caught", "R1# show logging | include list INTERNET-IN"),
            ("Test that permitted web traffic still works after the ACL is applied", "C:\\> ping 172.22.34.62"),
        ],
        test="'show access-lists INTERNET-IN' shows the entries in the intended order with match counters incrementing on the permit lines, spoofed private-source traffic is denied, permitted HTTP/HTTPS still reaches the server, and the logged deny shows what the implicit deny would have dropped.",
    ),
    dict(
        num=29, topic=5,
        title="Configure Control Plane Policing",
        objective="Configure and verify infrastructure security features — CoPP (ENCOR 5.2.b).",
        desc=(
            "During the last incident a flood of ICMP and SNMP drove the router CPU to 99% and OSPF "
            "adjacencies dropped — the device stopped routing because it was too busy answering management "
            "traffic. As the engineer you build a CoPP policy that rate-limits management and ICMP traffic to "
            "the control plane while guaranteeing routing protocol traffic always gets through."
        ),
        build="A CoPP policy applied to the control plane with separate classes for routing, management and ICMP, each policed at an appropriate rate, with verified conform and exceed counters.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2 routers",
        steps=[
            ("Open lab-29-copp/lab-29-copp.pkt and baseline the CPU utilisation", "R1# show processes cpu sorted | include CPU"),
            ("Create an ACL matching routing protocol traffic that must never be dropped", "R1(config)# access-list 120 permit ospf any any"),
            ("Add EIGRP and BGP to the same critical ACL", "R1(config)# access-list 120 permit tcp any any eq 179"),
            ("Create an ACL matching management traffic", "R1(config)# access-list 121 permit tcp any any eq 22"),
            ("Add SNMP to the management ACL", "R1(config)# access-list 121 permit udp any any eq 161"),
            ("Create an ACL matching ICMP, the usual flood vector", "R1(config)# access-list 122 permit icmp any any"),
            ("Define the class map for critical routing traffic", "R1(config)# class-map match-all COPP-CRITICAL"),
            ("Match the routing ACL inside the class map", "R1(config-cmap)# match access-group 120"),
            ("Define the management class map the same way", "R1(config)# class-map match-all COPP-MANAGEMENT"),
            ("Define the ICMP class map", "R1(config)# class-map match-all COPP-ICMP"),
            ("Build the policy map that will govern the control plane", "R1(config)# policy-map COPP-POLICY"),
            ("Give routing traffic a generous rate so it is never starved", "R1(config-pmap-c)# police 512000 conform-action transmit exceed-action transmit"),
            ("Rate-limit management traffic and drop the excess", "R1(config-pmap-c)# police 256000 conform-action transmit exceed-action drop"),
            ("Rate-limit ICMP hard, since this is the flood vector", "R1(config-pmap-c)# police 64000 conform-action transmit exceed-action drop"),
            ("Enter control-plane configuration mode", "R1(config)# control-plane"),
            ("Apply the policy to the control plane in the input direction", "R1(config-cp)# service-policy input COPP-POLICY"),
            ("Generate an ICMP flood and verify the exceed counters climb while OSPF stays up", "R2# ping 10.1.1.1 repeat 1000 size 1500"),
            ("Read the policy counters for conformed and exceeded traffic", "R1# show policy-map control-plane"),
        ],
        test="'show policy-map control-plane' shows the three classes with conformed bytes on all of them and exceeded/dropped bytes on the ICMP class during the flood, while 'show ip ospf neighbor' confirms the adjacency never dropped.",
    ),
    dict(
        num=30, topic=5,
        title="Analyse Wireless Security, REST API Security and Security Design",
        objective="Describe REST API security, configure wireless security features, and describe the components of network security design (ENCOR 5.3, 5.4, 5.5).",
        desc=(
            "You are reviewing three security designs before sign-off: the wireless authentication model for a "
            "new floor, the API integration a vendor has proposed, and the overall segmentation design. As the "
            "engineer you evaluate each against the exam's criteria — walking the 802.1X and 4-way handshake "
            "exchanges, finding the flaws in the vendor's API design, and placing each defence layer."
        ),
        build="A completed wireless authentication comparison, an annotated 4-way handshake walkthrough, a REST API security review naming every flaw in the vendor proposal, and a layered security design map.",
        services="Cisco Packet Tracer, WLC GUI, Postman or curl, security review worksheets",
        steps=[
            ("Open lab-30-security-design/ and read the three review packs provided", ""),
            ("Compare the wireless authentication methods in wireless-security.csv — PSK, 802.1X, WebAuth and MAB", ""),
            ("Identify the three 802.1X roles: supplicant, authenticator and authentication server", ""),
            ("Note that EAPOL carries EAP between supplicant and authenticator, and RADIUS carries it onward", ""),
            ("Walk the 4-way handshake: the AP sends ANonce, the client replies with SNonce and a MIC", ""),
            ("Continue the handshake: the AP sends the GTK, and the client acknowledges", ""),
            ("State what the handshake proves — both sides hold the PMK, without ever transmitting it", ""),
            ("Recommend an authentication method for each of the four use cases in the worksheet", ""),
            ("Move to the vendor's API proposal and check whether it uses HTTP or HTTPS", ""),
            ("Check how it authenticates — look for embedded credentials rather than a token", ""),
            ("Check whether the token is scoped, whether it expires, and where the vendor stores it", ""),
            ("Check for rate limiting and input validation on the exposed endpoints", ""),
            ("List every flaw you found with the fix in api-security-review.csv", ""),
            ("Now map the security design layers: threat defence, endpoint security and next-generation firewall", ""),
            ("Place segmentation in the map — TrustSec SGTs for policy and MACsec for link encryption", ""),
            ("Place network access control with 802.1X, MAB and WebAuth at the access edge", ""),
            ("Complete security-design-map.csv naming each layer, its control and what it defends against", ""),
        ],
        test="Your wireless comparison recommends 802.1X for corporate, PSK or WebAuth for guest and MAB with profiling for headless devices; your 4-way handshake walkthrough has all four messages in order; and api-security-review.csv names the HTTP transport, the embedded credentials and the absent rate limiting as flaws with concrete fixes.",
    ),
]
