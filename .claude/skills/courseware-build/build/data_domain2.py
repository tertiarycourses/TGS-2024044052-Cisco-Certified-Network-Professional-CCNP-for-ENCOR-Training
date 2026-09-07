"""
Domain 2 — Virtualization Technologies (ENCOR 2.0, 10%).  Labs 6–9.
"""

DOMAIN2 = [
    dict(
        num=6, topic=2,
        title="Configure and Verify VRF-Lite",
        objective="Configure and verify data path virtualization technologies — VRF (ENCOR 2.2.a).",
        desc=(
            "Your organisation must keep guest traffic and corporate traffic completely separate on the same "
            "physical router, and the acquisition it just completed uses the same 192.168.1.0/24 range as head "
            "office. As the network engineer you solve both problems with VRF-Lite: two independent routing "
            "tables on one device, with overlapping address space and no leaking between them."
        ),
        build="A router carrying two VRFs (CORP and GUEST) with overlapping 192.168.1.0/24 prefixes, proven isolated by a VRF-aware ping that succeeds inside a VRF and fails across VRFs.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1 router, CORP-PC and GUEST-PC",
        steps=[
            ("Open lab-06-vrf-lite/lab-06-vrf-lite.pkt and note both PCs use 192.168.1.10 in different VRFs", ""),
            ("Create the CORP VRF on R1", "R1(config)# vrf definition CORP"),
            ("Enable IPv4 address family inside the VRF", "R1(config-vrf)# address-family ipv4"),
            ("Create the GUEST VRF the same way", "R1(config)# vrf definition GUEST"),
            ("Assign G0/0 to the CORP VRF — note this clears any existing IP address", "R1(config-if)# vrf forwarding CORP"),
            ("Now add the address to the CORP interface", "R1(config-if)# ip address 192.168.1.1 255.255.255.0"),
            ("Assign G0/1 to the GUEST VRF and give it the identical address", "R1(config-if)# vrf forwarding GUEST"),
            ("Add the overlapping address to the GUEST interface", "R1(config-if)# ip address 192.168.1.1 255.255.255.0"),
            ("List the VRFs and confirm each owns its interface", "R1# show vrf"),
            ("Display the CORP routing table — it must be separate from the global table", "R1# show ip route vrf CORP"),
            ("Display the GUEST routing table and confirm the same prefix appears independently", "R1# show ip route vrf GUEST"),
            ("Ping inside the CORP VRF — this must succeed", "R1# ping vrf CORP 192.168.1.10"),
            ("Ping the same address without a VRF keyword and observe it consult the empty global table and fail", "R1# ping 192.168.1.10"),
        ],
        test="'show vrf' lists CORP and GUEST with their interfaces, both VRF routing tables carry 192.168.1.0/24 independently, 'ping vrf CORP' succeeds, and the unqualified ping fails — proving isolation rather than a broken configuration.",
    ),
    dict(
        num=7, topic=2,
        title="Configure and Verify a GRE Tunnel",
        objective="Configure and verify data path virtualization technologies — GRE tunneling (ENCOR 2.2.b).",
        desc=(
            "Head office and the branch are connected only across the public internet, but the routing "
            "protocol and multicast traffic they need to exchange cannot cross it. As the WAN engineer you "
            "build a GRE tunnel that carries those private networks over the public path, then demonstrate "
            "the critical limitation the exam always tests: GRE gives you transport, not confidentiality."
        ),
        build="A working GRE tunnel between RA (64.103.211.2) and RB (209.165.122.2) carrying 192.168.1.0/24 and 192.168.2.0/24, verified up/up with traffic passing.",
        services="Cisco Packet Tracer, Cisco IOS CLI, RA and RB routers, PCA and PCB",
        steps=[
            ("Open lab-07-gre/lab-07-gre.pkt and confirm RA and RB can reach each other over their public addresses", "RA# ping 209.165.122.2"),
            ("Create the tunnel interface on RA", "RA(config)# interface Tunnel0"),
            ("Give the tunnel its own private address in the 10.10.10.0/30 transit range", "RA(config-if)# ip address 10.10.10.1 255.255.255.252"),
            ("Set the tunnel source to RA's public interface", "RA(config-if)# tunnel source Serial0/0/0"),
            ("Set the tunnel destination to RB's public address", "RA(config-if)# tunnel destination 209.165.122.2"),
            ("Confirm the mode is GRE over IP, which is the IOS default", "RA(config-if)# tunnel mode gre ip"),
            ("Repeat on RB with the mirrored addresses", "RB(config-if)# ip address 10.10.10.2 255.255.255.252"),
            ("Set RB's tunnel source and destination back towards RA", "RB(config-if)# tunnel destination 64.103.211.2"),
            ("Add a static route on RA sending the remote LAN through the tunnel", "RA(config)# ip route 192.168.2.0 255.255.255.0 10.10.10.2"),
            ("Add the mirrored static route on RB", "RB(config)# ip route 192.168.1.0 255.255.255.0 10.10.10.1"),
            ("Verify the tunnel interface state and its source and destination", "RA# show interfaces Tunnel0"),
            ("Confirm the tunnel is up and carrying the right networks", "RA# show ip interface brief | include Tunnel"),
            ("Ping across the tunnel from PCA to PCB", "C:\\> ping 192.168.2.2"),
            ("Note the GRE overhead of 24 bytes and why tunnel MTU is usually set to 1476", ""),
        ],
        test="'show interfaces Tunnel0' reports Tunnel0 up, line protocol up with the correct source and destination, PCA pings PCB successfully, and you can state that GRE adds no encryption, authentication or integrity.",
    ),
    dict(
        num=8, topic=2,
        title="Configure and Verify a Site-to-Site IPsec VPN",
        objective="Configure and verify data path virtualization technologies — IPsec tunneling (ENCOR 2.2.b).",
        desc=(
            "The GRE tunnel from the previous lab carries payroll data in clear text, and the audit has "
            "flagged it. As the security-minded network engineer you now build a site-to-site IPsec VPN "
            "between R1 and R3 across the R2 ISP, working through both IKE phases and proving the tunnel "
            "only forms once interesting traffic matches on both ends."
        ),
        build="A functioning site-to-site IPsec VPN between R1 (192.168.1.0/24) and R3 (192.168.3.0/24) with a formed ISAKMP SA, established IPsec SAs and encrypted packet counters incrementing.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC-A and PC-C",
        steps=[
            ("Open lab-08-ipsec-vpn/lab-08-ipsec-vpn.pkt and confirm R1 and R3 reach each other through R2", "R1# ping 10.2.2.2"),
            ("Enable the security technology package if the lab image requires it", "R1(config)# license boot module c1900 technology-package securityk9"),
            ("Create the IKE Phase 1 policy defining how the management tunnel is protected", "R1(config)# crypto isakmp policy 10"),
            ("Set AES encryption, SHA hashing, pre-shared key authentication and DH group 5", "R1(config-isakmp)# encryption aes 256"),
            ("Set the pre-shared key and the peer it applies to", "R1(config)# crypto isakmp key Cisco123 address 10.2.2.2"),
            ("Define the Phase 2 transform set that protects the actual data", "R1(config)# crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac"),
            ("Write the interesting-traffic ACL — this must mirror exactly on the far end", "R1(config)# access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255"),
            ("Build the crypto map binding the peer, transform set and ACL together", "R1(config)# crypto map VPN-MAP 10 ipsec-isakmp"),
            ("Set the peer inside the crypto map", "R1(config-crypto-map)# set peer 10.2.2.2"),
            ("Apply the crypto map to the outside interface", "R1(config-if)# crypto map VPN-MAP"),
            ("Repeat the mirrored configuration on R3, reversing the ACL source and destination", "R3(config)# access-list 110 permit ip 192.168.3.0 0.0.0.255 192.168.1.0 0.0.0.255"),
            ("Generate interesting traffic from PC-A to PC-C to bring the tunnel up", "C:\\> ping 192.168.3.3"),
            ("Verify the Phase 1 ISAKMP SA is in QM_IDLE state", "R1# show crypto isakmp sa"),
            ("Verify the Phase 2 IPsec SAs and confirm the encrypt and decrypt counters are climbing", "R1# show crypto ipsec sa"),
        ],
        test="'show crypto isakmp sa' shows the peer in QM_IDLE and 'show crypto ipsec sa' shows non-zero '#pkts encaps' and '#pkts decaps' counters that increase with each ping — traffic between the two LANs is genuinely encrypted.",
    ),
    dict(
        num=9, topic=2,
        title="Explore LISP and VXLAN Network Virtualization",
        objective="Describe network virtualization concepts — LISP and VXLAN (ENCOR 2.3.a, 2.3.b).",
        desc=(
            "Your campus is moving to SD-Access, whose entire mobility story rests on LISP and whose data "
            "plane is VXLAN. As the network engineer you must be able to trace a packet through both. You "
            "walk the LISP map-request and map-reply exchange, follow an endpoint that roams between edge "
            "switches, then decode a VXLAN header field by field and calculate the encapsulation overhead."
        ),
        build="An annotated LISP registration and lookup walkthrough, a completed VXLAN header decode with all field sizes, and a calculated MTU requirement for the underlay.",
        services="Cisco Packet Tracer, packet-decode worksheet, vxlan-header.csv, lisp-mapping.csv",
        steps=[
            ("Open lab-09-lisp-vxlan/ and read the fabric topology showing edge nodes, border node and control plane node", ""),
            ("Identify the EID — the endpoint identifier, the host's own IP address that never changes as it roams", ""),
            ("Identify the RLOC — the routing locator, the address of the edge switch the host is attached to now", ""),
            ("Trace registration: the edge node registers the EID-to-RLOC binding with the map server", ""),
            ("Trace lookup: an ingress tunnel router sends a map-request to the map resolver", ""),
            ("Trace the reply: the map server returns the RLOC, and the ITR caches it in its map cache", ""),
            ("Model a roam — the host moves to a second edge node, which re-registers the same EID to a new RLOC", ""),
            ("State why the host keeps its IP address across the roam, and why that is what makes fabric mobility work", ""),
            ("Move to VXLAN and record the outer headers: outer MAC, outer IP, UDP with destination port 4789", ""),
            ("Record the 8-byte VXLAN header carrying the 24-bit VNI", ""),
            ("Calculate the total overhead — 50 bytes — and state the resulting underlay MTU of at least 1550", ""),
            ("Compare the segment ceiling: 4,094 VLANs against 16,777,216 VNIs", ""),
            ("Complete vxlan-header.csv with each field, its size and its purpose", ""),
        ],
        test="You can state the LISP lookup sequence (register, map-request, map-reply, cache), explain why an EID survives a roam, name UDP 4789 as the VXLAN port, and calculate the 50-byte overhead and the 1550-byte minimum underlay MTU.",
    ),
]
