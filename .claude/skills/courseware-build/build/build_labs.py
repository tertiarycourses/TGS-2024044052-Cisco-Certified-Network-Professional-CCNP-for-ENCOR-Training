#!/usr/bin/env python3
"""Generate the labs/ tree: one folder per lab with README, addressing table and mock data.

Driven by the same course_data + data_domainN single source as the PPT, LP and LG,
so lab numbering, titles, objectives and steps can never drift from the courseware.

Each lab folder contains:
  labs/lab-NN-<slug>/
    README.md              objectives, scenario, step-by-step, validation, checkpoints, exam focus
    addressing-table.csv   every device, interface and address used by the lab
    <mock data>.csv        the lab's data set (device inventory, flows, ACL matrix, …)
    topology.md            the ASCII topology diagram
"""
import os, sys, csv, re

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5; from data_domain6 import DOMAIN6
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4+DOMAIN5+DOMAIN6
TOPICS={t["num"]:t for t in C.TOPICS}

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)
LABS=os.path.join(REPO,"labs")

# ------------------------------------------------------------------ slugs
SLUGS={
 1:"cam-tcam", 2:"cef", 3:"campus-design", 4:"qos", 5:"sdwan-sdaccess",
 6:"vrf-lite", 7:"gre", 8:"ipsec-vpn", 9:"lisp-vxlan",
 10:"trunking-dtp", 11:"etherchannel", 12:"rstp", 13:"mst", 14:"stp-hardening",
 15:"eigrp-ospf", 16:"ospf-multiarea", 17:"ospfv3", 18:"ebgp",
 19:"wlc-wlan", 20:"wlan-troubleshoot", 21:"ip-services",
 22:"diagnostics", 23:"netflow-syslog", 24:"span-ipsla", 25:"netconf-restconf",
 26:"secure-access", 27:"aaa", 28:"acls", 29:"copp", 30:"security-design",
 31:"python", 32:"json", 33:"yang-dnac", 34:"eem", 35:"orchestration",
}

# ------------------------------------------------------------------ mock data
# addressing-table.csv per lab — drawn from the reference Packet Tracer topologies
ADDRESSING={
 1:[["Device","Interface","IP Address","Subnet Mask","VLAN","Notes"],
    ["S1","VLAN 10","192.168.10.2","255.255.255.0","10","Access switch under test"],
    ["S2","VLAN 10","192.168.10.3","255.255.255.0","10","Second access switch"],
    ["PC-A","NIC","192.168.10.10","255.255.255.0","10","MAC 000c.1234.5678, port F0/1"],
    ["PC-B","NIC","192.168.10.20","255.255.255.0","10","MAC 000c.8765.4321, port F0/2"],
    ["R1","G0/0","192.168.10.1","255.255.255.0","10","Default gateway"]],
 2:[["Device","Interface","IP Address","Subnet Mask","Notes"],
    ["R1","G0/0","192.168.10.1","255.255.255.0","LAN side"],
    ["R1","S0/0/0","10.1.1.1","255.255.255.252","Link to R2"],
    ["R2","S0/0/0","10.1.1.2","255.255.255.252","Link to R1"],
    ["R2","G0/0","192.168.20.1","255.255.255.0","Remote LAN"],
    ["PC-A","NIC","192.168.10.10","255.255.255.0","Gateway 192.168.10.1"],
    ["PC-B","NIC","192.168.20.10","255.255.255.0","Gateway 192.168.20.1"]],
 3:[["Device","Role","Management IP","Subnet Mask","Building","Notes"],
    ["SW-ACC-1","Access","10.10.1.11","255.255.255.0","A","24 x PoE edge ports"],
    ["SW-ACC-2","Access","10.10.1.12","255.255.255.0","A","24 x PoE edge ports"],
    ["SW-DIST-1","Distribution","10.10.1.1","255.255.255.0","A","L2/L3 boundary, HSRP active"],
    ["SW-DIST-2","Distribution","10.10.1.2","255.255.255.0","A","L2/L3 boundary, HSRP standby"],
    ["SW-ACC-3","Access","10.10.2.11","255.255.255.0","B","Merged company"],
    ["SW-DIST-3","Distribution","10.10.2.1","255.255.255.0","B","Merged company"]],
 4:[["Device","Interface","IP Address","Subnet Mask","Notes"],
    ["R1","G0/0","192.168.1.1","255.255.255.0","LAN with IP phones"],
    ["R1","S0/0/0","10.1.1.1","255.255.255.252","WAN, QoS applied outbound"],
    ["SW-1","VLAN 1","192.168.1.2","255.255.255.0","Access switch, trust boundary"],
    ["IP Phone","NIC","192.168.100.10","255.255.255.0","Voice VLAN 100, marks DSCP EF"],
    ["PC-A","NIC","192.168.1.10","255.255.255.0","Data VLAN 1, behind the phone"],
    ["WLC-1","Management","192.168.200.254","255.255.255.0","Wireless QoS / WMM mapping"]],
 5:[["Component","Plane","Address","Solution","Notes"],
    ["vBond-1","Orchestration","203.0.113.10","SD-WAN","Must be publicly reachable"],
    ["vSmart-1","Control","10.200.0.11","SD-WAN","Distributes OMP routes and policy"],
    ["vManage-1","Management","10.200.0.10","SD-WAN","GUI, API and templates"],
    ["cEdge-BR1","Data","10.201.1.1","SD-WAN","Branch 1 router"],
    ["cEdge-BR2","Data","10.201.2.1","SD-WAN","Branch 2 router"],
    ["DNAC-1","Management","10.100.0.10","SD-Access","Cisco DNA Center"],
    ["CP-Node-1","Control","10.100.1.1","SD-Access","LISP map server / map resolver"],
    ["Border-1","Border","10.100.1.2","SD-Access","Fabric border node"],
    ["Edge-1","Edge","10.100.1.11","SD-Access","Fabric edge node"]],
 6:[["Device","Interface","VRF","IP Address","Subnet Mask","Notes"],
    ["R1","G0/0","CORP","192.168.1.1","255.255.255.0","Overlapping prefix, corporate"],
    ["R1","G0/1","GUEST","192.168.1.1","255.255.255.0","Overlapping prefix, guest"],
    ["CORP-PC","NIC","CORP","192.168.1.10","255.255.255.0","Gateway 192.168.1.1 in CORP"],
    ["GUEST-PC","NIC","GUEST","192.168.1.10","255.255.255.0","Gateway 192.168.1.1 in GUEST"]],
 7:[["Device","Interface","IP Address","Subnet Mask","Default Gateway","Notes"],
    ["RA","G0/0","192.168.1.1","255.255.255.0","N/A","Head office LAN"],
    ["RA","S0/0/0","64.103.211.2","255.255.255.252","N/A","Public, tunnel source"],
    ["RA","Tunnel0","10.10.10.1","255.255.255.252","N/A","GRE tunnel"],
    ["RB","G0/0","192.168.2.1","255.255.255.0","N/A","Branch LAN"],
    ["RB","S0/0/0","209.165.122.2","255.255.255.252","N/A","Public, tunnel source"],
    ["RB","Tunnel0","10.10.10.2","255.255.255.252","N/A","GRE tunnel"],
    ["PCA","NIC","192.168.1.2","255.255.255.0","192.168.1.1","Head office host"],
    ["PCB","NIC","192.168.2.2","255.255.255.0","192.168.2.1","Branch host"]],
 8:[["Device","Interface","IP Address","Subnet Mask","Default Gateway","Notes"],
    ["R1","G0/0","192.168.1.1","255.255.255.0","N/A","Site 1 LAN"],
    ["R1","S0/0/0","10.1.1.2","255.255.255.252","N/A","VPN peer interface"],
    ["R2","S0/0/0","10.1.1.1","255.255.255.252","N/A","ISP, transit only"],
    ["R2","S0/0/1","10.2.2.1","255.255.255.252","N/A","ISP, transit only"],
    ["R3","G0/0","192.168.3.1","255.255.255.0","N/A","Site 3 LAN"],
    ["R3","S0/0/1","10.2.2.2","255.255.255.252","N/A","VPN peer interface"],
    ["PC-A","NIC","192.168.1.3","255.255.255.0","192.168.1.1","Interesting traffic source"],
    ["PC-C","NIC","192.168.3.3","255.255.255.0","192.168.3.1","Interesting traffic destination"]],
 9:[["Component","Role","EID / RLOC","VNI / Address","Notes"],
    ["Host-A","Endpoint","EID 10.10.10.10","VNI 10001","Roams between edge nodes"],
    ["Edge-1","Edge node / xTR","RLOC 10.100.1.11","VNI 10001","Host-A's original attachment"],
    ["Edge-2","Edge node / xTR","RLOC 10.100.1.12","VNI 10001","Host-A's attachment after the roam"],
    ["CP-Node-1","Map server / resolver","10.100.1.1","N/A","Holds the EID-to-RLOC bindings"],
    ["Border-1","Border node","10.100.1.2","N/A","Fabric exit to the rest of the network"],
    ["Host-B","Endpoint","EID 10.10.20.20","VNI 10002","Different VNI, no L2 adjacency to Host-A"]],
 10:[["Device","Interface","IP Address","Subnet Mask","VLAN","Notes"],
    ["S1","VLAN 99","192.168.99.1","255.255.255.0","99","Management, native VLAN"],
    ["S2","VLAN 99","192.168.99.2","255.255.255.0","99","Management, native VLAN"],
    ["S3","VLAN 99","192.168.99.3","255.255.255.0","99","Management, native VLAN"],
    ["PC0","NIC","192.168.10.1","255.255.255.0","10","Unaffected user"],
    ["PC1","NIC","192.168.20.1","255.255.255.0","20","AFFECTED — cannot reach server"],
    ["PC2","NIC","192.168.30.1","255.255.255.0","30","Unaffected user"],
    ["Server","NIC","192.168.20.100","255.255.255.0","20","File server for VLAN 20"]],
 11:[["Channel Group","Switches","Member Ports","Protocol","Expected Mode","Fault Injected"],
    ["Po1","S1 – S3","F0/21, F0/22","PAgP","desirable / auto","Speed and duplex mismatch on F0/22"],
    ["Po2","S1 – S2","G0/1, G0/2","LACP","active / passive","Both ends left passive"],
    ["Po3","S2 – S3","F0/23, F0/24","LACP","active / active","PAgP on one end, LACP on the other"]],
 12:[["Device","Bridge Priority","MAC Address","Role Before","Role After","Notes"],
    ["S1","32769","0001.aaaa.1111","Non-root","ROOT (priority 4096)","Intended root bridge"],
    ["S2","32769","0002.bbbb.2222","Non-root","Secondary root (28672)","Intended backup root"],
    ["S3","32769","0003.cccc.3333","ROOT (wrong)","Non-root","Access switch, wrongly root"],
    ["PC-A","N/A","000c.dddd.4444","N/A","N/A","Used to time convergence"]],
 13:[["MST Instance","VLAN Range","Root Switch","Secondary","Notes"],
    ["Instance 0 (IST)","Unmapped VLANs","S1","S2","The internal spanning tree"],
    ["Instance 1","1-100","S1","S2","First half of the campus VLANs"],
    ["Instance 2","101-200","S2","S1","Second half — load distribution"]],
 14:[["Port","Switch","Role","Feature Applied","Expected Behaviour"],
    ["F0/1","S1","Access / edge","PortFast + BPDU guard","Instant forwarding; err-disable on any BPDU"],
    ["F0/2","S1","Access / edge","PortFast + BPDU guard","Instant forwarding; err-disable on any BPDU"],
    ["G0/1","S1","Uplink to distribution","Root guard","Root-inconsistent on a superior BPDU"],
    ["G0/2","S1","Uplink to distribution","Root guard + loop guard","Protected against rogue root and unidirectional link"],
    ["F0/24","S1","Rogue switch port","PortFast + BPDU guard","Test port — plug the rogue switch here"]],
 15:[["Device","Interface","IP Address","Subnet Mask","Bandwidth (kbps)","Notes"],
    ["R1","G0/0","172.16.1.1","255.255.255.0","1000000","LAN"],
    ["R1","S0/0/0","172.16.3.1","255.255.255.252","1544","Slow path to R2"],
    ["R1","S0/0/1","192.168.10.5","255.255.255.252","64","Very slow path to R3"],
    ["R2","G0/0","172.16.2.1","255.255.255.0","1000000","LAN"],
    ["R2","S0/0/0","172.16.3.2","255.255.255.252","1544","Path to R1"],
    ["R3","G0/0","192.168.1.1","255.255.255.0","1000000","LAN"],
    ["R3","S0/0/0","192.168.10.6","255.255.255.252","64","Path to R1"]],
 16:[["Device","Interface","IP Address","Subnet Mask","OSPF Area","Router ID"],
    ["R1","G0/0","172.16.1.1","255.255.255.0","1","1.1.1.1"],
    ["R1","S0/0/0","172.16.3.1","255.255.255.252","0","1.1.1.1"],
    ["R1","S0/0/1","192.168.10.5","255.255.255.252","0","1.1.1.1"],
    ["R2","G0/0","172.16.2.1","255.255.255.0","1","2.2.2.2"],
    ["R2","S0/0/0","172.16.3.2","255.255.255.252","0","2.2.2.2"],
    ["R3","G0/0","192.168.1.1","255.255.255.0","2","3.3.3.3"],
    ["R3","S0/0/0","192.168.10.6","255.255.255.252","0","3.3.3.3"],
    ["PC1","NIC","172.16.1.10","255.255.255.0","N/A","Gateway 172.16.1.1"],
    ["PC3","NIC","192.168.1.10","255.255.255.0","N/A","Gateway 192.168.1.1"]],
 17:[["Device","Interface","IPv6 Address","Link-Local","OSPFv3 Area","Router ID"],
    ["RA","G0/0","2001:db8:1:a1::1/64","fe80::a","1","1.1.1.1"],
    ["RA","G0/1","2001:db8:1:a2::1/64","fe80::a","1","1.1.1.1"],
    ["RA","S0/0/0","2001:db8:1:ab::2/64","fe80::a","0","1.1.1.1"],
    ["RB","G0/0","2001:db8:1:b1::1/64","fe80::b","0","2.2.2.2"],
    ["RB","S0/0/0","2001:db8:1:ab::1/64","fe80::b","0","2.2.2.2"],
    ["RB","S0/0/1","2001:db8:1:bc::1/64","fe80::b","0","2.2.2.2"],
    ["RC","G0/0","2001:db8:1:c1::1/64","fe80::c","2","3.3.3.3"],
    ["RC","G0/1","2001:db8:1:d2::1/64","fe80::c","2","3.3.3.3"],
    ["RC","S0/0/1","2001:db8:1:bc::2/64","fe80::c","0","3.3.3.3"]],
 18:[["Device","Interface","IP Address","Subnet Mask","AS Number","Notes"],
    ["ACME1","G0/0","192.168.0.1","255.255.255.0","65001","Customer LAN"],
    ["ACME1","S0/0/0","1.1.1.2","255.255.255.252","65001","eBGP peer to ISP-Entry-1"],
    ["ACME1","S0/0/1","1.1.1.6","255.255.255.252","65001","eBGP peer to ISP-Entry-2"],
    ["ISP-Entry-1","S0/0/0","1.1.1.1","255.255.255.252","65000","Primary provider entry"],
    ["ISP-Entry-1","S0/0/1","1.1.1.5","255.255.255.252","65000","Secondary link"],
    ["ISP-Entry-2","S0/0/0","1.1.1.9","255.255.255.252","65000","Second provider entry"],
    ["OtherCo1","G0/0","172.16.10.1","255.255.255.0","65002","Remote AS to reach"],
    ["Server","NIC","172.16.10.2","255.255.255.0","N/A","Reachability test target"]],
 19:[["Device","Interface","IP Address","VLAN","Notes"],
    ["R-1","G0/0/1.5","192.168.5.1/24","5","Wireless client VLAN gateway"],
    ["R-1","G0/0/1.200","192.168.200.1/24","200","Management VLAN gateway"],
    ["R-1","G0/0/0","172.31.1.1/24","N/A","Server VLAN gateway"],
    ["SW-1","VLAN 200","192.168.200.100/24","200","Access switch management"],
    ["WLC-1","Management","192.168.200.254/24","200","Controller management interface"],
    ["WLC-1","Dynamic (VLAN 5)","192.168.5.254/24","5","Wireless client interface"],
    ["LAP-1","G0","DHCP","200","Joins the WLC over CAPWAP"],
    ["RADIUS Server","NIC","172.31.1.254/24","N/A","WPA2-Enterprise authentication"],
    ["Admin PC","NIC","192.168.200.200/24","200","Runs the WLC GUI"],
    ["Wireless Host","Wireless NIC","DHCP","5","Guest and corporate test client"]],
 20:[["Device","Interface","IP Address","VLAN","Fault"],
    ["R1","G0/0/0.10","192.168.10.1/24","10","—"],
    ["R1","G0/0/0.20","192.168.20.1/24","20","—"],
    ["R1","G0/0/0.200","192.168.200.1/24","200","—"],
    ["R1","G0/0/1","172.31.1.1/24","N/A","—"],
    ["SW1","VLAN 200","192.168.200.100/24","200","—"],
    ["WLC-1","Management","192.168.200.254/24","200","—"],
    ["LAP-1","G0","DHCP","200","—"],
    ["RADIUS Server","NIC","172.31.1.254/24","N/A","Fault 3: shared secret mismatch"],
    ["Admin PC","NIC","192.168.200.200/24","200","—"],
    ["Laptop1","Wireless0","DHCP","10","Fault 1: cannot see the SSID"],
    ["Laptop2","Wireless0","DHCP","20","Fault 2: associates but no IP address"]],
 21:[["Device","Interface","IP Address","Subnet Mask","Service","Notes"],
    ["R1","G0/1","192.168.1.1","255.255.255.0","HSRP","Active, priority 110, preempt"],
    ["R1","S0/0/0","209.165.200.226","255.255.255.0","NTP + NAT","NTP master stratum 3, NAT outside"],
    ["R1","G0/0","192.168.10.1","255.255.255.0","NAT","NAT inside"],
    ["R3","G0/1","192.168.1.3","255.255.255.0","HSRP","Standby, default priority 100"],
    ["HSRP Virtual","Virtual","192.168.1.254","255.255.255.0","HSRP","Group 1 virtual IP"],
    ["R2","G0/0","209.165.200.227","255.255.255.0","NTP","NTP client of R1"],
    ["PC-A","NIC","192.168.1.101","255.255.255.0","N/A","Gateway 192.168.1.254 (virtual)"],
    ["PC1","NIC","192.168.10.10","255.255.255.0","N/A","NAT inside host"]],
 22:[["Device","Interface","IP Address","Subnet Mask","MTU","Notes"],
    ["R1","G0/1","192.168.1.1","255.255.255.0","1500","Source of the diagnostics"],
    ["R1","S0/0/0","10.1.1.1","255.255.255.252","1400","MTU reduced — the injected fault"],
    ["R2","S0/0/0","10.1.1.2","255.255.255.252","1400","Transit"],
    ["R2","S0/0/1","10.2.2.1","255.255.255.252","1500","Transit"],
    ["R3","S0/0/1","10.2.2.2","255.255.255.252","1500","Far end"],
    ["R3","G0/1","192.168.3.1","255.255.255.0","1500","Destination LAN"],
    ["PC-A","NIC","192.168.1.3","255.255.255.0","1500","Reports the symptom"],
    ["Server","NIC","192.168.3.3","255.255.255.0","1500","The 'slow' application server"]],
 23:[["Device","Interface","IP Address","Subnet Mask","Role","Notes"],
    ["R1","G0/0","192.168.1.1","255.255.255.0","Monitored device","NetFlow monitor applied inbound"],
    ["R1","S0/0/0","10.1.1.1","255.255.255.252","Monitored device","WAN link"],
    ["R2","S0/0/0","10.1.1.2","255.255.255.252","Monitored device","Second device"],
    ["Syslog Server","NIC","192.168.1.100","255.255.255.0","Collector","Syslog and NetFlow collector"],
    ["SNMP Server","NIC","192.168.1.101","255.255.255.0","Collector","SNMPv3 poller"],
    ["NTP Source","NIC","209.165.200.226","255.255.255.0","Time source","Stratum 3 master"]],
 24:[["Device","Interface","IP Address","Subnet Mask","Role","Notes"],
    ["S1","F0/1","N/A","N/A","SPAN source","Server port being mirrored"],
    ["S1","F0/24","N/A","N/A","SPAN destination","Local analyser port"],
    ["S1","VLAN 199","N/A","N/A","RSPAN VLAN","Dedicated remote-span VLAN"],
    ["S2","F0/24","N/A","N/A","RSPAN destination","Analyser on the second switch"],
    ["R1","S0/0/0","209.165.200.225","255.255.255.0","IP SLA source","Probe source interface"],
    ["R2","G0/0","209.165.200.226","255.255.255.0","IP SLA target","Echo target"],
    ["Server","NIC","192.168.1.100","255.255.255.0","Monitored host","The capture subject"],
    ["Analyser","NIC","192.168.1.200","255.255.255.0","Analyser","Receives the mirrored traffic"]],
 25:[["Device","Interface","IP Address","Protocol","Port","Notes"],
    ["R1","G0/0","192.168.1.1","NETCONF","830","netconf-yang over SSH"],
    ["R1","G0/0","192.168.1.1","RESTCONF","443","HTTPS REST, JSON or XML"],
    ["R1","G0/0","192.168.1.1","SSH","22","CLI management"],
    ["Admin PC","NIC","192.168.1.50","Client","N/A","Runs curl, Postman and the Python scripts"],
    ["DNAC (sandbox)","N/A","sandboxdnac.cisco.com","HTTPS","443","Cisco DevNet always-on sandbox"]],
 26:[["Device","Interface","IP Address","Subnet Mask","Default Gateway","Notes"],
    ["RTA","G0/0","172.16.1.1","255.255.255.0","N/A","Device being hardened"],
    ["SW1","VLAN 1","172.16.1.2","255.255.255.0","172.16.1.1","Also hardened"],
    ["PCA","NIC","172.16.1.10","255.255.255.0","172.16.1.1","Admin workstation"]],
 27:[["Device","Interface","IP Address","Subnet Mask","Role","Notes"],
    ["R1","G0/1","192.168.1.1","255.255.255.0","TACACS+ client","aaa authentication via TACACS+"],
    ["R1","S0/0/0","10.1.1.2","255.255.255.252","Transit","To R2"],
    ["R2","G0/0","192.168.2.1","255.255.255.0","Transit","TACACS+ server segment"],
    ["R3","G0/1","192.168.3.1","255.255.255.0","RADIUS client","aaa authentication via RADIUS"],
    ["TACACS+ Server","NIC","192.168.2.2","255.255.255.0","AAA server","Key TacacsKey123, TCP 49"],
    ["RADIUS Server","NIC","192.168.3.2","255.255.255.0","AAA server","Key RadiusKey123, UDP 1645/1646"],
    ["PC-A","NIC","192.168.1.3","255.255.255.0","Admin host","Tests the login"]],
 28:[["Device","Interface","IP Address","Subnet Mask","Default Gateway","Notes"],
    ["R1","G0/0","172.22.34.65","255.255.255.224","N/A","User segment 1"],
    ["R1","G0/1","172.22.34.97","255.255.255.240","N/A","User segment 2"],
    ["R1","G0/2","172.22.34.1","255.255.255.192","N/A","Server segment"],
    ["R1","S0/0/0","209.165.200.226","255.255.255.224","N/A","Internet edge — ACL applied inbound"],
    ["Server","NIC","172.22.34.62","255.255.255.192","172.22.34.1","Web server, HTTP/HTTPS permitted"],
    ["PC1","NIC","172.22.34.66","255.255.255.224","172.22.34.65","Internal user"],
    ["PC2","NIC","172.22.34.98","255.255.255.240","172.22.34.97","Internal user"]],
 29:[["Device","Interface","IP Address","Subnet Mask","Role","Notes"],
    ["R1","G0/0","192.168.1.1","255.255.255.0","CoPP applied","Control plane protected"],
    ["R1","S0/0/0","10.1.1.1","255.255.255.252","OSPF adjacency","Must survive the flood"],
    ["R2","S0/0/0","10.1.1.2","255.255.255.252","Flood source","Generates the ICMP flood"],
    ["R2","G0/0","192.168.2.1","255.255.255.0","OSPF neighbour","Adjacency under test"],
    ["Admin PC","NIC","192.168.1.50","255.255.255.0","Management","SSH and SNMP source"]],
 30:[["Use Case","Recommended Method","Why","Notes"],
    ["Corporate laptops","802.1X with EAP-TLS","Certificate-based, strongest identity, no shared secret","Requires PKI and a supplicant"],
    ["Guest Wi-Fi","WebAuth captive portal","No credential distribution, acceptable-use acceptance","Weak identity — segment guests away"],
    ["Contractor devices","802.1X with PEAP-MSCHAPv2","Username and password against RADIUS/AD","Simpler than EAP-TLS, no client certificate"],
    ["IP cameras and printers","MAB with device profiling","Cannot run a supplicant","MAC is spoofable — always pair with profiling"],
    ["Small branch, no RADIUS","WPA2/WPA3 PSK","No server infrastructure needed","Rotate the key; every device shares it"]],
 31:[["Device","Hostname","Management IP","Platform","Status","Uptime (days)"],
    ["1","R1-CORE","10.1.1.1","ISR4451","up","412"],
    ["2","R2-EDGE","10.1.1.2","ISR4331","up","287"],
    ["3","SW1-ACC","10.1.2.11","C9200-24P","up","198"],
    ["4","SW2-ACC","10.1.2.12","C9200-24P","down","0"],
    ["5","SW3-DIST","10.1.2.1","C9300-48U","up","365"],
    ["6","WLC1","10.1.3.1","C9800-CL","up","145"]],
 32:[["Field","JSON Type","Example Value","Valid","Common Error"],
    ["hostname","string","\"R1-CORE\"","yes","Single quotes instead of double"],
    ["mgmt_ip","string","\"10.1.1.1\"","yes","Unquoted key"],
    ["uptime_days","number","412","yes","Quoting a number is legal but changes the type"],
    ["enabled","boolean","true","yes","Capitalised True — that is Python, not JSON"],
    ["last_error","null","null","yes","Using None — that is Python, not JSON"],
    ["interfaces","array","[{...},{...}]","yes","Trailing comma after the last element"],
    ["location","object","{\"site\":\"HQ\"}","yes","A // comment anywhere in the file"]],
 33:[["HTTP Code","Meaning","What Went Wrong","What To Do"],
    ["200","OK","Nothing — the request succeeded","Parse the response body"],
    ["201","Created","The resource was created","Read the Location header for its URI"],
    ["204","No Content","Succeeded, nothing to return","Common after a DELETE"],
    ["400","Bad Request","Malformed syntax or invalid JSON","Validate the payload before sending"],
    ["401","Unauthorized","Token missing, wrong or expired","Request a new token"],
    ["403","Forbidden","Token is valid but the account lacks permission","Fix the account's role, not the token"],
    ["404","Not Found","The URI does not exist","Check the endpoint path and the API version"],
    ["429","Too Many Requests","You exceeded the rate limit","Back off and retry, honouring Retry-After"],
    ["500","Internal Server Error","The server failed","Retry; if persistent, it is not your script"]],
 34:[["Applet","Event Detector","Trigger","Actions","Purpose"],
    ["INTERFACE-DOWN","syslog","Pattern: Serial0/0/0 changed state to down","show interfaces, show ip route, syslog msg","Capture state at the moment of failure"],
    ["HEALTH-CHECK","timer watchdog","Every 300 seconds","show processes cpu, syslog msg","Periodic health snapshot"],
    ["CONFIG-CHANGE","syslog","Pattern: CONFIG_I configured from","show running-config, syslog msg","Record what changed and when"],
    ["HIGH-CPU","snmp","CPU above 80%","show processes cpu sorted, syslog msg","Catch the process responsible"]],
 35:[["Tool","Architecture","Model","Transport","Language","Agent on Device?","Suitable for IOS?"],
    ["Puppet","Master / agent","Pull","TCP 8140","Ruby DSL","Yes","No — requires an agent"],
    ["Chef","Server / client","Pull","HTTPS","Ruby recipes","Yes","No — requires an agent"],
    ["Ansible","Control node only","Push","SSH / NETCONF / API","YAML playbooks","No","Yes — agentless"],
    ["SaltStack","Master / minion","Push","ZeroMQ (or SSH)","YAML states","Yes by default","Only in agentless salt-ssh mode"]],
}

# a second, richer mock data set per lab (named file)
EXTRA={
 1:("cam-table-baseline.csv",
    [["VLAN","MAC Address","Type","Ports","Learned At"],
     ["10","000c.1234.5678","DYNAMIC","Fa0/1","after ping from PC-A"],
     ["10","000c.8765.4321","DYNAMIC","Fa0/2","after ping reply from PC-B"],
     ["10","000c.1234.5678","STATIC","Fa0/1","pinned manually in step 7"],
     ["All","0100.0ccc.cccc","STATIC","CPU","CDP, always present"],
     ["All","0180.c200.0000","STATIC","CPU","STP, always present"]]),
 3:("design-comparison.csv",
    [["Criterion","2-Tier (Collapsed Core)","3-Tier (Dedicated Core)","Which wins for the merged network"],
     ["Devices required","4","6","2-tier"],
     ["Inter-block links (4 blocks)","6 (full mesh)","4 (one uplink each)","3-tier"],
     ["Cost","Lower","Higher","2-tier"],
     ["Convergence on failure","Slower — more paths to recompute","Faster — fewer, simpler paths","3-tier"],
     ["Scalability beyond 3 blocks","Poor — mesh grows as n(n-1)/2","Good — grows linearly","3-tier"],
     ["Operational simplicity","Fewer devices to manage","Clear separation of roles","Tie"],
     ["Recommendation","Single building only","Four buildings, 2,400 staff","3-TIER"]]),
 4:("qos-policy-map.csv",
    [["Traffic Class","Expected DSCP","Configured DSCP","802.11e UP (WMM)","Correct?","Symptom"],
     ["Voice bearer","EF (46)","EF (46)","6 — Voice","yes","—"],
     ["Call signalling","CS3 (24)","CS3 (24)","4 — Video","yes","—"],
     ["Video conferencing","AF41 (34)","AF41 (34)","5 — Video","yes","—"],
     ["Wireless voice","EF (46)","AF21 (18)","2 — Background","NO","Voice queued as background — audio breaks up under load"],
     ["Best effort data","DF (0)","DF (0)","0 — Best Effort","yes","—"],
     ["Scavenger","CS1 (8)","CS1 (8)","1 — Background","yes","—"]]),
 5:("failure-impact.csv",
    [["Component","Solution","Plane","If It Fails","Data Plane Still Forwards?"],
     ["vBond","SD-WAN","Orchestration","No new devices can onboard or be authenticated","yes"],
     ["vSmart","SD-WAN","Control","No new OMP routes or policy are distributed","yes"],
     ["vManage","SD-WAN","Management","No GUI, API, templates or monitoring","yes"],
     ["cEdge","SD-WAN","Data","That site loses connectivity","no, for that site"],
     ["Control plane node","SD-Access","Control","No new EID-to-RLOC resolution; cached entries still work","yes, for cached"],
     ["Border node","SD-Access","Border","No traffic in or out of the fabric","no, for external"],
     ["Edge node","SD-Access","Edge","Endpoints on that switch lose connectivity","no, for that switch"],
     ["DNA Center","SD-Access","Management","No provisioning or assurance; fabric keeps forwarding","yes"]]),
 9:("vxlan-header.csv",
    [["Header","Field","Size (bytes)","Purpose"],
     ["Outer Ethernet","Dst/Src MAC + type","14","Next-hop delivery in the underlay"],
     ["Outer IP","Src/Dst RLOC","20","Routed across the underlay"],
     ["Outer UDP","Src port (hash), Dst port 4789","8","Enables ECMP; 4789 identifies VXLAN"],
     ["VXLAN","Flags + 24-bit VNI + reserved","8","Identifies the segment — 16,777,216 possible"],
     ["Original frame","The encapsulated Layer 2 frame","varies","The payload being transported"],
     ["TOTAL OVERHEAD","","50","Underlay MTU must be at least 1550"]]),
 11:("etherchannel-faults.csv",
    [["Bundle","Symptom","Root Cause","Fix","Verify With"],
     ["Po1","One member port shows (s) suspended","Speed and duplex mismatch on F0/22","Match speed and duplex on both members","show interfaces status"],
     ["Po2","Bundle shows (SD) down, no members bundled","Both ends configured LACP passive","Set one end to 'channel-group 2 mode active'","show etherchannel summary"],
     ["Po3","Bundle never forms, no negotiation","PAgP on S3, LACP on S2","Use the same protocol both ends","show etherchannel 3 detail"]]),
 20:("troubleshooting-log.csv",
    [["Fault","Reported Symptom","Where To Look (GUI)","Root Cause","Fix","Verified By"],
     ["1","User cannot see the SSID","WLANs > WLAN > General and Advanced","WLAN disabled and SSID broadcast off","Enable the WLAN and enable Broadcast SSID","Client sees the SSID in its scan list"],
     ["2","Associates but gets no IP address","WLANs > Interface, Controller > Interfaces","WLAN mapped to the wrong dynamic interface / VLAN","Remap the WLAN to the VLAN 5 interface","ipconfig shows a 192.168.5.x address"],
     ["3","Authentication fails on corporate SSID","Security > AAA > RADIUS > Authentication","RADIUS shared secret does not match the server","Re-enter the shared secret on the WLC","Client appears under Monitor > Clients"]]),
 22:("diagnostic-log.csv",
    [["Test","Command","Result","What It Tells You"],
     ["Basic ping","ping 192.168.3.3","Success","Layer 3 reachability exists"],
     ["Sourced ping","ping 192.168.3.3 source g0/1","Success","The LAN source is routable too"],
     ["Large ping, DF set","ping 192.168.3.3 size 1500 df-bit","Fail","Something on the path cannot carry 1500 bytes"],
     ["Sweep 1400","ping 192.168.3.3 size 1400","Success","1400 fits — the limit is between 1400 and 1500"],
     ["Sweep 1450","ping 192.168.3.3 size 1450","Fail","The limit is between 1400 and 1450"],
     ["Traceroute","traceroute 192.168.3.3","Completes","The path itself is intact — this is an MTU issue, not a routing issue"],
     ["Interface MTU","show interfaces s0/0/0","MTU 1400","ROOT CAUSE: R1 S0/0/0 MTU was set to 1400"]]),
 23:("netflow-cache-sample.csv",
    [["Source IP","Destination IP","Protocol","Src Port","Dst Port","Packets","Bytes","Notes"],
     ["192.168.1.10","172.217.24.14","TCP","51234","443","1420","1863040","Normal HTTPS browsing"],
     ["192.168.1.11","192.168.1.100","UDP","51840","514","320","40960","Syslog to the collector"],
     ["192.168.1.12","8.8.8.8","UDP","53122","53","88","6864","DNS queries"],
     ["192.168.1.13","203.0.113.55","TCP","49152","445","98450","142899200","ANOMALY — huge SMB transfer to an external host"],
     ["192.168.1.14","192.168.1.100","UDP","62110","161","540","69120","SNMP polling"],
     ["192.168.1.15","172.16.5.20","TCP","50100","3389","2210","2895104","RDP session to a server"]]),
 25:("dnac-workflows.csv",
    [["DNA Center Workflow","What It Does","Manual Task It Replaces","API Base Path"],
     ["Design","Site hierarchy, network settings, IP pools, device credentials","Spreadsheets of site settings and per-device configuration","/dna/intent/api/v1/site"],
     ["Policy","Virtual networks, group-based access control, SGTs, application policy","Hand-written ACLs on every device","/dna/intent/api/v1/policy"],
     ["Provision","Push the design and policy to devices, assign devices to sites","Console cable and copy-paste per device","/dna/intent/api/v1/network-device"],
     ["Assurance","Health scores, issues, path trace, client 360 and device 360","Reading syslog and running show commands by hand","/dna/intent/api/v1/assurance"]]),
 28:("acl-test-matrix.csv",
    [["Test","Source","Destination","Protocol/Port","Expected","ACL Line That Decides"],
     ["1","10.5.5.5 (spoofed)","172.22.34.62","any","DENY","deny ip 10.0.0.0 0.255.255.255 any"],
     ["2","192.168.99.9 (spoofed)","172.22.34.62","any","DENY","deny ip 192.168.0.0 0.0.255.255 any"],
     ["3","203.0.113.20","172.22.34.62","TCP 80","PERMIT","permit tcp any host 172.22.34.62 eq 80"],
     ["4","203.0.113.20","172.22.34.62","TCP 443","PERMIT","permit tcp any host 172.22.34.62 eq 443"],
     ["5","203.0.113.20","172.22.34.62","TCP 22","DENY","implicit deny (logged)"],
     ["6","203.0.113.20","172.22.34.66","ICMP echo","DENY","deny icmp any any echo"],
     ["7","172.22.34.66","203.0.113.20","TCP established","PERMIT","permit tcp any any established"]]),
 29:("copp-classes.csv",
    [["Class","ACL","Matches","Police Rate (bps)","Exceed Action","Rationale"],
     ["COPP-CRITICAL","120","OSPF, EIGRP, BGP","512000","transmit","Routing must never be dropped — losing it is worse than any flood"],
     ["COPP-MANAGEMENT","121","SSH (22), SNMP (161)","256000","drop","Management matters, but not more than routing"],
     ["COPP-ICMP","122","All ICMP","64000","drop","The usual flood vector — rate-limit it hard"],
     ["class-default","—","Everything else to the CPU","32000","drop","Catch-all backstop"]]),
 30:("api-security-review.csv",
    [["Finding","Severity","What The Vendor Proposed","Why It Is Wrong","Required Fix"],
     ["1","Critical","API called over plain HTTP","Credentials and data are readable on the wire","Require HTTPS/TLS 1.2 or better"],
     ["2","Critical","Username and password embedded in the script","Anyone with the script has permanent access","Use a short-lived token or OAuth 2.0"],
     ["3","High","Token has no expiry","A leaked token is valid forever","Set a short TTL and refresh"],
     ["4","High","Integration uses a full-admin account","A read-only job holds write access","Scope the token to least privilege"],
     ["5","Medium","No rate limiting on the endpoint","A buggy loop or an attacker can exhaust the service","Enforce a rate limit and return 429"],
     ["6","Medium","Query built by string concatenation","Injection risk","Parameterise and validate server-side"],
     ["7","Medium","Token committed to the Git repository","Secret exposed in history forever","Move to a secrets manager, rotate the token"]]),
 33:("yang-model-extract.csv",
    [["Node","YANG Type","Parent","Data Type","Purpose"],
     ["interfaces","container","(root)","—","Groups all interface configuration"],
     ["interface","list (key: name)","interfaces","—","Repeats once per interface"],
     ["name","leaf","interface","string","The interface name — the list key"],
     ["description","leaf","interface","string","Free-text description"],
     ["type","leaf","interface","identityref","ethernetCsmacd, softwareLoopback, etc"],
     ["enabled","leaf","interface","boolean","Administrative state"],
     ["ipv4","container","interface","—","Groups the IPv4 configuration"],
     ["address","list (key: ip)","ipv4","—","Repeats per address on the interface"]]),
}

TOPOLOGY={
 1:"""    PC-A (192.168.10.10)          PC-B (192.168.10.20)
         |  Fa0/1                        |  Fa0/2
         +----------[  S1  ]-------------+
                       | Gi0/1 (trunk)
                    [  S2  ]
                       |
                    [  R1  ] 192.168.10.1  (default gateway)""",
 2:"""  PC-A                R1                     R2                PC-B
192.168.10.10 --- G0/0        S0/0/0 ---- S0/0/0        G0/0 --- 192.168.20.10
              192.168.10.1  10.1.1.1    10.1.1.2   192.168.20.1
                            \\____ 10.1.1.0/30 ____/""",
 6:"""                    +----------------+
   CORP-PC -------- | G0/0  VRF CORP |
 192.168.1.10       |                |   R1 — one router, two routing tables
   GUEST-PC ------- | G0/1  VRF GUEST|
 192.168.1.10       +----------------+
   (identical addresses — isolated because they are in different VRFs)""",
 7:"""  PCA                RA                              RB                PCB
192.168.1.2 --- G0/0    S0/0/0 --- [ internet ] --- S0/0/0    G0/0 --- 192.168.2.2
            192.168.1.1  64.103.211.2          209.165.122.2  192.168.2.1
                          \\                                  /
                           Tunnel0 10.10.10.1 -- 10.10.10.2 (GRE)""",
 8:"""  PC-A            R1              R2 (ISP)            R3            PC-C
192.168.1.3 --- G0/0  S0/0/0 --- S0/0/0  S0/0/1 --- S0/0/1  G0/0 --- 192.168.3.3
            192.168.1.1 10.1.1.2  10.1.1.1 10.2.2.1  10.2.2.2 192.168.3.1
                        \\________ IPsec tunnel (protects 192.168.1.0 <-> 192.168.3.0) ________/""",
 10:"""        PC1 (VLAN 20 - AFFECTED)      Server (VLAN 20)
              |                              |
   [  S1  ] =========== trunk =========== [  S2  ]
      |  Gi0/1        (802.1Q)        Gi0/1  |
   [  S3  ]                                  PC0/PC2
   Native VLAN 99 must match on both ends; VLANs 10, 20, 99 must be allowed.""",
 12:"""                 [  S1  ]  <- should be ROOT (priority 4096)
                 /        \\
          Gi0/1 /          \\ Gi0/2
        [  S2  ] ---------- [  S3  ]  <- currently root (WRONG)
          secondary root      access switch""",
 16:"""   Area 1              Area 0 (backbone)             Area 2
  172.16.1.0/24                                     192.168.1.0/24
      |                                                   |
    [ R1 ] ==== 172.16.3.0/30 ==== [ R2 ]                 |
    ABR          \\                                       |
                  \\____ 192.168.10.4/30 ____ [ R3 ] -----+
                                              ABR / stub""",
 18:"""            AS 65000 (ISP)
      [ ISP-Entry-1 ]      [ ISP-Entry-2 ]
        1.1.1.1              1.1.1.9
           |                    |
        1.1.1.2              1.1.1.6
      [        ACME1 — AS 65001        ]
              192.168.0.0/24
   eBGP to both entry points for multihomed resilience.""",
 19:"""  Wireless Host ~~~ [ LAP-1 ] --- [ SW-1 ] --- [ R-1 ] --- RADIUS 172.31.1.254
        (VLAN 5)          CAPWAP        VLAN 200      |
                          5246 ctrl                   |
                          5247 data              [ WLC-1 ]
                                              192.168.200.254""",
 21:"""     PC-A (gateway 192.168.1.254 — the HSRP virtual IP)
             |
       [  S1  ]
        /      \\
   [ R1 ]      [ R3 ]        R1: priority 110, preempt -> ACTIVE
  ACTIVE       STANDBY       R3: priority 100          -> STANDBY
     |
  S0/0/0 209.165.200.226  (NTP master, NAT outside)""",
 27:"""   PC-A --- [ R1 ] --- [ R2 ] --- [ R3 ] --- PC-C
             TACACS+       |         RADIUS
             client        |         client
                    TACACS+ Server   RADIUS Server
                    192.168.2.2      192.168.3.2
   Always configure the LOCAL fallback before 'aaa new-model'.""",
 29:"""              control plane (CPU)
                     ^
                     |  service-policy input COPP-POLICY
              +------+------+
   OSPF ----> | COPP-CRITICAL | 512k  transmit  (never starve routing)
   SSH  ----> | COPP-MANAGEMENT| 256k drop
   ICMP ----> | COPP-ICMP      |  64k drop      (the flood vector)
              +---------------+""",
}

def slug_dir(a):
    return f"lab-{a['num']:02d}-{SLUGS[a['num']]}"

def write_csv(path, rows):
    with open(path,"w",newline="") as f:
        csv.writer(f).writerows(rows)

def lab_readme(a, t):
    L=[]
    L.append(f"# Lab {a['num']} — {a['title']}")
    L.append("")
    L.append(f"**Topic {t['code']}: {t['title']}** · {t['weighting']} of the exam · "
             f"Skills Framework {t['tsc']} ({C.TSC_CODE})")
    L.append("")
    L.append("## Exam Objective")
    L.append("")
    L.append(a["objective"])
    L.append("")
    L.append("## Scenario")
    L.append("")
    L.append(a["desc"])
    L.append("")
    L.append("## What You'll Build")
    L.append("")
    L.append(a["build"])
    L.append("")
    L.append("## Tools and Devices")
    L.append("")
    L.append(a["services"]+".")
    L.append("")
    if a["num"] in TOPOLOGY:
        L.append("## Topology")
        L.append("")
        L.append("```text")
        L.append(TOPOLOGY[a["num"]])
        L.append("```")
        L.append("")
    L.append("## Lab Files")
    L.append("")
    L.append(f"| File | What it is |")
    L.append(f"| --- | --- |")
    L.append(f"| `{slug_dir(a)}.pkt` | The Cisco Packet Tracer topology for this lab |")
    L.append(f"| `addressing-table.csv` | Every device, interface and address used here |")
    if a["num"] in EXTRA:
        L.append(f"| `{EXTRA[a['num']][0]}` | The mock data set this lab works with |")
    L.append(f"| `topology.md` | The topology diagram in text form |")
    L.append("")
    L.append("## Addressing Table")
    L.append("")
    rows=ADDRESSING[a["num"]]
    L.append("| "+" | ".join(rows[0])+" |")
    L.append("| "+" | ".join("---" for _ in rows[0])+" |")
    for r in rows[1:]:
        L.append("| "+" | ".join(r)+" |")
    L.append("")
    L.append("## Steps")
    L.append("")
    for i,(instr,cmd) in enumerate(a["steps"],1):
        L.append(f"{i}. {instr}")
        if cmd:
            L.append("")
            L.append("   ```text")
            L.append(f"   {cmd}")
            L.append("   ```")
            L.append("")
    L.append("")
    L.append("## Validation")
    L.append("")
    L.append(a["test"])
    L.append("")
    L.append("## Checkpoint Questions")
    L.append("")
    for q in CHECKPOINTS.get(a["num"], [
        "Which exam objective does this lab satisfy, and what verb does it use?",
        "Which single show command best proves this configuration is working?",
        "What is the most likely reason this configuration would fail in production?",
        "What would you check first if the validation step did not pass?"]):
        L.append(f"1. {q}")
    L.append("")
    L.append("## Exam Focus")
    L.append("")
    L.append(EXAM_FOCUS.get(a["num"],
        f"This lab maps directly to {a['objective']} Know both the configuration and the verification command — "
        "the exam asks for either, and often shows you output and asks what it proves."))
    L.append("")
    return "\n".join(L)

CHECKPOINTS={
 1:["Why can an ACL not be stored in CAM?",
    "What happens to a frame whose destination MAC is not in the CAM table?",
    "What is the default MAC address ageing time, and why does it exist?",
    "Which table holds the Layer 2 rewrite information used by CEF?"],
 2:["What is the difference between the RIB and the FIB?",
    "Why is CEF called 'topology-based' rather than 'traffic-driven'?",
    "What did the CPU do differently when you disabled CEF?",
    "Which two tables must both be populated for CEF to switch a packet in hardware?"],
 3:["What is the trigger that justifies a dedicated core layer?",
    "How many inter-block links does a full mesh of six distribution blocks need?",
    "Which layer must never carry ACLs or policy, and why?",
    "Where does the Layer 2 to Layer 3 boundary sit in a traditional campus design?"],
 4:["Which DSCP value should voice bearer traffic carry, and what is its decimal value?",
    "What does 'trust boundary' mean, and where should it normally be?",
    "What is the difference between policing and shaping?",
    "Why does a DSCP-to-WMM mismatch degrade voice over Wi-Fi but not over the wire?"],
 5:["Which SD-WAN component must be publicly reachable, and why?",
    "If vSmart fails, does existing traffic keep flowing? Explain.",
    "What is the SD-Access control plane protocol, and what is its data plane?",
    "What is the difference between an EID and an RLOC?"],
 6:["Why does a ping without the 'vrf' keyword fail even though the VRF ping succeeds?",
    "What happens to an interface's IP address when you assign it to a VRF?",
    "How can two interfaces on one router carry the same IP address?",
    "What is the difference between VRF-Lite and full MPLS VPN?"],
 7:["What security does GRE provide?",
    "Why is the tunnel MTU usually set to 1476?",
    "What are the two commands that define where a GRE tunnel goes?",
    "Why would you choose GRE over IPsec alone for a site-to-site link carrying OSPF?"],
 8:["What does IKE Phase 1 build, and what does Phase 2 build?",
    "Why must the interesting-traffic ACL mirror exactly on both ends?",
    "Which show command proves traffic is actually being encrypted?",
    "What does QM_IDLE mean in 'show crypto isakmp sa'?"],
 9:["Which UDP port does VXLAN use?",
    "How many bytes of overhead does VXLAN add, and what underlay MTU does that require?",
    "How does a host keep its IP address when it roams between fabric edge nodes?",
    "How many segments can a 24-bit VNI address, compared with 802.1Q VLANs?"],
 10:["What happens when both ends of a link are set to 'dynamic auto'?",
     "What is the symptom of a native VLAN mismatch, and which protocol warns you?",
     "Why is 'switchport nonegotiate' considered good production practice?",
     "What does 'switchport trunk allowed vlan 20' do that 'add 20' does not?"],
 11:["Which two LACP mode combinations will NOT form a bundle?",
     "Name three parameters that must match across EtherChannel member ports.",
     "What do the flags (SU), (SD) and (s) mean in 'show etherchannel summary'?",
     "Can you mix PAgP on one end and LACP on the other? Why?"],
 12:["What two values make up the bridge ID, and which is compared first?",
     "In what increments must STP priority be set, and why?",
     "What are the two new port roles RSTP adds over legacy STP?",
     "Roughly how long does legacy STP take to converge, and RSTP?"],
 13:["Which three values must match exactly for switches to be in the same MST region?",
     "Why does mapping 200 VLANs onto 2 instances reduce switch CPU?",
     "How do you achieve load distribution with MST?",
     "What is instance 0 called, and what does it carry?"],
 14:["What does BPDU guard do when a PortFast port receives a BPDU?",
     "How does root guard's response differ from BPDU guard's?",
     "What failure mode does loop guard defend against?",
     "Why should PortFast never be enabled on a trunk to another switch?"],
 15:["What is the feasibility condition, and what does it guarantee?",
     "Which command enables unequal-cost load balancing in EIGRP?",
     "How is OSPF cost calculated by default?",
     "Name one thing EIGRP can do that OSPF cannot."],
 16:["What makes a router an ABR?",
     "Which LSA type does area summarization produce?",
     "What does a stub area block, and what does a totally stubby area additionally block?",
     "Name four things that must match for two routers to form an OSPF adjacency."],
 17:["Why does OSPFv3 still need a 32-bit router ID?",
     "How is OSPFv3 enabled on an interface, and how does that differ from OSPFv2?",
     "Which addresses do OSPFv3 adjacencies use?",
     "What command must be enabled before any IPv6 routing works?"],
 18:["Which TCP port does BGP use?",
     "Why does peering to a loopback require 'ebgp-multihop'?",
     "What are the first three steps of the BGP best-path algorithm?",
     "Why use 'clear ip bgp * soft in' rather than a hard clear?"],
 19:["Which two UDP ports does CAPWAP use, and what does each carry?",
     "Name four ways an AP can discover a controller.",
     "What is the difference between WPA2-Personal and WPA2-Enterprise?",
     "What does the dynamic interface on a WLC do?"],
 20:["If a client associates but gets no IP address, what should you check first?",
     "What is the difference between a 401-style authentication failure and a mapping error?",
     "Why does the exam specify 'GUI only' for this objective?",
     "Where in the WLC GUI do you verify that an AP has joined?"],
 21:["What does the stratum number in NTP represent?",
     "What makes PAT different from static NAT?",
     "What is HSRP's default priority, and is preemption on or off by default?",
     "How does VRRP's preemption default differ from HSRP's?"],
 22:["What does a large ping with the DF bit set prove when it fails?",
     "What do asterisks in traceroute output mean?",
     "Why must debug be scoped with a condition on a production router?",
     "Which command turns off every running debug at once?"],
 23:["What are the three components of a Flexible NetFlow configuration?",
     "What is the difference between a key field and a non-key field?",
     "Why is SNMPv3 required in production rather than v2c?",
     "What syslog severity level is 'informational', and what does trap level mean?"],
 24:["What is the difference between SPAN, RSPAN and ERSPAN?",
     "What must be configured on the VLAN used by RSPAN?",
     "What does an IP SLA tracked object let you do that a raw SLA cannot?",
     "Why would you use NetFlow instead of SPAN for a whole network?"],
 25:["Which port does NETCONF use, and which does RESTCONF use?",
     "What does NETCONF offer that RESTCONF does not?",
     "What must be generated before either protocol will run?",
     "Name the four Cisco DNA Center workflows."],
 26:["Why is a type 7 password unacceptable?",
     "What must be configured before 'crypto key generate rsa' will work?",
     "What does 'transport input ssh' do?",
     "What does 'login block-for 120 attempts 3 within 60' protect against?"],
 27:["Why must the local fallback user exist before you enable 'aaa new-model'?",
     "Name three differences between TACACS+ and RADIUS.",
     "Which protocol is preferred for device administration, and which for network access?",
     "What does the 'local' keyword at the end of a method list do?"],
 28:["Where should a standard ACL be placed, and where an extended ACL?",
     "What is the implicit last line of every ACL?",
     "Why add an explicit 'deny ip any any log' when the implicit deny already exists?",
     "What does the 'established' keyword match?"],
 29:["What does CoPP protect, and from what?",
     "Why must the routing class be policed with 'exceed-action transmit'?",
     "In which direction is a CoPP policy applied?",
     "Which show command reveals the conformed and exceeded byte counters?"],
 30:["What are the three roles in an 802.1X exchange?",
     "What does the 4-way handshake prove, and what does it never transmit?",
     "Why is MAB weak, and what is normally paired with it?",
     "What is the difference between a 401 and a 403 in REST API terms?"],
 31:["What is the difference between a list and a dictionary in Python?",
     "How do you safely access a dictionary key that may not exist?",
     "What does .json() return when called on a requests response?",
     "Why does Python raise an error on inconsistent indentation?"],
 32:["Name the six JSON value types.",
     "Why is a trailing comma invalid in JSON?",
     "What is wrong with True and None in a JSON file?",
     "What Python type does a JSON object become when parsed?"],
 33:["What does a container do in a YANG model, and how does a list differ?",
     "Which header carries the DNA Center token, and how do you obtain it?",
     "What is the difference between a 401 and a 403?",
     "What does a 429 tell you to do?"],
 34:["What are the three required parts of an EEM applet?",
     "Why is 1.0, 2.0, 3.0 the safe action numbering rather than 1, 2, 10?",
     "Why must the first action usually be 'enable'?",
     "Name three EEM event detectors."],
 35:["Which of the four tools are agent-based, and which are agentless?",
     "Why does the no-agent constraint rule out Puppet and Chef for IOS?",
     "What does idempotency mean, and how did the playbook demonstrate it?",
     "What is the difference between a push and a pull model?"],
}

EXAM_FOCUS={
 1:"Know which table answers which question: a question about a MAC address wants CAM, one about an ACL or QoS wants TCAM. CAM is exact-match; TCAM is masked (ternary), which is precisely why ACLs live there.",
 2:"CEF is the default and the answer to almost every 'which switching method is fastest' question. Remember the pair: the FIB holds the forwarding decision, the adjacency table holds the Layer 2 rewrite. Both are built BEFORE traffic arrives.",
 3:"The trigger for a dedicated core is roughly three distribution blocks, not a user count. Be ready to justify it with the link maths: a full mesh grows as n(n-1)/2, a core grows linearly.",
 4:"Voice is DSCP EF (46). Mark once at the trust boundary and act everywhere else. Policing drops, shaping buffers — shape towards your provider, police traffic coming from them.",
 5:"Keep SD-WAN and SD-Access apart: SD-WAN is the WAN with OMP/vSmart and IPsec; SD-Access is the campus with LISP and VXLAN. Both appear in domain 1 and questions rely on you confusing them.",
 6:"Every show, ping and traceroute in a VRF must be qualified with the vrf keyword. An unqualified command consults the global table and looks like a failure when the configuration is actually correct.",
 7:"GRE provides NO confidentiality, integrity or authentication. It does carry routing protocols and multicast, which plain IPsec cannot — which is why GRE over IPsec is the classic enterprise answer.",
 8:"Phase 1 builds one bidirectional ISAKMP SA; Phase 2 builds the unidirectional IPsec SAs that carry data. A mismatched interesting-traffic ACL is the classic Phase 2 failure. Non-zero encaps/decaps counters are the proof.",
 9:"Memorise: VXLAN is UDP 4789, 8-byte header, 24-bit VNI, 50 bytes total overhead, so the underlay needs an MTU of at least 1550. LISP separates the EID (who) from the RLOC (where).",
 10:"Two 'dynamic auto' ends never trunk. A native VLAN mismatch causes VLAN leaking and a CDP warning. Production practice is always to hard-set the mode and add 'switchport nonegotiate'.",
 11:"Two passive LACP ends or two auto PAgP ends will never bundle — at least one side must initiate. Members must match on speed, duplex, trunk mode, allowed VLANs and native VLAN.",
 12:"Lowest bridge ID wins the root election, and priority is compared before MAC. Priority must be a multiple of 4096. RSTP converges in seconds because proposal/agreement and alternate ports are pre-computed.",
 13:"Name, revision number and VLAN-to-instance map must match EXACTLY or the switches are in different MST regions. Load-balance by making different switches root for different instances.",
 14:"Each feature defends a different failure: BPDU guard err-disables on any BPDU, root guard blocks a superior BPDU (root-inconsistent, not err-disabled), loop guard covers unidirectional links.",
 15:"EIGRP's feasibility condition: the feasible successor's REPORTED distance must be less than the current FEASIBLE distance. Unequal-cost load balancing needs 'variance' — OSPF cannot do it at all.",
 16:"Adjacency requires matching hello/dead timers, area ID, subnet mask, authentication and stub flags. Summarization at the ABR produces one Type 3 LSA. Stub areas block Type 5; totally stubby also blocks Type 3.",
 17:"OSPFv3 is enabled per interface ('ipv6 ospf 10 area N'), still needs a 32-bit router ID, and forms adjacencies over link-local addresses. 'ipv6 unicast-routing' must be on first.",
 18:"eBGP peers are directly connected with TTL 1 by default — peering to a loopback needs 'ebgp-multihop' AND 'update-source'. Best path order starts weight, local preference, locally originated, AS-path length.",
 19:"CAPWAP: UDP 5246 control (DTLS-encrypted), UDP 5247 data. AP discovery order: broadcast, DHCP option 43, DNS, previously learnt list. 'The AP will not join' is usually option 43, DNS or a certificate mismatch.",
 20:"This objective explicitly says GUI only — the exam will not accept a CLI answer. Work the layers in order: is the WLAN enabled and broadcast, is it mapped to the right interface/VLAN, does RADIUS answer?",
 21:"Defaults matter here: HSRP priority 100 with preemption OFF, VRRP preemption ON. Configuring a higher HSRP priority without 'standby preempt' means that router will never become active.",
 22:"A large ping with df-bit that fails while traceroute completes points at MTU, not routing. Always scope a debug with a condition, and always 'undebug all' afterwards.",
 23:"Flexible NetFlow has exactly three parts: record (key/non-key fields), exporter (where to send), monitor (binds them, applied to an interface). Miss any one and you get no flows.",
 24:"SPAN is local, RSPAN crosses a dedicated VLAN that must be flagged 'remote-span', ERSPAN encapsulates in GRE to cross a routed network. IP SLA plus a tracked object is what makes a route withdraw on failure.",
 25:"NETCONF is XML over SSH 830 with candidate/running datastores and transactional commit. RESTCONF is JSON or XML over HTTPS 443 with REST verbs but no transaction. Both are driven by the same YANG models.",
 26:"'username … secret' hashes; 'password' stores type 7, which is trivially reversible. SSH needs a hostname, a domain name and an RSA key before it will start. 'transport input ssh' is what actually removes Telnet.",
 27:"Create the local fallback user BEFORE 'aaa new-model'. TACACS+ = TCP 49, encrypts the whole payload, separates authn from authz, used for device admin. RADIUS = UDP, encrypts only the password, used for network access.",
 28:"Standard ACLs match source only and go near the destination; extended ACLs match everything and go near the source. Every ACL ends in an implicit deny — that is the most common self-inflicted outage.",
 29:"CoPP applies a QoS policy to the control plane in the INPUT direction. Routing classes must use 'exceed-action transmit' — dropping routing traffic to protect the CPU defeats the purpose entirely.",
 30:"802.1X roles: supplicant, authenticator, authentication server. EAPOL runs supplicant-to-authenticator; RADIUS carries it onward. The 4-way handshake derives PTK/GTK from the PMK without ever transmitting the key.",
 31:"You will be shown a script and asked what it prints — not asked to write one. Practise reading list-of-dictionary structures, loops and conditionals, and know that .get() avoids a KeyError.",
 32:"The classic invalid-JSON traps are a trailing comma, single quotes, an unquoted key, a comment, and Python's True/None instead of JSON's true/null. Keys are ALWAYS in double quotes.",
 33:"Token flow: POST with Basic auth to get an X-Auth-Token, then send that token in the header. 401 means fix the token; 403 means fix the account's permissions. That distinction is examined directly.",
 34:"An applet needs a name, exactly one event statement and numbered actions. Number them 1.0, 2.0, 3.0 because actions run in LEXICAL order — 10 would sort before 2.",
 35:"Puppet and Chef are agent-based pull; Ansible is agentless push over SSH/API; SaltStack is minion-based unless run in salt-ssh mode. Network devices that cannot run an agent are why Ansible dominates network automation.",
}

# ------------------------------------------------------------------ write everything
os.makedirs(LABS,exist_ok=True)
written=[]
for a in ACT:
    t=TOPICS[a["topic"]]
    d=os.path.join(LABS,slug_dir(a))
    os.makedirs(d,exist_ok=True)
    with open(os.path.join(d,"README.md"),"w") as f:
        f.write(lab_readme(a,t))
    write_csv(os.path.join(d,"addressing-table.csv"), ADDRESSING[a["num"]])
    if a["num"] in EXTRA:
        name,rows=EXTRA[a["num"]]
        write_csv(os.path.join(d,name), rows)
    with open(os.path.join(d,"topology.md"),"w") as f:
        f.write(f"# Lab {a['num']} Topology — {a['title']}\n\n```text\n"
                +TOPOLOGY.get(a["num"],
                  "See the addressing table and open the .pkt file in Cisco Packet Tracer\n"
                  "for the full topology. This lab is worksheet- or script-based rather than\n"
                  "built on a single physical topology.")
                +"\n```\n")
    written.append(slug_dir(a))

# ------------------------------------------------------------------ labs/README.md index
idx=[f"# {C.TITLE} — Labs Index",""]
idx.append(f"**WSQ Course Code:** {C.COURSE_CODE}  |  **Cisco Exam:** {C.EXAM_CODE} — {C.EXAM_NAME}  |  **Version {C.VERSION}**")
idx.append("")
idx.append("Complete the labs in order. Each lab has its own folder containing the Packet Tracer topology, "
           "the addressing table, a mock data set and a README with objectives, scenario, full step-by-step "
           "instructions, validation checks, checkpoint questions and an ENCOR exam focus note.")
idx.append("")
idx.append("| Lab | Title | Exam Domain | Weighting | Folder |")
idx.append("| --- | --- | --- | --- | --- |")
for a in ACT:
    t=TOPICS[a["topic"]]
    idx.append(f"| {a['num']:02d} | [{a['title']}]({slug_dir(a)}/README.md) | "
               f"{t['exam']} | {t['weighting']} | `{slug_dir(a)}/` |")
idx.append("")
idx.append("## Labs by Exam Domain")
idx.append("")
for t in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==t["num"]]
    idx.append(f"### Topic {t['code']} — {t['title']} ({t['weighting']})")
    idx.append("")
    idx.append(f"{t['subtitle']}. Skills Framework {t['tsc']}.")
    idx.append("")
    for a in acts:
        idx.append(f"- **Lab {a['num']:02d}** — [{a['title']}]({slug_dir(a)}/README.md) — {a['objective']}")
    idx.append("")
idx.append("## Before You Start")
idx.append("")
idx.append("See [tools.md](tools.md) for the full lab environment setup.")
idx.append("")
with open(os.path.join(LABS,"README.md"),"w") as f:
    f.write("\n".join(idx))

# ------------------------------------------------------------------ labs/tools.md
tm=[f"# Lab Environment and Tools",""]
tm.append(f"For {C.TITLE} ({C.COURSE_CODE}), preparing for Cisco {C.EXAM_CODE}.")
tm.append("")
tm.append("## Required Tools")
tm.append("")
tm.append("| Tool | Purpose |")
tm.append("| --- | --- |")
for name,desc in C.LAB_TOOLS:
    tm.append(f"| {name} | {desc} |")
tm.append("")
tm.append("## Installing Cisco Packet Tracer")
tm.append("")
tm.append("1. Create a free account at [netacad.com](https://www.netacad.com).")
tm.append("2. Enrol in the free 'Getting Started with Cisco Packet Tracer' course, which unlocks the download.")
tm.append("3. Download and install the release for your operating system (Windows, macOS or Linux).")
tm.append("4. Launch Packet Tracer and sign in with your NetAcad account — it will not open a topology until you do.")
tm.append("5. Open any `.pkt` file from a lab folder to confirm the install works.")
tm.append("")
tm.append("## Cisco IOS CLI Quick Reference")
tm.append("")
tm.append("| Mode | Prompt | How to get there | What you do here |")
tm.append("| --- | --- | --- | --- |")
tm.append("| User EXEC | `Router>` | Default on connect | Limited show commands |")
tm.append("| Privileged EXEC | `Router#` | `enable` | All show commands, debug, copy, reload |")
tm.append("| Global config | `Router(config)#` | `configure terminal` | Device-wide configuration |")
tm.append("| Interface config | `Router(config-if)#` | `interface g0/0` | Per-interface configuration |")
tm.append("| Line config | `Router(config-line)#` | `line vty 0 4` | Console, VTY and AUX settings |")
tm.append("| Router config | `Router(config-router)#` | `router ospf 10` | Routing protocol configuration |")
tm.append("")
tm.append("## The Show Commands That Matter Most")
tm.append("")
tm.append("| Command | What it proves |")
tm.append("| --- | --- |")
for cmd,what in [
 ("show running-config","What is actually configured right now"),
 ("show ip interface brief","Interface addresses and up/down state — the fastest health check"),
 ("show ip route","The RIB: which routes the router has chosen"),
 ("show ip cef","The FIB: what CEF will actually use to forward"),
 ("show mac address-table","The CAM table on a switch"),
 ("show interfaces trunk","Trunk mode, native VLAN and allowed VLANs"),
 ("show etherchannel summary","Bundle state and which members are bundled"),
 ("show spanning-tree","Root bridge, port roles and port states"),
 ("show ip ospf neighbor","OSPF adjacency state — must reach FULL"),
 ("show ip eigrp topology","Successors and feasible successors"),
 ("show ip bgp summary","BGP session state and prefixes received"),
 ("show standby brief","HSRP active/standby and the virtual IP"),
 ("show ip nat translations","Active NAT/PAT translations"),
 ("show crypto isakmp sa","IKE Phase 1 state — QM_IDLE means established"),
 ("show crypto ipsec sa","Phase 2 SAs and the encaps/decaps counters"),
 ("show flow monitor <name> cache","The NetFlow flow cache"),
 ("show ip sla statistics","IP SLA probe results and RTT"),
 ("show access-lists","ACL contents and per-line match counters"),
 ("show policy-map control-plane","CoPP conformed and exceeded counters"),
 ("show event manager policy registered","Which EEM applets are armed"),
]:
    tm.append(f"| `{cmd}` | {what} |")
tm.append("")
tm.append("## Safety Note")
tm.append("")
tm.append("Every lab in this course runs in Cisco Packet Tracer, a simulator. When you apply these techniques "
          "to a production network, follow your organisation's change-management process. Several commands "
          "used here — clearing a MAC address table, shutting an interface, applying an ACL or a CoPP policy — "
          "will interrupt live traffic. Take a configuration backup first and have a documented rollback.")
tm.append("")
with open(os.path.join(LABS,"tools.md"),"w") as f:
    f.write("\n".join(tm))

print(f"Wrote {len(written)} lab folders to {LABS}")
print(f"  + README.md index and tools.md")
