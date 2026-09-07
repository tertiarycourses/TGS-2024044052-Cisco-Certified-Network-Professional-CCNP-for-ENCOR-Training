"""
SINGLE SOURCE OF TRUTH — Cisco Certified Network Professional (CCNP) for ENCOR Training.

Course code TGS-2024044052.  5 days / 40 hours.

Every artifact (PPT, LP, LG, LG.md, labs index, assessment) is generated from this
file plus data_domain1.py … data_domain6.py, so titles, lab numbering, learning
outcomes, the schedule and the assessment can never drift apart.

Guiding principle: the course material is 100% aligned to the Cisco ENCOR 350-401
v1.1 exam blueprint (the six exam domains and their weightings) AND to the WSQ TSC
"Network Configuration" ICT-DIT-3009-1.1, so learners can pass the exam and be
assessed Competent.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Cisco Certified Network Professional (CCNP) for ENCOR Training"
SHORT_TITLE  = "Cisco Certified Network Professional (CCNP) for ENCOR Training"
COURSE_CODE  = "TGS-2024044052"
VERSION      = "v6.0"
VERSION_DATE = "7 September 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr Alfred Ang"
DAYS         = 5

# Cisco exam this course prepares learners for
EXAM_CODE    = "350-401 ENCOR v1.1"
EXAM_NAME    = "Implementing Cisco Enterprise Network Core Technologies"
PRACTICE_EXAM_URL = "https://exams.tertiaryinfotech.com/practice-exams/cisco/cisco-ccnp-encor"

# ------------------------------------------------------------------ skills framework
TSC_TITLE = "Network Configuration"
TSC_CODE  = "ICT-DIT-3009-1.1"

TSC_KNOWLEDGE = [
    ("K1", "Key network components – their functions and interdependencies"),
    ("K2", "Techniques in implementation and configuration of servers, devices and other network components"),
    ("K3", "Features of network management tools"),
    ("K4", "Configuration of network servers and devices"),
    ("K5", "Network access management"),
    ("K6", "Network tracking and assessment tools"),
]

TSC_ABILITIES = [
    ("A1", "Translate the organisational requirements to technical requirements"),
    ("A2", "Identify the key network components to be configured to meet the technical requirements"),
    ("A3", "Implement multiple servers and devices in line with the organisation's network blueprint"),
    ("A4", "Manage user network access in accordance to organisational guidelines and specifications"),
    ("A5", "Identify suitable network management tools to be used"),
    ("A6", "Implement procedures to ensure regular network reporting, administration and assessment of stability"),
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Translate organizational networking needs into technical configurations by selecting appropriate network components, considering their functions and interdependencies.",
    "LO2: Identify and choose key network components for configuration, utilizing techniques in server and device implementation aligned with technical requirements.",
    "LO3: Implement a variety of servers and devices effectively, following the organizational network blueprint to enhance network performance and reliability.",
    "LO4: Manage network access, ensuring compliance with organizational guidelines and specifications to maintain secure and efficient user connectivity.",
    "LO5: Select and deploy network management tools effectively, optimizing network performance and user experience in line with organizational needs.",
    "LO6: Conduct regular network reporting and administration, employing assessment tools to ensure network stability and alignment with organizational objectives.",
]

# ------------------------------------------------------------------ topics = the six ENCOR exam domains
TOPICS = [
    dict(num=1, code="01",
         title="Enterprise Architecture",
         subtitle="Design principles · wireless design · SD-WAN · SD-Access · QoS · switching mechanisms",
         weighting="15%",
         tsc="K1, A1",
         exam="ENCOR domain 1.0 Architecture",
         concepts=[
            "Enterprise campus designs are layered: a 2-tier (collapsed core) design merges core and distribution and suits a single building, while a 3-tier design keeps a dedicated core and is justified once you exceed roughly three distribution blocks.",
            "The access layer terminates end devices and enforces port security, PoE and QoS trust; the distribution layer aggregates and is the boundary where Layer 2 becomes Layer 3; the core is a high-speed, low-latency transit fabric that must never run policy.",
            "High availability is delivered in three planes: redundancy of hardware and links, FHRP (HSRP, VRRP, GLBP) for default-gateway resilience, and SSO/NSF so a supervisor failover does not tear down routing adjacencies.",
            "Wireless deployment models trade control against latency — centralized (all traffic tunnelled to a WLC), distributed/FlexConnect (locally switched at the branch), controller-less (Mobility Express), cloud-managed (Meraki) and remote branch.",
            "Location services (RSSI trilateration, Angle of Arrival with Hyperlocation, BLE beacons) drive asset tracking and analytics; accuracy depends on AP density and placement, not on client radio power.",
            "Client density planning is a capacity problem, not a coverage problem: high-density areas need smaller cells, lower AP transmit power, narrower channel widths and band steering to 5 GHz.",
            "Cisco SD-WAN separates a control plane (vSmart), an orchestration plane (vBond), a management plane (vManage) and a data plane (vEdge/cEdge) — OMP distributes routes and policy, and IPsec builds the fabric.",
            "Cisco SD-Access builds a VXLAN overlay on any IP underlay: the control plane is LISP (map server / map resolver), the data plane is VXLAN, and policy is carried as SGTs enforced by TrustSec.",
            "QoS components are classification and marking (DSCP/CoS), queuing and scheduling (LLQ/CBWFQ), congestion avoidance (WRED), policing (drops) and shaping (buffers) — mark once, at the trust boundary, and act everywhere.",
            "Wireless QoS maps DSCP to the 802.11e user-priority (WMM) access categories; a mismatch between the wired DSCP and the wireless UP is the most common reason voice quality collapses over Wi-Fi.",
            "Hardware switching is a table story: CAM is exact-match (MAC address table), TCAM is ternary and stores masked entries for ACLs and QoS, the FIB is the CEF-prepared copy of the RIB, and the adjacency table holds the rewrite information.",
            "Cisco Express Forwarding replaces process and fast switching by building the FIB and adjacency table ahead of traffic — so the first packet of a flow is switched in hardware just like the millionth.",
         ]),
    dict(num=2, code="02",
         title="Virtualization Technologies",
         subtitle="Hypervisors · virtual machines · virtual switching · VRF · GRE and IPsec · LISP and VXLAN",
         weighting="10%",
         tsc="K2, A2",
         exam="ENCOR domain 2.0 Virtualization",
         concepts=[
            "A Type 1 (bare-metal) hypervisor such as ESXi, KVM or Hyper-V runs directly on the hardware and is what data centres deploy; a Type 2 hypervisor such as VMware Workstation or VirtualBox runs as an application on a host OS and suits a lab.",
            "A virtual machine packages vCPU, vRAM, vNIC and virtual disk with a full guest OS — heavier than a container but fully isolated, which is why network functions (CSR 1000v, ASAv, WLC-v) ship as VMs.",
            "Virtual switching (vSwitch, Cisco Nexus 1000v, DVS) moves the access layer inside the hypervisor: VM-to-VM traffic on the same host never touches a physical switch, which is exactly why it can bypass your physical ACLs.",
            "VRF (Virtual Routing and Forwarding) creates multiple independent routing tables on one device — the same IP prefix can exist in two VRFs without conflict, giving Layer 3 segmentation without extra hardware.",
            "VRF-Lite is VRF without MPLS: you define the VRF, assign interfaces with 'vrf forwarding', and every show/ping/traceroute must then be qualified with 'vrf <name>' or it consults the global table and appears to fail.",
            "GRE tunnels are simple, multiprotocol and support routing protocols and multicast — but they provide no confidentiality, integrity or authentication whatsoever.",
            "IPsec provides confidentiality, integrity, authentication and anti-replay; the classic enterprise pattern is GRE over IPsec, which gives you the routing and multicast support of GRE plus the protection of IPsec.",
            "IPsec negotiates in two phases: IKE Phase 1 builds a bidirectional management tunnel (ISAKMP SA), and Phase 2 builds the unidirectional IPsec SAs that actually carry data — an interesting-traffic ACL mismatch is the classic Phase 2 failure.",
            "LISP splits location from identity: an EID identifies the endpoint and an RLOC identifies where it currently attaches, with a map server / map resolver providing the lookup — this is what makes SD-Access mobility work.",
            "VXLAN encapsulates a Layer 2 frame in UDP (port 4789) and carries it across a routed underlay, extending Layer 2 without spanning tree and lifting the segment ceiling from 4,094 VLANs to 16 million VNIs.",
         ]),
    dict(num=3, code="03",
         title="Network Infrastructure",
         subtitle="Layer 2 · Layer 3 routing · wireless · IP services — the largest exam domain",
         weighting="30%",
         tsc="K3, A3",
         exam="ENCOR domain 3.0 Infrastructure",
         concepts=[
            "An 802.1Q trunk carries multiple VLANs on one link by inserting a 4-byte tag; the native VLAN is sent untagged, and a native-VLAN mismatch between two ends produces VLAN leaking that CDP will warn you about.",
            "DTP negotiates trunking automatically, which is convenient and insecure — production practice is to hard-set 'switchport mode trunk' or 'access' and disable negotiation with 'switchport nonegotiate'.",
            "EtherChannel bundles up to eight physical links into one logical link; PAgP is Cisco-proprietary (desirable/auto) and LACP is the IEEE 802.3ad standard (active/passive) — two 'auto' or two 'passive' ends will never form a bundle.",
            "EtherChannel members must match on speed, duplex, trunk mode, allowed VLAN list and native VLAN — a mismatch on any of these suspends the port, and 'show etherchannel summary' flags it.",
            "STP elects a root bridge by lowest bridge ID (priority + MAC), then each non-root switch picks one root port by lowest cumulative path cost, then each segment picks a designated port — every remaining port is blocked.",
            "RSTP (802.1w) converges in seconds rather than the 30–50 seconds of legacy STP by using proposal/agreement on point-to-point links, plus alternate and backup port roles that are pre-computed standby paths.",
            "MST (802.1s) maps many VLANs onto a few instances so a 1,000-VLAN campus runs two or three spanning trees instead of a thousand — switches only share an MST region when name, revision and VLAN-to-instance map match exactly.",
            "STP protection features each defend a different attack: PortFast skips listening/learning on edge ports, BPDU guard shuts a PortFast port that receives a BPDU, root guard prevents a superior BPDU from moving the root, and loop guard covers unidirectional link failures.",
            "EIGRP is an advanced distance-vector protocol using DUAL: the successor is the best path, and a feasible successor is a guaranteed loop-free backup that meets the feasibility condition (its reported distance is less than the current feasible distance).",
            "OSPF is a link-state protocol: every router floods LSAs, builds an identical LSDB for the area, and independently runs Dijkstra's SPF to compute its own shortest-path tree — cost is the metric, by default reference bandwidth over interface bandwidth.",
            "OSPF area types control LSA flooding: a stub area blocks external LSAs (Type 5), a totally stubby area also blocks summaries (Type 3), and NSSA allows local redistribution via Type 7 LSAs that the ABR translates to Type 5.",
            "OSPF neighbours only form when hello/dead timers, area ID, subnet mask, authentication and stub flags all match; on broadcast networks a DR and BDR are elected to prevent an n-squared adjacency mesh.",
            "eBGP is a path-vector protocol between autonomous systems: it forms TCP 179 sessions with explicitly configured neighbours, and its best-path algorithm evaluates weight, local preference, AS-path length, origin, MED and more — in that order.",
            "eBGP peers are normally directly connected and default to a TTL of 1; peering to a loopback therefore requires 'ebgp-multihop' and 'update-source', which is the most common eBGP lab failure.",
            "Policy-based routing overrides the routing table for selected traffic using a route-map matched on an ACL, letting you send (say) guest traffic out a different path than the RIB's best path.",
            "Wireless Layer 1 is a power budget: RSSI is the received signal strength, SNR is the margin between signal and noise floor, and a healthy data connection wants roughly -67 dBm RSSI and 25 dB SNR.",
            "AP modes serve different jobs — local (normal service), FlexConnect (branch local switching), monitor (scanning only), sniffer (packet capture), bridge/mesh, and SE-Connect for spectrum analysis.",
            "An AP joins a WLC by CAPWAP: it discovers candidate controllers (broadcast, DHCP option 43, DNS, or a previously learnt list), selects one by priority and AP capacity, then builds a DTLS-encrypted CAPWAP control tunnel on UDP 5246 and a data tunnel on UDP 5247.",
            "Layer 2 roaming keeps the client in the same subnet so only the AP association changes; Layer 3 roaming crosses a subnet boundary and requires an anchor/foreign controller tunnel so the client's IP address survives the move.",
            "NTP disciplines clocks in a stratum hierarchy so logs, certificates and troubleshooting timelines correlate; PTP (1588) provides sub-microsecond hardware-timestamped accuracy where NTP's millisecond accuracy is not enough.",
            "NAT translates a private inside-local address to a public inside-global address; PAT overloads one public address across many hosts by also translating the source port, which is why 'ip nat inside source list 1 interface g0/0 overload' is the ubiquitous branch configuration.",
            "First-hop redundancy protocols present one virtual IP and virtual MAC to hosts: HSRP is Cisco (active/standby, group 0 default, preemption off by default), VRRP is the standard (master/backup, preemption on by default), and GLBP additionally load-balances across gateways.",
            "Multicast delivers one stream to many receivers: IGMP is how hosts join a group on the LAN, PIM builds the distribution tree between routers, and the Reverse Path Forwarding check discards any multicast packet that did not arrive on the interface the router would use to reach the source.",
         ]),
    dict(num=4, code="04",
         title="Network Assurance",
         subtitle="Diagnostics · NetFlow · SPAN/RSPAN/ERSPAN · IP SLA · DNA Center · NETCONF and RESTCONF",
         weighting="10%",
         tsc="K5, A4",
         exam="ENCOR domain 4.0 Network Assurance",
         concepts=[
            "Diagnose from the bottom up: ping proves reachability, extended ping proves it from the right source, traceroute locates where the path breaks, and debug shows why — but debug is CPU-expensive and must be scoped.",
            "Conditional debugging ('debug interface', 'debug platform condition') restricts output to one interface, one MAC or one IP so you can safely debug on a production device without drowning the console.",
            "SNMP polls devices for counters and state: v2c is community-string based and sends everything in clear text, while v3 adds authentication and encryption and is the only version acceptable in production.",
            "Syslog messages carry a facility, a severity 0–7 (0 emergency to 7 debugging) and a mnemonic; sending them to a central collector with accurate NTP timestamps is what makes post-incident correlation possible.",
            "Flexible NetFlow is built from three parts: a flow record (the key and non-key fields you want), a flow exporter (where to send it), and a flow monitor (which binds them and is applied to an interface).",
            "NetFlow answers 'who is talking to whom, how much and for how long' — it is a summarised conversation record, not a packet capture, so it scales to a whole network where SPAN never could.",
            "SPAN copies traffic from a source port or VLAN to a destination port on the same switch, RSPAN carries the copy across a dedicated VLAN to another switch, and ERSPAN encapsulates it in GRE so it can cross a routed network.",
            "IP SLA generates synthetic probes — ICMP echo, UDP jitter, HTTP — and measures latency, jitter and loss continuously, so you learn the path degraded before the user calls.",
            "Tracking an IP SLA operation with an object lets you drive real behaviour from measurement: a static route or an HSRP priority can be withdrawn automatically when the probe fails.",
            "Cisco DNA Center organises work into four workflows — Design (site hierarchy and settings), Policy (SGTs and access), Provision (push to devices) and Assurance (health scores and issues) — and it is API-first, so anything the GUI does can be automated.",
            "NETCONF is an XML-based configuration protocol running over SSH on port 830 with explicit candidate/running datastores and transactional commits, so a partial failure rolls back cleanly.",
            "RESTCONF exposes the same YANG models as HTTPS REST on port 443 using GET, POST, PUT, PATCH and DELETE with JSON or XML — simpler for scripts, but without NETCONF's transactional guarantees.",
         ]),
    dict(num=5, code="05",
         title="Network Security",
         subtitle="Device access control · AAA · ACLs and CoPP · REST API security · wireless security · security design",
         weighting="20%",
         tsc="K4, A6",
         exam="ENCOR domain 5.0 Security",
         concepts=[
            "Device access control starts with the lines: console, VTY and AUX each need a password and a login method, and 'transport input ssh' plus 'no ip http server' removes the plaintext paths.",
            "Local user authentication with 'username … secret' stores a strong hash (type 8/9 scrypt where supported), whereas 'password' stores a trivially reversible type 7 — never use type 7 for anything that matters.",
            "AAA separates Authentication (who are you), Authorization (what may you do) and Accounting (what did you do) — and 'aaa authentication login default group tacacs+ local' keeps a local fallback so a server outage does not lock you out.",
            "TACACS+ encrypts the whole payload, uses TCP 49 and separates authentication from authorization, which is why it is preferred for device administration; RADIUS uses UDP, encrypts only the password, and is the standard for network access (802.1X).",
            "A standard ACL matches source address only and belongs close to the destination; an extended ACL matches source, destination, protocol and port and belongs close to the source so unwanted traffic is dropped early.",
            "Every ACL ends in an implicit 'deny any' — an ACL with only permit statements for your management subnet will silently drop everything else, which is the single most common cause of a self-inflicted lockout.",
            "Control Plane Policing protects the CPU by applying a QoS policy to the control plane itself, rate-limiting management and routing traffic so a flood of ICMP or SNMP cannot starve the device of the CPU it needs to keep routing.",
            "REST API security rests on transport (always HTTPS/TLS), authentication (tokens or OAuth 2.0 rather than embedded credentials), authorization scope, rate limiting, and input validation — and tokens must never be committed to a repository.",
            "802.1X is a three-party conversation: the supplicant (client), the authenticator (switch or WLC) and the authentication server (RADIUS/ISE); EAPOL carries EAP between supplicant and authenticator, RADIUS carries it onward.",
            "WPA2/WPA3 personal uses a pre-shared key, enterprise uses 802.1X; either way the 4-way handshake derives fresh session keys (PTK/GTK) from the PMK, and it is what proves both sides hold the key without ever sending it.",
            "WebAuth intercepts the first HTTP request and presents a captive portal — right for guest access, wrong for anything that needs strong identity, and useless for headless devices.",
            "MAB (MAC Authentication Bypass) authenticates a device by its MAC address for printers and IP cameras that cannot run a supplicant — it is weak, because a MAC is trivially spoofed, so it is paired with profiling.",
            "Network security design layers threat defence (IPS/NGIPS), endpoint security (AMP), a next-generation firewall (application-aware, identity-aware), and segmentation with TrustSec SGTs and MACsec link encryption.",
            "TrustSec tags traffic with a Security Group Tag at ingress and enforces it as an SGACL at egress, so policy follows identity rather than IP address — which is what makes policy survive DHCP and mobility.",
         ]),
    dict(num=6, code="06",
         title="Network Automation",
         subtitle="Python · JSON · YANG · DNA Center and vManage APIs · REST responses · EEM · orchestration tools",
         weighting="15%",
         tsc="K6, A5",
         exam="ENCOR domain 6.0 Automation",
         concepts=[
            "The ENCOR exam asks you to interpret Python, not to write an application: you must read a script and predict its output, so lists, dictionaries, loops, conditionals, functions and the requests library are the working set.",
            "A Python dictionary maps keys to values and is exactly how a parsed JSON object arrives — nested API responses are therefore navigated with chained keys and indexes such as response['response'][0]['hostname'].",
            "JSON has six value types — string, number, boolean, null, array and object — with keys always in double quotes, no trailing commas and no comments; a single trailing comma is the most common invalid-JSON exam trap.",
            "YANG is a data modelling language that defines the structure, types and constraints of configuration and operational data; NETCONF and RESTCONF are the protocols that carry data conforming to those models.",
            "A YANG model is a tree of containers, lists, leaves and leaf-lists — a container groups, a list has a key and repeats, a leaf holds one typed value — and the same model drives both NETCONF XML and RESTCONF JSON.",
            "The Cisco DNA Center Intent API is token-based: POST to /dna/system/api/v1/auth/token with Basic auth to receive an X-Auth-Token, then send that token in the header of every subsequent call.",
            "The vManage API authenticates with a session cookie from /j_security_check plus an XSRF token for write operations, and exposes device inventory, statistics and policy over /dataservice endpoints.",
            "REST response codes group by class: 2xx succeeded (200 OK, 201 Created, 204 No Content), 4xx you made an error (400 bad request, 401 unauthenticated, 403 unauthorised, 404 not found, 429 rate-limited), and 5xx the server failed.",
            "A 401 means the token is missing, wrong or expired, while a 403 means the token is valid but the account lacks permission — reading that difference correctly is the fastest way to fix a failing API script.",
            "EEM (Embedded Event Manager) runs on the device itself: an event detector (syslog, SNMP, interface, timer, CLI) triggers an applet whose actions run CLI commands, write logs, send mail or set variables — automation with no external server.",
            "An EEM applet needs 'event manager applet NAME', one event statement, and numbered action statements which run in lexical order — so 1.0, 2.0, 3.0 is the safe numbering convention, not 1, 2, 10.",
            "Agent-based tools (Puppet, Chef) install software on the managed node and pull the desired state on a schedule; agentless tools (Ansible, SaltStack in agentless mode) push over SSH or an API and are far easier to adopt on network devices that cannot run an agent.",
            "Ansible is declarative and idempotent: a playbook describes the desired end state, and running it twice makes no second change — which is what makes it safe to re-run against production.",
         ]),
]

# ------------------------------------------------------------------ day themes (8 training hours/day)
DAY_THEMES = {
    1: "Enterprise Architecture — design, switching paths, campus LAN and high availability",
    2: "Virtualization Technologies — hypervisors, VRF, GRE/IPsec, LISP and VXLAN",
    3: "Network Infrastructure — Layer 2, EIGRP/OSPF/BGP and IP services",
    4: "Network Infrastructure (wireless), Network Assurance and Network Security",
    5: "Network Automation, revision and final assessment",
}

# Which topics are taught on which day (drives the Lesson Plan schedule)
DAY_TOPICS = {
    1: [1],
    2: [2],
    3: [3],
    4: [3, 4, 5],
    5: [6],
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — hands-on Cisco configuration and verification tasks, 1 hour, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)

# ------------------------------------------------------------------ lab environment
LAB_TOOLS = [
    ("Cisco Packet Tracer 8.2+", "The primary lab environment. Every .pkt/.pka topology in labs/ opens in Packet Tracer — free from the Cisco Networking Academy."),
    ("Cisco IOS / IOS XE CLI", "All configuration is done at the IOS CLI, so the commands transfer directly to real 9200/9300 switches and ISR/CSR routers."),
    ("Wireless LAN Controller (WLC)", "The Packet Tracer WLC GUI is used for the WLAN, WPA2-Enterprise and wireless troubleshooting labs."),
    ("Python 3.10+", "Used for the automation labs — interpreting scripts, parsing JSON and calling REST APIs."),
    ("Postman or curl", "Used to exercise the Cisco DNA Center and RESTCONF APIs and to read response codes."),
    ("A text editor", "VS Code or any editor for writing Python scripts, JSON payloads and saved configurations."),
]

# ------------------------------------------------------------------ next steps
RECOMMENDED_COURSES = [
    "WSQ Cisco Certified Network Associate (CCNA) Training",
    "WSQ Cisco Certified Network Professional (CCNP) for ENARSI Training",
    "WSQ Certified Ethical Hacker (CEH) Training",
    "WSQ ISC2 Certified Information Systems Security Professional (CISSP) Training",
    "WSQ CompTIA Network+ Training",
    "WSQ Network Automation with Python and Ansible",
]
