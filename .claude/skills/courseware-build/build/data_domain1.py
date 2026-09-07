"""
Domain 1 — Enterprise Architecture (ENCOR 1.0, 15%).  Labs 1–5.

Every lab runs in Cisco Packet Tracer 8.2+ against the topology shipped in
labs/lab-NN-*/ .  The `steps` pairs are (instruction, command) and are the single
source for the PPT step slides, the Learner Guide procedure and the lab README.
"""

DOMAIN1 = [
    dict(
        num=1, topic=1,
        title="Investigate the CAM and TCAM Tables",
        objective="Describe hardware switching mechanisms such as CAM, TCAM, FIB, RIB and adjacency tables (ENCOR 1.6).",
        desc=(
            "You take the role of a campus network engineer verifying how an access switch actually "
            "forwards a frame. You generate traffic between hosts, watch the MAC address table (CAM) "
            "populate by learning source addresses, then age an entry out and observe the switch flood "
            "the unknown unicast. You finish by inspecting how TCAM stores the masked ACL and QoS entries "
            "that CAM's exact-match lookup cannot hold."
        ),
        build="A documented CAM table showing dynamically learned entries, one static entry you added, and a written comparison of CAM versus TCAM lookup behaviour.",
        services="Cisco Packet Tracer, Cisco IOS CLI, S1/S2 access switches, PC-A and PC-B",
        steps=[
            ("Open lab-01-cam-tcam/lab-01-cam-tcam.pkt and confirm PC-A (192.168.10.10) and PC-B (192.168.10.20) are in VLAN 10", ""),
            ("Clear the switch MAC address table so you start from a known empty state", "S1# clear mac address-table dynamic"),
            ("Display the empty table and note that only the CPU entries remain", "S1# show mac address-table"),
            ("From PC-A, ping PC-B to make the switch learn both source MAC addresses", "C:\\> ping 192.168.10.20"),
            ("Display the CAM table again and record the two dynamic entries, their VLAN and their ports", "S1# show mac address-table dynamic"),
            ("Show the ageing time — the timer that removes an entry when a host goes quiet", "S1# show mac address-table aging-time"),
            ("Add a static CAM entry so PC-A's MAC is pinned to F0/1 and never ages out", "S1(config)# mac address-table static 000c.1234.5678 vlan 10 interface FastEthernet0/1"),
            ("Verify the static entry appears with type STATIC, not DYNAMIC", "S1# show mac address-table static"),
            ("Count the total entries the switch is currently holding", "S1# show mac address-table count"),
            ("Apply an ACL so the switch programs masked entries into TCAM rather than CAM", "S1(config)# access-list 10 permit 192.168.10.0 0.0.0.255"),
            ("Inspect the platform TCAM utilisation to see the ACL and QoS regions", "S1# show platform tcam utilization"),
            ("Write two sentences in your notes explaining why an ACL cannot live in CAM", ""),
        ],
        test="'show mac address-table dynamic' lists both PC MAC addresses against the correct ports and VLAN 10, 'show mac address-table static' shows your pinned entry, and you can state that CAM does exact-match on MAC while TCAM does masked match for ACL/QoS.",
    ),
    dict(
        num=2, topic=1,
        title="Analyse Cisco Express Forwarding",
        objective="Describe and verify CEF, the FIB and the adjacency table, and contrast them with process and fast switching (ENCOR 1.6).",
        desc=(
            "Continuing as the campus engineer, you now move up to Layer 3 and prove how the router "
            "forwards in hardware. You examine the RIB, then the FIB that CEF builds from it ahead of any "
            "traffic, then the adjacency table that holds the Layer 2 rewrite. You disable CEF to watch "
            "forwarding fall back to process switching, observe the CPU cost, and re-enable it."
        ),
        build="A side-by-side record of the RIB, the FIB and the adjacency table for one destination prefix, plus measured evidence of the CPU difference when CEF is disabled.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1 and R2 routers, PC-A and PC-B",
        steps=[
            ("Open lab-02-cef/lab-02-cef.pkt and confirm R1 G0/0 is 192.168.10.1 and the R1–R2 link is 10.1.1.0/30", ""),
            ("Display the routing table (the RIB) — the control plane's view of the network", "R1# show ip route"),
            ("Display the FIB that CEF has pre-built from that RIB", "R1# show ip cef"),
            ("Look at one specific prefix in the FIB and note its next hop and outgoing interface", "R1# show ip cef 192.168.20.0"),
            ("Display the adjacency table holding the Layer 2 rewrite string for that next hop", "R1# show adjacency detail"),
            ("Confirm CEF is enabled globally and per interface", "R1# show ip interface brief | include Protocol"),
            ("Baseline the CPU before you change anything", "R1# show processes cpu sorted | include CPU"),
            ("Disable CEF globally to force process switching", "R1(config)# no ip cef"),
            ("Generate sustained traffic from PC-A to PC-B and observe the CPU climb", "C:\\> ping 192.168.20.10 -n 100"),
            ("Re-check the CPU utilisation and record the difference", "R1# show processes cpu sorted | include CPU"),
            ("Re-enable CEF and confirm the FIB is repopulated", "R1(config)# ip cef"),
            ("Verify the FIB is back and traffic is switched in hardware again", "R1# show ip cef summary"),
        ],
        test="'show ip cef' returns a populated FIB and 'show adjacency detail' shows a valid rewrite for the next hop; with CEF disabled you can point to a measurably higher CPU figure during the ping, and it falls again once CEF is re-enabled.",
    ),
    dict(
        num=3, topic=1,
        title="Compare Two-Tier and Three-Tier Campus Designs",
        objective="Explain enterprise design principles including 2-tier, 3-tier, fabric and cloud designs (ENCOR 1.1.a).",
        desc=(
            "A 400-staff company on one campus is merging with a 2,000-staff company across four buildings. "
            "As the design engineer you must recommend a campus architecture for the merged organisation. "
            "You document the current 2-tier collapsed-core design, model the merged requirement, and justify "
            "whether a dedicated core layer is now warranted — the exact judgement the exam tests."
        ),
        build="A completed design comparison table and a one-page written recommendation stating whether to move to a 3-tier design, with the trigger conditions that justify it.",
        services="Cisco Packet Tracer, network diagram, design decision worksheet",
        steps=[
            ("Open lab-03-campus-design/lab-03-campus-design.pkt and identify which switches are access and which are distribution", ""),
            ("Record what each layer is doing today — port security and PoE at access, routing at distribution", "SW-DIST-1# show ip route"),
            ("Confirm the distribution layer is the Layer 2 to Layer 3 boundary by checking the SVIs", "SW-DIST-1# show ip interface brief | include Vlan"),
            ("Count the distribution blocks the merged network will need (one per building)", ""),
            ("Apply the design rule: a dedicated core is justified beyond roughly three distribution blocks", ""),
            ("Calculate the full-mesh link count without a core — n(n-1)/2 for four blocks", ""),
            ("Complete the comparison table in design-comparison.csv for cost, cabling, convergence and scalability", ""),
            ("Document where high availability belongs — redundant supervisors, links, FHRP and SSO/NSF", ""),
            ("State which layer must never carry policy, and why the core stays simple and fast", ""),
            ("Write your recommendation with the trigger conditions that would justify the change", ""),
        ],
        test="Your recommendation names 3-tier for the merged network, shows the full-mesh link count that falls from six inter-block links to four uplinks once a core is added, and states that the core layer carries no ACLs or policy.",
    ),
    dict(
        num=4, topic=1,
        title="Interpret Wired and Wireless QoS Configurations",
        objective="Interpret wired and wireless QoS configurations, including QoS components and QoS policy (ENCOR 1.5).",
        desc=(
            "Voice calls on the campus wireless network are breaking up during busy periods. As the network "
            "engineer you trace the QoS treatment of a voice packet end to end: you read the classification "
            "and marking at the wired trust boundary, examine the queuing policy, then check how DSCP maps to "
            "the 802.11e WMM access category on the wireless side — where the mismatch usually is."
        ),
        build="A documented end-to-end QoS policy showing the class map, policy map and service policy, plus the DSCP-to-WMM mapping table that explains the voice degradation.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1 router, SW-1 switch, WLC",
        steps=[
            ("Open lab-04-qos/lab-04-qos.pkt and locate the IP phone, the access switch and the WAN router", ""),
            ("Display the class maps that classify traffic into voice, video and best effort", "R1# show class-map"),
            ("Display the policy map that assigns bandwidth and priority to each class", "R1# show policy-map"),
            ("Identify the low-latency queue reserved for voice — the strict-priority queue", "R1# show policy-map interface Serial0/0/0"),
            ("Read the marking: voice should carry DSCP EF (46), call signalling CS3 (24), video AF41 (34)", "R1# show policy-map interface | include dscp"),
            ("Check the trust boundary on the access port where the phone connects", "SW-1# show mls qos interface FastEthernet0/1"),
            ("Confirm the switch trusts the DSCP the phone marks rather than remarking it", "SW-1# show mls qos interface FastEthernet0/1 | include trust"),
            ("Inspect the queuing and drop behaviour under congestion", "R1# show policy-map interface Serial0/0/0 | include drops"),
            ("Record the DSCP to 802.11e user-priority mapping — EF should map to WMM Voice (UP 6)", ""),
            ("Identify in qos-policy-map.csv which class is mismarked and explain the audio symptom it causes", ""),
        ],
        test="You can trace a voice packet from the phone's EF marking, through the trusted access port, into the priority queue on the WAN interface, and state which DSCP-to-WMM mapping is wrong and why calls break up.",
    ),
    dict(
        num=5, topic=1,
        title="Explore SD-WAN and SD-Access Architecture",
        objective="Explain the working principles of the Cisco SD-WAN and SD-Access solutions and their control and data plane elements (ENCOR 1.3, 1.4).",
        desc=(
            "Your organisation is evaluating both Cisco SD-WAN for its branch WAN and SD-Access for its "
            "campus. As the architect you must be able to name every plane element and say what breaks if it "
            "fails. You map the four SD-WAN planes and the SD-Access LISP/VXLAN/TrustSec stack, then work "
            "through failure scenarios that the exam poses as 'what happens if…' questions."
        ),
        build="Two completed architecture maps — SD-WAN's four planes and SD-Access's control/data/policy planes — plus a failure-impact table for each component.",
        services="Cisco Packet Tracer, architecture worksheet, sdwan-components.csv, sdaccess-components.csv",
        steps=[
            ("Open lab-05-sdwan-sdaccess/ and read the two topology diagrams provided", ""),
            ("Map the SD-WAN orchestration plane to vBond and state what it does — authenticates and introduces devices", ""),
            ("Map the control plane to vSmart and note it distributes routes and policy over OMP, never carrying data", ""),
            ("Map the management plane to vManage — the GUI, API and configuration templates", ""),
            ("Map the data plane to the vEdge/cEdge routers that build the IPsec fabric between sites", ""),
            ("Answer the failure question: if vSmart fails, existing data plane tunnels keep forwarding but no new routes are learned", ""),
            ("Move to SD-Access and identify the underlay — any routed IP network providing reachability", ""),
            ("Identify the overlay data plane as VXLAN and note the VNI replaces the VLAN as the segment identifier", ""),
            ("Identify the control plane as LISP, with the map server and map resolver resolving EID to RLOC", ""),
            ("Identify the policy plane as TrustSec, carrying SGTs enforced as SGACLs at egress", ""),
            ("Name the fabric roles: control plane node, border node, edge node and wireless LAN controller", ""),
            ("Complete the failure-impact table for each component in both architectures", ""),
        ],
        test="You can name all four SD-WAN planes with their controller, state that a vSmart outage stops new route learning but not existing forwarding, and correctly identify LISP as the SD-Access control plane and VXLAN as its data plane.",
    ),
]
