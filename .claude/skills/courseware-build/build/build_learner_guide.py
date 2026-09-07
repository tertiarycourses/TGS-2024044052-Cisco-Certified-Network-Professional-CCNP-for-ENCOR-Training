#!/usr/bin/env python3
"""Generate the Cisco CCNP ENCOR Learner Guide as BOTH a Markdown mirror (LG-*.md at repo
root) and a DOCX (courseware/LG-*.docx) from one source, so they never diverge.

House format: cover page, Document Version Control Record, auto TOC, Arial 11pt
body, one section per lab (Objective · Goal · What you'll build · Step-by-step
with commands · Test it), plus setup, exam-prep and glossary. All content is
driven by course_data + the domain data files, keeping the LG 100% aligned with
the slide deck, Lesson Plan and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5; from data_domain6 import DOMAIN6
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5+DOMAIN6
import prodoc
def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

# ---------------- block DSL (single content stream → MD + DOCX) ----------------
B=[]
def h1(t): B.append(("h1",t))
def h2(t): B.append(("h2",t))
def h3(t): B.append(("h3",t))
def p(t):  B.append(("p",t))
def bullets(xs): B.append(("bullets",xs))
def steps(xs): B.append(("steps",xs))
def code(t): B.append(("code",t))
def note(t): B.append(("note",t))
def rule(): B.append(("rule",))
def img(name,cap=""): B.append(("img",name,cap))

# ---------------- content ----------------
h1("Introduction")
p(f"This Learner Guide accompanies the WSQ course {C.TITLE} ({C.COURSE_CODE}), conducted by {C.ORG}. "
  f"It provides detailed, step-by-step instructions for all 35 hands-on labs, organised by the six official "
  f"exam domains of Cisco {C.EXAM_CODE} — {C.EXAM_NAME}. Every lab maps to a published exam objective and "
  "is completed in Cisco Packet Tracer using the Cisco IOS command line, so the commands you learn here "
  "transfer directly to real Catalyst switches and ISR/Catalyst routers.")
p("Use this guide alongside the course slides and the lab folders in labs/ of the course repository. "
  "Each lab folder contains its own topology file, addressing table and mock data set. The slides carry the "
  "concepts, the diagrams and the verification criteria; this guide carries the full procedure with every "
  "command. Work through the steps in order — later steps depend on the state earlier ones create.")
p("All configuration in this course is performed in a simulated lab environment. When you apply these "
  "techniques to a production network, follow your organisation's change-management process: take a "
  "configuration backup first, schedule the change, and have a documented rollback. Several commands in "
  "this guide — clearing a MAC table, shutting an interface, applying an ACL or a CoPP policy — will "
  "interrupt live traffic if run on a production device.")

h1("Course Learning Outcomes")
bullets(C.LEARNING_OUTCOMES)

h1("The ENCOR 350-401 Exam Blueprint")
p(f"This course is built directly on the Cisco {C.EXAM_CODE} exam blueprint. The six topics are the six exam "
  "domains, in the same order and with the same weightings, so time spent in class is proportional to time "
  "spent in the exam. The official topic list is published at https://learningnetwork.cisco.com/s/encor-exam-topics.")
bullets([f"Topic {t['code']} — {t['title']} ({t['exam']}) — {t['weighting']} of the exam. {t['subtitle']}."
         for t in C.TOPICS])
p("The exam runs 120 minutes and is the core exam for both CCNP Enterprise and CCIE Enterprise. Passing it "
  "alone earns the Cisco Certified Specialist – Enterprise Core certification; CCNP Enterprise additionally "
  "requires one concentration exam such as ENARSI.")
h3("Read the verb in each objective")
bullets([
 "Configure and verify — you must know the configuration commands AND the show command that proves it worked.",
 "Troubleshoot — you are given a broken configuration and must find and fix it; the labs marked 'Troubleshoot' start broken on purpose.",
 "Describe — conceptual only; the exam will not ask you for a command, but it will ask you what a component does.",
 "Interpret — you are shown a configuration, a script or an output and asked to predict the result.",
 "Compare — you must state the differences and, usually, choose one for a given scenario.",
])

h1("Before You Start — Lab Environment Setup")
h3("What you need")
bullets([f"{name} — {desc}" for name,desc in C.LAB_TOOLS])
h3("Install and verify Cisco Packet Tracer")
p("Packet Tracer is free from the Cisco Networking Academy (netacad.com). Create a free account, download "
  "the release for your operating system, install it, and sign in on first launch — Packet Tracer requires "
  "a Networking Academy login before it will open a topology file.")
code("# Verify your install before Day 1:\n"
     "#  1. Launch Cisco Packet Tracer and sign in with your NetAcad account\n"
     "#  2. File > Open, and open any .pkt file from the labs/ folder\n"
     "#  3. Click a router, then the CLI tab — you should get a prompt\n"
     "#  4. Press Enter, then type 'enable' to reach privileged EXEC mode")
h3("The lab folder layout")
p("Every lab in this course has its own folder under labs/, containing the topology file, a README with the "
  "procedure, the addressing table, and the mock data set (CSV) the lab works with. Open the folder before "
  "you start the lab and keep the addressing table visible — most configuration errors in these labs are "
  "an address or an interface typed from memory rather than read from the table.")
code("labs/\n"
     "  README.md                     the lab index\n"
     "  tools.md                      the tool reference for the whole course\n"
     "  lab-01-cam-tcam/\n"
     "    README.md                   objectives, scenario, full step-by-step, validation\n"
     "    lab-01-cam-tcam.pkt         the Packet Tracer topology\n"
     "    addressing-table.csv        every device, interface and address\n"
     "    *.csv                       the lab's mock data set")
h3("Cisco IOS CLI conventions used throughout this guide")
bullets([
 "Router> is user EXEC mode. Type 'enable' to reach privileged EXEC (Router#), where the show commands live.",
 "Router# is privileged EXEC. Type 'configure terminal' to reach global configuration (Router(config)#).",
 "Router(config)# is global configuration. 'interface g0/0' moves to interface configuration (Router(config-if)#).",
 "'exit' moves up one level; 'end' or Ctrl-Z returns to privileged EXEC from anywhere.",
 "Commands can be abbreviated to the shortest unique string — 'sh ip int br' is 'show ip interface brief'. This guide spells them in full so you learn the real command.",
 "Tab completes a command; '?' lists what may come next. Both work at every level and are the fastest way to recover when you are unsure.",
 "'copy running-config startup-config' (or 'write memory') saves your work. A reload without it discards everything you configured.",
])
h3("Recovering when a lab goes wrong")
bullets([
 "'show running-config' shows what is actually configured — compare it against the step you thought you ran.",
 "'show ip interface brief' is the fastest health check: an interface that is administratively down needs 'no shutdown'.",
 "To remove any command, retype it with 'no' in front: 'no ip address', 'no router ospf 10'.",
 "If a topology is beyond repair, close it without saving and reopen the .pkt file to return to the starting state.",
])


# one diagram per topic, embedded so the LG carries the visuals, not just the PPT
TOPIC_IMAGES = {
 1: [("campus-tiers.png","Two-tier versus three-tier campus design — the decision is driven by the number of distribution blocks."),
     ("three-planes.png","The three planes of a network device — the model used throughout this course."),
     ("forwarding-tables.png","The forwarding tables: which one answers which question.")],
 2: [("vxlan-header.png","The VXLAN header — 50 bytes of overhead, which is why the underlay MTU must be at least 1550."),
     ("sdaccess-stack.png","Cisco SD-Access: LISP control plane, VXLAN data plane, TrustSec policy plane.")],
 3: [("stp-protection.png","Spanning Tree protection features — each defends a different failure mode."),
     ("capwap-join.png","The AP join process: CAPWAP control on UDP 5246, data on UDP 5247.")],
 4: [("sdwan-planes.png","Cisco SD-WAN's four planes and what fails when each controller is lost.")],
 5: [("aaa-flow.png","AAA and 802.1X — the three roles and which protocol runs between which pair.")],
 6: [],
}

# ---------------- per-topic, per-lab ----------------
TOPICS_BY_NUM={t["num"]:t for t in C.TOPICS}
for t in C.TOPICS:
    h1(f"Topic {t['code']} — {t['title']}  ({t['weighting']})")
    p(t["subtitle"]+".")
    p(f"Exam domain: {t['exam']}. Skills Framework mapping: {t['tsc']} of TSC {C.TSC_TITLE} ({C.TSC_CODE}).")
    h3("Key concepts")
    bullets(t["concepts"])
    for _n,_c in TOPIC_IMAGES.get(t["num"],[]):
        img(_n,_c)
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        h2(f"Lab {a['num']} — {a['title']}")
        p(f"Exam objective: {a['objective']}")
        p(f"Scenario: {a['desc']}")
        h3("What you'll build")
        p(a["build"])
        h3("Tools and devices")
        p(a["services"]+".")
        h3("Step-by-step")
        steps([(instr,cmd) for (instr,cmd) in a["steps"]])
        h3("Validation — test it")
        p(a["test"])
        note(f"The topology file, addressing table and mock data for this lab are in labs/lab-{a['num']:02d}-*/ . "
             f"Configuration commands change device state — on a production network, back up the configuration "
             f"and follow change management before running them.")
        rule()

h1("Exam Focus — Cross-Cutting Topics")
p("These topics are examined across several domains and appear in the slides, but they do not each have a "
  "dedicated hands-on lab. Study this section alongside the labs so the knowledge questions on the exam are covered.")

h3("Multicast — RPF, PIM and IGMP (Objective 3.4.d)")
p("Multicast sends one stream to many receivers without unicasting a copy to each. Three mechanisms make it work:")
bullets([
 "IGMP operates between hosts and the local router. IGMPv2 has a leave group message; IGMPv3 adds source-specific multicast, letting a host join a group only from a named source.",
 "PIM builds the distribution tree between routers. PIM Dense Mode floods then prunes and suits dense receiver populations; PIM Sparse Mode uses an explicit join to a rendezvous point and is what enterprises actually deploy.",
 "The Reverse Path Forwarding check discards any multicast packet that did not arrive on the interface the router would use to reach the source. It is what prevents multicast loops — and an RPF failure is the most common reason a stream silently does not arrive.",
 "Addresses: 224.0.0.0/4 is the multicast range. 224.0.0.5 and 224.0.0.6 are OSPF, 224.0.0.10 is EIGRP, and 224.0.0.13 is PIM.",
])

h3("Policy-Based Routing (Objective 3.2.d)")
p("PBR overrides the routing table for selected traffic. You match traffic with an ACL inside a route-map, set "
  "the next hop or exit interface, and apply the route-map to the ingress interface with 'ip policy route-map'. "
  "Use it when the business requirement contradicts the best path — sending guest traffic out a cheap link while "
  "corporate traffic takes the fast one, for example.")
code("access-list 100 permit ip 192.168.20.0 0.0.0.255 any\n"
     "route-map GUEST-PATH permit 10\n"
     "  match ip address 100\n"
     "  set ip next-hop 10.1.1.2\n"
     "interface GigabitEthernet0/1\n"
     "  ip policy route-map GUEST-PATH")

h3("Wireless Layer 1 and AP Modes (Objectives 3.3.a, 3.3.b)")
bullets([
 "RSSI is the received signal strength in dBm — a negative number, where closer to zero is stronger. Aim for about -67 dBm for a reliable data connection.",
 "SNR is the margin in dB between the signal and the noise floor. Aim for 25 dB or better; a strong signal with a high noise floor still performs badly.",
 "Bands: 2.4 GHz has three non-overlapping channels (1, 6, 11), travels further and is more congested; 5 GHz has many more channels, shorter range and far less interference.",
 "AP modes: local (normal client service), FlexConnect (branch local switching), monitor (scanning only, no clients), sniffer (packet capture), bridge/mesh, and SE-Connect for spectrum analysis.",
 "Antennas: omnidirectional radiates in all directions for general coverage; directional (Yagi, patch, dish) concentrates gain along one axis for corridors, warehouses and point-to-point links.",
])

h3("Layer 2 and Layer 3 Roaming (Objective 3.3.d)")
p("In a Layer 2 roam the client moves between APs inside the same subnet, so only the association changes and "
  "the IP address is naturally retained. In a Layer 3 roam the client crosses a subnet boundary; to keep the "
  "session alive the original controller becomes the anchor and the new one the foreign controller, and the "
  "client's traffic is tunnelled back to the anchor so the IP address survives. Design so that most roams are "
  "Layer 2 — Layer 3 roaming works, but every roamed client adds a tunnel.")

h3("Virtual Switching and the Hypervisor (Objectives 2.1.a–c)")
bullets([
 "A Type 1 hypervisor (ESXi, KVM, Hyper-V) runs on bare metal and is what production uses; a Type 2 (Workstation, VirtualBox, Fusion) runs on a host OS and suits a lab.",
 "A virtual switch moves the access layer inside the host. Traffic between two VMs on the same host and vSwitch never reaches a physical switch — so your physical ACLs, SPAN sessions and IPS never see it.",
 "That blind spot is the reason for distributed virtual switches and for putting policy in the hypervisor: if you cannot see the traffic, you cannot filter it.",
])

h3("REST API Security (Objective 5.3)")
bullets([
 "Transport — always HTTPS/TLS. An API over plain HTTP exposes the token on every call.",
 "Authentication — use a short-lived token or OAuth 2.0, never credentials embedded in the script or the URL.",
 "Authorization — scope the token to the least privilege the integration needs; a read-only integration must not hold a write token.",
 "Rate limiting — protects the API from both abuse and a buggy client in a loop; expect HTTP 429 when you exceed it.",
 "Input validation — validate on the server, never only in the client, and never build a query by string concatenation.",
 "Secret handling — tokens belong in an environment variable or a secrets manager, never committed to a repository.",
])

h3("Network Security Design Components (Objective 5.5)")
bullets([
 "Threat defence — IPS/NGIPS inspects traffic for known attack signatures and anomalous behaviour.",
 "Endpoint security — AMP or an equivalent EDR agent on the host, because not all traffic crosses a chokepoint.",
 "Next-generation firewall — application-aware and identity-aware, so policy is written about users and applications rather than ports.",
 "TrustSec — an SGT applied at ingress and enforced as an SGACL at egress, so policy follows identity rather than IP address and survives DHCP and mobility.",
 "MACsec — 802.1AE hop-by-hop Layer 2 encryption, protecting the link itself rather than the session.",
 "Network access control — 802.1X where the endpoint can run a supplicant, MAB with profiling where it cannot, and WebAuth for guests.",
])

h1("Exam Preparation")
h3("How to revise")
bullets([
 "Work the blueprint objective by objective and rate your confidence on each. Anything below 'I could configure this from memory' goes on the revision list.",
 "Rebuild every lab from a blank configuration. Reading the procedure is not the same as recalling it — the exam tests recall.",
 "For each 'configure and verify' objective, be able to write the configuration AND name the show command that proves it.",
 "Learn the defaults: STP priority 32768 in increments of 4096, HSRP priority 100 with preemption OFF, VRRP preemption ON, OSPF hello 10 seconds on broadcast, BGP TCP port 179.",
 "Learn the port numbers: CAPWAP 5246 control and 5247 data, NETCONF 830, RESTCONF 443, VXLAN UDP 4789, TACACS+ TCP 49, RADIUS UDP 1812/1813 (or 1645/1646), BGP TCP 179, syslog UDP 514, SNMP UDP 161/162.",
])
h3("Take the practice exam")
p(f"The matching practice exam for this course is at {C.PRACTICE_EXAM_URL} — 200 original questions across "
  "two full 100-question exams, each 120 minutes, weighted to the same six domains. Use Practice mode while "
  "you are still learning, because it explains every answer immediately. Switch to Exam mode in your final "
  "week, because 100 questions in 120 minutes is about 72 seconds per question and the pacing is what catches "
  "people out. A free sample exam is available without payment details.")
h3("On exam day")
bullets([
 "Read the whole question before the options — ENCOR questions often turn on one qualifier such as 'directly connected' or 'GUI only'.",
 "Eliminate answers that are true but do not answer the question asked. Several options are usually factually correct.",
 "For configuration questions, mentally run the commands in order and check the mode each one needs.",
 "Flag and move on. A question you cannot place in 90 seconds is costing you two you could have answered.",
])

h1("Glossary")
gl=[
 ("CAM","Content Addressable Memory — the switch MAC address table. Exact-match lookup of MAC to port and VLAN."),
 ("TCAM","Ternary CAM — stores masked entries, which is what ACLs and QoS policies need. CAM cannot hold them."),
 ("RIB","Routing Information Base — the routing table; the control plane's chosen best routes from every source."),
 ("FIB","Forwarding Information Base — CEF's hardware-ready copy of the RIB, built before any traffic arrives."),
 ("CEF","Cisco Express Forwarding — topology-based switching using the FIB and adjacency table. The default and the fastest."),
 ("Adjacency table","Holds the Layer 2 rewrite string for each next hop, so CEF can build the new frame header in hardware."),
 ("FHRP","First Hop Redundancy Protocol — HSRP, VRRP or GLBP, giving hosts one virtual gateway that survives a router failure."),
 ("HSRP","Hot Standby Router Protocol — Cisco's FHRP. Active/Standby, default priority 100, preemption OFF by default."),
 ("VRRP","Virtual Router Redundancy Protocol — the IEEE standard FHRP. Master/Backup, preemption ON by default."),
 ("GLBP","Gateway Load Balancing Protocol — Cisco FHRP that also load-balances across multiple forwarders."),
 ("SSO / NSF","Stateful Switchover keeps the standby supervisor in sync; Non-Stop Forwarding keeps forwarding while routing reconverges."),
 ("DTP","Dynamic Trunking Protocol — negotiates trunking automatically. Convenient and insecure; disable with 'switchport nonegotiate'."),
 ("Native VLAN","The VLAN sent untagged on an 802.1Q trunk. A mismatch between ends causes VLAN leaking."),
 ("EtherChannel","Bundling of up to eight physical links into one logical link. Negotiated by PAgP (Cisco) or LACP (IEEE 802.3ad)."),
 ("PAgP / LACP","Port Aggregation Protocol (desirable/auto) and Link Aggregation Control Protocol (active/passive). Two passive or two auto ends never form a bundle."),
 ("STP / RSTP / MST","Spanning Tree (802.1D), Rapid Spanning Tree (802.1w, converges in seconds) and Multiple Spanning Tree (802.1s, many VLANs onto few instances)."),
 ("BPDU","Bridge Protocol Data Unit — the frame switches exchange to build and maintain the spanning tree."),
 ("Root guard / BPDU guard","Root guard stops a superior BPDU moving the root; BPDU guard err-disables a PortFast port that receives any BPDU."),
 ("EIGRP","Enhanced Interior Gateway Routing Protocol — advanced distance vector using DUAL, with successors and feasible successors."),
 ("Feasible successor","A guaranteed loop-free EIGRP backup path whose reported distance is below the current feasible distance."),
 ("OSPF","Open Shortest Path First — link-state protocol. Every router floods LSAs, builds an identical LSDB per area, and runs Dijkstra's SPF."),
 ("LSA / LSDB","Link State Advertisement and Link State Database. Type 1 router, Type 2 network, Type 3 summary, Type 5 external, Type 7 NSSA external."),
 ("ABR / ASBR","Area Border Router (interfaces in two areas) and Autonomous System Boundary Router (redistributes external routes)."),
 ("eBGP","External BGP — a path-vector protocol between autonomous systems over TCP 179, with a multi-step best-path algorithm."),
 ("PBR","Policy-Based Routing — overriding the routing table for selected traffic using a route-map matched on an ACL."),
 ("VRF","Virtual Routing and Forwarding — multiple independent routing tables on one device, allowing overlapping address space."),
 ("GRE","Generic Routing Encapsulation — a simple multiprotocol tunnel supporting routing protocols and multicast, with no encryption at all."),
 ("IPsec","A suite providing confidentiality, integrity, authentication and anti-replay. IKE Phase 1 builds the management tunnel, Phase 2 the data SAs."),
 ("LISP","Locator/ID Separation Protocol — separates the endpoint identifier (EID) from its routing locator (RLOC). The SD-Access control plane."),
 ("VXLAN","Virtual Extensible LAN — Layer 2 over UDP 4789 with a 24-bit VNI, giving 16 million segments and 50 bytes of overhead."),
 ("CAPWAP","Control And Provisioning of Wireless Access Points — the AP-to-WLC tunnel. Control on UDP 5246, data on UDP 5247."),
 ("RSSI / SNR","Received Signal Strength Indicator in dBm, and Signal-to-Noise Ratio in dB. Target roughly -67 dBm and 25 dB."),
 ("NAT / PAT","Network Address Translation, and Port Address Translation (overload) which shares one public address across many hosts by also translating the port."),
 ("NTP / PTP","Network Time Protocol (millisecond accuracy, stratum hierarchy) and Precision Time Protocol (sub-microsecond, hardware timestamped)."),
 ("NetFlow","Flow records answering who talked to whom, how much and for how long. Flexible NetFlow is built from a record, an exporter and a monitor."),
 ("SPAN / RSPAN / ERSPAN","Port mirroring locally, across a dedicated VLAN to another switch, and encapsulated in GRE across a routed network."),
 ("IP SLA","Synthetic probes measuring latency, jitter and loss continuously; can drive a tracked object that withdraws a route on failure."),
 ("AAA","Authentication, Authorization and Accounting. Always configure a local fallback method so a server outage cannot lock you out."),
 ("TACACS+ / RADIUS","TACACS+ encrypts the whole payload over TCP 49 and separates authn from authz — used for device administration. RADIUS uses UDP and encrypts only the password — used for network access."),
 ("CoPP","Control Plane Policing — a QoS policy applied to the control plane, rate-limiting traffic to the CPU so a flood cannot stop the device routing."),
 ("802.1X","Port-based network access control with three roles: supplicant, authenticator and authentication server. EAPOL carries EAP to the authenticator."),
 ("MAB","MAC Authentication Bypass — authenticating a device by its MAC address, for printers and cameras that cannot run a supplicant. Weak, so pair it with profiling."),
 ("4-way handshake","The WPA2/WPA3 exchange that derives fresh session keys (PTK/GTK) from the PMK, proving both sides hold the key without ever sending it."),
 ("TrustSec / SGT","Cisco's identity-based segmentation. A Security Group Tag is applied at ingress and enforced as an SGACL at egress."),
 ("MACsec","IEEE 802.1AE hop-by-hop Layer 2 encryption, protecting the link rather than the session."),
 ("YANG","A data modelling language defining the structure and constraints of configuration and operational data, carried by NETCONF and RESTCONF."),
 ("NETCONF","XML configuration protocol over SSH port 830, with candidate/running datastores and transactional commits that roll back cleanly."),
 ("RESTCONF","The same YANG models exposed as HTTPS REST on port 443 using GET, POST, PUT, PATCH and DELETE, with JSON or XML."),
 ("EEM","Embedded Event Manager — on-device automation. An event detector triggers an applet whose numbered actions run CLI commands."),
 ("Idempotency","Running the same configuration operation twice produces no second change. What makes an Ansible playbook safe to re-run."),
 ("SD-WAN planes","vBond orchestration, vSmart control (OMP), vManage management, and vEdge/cEdge data plane."),
 ("SD-Access","VXLAN data plane over any routed underlay, LISP control plane, TrustSec policy plane, managed by Cisco DNA Center."),
]
B.append(("dl",gl))

# ---------------- render Markdown ----------------
def _anchor(txt):
    return "".join(ch.lower() if ch.isalnum() else ("-" if ch in " -" else "") for ch in txt)

def render_md():
    out=[f"# {C.TITLE} — Learner Guide",""]
    out.append(f"**WSQ Course Code:** {C.COURSE_CODE}  |  **Conducted by:** {C.ORG} ({C.UEN.replace('UEN: ','UEN ')})  |  **Version {C.VERSION} · {C.VERSION_DATE}**")
    out.append("")
    # TOC (h1 + h2)
    out.append("## Contents"); out.append("")
    for kind,*rest in B:
        if kind=="h1": out.append(f"- [{rest[0]}](#{_anchor(rest[0])})")
        elif kind=="h2": out.append(f"  - [{rest[0]}](#{_anchor(rest[0])})")
    out.append("")
    for kind,*rest in B:
        if kind=="h1": out+=["",f"## {rest[0]}",""]
        elif kind=="h2": out+=["",f"### {rest[0]}",""]
        elif kind=="h3": out+=[f"**{rest[0]}**",""]
        elif kind=="p": out+=[rest[0],""]
        elif kind=="bullets": out+=[f"- {x}" for x in rest[0]]+[""]
        elif kind=="steps":
            for i,(instr,cmd) in enumerate(rest[0],1):
                out.append(f"{i}. {instr}")
                if cmd: out+=["",f"   ```bash",f"   {cmd}","   ```",""]
            out.append("")
        elif kind=="code": out+=["```bash",rest[0],"```",""]
        elif kind=="note": out+=[f"> **Note:** {rest[0]}",""]
        elif kind=="img":
            out+=[f"![{rest[1]}](courseware/assets/{rest[0]})","",f"*{rest[1]}*",""]
        elif kind=="rule": out+=["---",""]
        elif kind=="dl":
            for term,defn in rest[0]: out.append(f"- **{term}** — {defn}")
            out.append("")
    return "\n".join(out)

MD_OUT=os.path.join(REPO,f"LG-{C.SHORT_TITLE}.md")
with open(MD_OUT,"w") as f: f.write(render_md())
print("Saved",MD_OUT)

# ---------------- render DOCX ----------------
BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
INKCODE=RGBColor(0x0B,0x30,0x60)
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)
prodoc.add_cover_page(doc,"LEARNER GUIDE",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=None, course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("5.0","1 April 2024","Previous release — CCNP ENCOR Learner Guide built on the legacy master trainer slides and discovery exercises.",C.TRAINER),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,"Full rebuild against the Cisco ENCOR 350-401 v1.1 exam blueprint. Six topics realigned to the six exam domains with their published weightings; 35 hands-on Packet Tracer labs with complete step-by-step procedures replacing the legacy discovery exercises; added an Exam Focus section covering multicast, policy-based routing, wireless Layer 1, roaming, virtual switching, REST API security and security design; added a 50-term glossary and an exam preparation section.",C.TRAINER),
])
prodoc.add_toc(doc)


# ---- per-list numbering restart -------------------------------------------------
# python-docx's "List Number" style shares ONE numbering instance across the whole
# document, so every lab would continue 1..516. Clone the abstract numbering into a
# fresh w:num for each steps block and point the paragraphs at it, so each lab
# restarts at 1 — which is what a learner following a single lab needs.
from docx.oxml.ns import qn as _qn
from docx.oxml import OxmlElement as _El

def _numbering_part(doc):
    return doc.part.numbering_part.element

def _abstract_id_of_list_number(doc):
    """Find the DECIMAL abstract numbering (List Number), not the bullet one.

    numbering.xml carries several abstractNum definitions; picking the first w:num
    blindly lands on the bullet definition and every step renders as a dot. Match on
    numFmt="decimal" at level 0, and fall back to the style link.
    """
    numbering=_numbering_part(doc)
    for an in numbering.findall(_qn('w:abstractNum')):
        lvl=an.find(_qn('w:lvl'))
        if lvl is None: continue
        fmt=lvl.find(_qn('w:numFmt'))
        if fmt is not None and fmt.get(_qn('w:val'))=='decimal':
            return an.get(_qn('w:abstractNumId'))
    for an in numbering.findall(_qn('w:abstractNum')):
        sl=an.find(_qn('w:styleLink')) or an.find(_qn('w:numStyleLink'))
        if sl is not None and 'Number' in (sl.get(_qn('w:val')) or ''):
            return an.get(_qn('w:abstractNumId'))
    return None

def _new_num_instance(doc):
    """Create a fresh w:num on the List Number abstract numbering, with an explicit
    level override that RESTARTS the count at 1.

    A new w:num alone is not enough: Word and LibreOffice both continue the shared
    abstract counter unless the instance carries <w:lvlOverride><w:startOverride/>.
    Without it the LG numbers every lab's steps 1..516 in one run.
    """
    numbering=_numbering_part(doc)
    aid=_abstract_id_of_list_number(doc)
    if aid is None: return None
    used=[int(n.get(_qn('w:numId'))) for n in numbering.findall(_qn('w:num'))]
    new_id=(max(used)+1) if used else 1
    num=_El('w:num'); num.set(_qn('w:numId'),str(new_id))
    a=_El('w:abstractNumId'); a.set(_qn('w:val'),aid); num.append(a)
    ov=_El('w:lvlOverride'); ov.set(_qn('w:ilvl'),'0')
    so=_El('w:startOverride'); so.set(_qn('w:val'),'1'); ov.append(so)
    num.append(ov)
    numbering.append(num)
    return new_id

def _set_num_id(par,num_id):
    pPr=par._p.get_or_add_pPr()
    numPr=pPr.find(_qn('w:numPr'))
    if numPr is None:
        numPr=_El('w:numPr'); pPr.append(numPr)
    for tag,val in (('w:ilvl','0'),('w:numId',str(num_id))):
        el=numPr.find(_qn(tag))
        if el is None:
            el=_El(tag); numPr.append(el)
        el.set(_qn('w:val'),val)

def code_para(text):
    for line in text.split("\n"):
        para=doc.add_paragraph(); prodoc._shade_para(para) if hasattr(prodoc,"_shade_para") else None
        r=para.add_run(line); r.font.name="Consolas"; r.font.size=Pt(9.5); r.font.color.rgb=INKCODE

for kind,*rest in B:
    if kind=="h1": doc.add_heading(rest[0],level=1)
    elif kind=="h2": doc.add_heading(rest[0],level=2)
    elif kind=="h3":
        para=doc.add_paragraph(); r=para.add_run(rest[0]); r.bold=True; r.font.size=Pt(11); r.font.color.rgb=BRAND
    elif kind=="p": doc.add_paragraph(rest[0])
    elif kind=="bullets":
        for x in rest[0]: doc.add_paragraph(x,style="List Bullet")
    elif kind=="steps":
        _nid=_new_num_instance(doc)          # a fresh list -> this lab restarts at 1
        for i,(instr,cmd) in enumerate(rest[0],1):
            para=doc.add_paragraph(style="List Number"); para.add_run(instr)
            if _nid: _set_num_id(para,_nid)
            if cmd: code_para(cmd)
    elif kind=="code": code_para(rest[0])
    elif kind=="note":
        para=doc.add_paragraph(); r=para.add_run("Note: "); r.bold=True; r.font.color.rgb=BRAND
        para.add_run(rest[0]).font.size=Pt(10)
    elif kind=="img":
        _p=os.path.join(REPO,"courseware","assets",rest[0])
        if os.path.exists(_p):
            _par=doc.add_paragraph(); _par.alignment=WD_ALIGN_PARAGRAPH.CENTER
            _par.add_run().add_picture(_p,width=Inches(6.2))
            _cap=doc.add_paragraph(); _cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
            _r=_cap.add_run(rest[1]); _r.italic=True; _r.font.size=Pt(9.5); _r.font.color.rgb=GREY
    elif kind=="rule": doc.add_paragraph("")
    elif kind=="dl":
        for term,defn in rest[0]:
            para=doc.add_paragraph(style="List Bullet")
            r=para.add_run(term+" — "); r.bold=True; para.add_run(defn)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
DOCX_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.docx")
doc.save(DOCX_OUT)
print("Saved",DOCX_OUT)
