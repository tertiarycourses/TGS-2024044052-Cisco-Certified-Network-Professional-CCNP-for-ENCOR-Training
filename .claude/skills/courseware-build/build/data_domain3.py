"""
Domain 3 — Network Infrastructure (ENCOR 3.0, 30%).  Labs 10–21.

The largest exam domain, so it carries the largest share of the hands-on time:
Layer 2 (trunking, EtherChannel, STP), Layer 3 (EIGRP, OSPF, eBGP, PBR),
wireless (WLC, roaming, troubleshooting) and IP services (NTP, NAT, FHRP, multicast).
"""

DOMAIN3 = [
    dict(
        num=10, topic=3,
        title="Troubleshoot 802.1Q Trunking and DTP",
        objective="Troubleshoot static and dynamic 802.1q trunking protocols (ENCOR 3.1.a).",
        desc=(
            "Users in VLAN 20 on the second floor have lost access to their file server while VLAN 10 users "
            "are unaffected. As the support engineer you work the trunk between S1 and S2: you verify the "
            "trunk formed at all, check the allowed VLAN list that is silently pruning VLAN 20, and resolve "
            "a native VLAN mismatch that CDP is already warning you about in the logs."
        ),
        build="A repaired 802.1Q trunk carrying VLANs 10, 20 and 99 with a matching native VLAN on both ends, and DTP disabled in favour of a hard-set trunk.",
        services="Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches, PC0–PC5",
        steps=[
            ("Open lab-10-trunking-dtp/lab-10-trunking-dtp.pkt and confirm PC1 (VLAN 20) cannot reach the server", "C:\\> ping 192.168.20.1"),
            ("Check whether the link between S1 and S2 formed a trunk at all", "S1# show interfaces trunk"),
            ("Look at the switchport detail — note the administrative and operational mode differ", "S1# show interfaces GigabitEthernet0/1 switchport"),
            ("Read the DTP negotiation state; two 'dynamic auto' ends never form a trunk", "S1# show dtp interface GigabitEthernet0/1"),
            ("Hard-set the trunk on S1 rather than relying on negotiation", "S1(config-if)# switchport mode trunk"),
            ("Do the same on S2 so neither end depends on DTP", "S2(config-if)# switchport mode trunk"),
            ("Disable DTP negotiation entirely on both ends", "S1(config-if)# switchport nonegotiate"),
            ("Re-check the trunk and read the allowed VLAN list — VLAN 20 is missing", "S1# show interfaces trunk"),
            ("Add VLAN 20 back to the allowed list without wiping the others", "S1(config-if)# switchport trunk allowed vlan add 20"),
            ("Check the console log for the CDP native VLAN mismatch warning", "S1# show logging | include NATIVE_VLAN_MISMATCH"),
            ("Compare the native VLAN on each end", "S1# show interfaces trunk | include Native"),
            ("Set the native VLAN to 99 on both ends so they match", "S1(config-if)# switchport trunk native vlan 99"),
            ("Verify the trunk now carries all three VLANs with a matching native VLAN", "S1# show interfaces trunk"),
            ("Confirm the VLAN 20 user can reach the server again", "C:\\> ping 192.168.20.1"),
        ],
        test="'show interfaces trunk' reports mode 'on' with VLANs 10, 20 and 99 allowed and native VLAN 99 on both switches, the mismatch log stops, and the VLAN 20 PC pings its server.",
    ),
    dict(
        num=11, topic=3,
        title="Troubleshoot Static and Dynamic EtherChannels",
        objective="Troubleshoot static and dynamic EtherChannels — PAgP and LACP (ENCOR 3.1.b).",
        desc=(
            "Three EtherChannel bundles were configured across the distribution layer over the weekend and "
            "only one came up. As the engineer on duty you diagnose each: one has both ends passive so LACP "
            "never initiates, one has a speed and duplex mismatch that suspends a member port, and one mixes "
            "PAgP on one end with LACP on the other — a combination that can never negotiate."
        ),
        build="Three working EtherChannel bundles — Po1 with PAgP, Po2 with LACP and Po3 negotiated LACP — all showing SU (in use) with every member port bundled.",
        services="Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches",
        steps=[
            ("Open lab-11-etherchannel/lab-11-etherchannel.pkt and check the state of all three port channels", "S1# show etherchannel summary"),
            ("Read the flags column — SU means in use, SD means down, and (s) means suspended", ""),
            ("Investigate Po2 where both ends were left passive", "S1# show etherchannel 2 port-channel"),
            ("Set S1's end of Po2 to LACP active so one side initiates", "S1(config-if-range)# channel-group 2 mode active"),
            ("Confirm the S2 end stays passive — active-to-passive is a valid LACP pairing", "S2# show etherchannel summary"),
            ("Investigate the suspended member port on Po1", "S1# show interfaces FastEthernet0/22 | include duplex"),
            ("Compare the two member ports and find the speed and duplex mismatch", "S1# show interfaces status | include Fa0/21|Fa0/22"),
            ("Correct the mismatched port so both members match", "S1(config-if)# duplex full"),
            ("Set the matching speed on the same port", "S1(config-if)# speed 100"),
            ("Investigate Po3, which mixes protocols across the two ends", "S3# show etherchannel 3 detail | include protocol"),
            ("Remove the PAgP configuration from the mismatched end", "S3(config-if-range)# no channel-group 3 mode desirable"),
            ("Re-apply the same protocol both ends use — LACP active", "S3(config-if-range)# channel-group 3 mode active"),
            ("Verify all three bundles are now SU with every member bundled", "S1# show etherchannel summary"),
            ("Confirm the load-balancing method the switch is using", "S1# show etherchannel load-balance"),
        ],
        test="'show etherchannel summary' shows Po1, Po2 and Po3 all with flags (SU) and every member port marked (P) for bundled — no (s) suspended and no (D) down ports remain.",
    ),
    dict(
        num=12, topic=3,
        title="Configure RSTP and Tune the Spanning Tree",
        objective="Configure and verify common Spanning Tree Protocols — RSTP — and Spanning Tree enhancements (ENCOR 3.1.c).",
        desc=(
            "The spanning tree in the distribution block elected an access switch as root, so traffic between "
            "two distribution switches is taking a suboptimal path through the wiring closet. As the engineer "
            "you deterministically move the root where it belongs, tune the port costs, migrate the network "
            "from legacy PVST+ to Rapid PVST+, and measure the convergence improvement."
        ),
        build="A spanning tree with S1 as the deterministic root bridge and S2 as the secondary, running Rapid PVST+, with a measured convergence time on link failure.",
        services="Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches, PC-A",
        steps=[
            ("Open lab-12-rstp/lab-12-rstp.pkt and identify which switch is currently root for VLAN 1", "S1# show spanning-tree vlan 1"),
            ("Note the root bridge ID and compare it with each switch's own bridge ID", "S1# show spanning-tree vlan 1 | include Root ID|Bridge ID"),
            ("Record which ports are root, designated and blocking across the three switches", "S1# show spanning-tree vlan 1 | include Desg|Root|Altn"),
            ("Make S1 the primary root using the macro, which sets a priority below the current root", "S1(config)# spanning-tree vlan 1 root primary"),
            ("Make S2 the secondary root so failover is also deterministic", "S2(config)# spanning-tree vlan 1 root secondary"),
            ("Verify S1 now reports 'This bridge is the root'", "S1# show spanning-tree vlan 1"),
            ("Set an exact priority instead of the macro to see the increments of 4096", "S1(config)# spanning-tree vlan 1 priority 4096"),
            ("Examine the port cost on the root port before you change it", "S3# show spanning-tree vlan 1 interface FastEthernet0/1 cost"),
            ("Manipulate the path by raising the cost on one link so the other becomes preferred", "S3(config-if)# spanning-tree cost 100"),
            ("Confirm the root port moved to the lower-cost path", "S3# show spanning-tree vlan 1"),
            ("Migrate all three switches from PVST+ to Rapid PVST+", "S1(config)# spanning-tree mode rapid-pvst"),
            ("Verify the protocol is now rstp and note the alternate and backup port roles", "S1# show spanning-tree vlan 1 | include protocol"),
            ("Shut the root port on S3 and time how long the alternate port takes to forward", "S3(config-if)# shutdown"),
            ("Bring the port back and record the convergence figures for both protocols", "S3(config-if)# no shutdown"),
        ],
        test="'show spanning-tree vlan 1' on S1 states 'This bridge is the root' with priority 4096, all switches report protocol rstp, and your recorded convergence after the link failure is seconds rather than the 30–50 seconds of legacy STP.",
    ),
    dict(
        num=13, topic=3,
        title="Configure Multiple Spanning Tree (MST)",
        objective="Configure and verify common Spanning Tree Protocols — MST (ENCOR 3.1.c).",
        desc=(
            "The campus carries 200 VLANs, and running one spanning tree per VLAN is consuming switch CPU "
            "and making troubleshooting impractical. As the engineer you consolidate them onto two MST "
            "instances, load-balancing the VLANs across two roots, and confirm all switches join the same "
            "MST region — which requires name, revision and VLAN map to match exactly."
        ),
        build="A three-switch MST region named CAMPUS with VLANs mapped to instances 1 and 2, S1 root for instance 1 and S2 root for instance 2, giving true load distribution.",
        services="Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches",
        steps=[
            ("Open lab-13-mst/lab-13-mst.pkt and count how many spanning tree instances are running today", "S1# show spanning-tree summary"),
            ("Change the spanning tree mode to MST on S1", "S1(config)# spanning-tree mode mst"),
            ("Enter MST configuration mode to define the region", "S1(config)# spanning-tree mst configuration"),
            ("Name the region — this must match character for character on every switch", "S1(config-mst)# name CAMPUS"),
            ("Set the revision number, which must also match exactly", "S1(config-mst)# revision 1"),
            ("Map the first half of the VLANs to instance 1", "S1(config-mst)# instance 1 vlan 1-100"),
            ("Map the second half to instance 2", "S1(config-mst)# instance 2 vlan 101-200"),
            ("Review the pending configuration before you commit it", "S1(config-mst)# show pending"),
            ("Apply the identical region configuration to S2 and S3", "S2(config-mst)# name CAMPUS"),
            ("Make S1 the root for instance 1", "S1(config)# spanning-tree mst 1 root primary"),
            ("Make S2 the root for instance 2 so the two instances take different paths", "S2(config)# spanning-tree mst 2 root primary"),
            ("Verify the region name, revision and the configuration digest all match across switches", "S1# show spanning-tree mst configuration"),
            ("Confirm both instances are running with the intended roots", "S1# show spanning-tree mst"),
            ("Tune an MST port cost on one instance to influence its path independently", "S3(config-if)# spanning-tree mst 1 cost 100000"),
        ],
        test="'show spanning-tree mst configuration' returns the same region name CAMPUS, revision 1 and identical configuration digest on all three switches, and 'show spanning-tree mst' shows S1 root for instance 1 and S2 root for instance 2.",
    ),
    dict(
        num=14, topic=3,
        title="Harden the Spanning Tree with PortFast, BPDU Guard and Root Guard",
        objective="Configure and verify Spanning Tree enhancements such as root guard and BPDU guard (ENCOR 3.1.c).",
        desc=(
            "A contractor plugged a personal switch into a meeting-room wall port last month and became the "
            "spanning tree root, black-holing the floor for four minutes. As the engineer you make that "
            "impossible: PortFast on edge ports so hosts get an instant link, BPDU guard to shut any edge "
            "port that receives a BPDU, and root guard on the distribution uplinks."
        ),
        build="Edge ports running PortFast with BPDU guard globally enabled, root guard on the distribution-facing uplinks, and a demonstrated err-disable when a rogue BPDU arrives.",
        services="Cisco Packet Tracer, Cisco IOS CLI, S1/S2/S3 switches, rogue switch, PC-A",
        steps=[
            ("Open lab-14-stp-hardening/lab-14-stp-hardening.pkt and time how long a PC port takes to forward", ""),
            ("Enable PortFast on the access port so it skips listening and learning", "S1(config-if)# spanning-tree portfast"),
            ("Enable PortFast by default on all non-trunking ports", "S1(config)# spanning-tree portfast default"),
            ("Verify PortFast is active on the interface", "S1# show spanning-tree interface FastEthernet0/1 portfast"),
            ("Enable BPDU guard on that specific interface", "S1(config-if)# spanning-tree bpduguard enable"),
            ("Enable BPDU guard globally for every PortFast-enabled port", "S1(config)# spanning-tree portfast bpduguard default"),
            ("Connect the rogue switch to the PortFast port and watch the port err-disable", "S1# show interfaces status err-disabled"),
            ("Read the log entry that names BPDU guard as the cause", "S1# show logging | include BPDUGUARD"),
            ("Configure automatic recovery so the port returns after five minutes", "S1(config)# errdisable recovery cause bpduguard"),
            ("Set the recovery interval", "S1(config)# errdisable recovery interval 300"),
            ("Apply root guard to the uplink so no superior BPDU can move the root", "S1(config-if)# spanning-tree guard root"),
            ("Verify root guard is applied and note it puts the port in root-inconsistent rather than shutting it", "S1# show spanning-tree inconsistentports"),
            ("Enable loop guard to cover unidirectional link failures", "S1(config)# spanning-tree loopguard default"),
            ("Summarise which feature defends which failure mode in your notes", "S1# show spanning-tree summary"),
        ],
        test="The rogue switch's BPDU puts the PortFast port into err-disabled with a BPDUGUARD log entry, 'show spanning-tree inconsistentports' reports a root-inconsistent port when a superior BPDU hits the guarded uplink, and errdisable recovery is armed.",
    ),
    dict(
        num=15, topic=3,
        title="Compare EIGRP and OSPF Path Selection",
        objective="Compare routing concepts of EIGRP and OSPF — advanced distance vector versus link state, load balancing, path selection, metrics and area types (ENCOR 3.2.a).",
        desc=(
            "Your network runs EIGRP in the legacy branch estate and OSPF in the new campus, and you must "
            "explain to management why the two choose different paths across the identical topology. As the "
            "engineer you configure both over the same links, compare their metrics, and demonstrate the one "
            "capability EIGRP has that OSPF does not: unequal-cost load balancing."
        ),
        build="Both protocols running over one topology with documented metric calculations, an identified successor and feasible successor in EIGRP, and working unequal-cost load balancing via the variance command.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers",
        steps=[
            ("Open lab-15-eigrp-ospf/lab-15-eigrp-ospf.pkt and review the three-router topology with unequal-bandwidth links", ""),
            ("Enable EIGRP in named mode on R1", "R1(config)# router eigrp CAMPUS"),
            ("Enter the IPv4 unicast address family with autonomous system 100", "R1(config-router)# address-family ipv4 unicast autonomous-system 100"),
            ("Advertise the connected networks", "R1(config-router-af)# network 172.16.0.0 0.0.255.255"),
            ("Verify the EIGRP neighbours have formed", "R1# show ip eigrp neighbors"),
            ("Examine the topology table and identify the successor and the feasible successor", "R1# show ip eigrp topology"),
            ("Read the feasibility condition — the feasible successor's reported distance must be below the feasible distance", "R1# show ip eigrp topology all-links"),
            ("Enable unequal-cost load balancing with variance", "R1(config-router-af)# variance 2"),
            ("Confirm two unequal paths now appear in the routing table", "R1# show ip route eigrp"),
            ("Now enable OSPF process 10 on the same routers", "R1(config)# router ospf 10"),
            ("Set an explicit router ID rather than letting IOS pick one", "R1(config-router)# router-id 1.1.1.1"),
            ("Advertise the same networks into area 0", "R1(config-router)# network 172.16.0.0 0.0.255.255 area 0"),
            ("Verify OSPF adjacencies reached FULL state", "R1# show ip ospf neighbor"),
            ("Compare the OSPF cost with the EIGRP composite metric for the same destination", "R1# show ip route ospf"),
            ("Record which protocol picked which path and explain why in your notes", ""),
        ],
        test="'show ip eigrp topology' identifies a successor and at least one feasible successor with its reported distance, the routing table shows two unequal-cost paths after variance 2, and OSPF neighbours reach FULL with a cost you can calculate from reference bandwidth over interface bandwidth.",
    ),
    dict(
        num=16, topic=3,
        title="Configure Multiarea OSPFv2 with Summarization and Filtering",
        objective="Configure simple OSPFv2 environments including multiple normal areas, summarization and filtering (ENCOR 3.2.b).",
        desc=(
            "The campus OSPF domain has grown to a single area carrying 400 routes, and every link flap "
            "triggers a full SPF run everywhere. As the engineer you split it into multiple areas, place the "
            "ABR correctly, summarise at the area boundary to contain the flooding, and make LAN interfaces "
            "passive so no adjacency is ever attempted towards a host."
        ),
        build="A multiarea OSPFv2 domain with area 0 backbone plus areas 1 and 2, route summarization at the ABR, passive LAN interfaces, and a stub area that blocks external LSAs.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, PC1/PC2/PC3",
        steps=[
            ("Open lab-16-ospf-multiarea/lab-16-ospf-multiarea.pkt and note R1 172.16.1.1, R2 172.16.2.1, R3 192.168.1.1", ""),
            ("Start OSPF process 10 on R1 and set the router ID", "R1(config)# router ospf 10"),
            ("Set the router ID explicitly to 1.1.1.1", "R1(config-router)# router-id 1.1.1.1"),
            ("Place the backbone link into area 0", "R1(config-router)# network 172.16.3.0 0.0.0.3 area 0"),
            ("Place the LAN into area 1", "R1(config-router)# network 172.16.1.0 0.0.0.255 area 1"),
            ("Make the LAN interface passive so no hello is sent towards hosts", "R1(config-router)# passive-interface GigabitEthernet0/0"),
            ("Repeat on R2 with router ID 2.2.2.2 and its own area", "R2(config-router)# router-id 2.2.2.2"),
            ("Repeat on R3 with router ID 3.3.3.3 placing its LAN in area 2", "R3(config-router)# network 192.168.1.0 0.0.0.255 area 2"),
            ("Verify all adjacencies reached FULL", "R1# show ip ospf neighbor"),
            ("Identify which router is the ABR because it has interfaces in two areas", "R1# show ip ospf | include Area"),
            ("Summarise area 1's prefixes at the ABR to contain flooding", "R1(config-router)# area 1 range 172.16.0.0 255.255.0.0"),
            ("Confirm the summary appears as a single Type 3 LSA instead of many", "R2# show ip ospf database summary"),
            ("Configure area 2 as a stub so external LSAs never enter it", "R3(config-router)# area 2 stub"),
            ("Apply the matching stub command on the ABR — both ends must agree or the adjacency drops", "R1(config-router)# area 2 stub"),
            ("Verify the routing tables and the LSA types present in each area", "R3# show ip ospf database"),
        ],
        test="All OSPF neighbours are FULL, 'show ip ospf' identifies the ABR with interfaces in two areas, the area 1 prefixes appear as one summarised Type 3 LSA in the backbone, and the stub area's database contains no Type 5 external LSAs.",
    ),
    dict(
        num=17, topic=3,
        title="Configure Multiarea OSPFv3 for IPv6",
        objective="Configure simple OSPFv3 environments including multiple normal areas (ENCOR 3.2.b).",
        desc=(
            "The organisation is dual-stacking, and IPv6 needs its own routing. As the engineer you configure "
            "OSPFv3 across three routers, working with the differences that catch people out: OSPFv3 is "
            "enabled per interface rather than with network statements, it still needs a 32-bit router ID even "
            "though it routes IPv6, and adjacencies form over link-local addresses."
        ),
        build="A multiarea OSPFv3 domain with RA in area 1, RB in area 0 and RC in area 2, full adjacencies over link-local addresses, and end-to-end IPv6 reachability.",
        services="Cisco Packet Tracer, Cisco IOS CLI, RA/RB/RC routers",
        steps=[
            ("Open lab-17-ospfv3/lab-17-ospfv3.pkt and note the 2001:db8:1::/64 addressing plan", ""),
            ("Enable IPv6 unicast routing — nothing IPv6 works without it", "RA(config)# ipv6 unicast-routing"),
            ("Start the OSPFv3 process", "RA(config)# ipv6 router ospf 10"),
            ("Set the 32-bit router ID, still required even though this routes IPv6", "RA(config-rtr)# router-id 1.1.1.1"),
            ("Move to the LAN interface and enable OSPFv3 on it directly", "RA(config-if)# ipv6 ospf 10 area 1"),
            ("Enable OSPFv3 on the second LAN interface, also in area 1", "RA(config-if)# ipv6 ospf 10 area 1"),
            ("Enable OSPFv3 on the backbone link in area 0", "RA(config-if)# ipv6 ospf 10 area 0"),
            ("Set the link-local address explicitly so adjacencies are easy to read", "RA(config-if)# ipv6 address fe80::a link-local"),
            ("Repeat on RB with router ID 2.2.2.2, all interfaces in area 0", "RB(config-rtr)# router-id 2.2.2.2"),
            ("Repeat on RC with router ID 3.3.3.3, its LANs in area 2", "RC(config-if)# ipv6 ospf 10 area 2"),
            ("Verify the adjacencies formed and note they use link-local addresses", "RA# show ipv6 ospf neighbor"),
            ("Confirm each interface is in the intended area", "RA# show ipv6 ospf interface brief"),
            ("Inspect the IPv6 routing table for inter-area routes marked OI", "RA# show ipv6 route ospf"),
            ("Test end-to-end IPv6 reachability across all three areas", "RA# ping 2001:db8:1:c1::1"),
        ],
        test="'show ipv6 ospf neighbor' shows all neighbours FULL with link-local addresses as the neighbour address, 'show ipv6 route ospf' contains OI inter-area routes, and RA pings RC's LAN across the backbone.",
    ),
    dict(
        num=18, topic=3,
        title="Configure and Verify eBGP",
        objective="Configure and verify eBGP between directly connected neighbours, including best path selection and neighbour relationships (ENCOR 3.2.c).",
        desc=(
            "ACME is multihoming to two ISP entry points for internet resilience. As the WAN engineer you "
            "configure eBGP to both providers, advertise your own prefix, then influence which path inbound "
            "and outbound traffic takes — and you deliberately break the session by peering to a loopback "
            "without ebgp-multihop, so you recognise the most common eBGP failure in the field."
        ),
        build="Established eBGP sessions from ACME1 to both ISP entry points, the local prefix advertised and visible in both providers' tables, and a demonstrated path preference change.",
        services="Cisco Packet Tracer, Cisco IOS CLI, ACME1, OtherCo1, ISP-Entry-1, ISP-Entry-2",
        steps=[
            ("Open lab-18-ebgp/lab-18-ebgp.pkt and confirm ACME1 S0/0/0 is 1.1.1.2 peering to 1.1.1.1", "ACME1# ping 1.1.1.1"),
            ("Start BGP with ACME's autonomous system number", "ACME1(config)# router bgp 65001"),
            ("Define the eBGP neighbour and its remote AS", "ACME1(config-router)# neighbor 1.1.1.1 remote-as 65000"),
            ("Advertise the local LAN prefix into BGP", "ACME1(config-router)# network 192.168.0.0 mask 255.255.255.0"),
            ("Disable auto-summary so classful summarisation does not surprise you", "ACME1(config-router)# no auto-summary"),
            ("Verify the session moved to Established by checking the state and prefix count", "ACME1# show ip bgp summary"),
            ("Read the BGP table and identify the best path, marked with >", "ACME1# show ip bgp"),
            ("Examine the attributes BGP used to choose it", "ACME1# show ip bgp 172.16.10.0"),
            ("Add the second provider session for redundancy", "ACME1(config-router)# neighbor 1.1.1.5 remote-as 65000"),
            ("Verify both neighbours are Established", "ACME1# show ip bgp neighbors | include BGP state"),
            ("Influence outbound path selection by raising local preference on one neighbour's routes", "ACME1(config)# route-map PREFER-ISP1 permit 10"),
            ("Set the local preference value inside the route map", "ACME1(config-route-map)# set local-preference 200"),
            ("Apply the route map inbound from the preferred provider", "ACME1(config-router)# neighbor 1.1.1.1 route-map PREFER-ISP1 in"),
            ("Clear the session softly so the policy takes effect without dropping the peering", "ACME1# clear ip bgp * soft in"),
            ("Confirm the best path moved to the preferred provider", "ACME1# show ip bgp"),
        ],
        test="'show ip bgp summary' shows both neighbours Established with a non-zero prefix count, 'show ip bgp' marks the best path with >, and after the local preference change the best-path marker moves to the preferred provider's route.",
    ),
    dict(
        num=19, topic=3,
        title="Configure a Basic WLAN and WPA2-Enterprise on the WLC",
        objective="Describe AP discovery and join, wireless segmentation with groups, profiles and tags, and configure wireless security features (ENCOR 3.3.c, 3.3.f, 5.4).",
        desc=(
            "The office is deploying its first controller-based wireless network. As the wireless engineer you "
            "build the WLC configuration end to end through the GUI: interfaces and VLANs, a PSK guest WLAN, "
            "then a WPA2-Enterprise corporate WLAN backed by RADIUS. You watch the AP complete its CAPWAP "
            "discovery and join, and confirm clients land in the right VLAN."
        ),
        build="A WLC with a management interface on 192.168.200.254, a joined LAP, a PSK guest WLAN and a WPA2-Enterprise corporate WLAN authenticating against the RADIUS server at 172.31.1.254.",
        services="Cisco Packet Tracer, WLC-1 GUI, LAP-1, R1, SW1, RADIUS server, wireless hosts",
        steps=[
            ("Open lab-19-wlc-wlan/lab-19-wlc-wlan.pkt and browse to the WLC at https://192.168.200.254 from the Admin PC", ""),
            ("Log in to the WLC GUI and review the Monitor summary page", ""),
            ("Under Controller > Interfaces, create the VLAN 5 dynamic interface for wireless clients", ""),
            ("Set the interface IP as 192.168.5.254/24 with gateway 192.168.5.1 and the DHCP server address", ""),
            ("Confirm the AP has completed CAPWAP discovery and joined under Wireless > All APs", ""),
            ("Note the CAPWAP control tunnel on UDP 5246 and the data tunnel on UDP 5247", ""),
            ("Under WLANs, create the guest WLAN and set its SSID and profile name", ""),
            ("Map the guest WLAN to the VLAN 5 dynamic interface", ""),
            ("On the Security tab, set Layer 2 security to WPA2 with PSK and enter the pre-shared key", ""),
            ("Enable the WLAN under General and verify it appears in the WLAN list", ""),
            ("Now create the corporate WLAN for WPA2-Enterprise", ""),
            ("Under Security > AAA Servers, add the RADIUS server 172.31.1.254 with its shared secret", ""),
            ("Set the corporate WLAN's Layer 2 security to WPA2 with 802.1X and select that RADIUS server", ""),
            ("Connect a wireless host to the guest SSID and confirm it receives a VLAN 5 address", "C:\\> ipconfig"),
            ("Connect a second host to the corporate SSID with a RADIUS username and password", ""),
            ("Verify both clients under Monitor > Clients showing their SSID, VLAN and policy", ""),
        ],
        test="The LAP shows as joined and associated in Wireless > All APs, both WLANs appear enabled in the WLAN list, the guest client receives a 192.168.5.x address, and the corporate client authenticates against RADIUS and appears under Monitor > Clients.",
    ),
    dict(
        num=20, topic=3,
        title="Troubleshoot WLAN and Wireless Client Connectivity",
        objective="Troubleshoot WLAN configuration and wireless client connectivity issues using GUI only (ENCOR 3.3.e).",
        desc=(
            "Three separate wireless complaints arrive the same morning: one user cannot see the SSID, one "
            "associates but gets no IP address, and one authenticates but cannot reach the internal server. As "
            "the wireless support engineer you must resolve all three using the WLC GUI only — no CLI — which "
            "is exactly how the exam frames this objective."
        ),
        build="Three resolved wireless faults with a documented root cause for each: a disabled/misbroadcast WLAN, a wrong interface-to-VLAN mapping, and a RADIUS shared-secret mismatch.",
        services="Cisco Packet Tracer, WLC-1 GUI, LAP-1, RADIUS server, Laptop1 and Laptop2",
        steps=[
            ("Open lab-20-wlan-troubleshoot/lab-20-wlan-troubleshoot.pkt and log in to the WLC GUI as the admin", ""),
            ("Fault 1: the user cannot see the SSID — check whether the WLAN is enabled under WLANs", ""),
            ("Check the Broadcast SSID setting on the WLAN's Advanced tab", ""),
            ("Confirm the WLAN is applied to the AP group or policy tag serving that AP", ""),
            ("Enable the WLAN and its SSID broadcast, then confirm the client can see it", ""),
            ("Fault 2: the client associates but has no IP address — inspect the WLAN's interface mapping", ""),
            ("Compare the mapped dynamic interface's VLAN with the VLAN the DHCP scope serves", ""),
            ("Check the DHCP server address configured on the dynamic interface", ""),
            ("Correct the interface-to-VLAN mapping and renew the client address", "C:\\> ipconfig /renew"),
            ("Fault 3: the corporate client fails authentication — open Security > AAA > RADIUS > Authentication", ""),
            ("Verify the RADIUS server IP, port 1812 and that the server is marked enabled", ""),
            ("Re-enter the shared secret so it matches the one configured on the RADIUS server", ""),
            ("Retry the client association and watch it succeed under Monitor > Clients", ""),
            ("Record each fault, its symptom, its root cause and its fix in troubleshooting-log.csv", ""),
        ],
        test="All three clients reach a working state: the SSID is visible and broadcast, the DHCP client holds an address in the correct VLAN, the 802.1X client authenticates, and troubleshooting-log.csv names a distinct root cause for each fault.",
    ),
    dict(
        num=21, topic=3,
        title="Configure NTP, NAT/PAT and HSRP",
        objective="Interpret NTP configurations, configure NAT/PAT, and configure first hop redundancy protocols such as HSRP and VRRP (ENCOR 3.4.a, 3.4.b, 3.4.c).",
        desc=(
            "The branch office needs three IP services before it goes live: synchronised time so logs "
            "correlate, PAT so its private hosts reach the internet through one public address, and a "
            "redundant default gateway so a router failure does not black-hole the LAN. As the branch engineer "
            "you configure all three and prove the HSRP failover actually works."
        ),
        build="A branch router synchronised to an NTP master, PAT translating 192.168.10.0/24 out one public address, and an HSRP group with virtual IP 192.168.1.254 that fails over on preemption.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1/R2/R3 routers, S1/S3 switches, PC-A and PC-B",
        steps=[
            ("Open lab-21-ip-services/lab-21-ip-services.pkt and review the three service requirements", ""),
            ("Configure R1 as the NTP master at stratum 3", "R1(config)# ntp master 3"),
            ("Point R2 at R1 as its NTP server", "R2(config)# ntp server 209.165.200.226"),
            ("Verify the clock synchronised and note the stratum", "R2# show ntp status"),
            ("Check the association and confirm the * marks the synchronised peer", "R2# show ntp associations"),
            ("Make timestamps meaningful by logging with the actual date and time", "R2(config)# service timestamps log datetime msec"),
            ("Now configure PAT — define which inside addresses may be translated", "R1(config)# access-list 1 permit 192.168.10.0 0.0.0.255"),
            ("Mark the inside interface", "R1(config-if)# ip nat inside"),
            ("Mark the outside interface", "R1(config-if)# ip nat outside"),
            ("Create the overload translation using the outside interface address", "R1(config)# ip nat inside source list 1 interface Serial0/0/0 overload"),
            ("Generate traffic from PC1 and inspect the translation table", "R1# show ip nat translations"),
            ("Check the translation statistics for hits and misses", "R1# show ip nat statistics"),
            ("Now configure HSRP on R1 as the intended active router", "R1(config-if)# standby 1 ip 192.168.1.254"),
            ("Raise R1's priority above the default of 100", "R1(config-if)# standby 1 priority 110"),
            ("Enable preemption so R1 reclaims the active role after a recovery", "R1(config-if)# standby 1 preempt"),
            ("Configure R3 as the standby with default priority", "R3(config-if)# standby 1 ip 192.168.1.254"),
            ("Verify R1 is Active and R3 is Standby with the correct virtual IP and MAC", "R1# show standby brief"),
            ("Shut R1's LAN interface and confirm R3 takes over while PC-A keeps pinging", "R1(config-if)# shutdown"),
        ],
        test="'show ntp status' reports the clock is synchronised, 'show ip nat translations' lists inside-local to inside-global entries with differing ports, and 'show standby brief' shows R1 Active / R3 Standby — with R3 becoming Active and PC-A's ping continuing when R1's interface is shut.",
    ),
]
