#!/usr/bin/env python3
"""Generate the course's diagram assets as PNGs for placement on slides.

These are network topology and architecture diagrams drawn with matplotlib —
vector-accurate, on-brand, and far more useful for a Cisco course than stock
photography. Every asset produced here is placed on a slide by build_slides.py.

Output: courseware/assets/*.png
"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE)
OUT=os.path.join(REPO,"courseware","assets")
os.makedirs(OUT,exist_ok=True)

# brand palette (matches the deck)
BLUE="#1F6FEB"; TEAL="#10B981"; AMBER="#F59E0B"; VIOLET="#7C3AED"
INK="#161B26"; GREY="#5B6372"; LIGHT="#F5F8FC"; LINE="#E2E8F0"; WHITE="#FFFFFF"
RED="#DC2626"

import textwrap

def wrap(t,w):
    return "\n".join(textwrap.wrap(t,w))

FONT="DejaVu Sans"
plt.rcParams["font.family"]=FONT

def new_fig(w=12,h=6.4):
    fig,ax=plt.subplots(figsize=(w,h),dpi=170)
    ax.set_xlim(0,100); ax.set_ylim(0,100)
    ax.axis("off"); fig.patch.set_facecolor(WHITE)
    return fig,ax

def box(ax,x,y,w,h,label,sub="",fc=LIGHT,ec=BLUE,lw=1.8,fs=11,tc=INK,radius=1.6,bold=True):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={radius}",
                     linewidth=lw,edgecolor=ec,facecolor=fc,zorder=2)
    ax.add_patch(p)
    if sub:
        ax.text(x+w/2,y+h*0.60,label,ha="center",va="center",fontsize=fs,
                color=tc,fontweight="bold" if bold else "normal",zorder=3)
        ax.text(x+w/2,y+h*0.28,sub,ha="center",va="center",fontsize=fs-2.5,
                color=GREY,zorder=3)
    else:
        ax.text(x+w/2,y+h/2,label,ha="center",va="center",fontsize=fs,
                color=tc,fontweight="bold" if bold else "normal",zorder=3)
    return p

def arrow(ax,x1,y1,x2,y2,color=BLUE,lw=2.0,style="-|>",ls="-",rad=0.0):
    a=FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=16,
                      linewidth=lw,color=color,linestyle=ls,zorder=1,
                      connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a); return a

def line(ax,x1,y1,x2,y2,color=GREY,lw=1.8,ls="-"):
    ax.plot([x1,x2],[y1,y2],color=color,linewidth=lw,linestyle=ls,zorder=1)

def title(ax,t,sub=""):
    ax.text(2,95,t,fontsize=17,fontweight="bold",color=INK,va="top")
    if sub: ax.text(2,89.5,sub,fontsize=11,color=GREY,va="top")

def save(fig,name):
    path=os.path.join(OUT,name)
    fig.savefig(path,bbox_inches="tight",facecolor=WHITE,dpi=170)
    plt.close(fig)
    print("  wrote",name)
    return path

# ---------------------------------------------------------------- 1. campus tiers
def campus_tiers():
    fig,ax=new_fig()
    title(ax,"Two-Tier vs Three-Tier Campus Design",
          "The trigger is the number of distribution blocks, not the number of users")
    # left: 2-tier
    ax.text(24,80,"2-TIER  ·  Collapsed Core",ha="center",fontsize=12,fontweight="bold",color=BLUE)
    box(ax,10,60,28,10,"Collapsed Core / Distribution","Routing · policy · L2-L3 boundary",fc="#E8F0FE",ec=BLUE,fs=10)
    for i,x in enumerate([8,20,32]):
        box(ax,x,38,12,8,f"Access {i+1}","",fc=LIGHT,ec=GREY,fs=9)
        line(ax,x+6,46,24,60,color=BLUE,lw=1.6)
    ax.text(24,30,"Fewer devices · lower cost\nRight for one building",ha="center",fontsize=9.5,color=GREY)
    # divider
    line(ax,50,25,50,84,color=LINE,lw=1.5,ls="--")
    # right: 3-tier
    ax.text(76,80,"3-TIER  ·  Dedicated Core",ha="center",fontsize=12,fontweight="bold",color=TEAL)
    box(ax,64,70,24,8,"Core","High-speed transit only · NO policy",fc="#E8F7EE",ec=TEAL,fs=10)
    for x in [58,80]:
        box(ax,x,54,16,7,"Distribution","",fc="#E8F0FE",ec=BLUE,fs=9)
        line(ax,x+8,61,76,70,color=TEAL,lw=1.6)
    for x in [56,68,80,90]:
        box(ax,x,38,9,7,"Access","",fc=LIGHT,ec=GREY,fs=8)
    for x,px in [(56,66),(68,66),(80,88),(90,88)]:
        line(ax,x+4.5,45,px,54,color=BLUE,lw=1.4)
    ax.text(76,30,"Scales linearly · faster convergence\nJustified beyond ~3 distribution blocks",ha="center",fontsize=9.5,color=GREY)
    # bottom note
    box(ax,10,10,80,11,"","",fc="#FFF8E6",ec=AMBER,lw=1.6)
    ax.text(50,18.5,"THE SCALING ARGUMENT",ha="center",fontsize=9.5,fontweight="bold",color=AMBER)
    ax.text(50,13.5,"Without a core, inter-block links grow as n(n-1)/2 — six blocks need fifteen links.\n"
                    "With a core they grow linearly: one uplink per block.",
            ha="center",fontsize=9.5,color=INK)
    return save(fig,"campus-tiers.png")

# ---------------------------------------------------------------- 2. three planes
def three_planes():
    fig,ax=new_fig()
    title(ax,"The Three Planes of a Network Device",
          "A model you will use in every topic this week")
    rows=[
        (68,"MANAGEMENT PLANE","How you configure and monitor the device",
         "SSH · SNMP · NETCONF (830) · RESTCONF (443) · syslog",VIOLET,"#F3EDFE"),
        (46,"CONTROL PLANE","Decides where packets should go — runs in software on the CPU",
         "OSPF · EIGRP · BGP · STP · LISP · ARP · CDP",BLUE,"#E8F0FE"),
        (24,"DATA PLANE","Forwards packets — runs in hardware at line rate",
         "CEF · FIB · adjacency table · CAM · TCAM",TEAL,"#E8F7EE"),
    ]
    for y,name,what,egs,col,fill in rows:
        box(ax,8,y,72,16,"","",fc=fill,ec=col,lw=2.0)
        ax.text(11,y+11.5,name,fontsize=12,fontweight="bold",color=col,va="center")
        ax.text(11,y+7.2,what,fontsize=9.8,color=INK,va="center")
        ax.text(11,y+3.2,egs,fontsize=9,color=GREY,va="center",style="italic")
    # CoPP annotation
    arrow(ax,84,32,84,52,color=AMBER,lw=2.4,style="-|>")
    ax.text(86,42,"CoPP\nprotects the\ncontrol plane\nfrom the\ndata plane",fontsize=9,
            color=AMBER,va="center",fontweight="bold")
    ax.text(8,12,"Why it matters: 'the control plane is down' means something very different from "
                 "'the data plane is down'.\nSD-WAN separates these planes onto different devices entirely.",
            fontsize=9.5,color=GREY,va="top")
    return save(fig,"three-planes.png")

# ---------------------------------------------------------------- 3. forwarding tables
def forwarding_tables():
    fig,ax=new_fig()
    title(ax,"The Forwarding Tables — Which One Answers Which Question",
          "Know which table an exam question is really about")
    cols=[
        (6, "CAM","MAC → port","Exact match","Learned from\nsource MACs",TEAL),
        (25,"TCAM","ACL / QoS","Ternary (masked)","Compiled from\nACLs and policies",VIOLET),
        (44,"RIB","Best routes","Longest prefix","Routing protocols\nand static routes",BLUE),
        (63,"FIB","CEF's copy","Longest prefix","Built from the RIB\nBEFORE traffic",BLUE),
        (82,"Adjacency","L2 rewrite","Next-hop lookup","ARP and the\nneighbour tables",AMBER),
    ]
    for x,name,holds,match,pop,col in cols:
        box(ax,x,34,16,42,"","",fc=LIGHT,ec=col,lw=2.0)
        ax.add_patch(Rectangle((x,74),16,2,facecolor=col,edgecolor="none",zorder=3))
        ax.text(x+8,69,name,ha="center",fontsize=13,fontweight="bold",color=col)
        ax.text(x+8,61.5,holds,ha="center",fontsize=10,color=INK,fontweight="bold")
        ax.text(x+8,53,match,ha="center",fontsize=9,color=GREY)
        ax.text(x+8,42,pop,ha="center",fontsize=8.5,color=GREY,va="center")
    # flow arrows RIB -> FIB -> adjacency
    arrow(ax,60,55,63,55,color=BLUE,lw=2.2)
    arrow(ax,79,55,82,55,color=AMBER,lw=2.2)
    box(ax,6,12,92,15,"","",fc="#E8F0FE",ec=BLUE,lw=1.8)
    ax.text(50,22.5,"THE EXAM SHORTCUT",ha="center",fontsize=10,fontweight="bold",color=BLUE)
    ax.text(50,17,"A question naming a MAC address wants CAM.   A question naming an ACL or QoS policy wants TCAM.\n"
                  "A question naming a next hop wants the FIB and the adjacency table — CEF uses both together.",
            ha="center",fontsize=9.5,color=INK)
    return save(fig,"forwarding-tables.png")

# ---------------------------------------------------------------- 4. SD-WAN planes
def sdwan_planes():
    fig,ax=new_fig(12,7.0)
    title(ax,"Cisco SD-WAN — The Four Planes",
          "Know each controller, and what breaks when it fails")
    ctrl=[(8,"vBond","Orchestration","Authenticates and\nintroduces devices",VIOLET,"#F3EDFE"),
          (31,"vSmart","Control","Distributes routes\nand policy via OMP",BLUE,"#E8F0FE"),
          (54,"vManage","Management","GUI, API and\nconfiguration templates",AMBER,"#FFF8E6")]
    for x,n,plane,what,col,fill in ctrl:
        box(ax,x,58,20,26,"","",fc=fill,ec=col,lw=2.0)
        ax.text(x+10,79.5,n,ha="center",fontsize=13,fontweight="bold",color=col)
        ax.text(x+10,73.5,plane.upper(),ha="center",fontsize=8.5,fontweight="bold",color=GREY)
        ax.text(x+10,65,what,ha="center",fontsize=8.5,color=INK,linespacing=1.5)
    # data plane
    box(ax,8,26,66,18,"","",fc="#E8F7EE",ec=TEAL,lw=2.0)
    ax.text(41,39,"DATA PLANE  ·  vEdge / cEdge",ha="center",fontsize=12,fontweight="bold",color=TEAL)
    for i,x in enumerate([14,32,50]):
        box(ax,x,29,14,7,f"Site {i+1}","",fc=WHITE,ec=TEAL,fs=9)
    ax.text(41,22.5,"IPsec fabric between sites",ha="center",fontsize=8.5,color=GREY,va="top")
    for x in [18,41,64]:
        line(ax,x,58,x,44,color=GREY,lw=1.4,ls="--")
    # failure panel
    box(ax,78,26,20,58,"","",fc=LIGHT,ec=RED,lw=1.8)
    ax.text(88,80,"IF IT FAILS",ha="center",fontsize=10,fontweight="bold",color=RED)
    fails=[("vBond","No new device\ncan onboard"),
           ("vSmart","No NEW routes —\nexisting tunnels\nkeep forwarding"),
           ("vManage","No GUI or\nmonitoring; fabric\nkeeps running")]
    y=73
    for n,f in fails:
        ax.text(88,y,n,ha="center",fontsize=8.8,fontweight="bold",color=INK)
        ax.text(88,y-7.5,wrap(f.replace("\n"," "),22),ha="center",fontsize=7.0,
                color=GREY,va="center",linespacing=1.55)
        y-=17
    ax.text(8,14,"Exam point: only vBond must be publicly reachable. A vSmart outage stops new route learning "
                 "but does NOT stop existing traffic.",fontsize=9.5,color=GREY,va="top")
    return save(fig,"sdwan-planes.png")

# ---------------------------------------------------------------- 5. SD-Access stack
def sdaccess_stack():
    fig,ax=new_fig()
    title(ax,"Cisco SD-Access — Underlay, Overlay and Policy",
          "LISP is the control plane · VXLAN is the data plane · TrustSec is the policy plane")
    layers=[(70,"POLICY PLANE  ·  TrustSec","SGT applied at ingress, enforced as an SGACL at egress — policy follows identity, not IP",VIOLET,"#F3EDFE"),
            (52,"CONTROL PLANE  ·  LISP","Map server / map resolver answers 'where is this endpoint right now' (EID → RLOC)",BLUE,"#E8F0FE"),
            (34,"OVERLAY DATA PLANE  ·  VXLAN","UDP 4789 · 24-bit VNI replaces the VLAN · 16 million segments · 50 bytes overhead",TEAL,"#E8F7EE"),
            (16,"UNDERLAY  ·  Any routed IP network","Provides reachability between fabric nodes. Carries no client state. MTU ≥ 1550",GREY,LIGHT)]
    for y,name,what,col,fill in layers:
        box(ax,8,y,84,15,"","",fc=fill,ec=col,lw=2.0)
        ax.text(11,y+9.8,name,fontsize=11.5,fontweight="bold",color=col,va="center")
        ax.text(11,y+4.5,what,fontsize=9.3,color=INK,va="center")
    # roles strip
    ax.text(50,7,"FABRIC ROLES:   Control plane node  ·  Border node  ·  Edge node  ·  Wireless LAN controller",
            ha="center",fontsize=9.5,fontweight="bold",color=INK)
    ax.text(50,3,"Because the endpoint keeps its IP when it roams, policy and mobility stop depending on the subnet.",
            ha="center",fontsize=9,color=GREY)
    return save(fig,"sdaccess-stack.png")

# ---------------------------------------------------------------- 6. CAPWAP join
def capwap_join():
    fig,ax=new_fig()
    title(ax,"How an AP Joins a Controller — CAPWAP",
          "'The AP will not join' is almost always option 43, DNS, or a certificate mismatch")
    steps=[("1","Get an address","AP boots and\ntakes DHCP"),
           ("2","Discover the WLC","Broadcast · DHCP\noption 43 · DNS ·\nstored list"),
           ("3","Select one","By priority, then\nlowest AP load"),
           ("4","Join over DTLS","Control tunnel\nUDP 5246"),
           ("5","Download & serve","Image and config,\nthen data — 5247")]
    x=4
    for i,(n,t,d) in enumerate(steps):
        col=[VIOLET,BLUE,BLUE,TEAL,TEAL][i]
        box(ax,x,42,17,30,"","",fc=LIGHT,ec=col,lw=2.0)
        c=Circle((x+8.5,66),3.4,facecolor=col,edgecolor="none",zorder=3); ax.add_patch(c)
        ax.text(x+8.5,66,n,ha="center",va="center",fontsize=12,fontweight="bold",color=WHITE,zorder=4)
        ax.text(x+8.5,56,t,ha="center",fontsize=10,fontweight="bold",color=INK)
        ax.text(x+8.5,48,d,ha="center",fontsize=8.2,color=GREY,va="center")
        if i<4: arrow(ax,x+17.4,57,x+19.6,57,color=col,lw=2.2)
        x+=19.6
    # ports callout
    box(ax,10,16,36,18,"","",fc="#E8F0FE",ec=BLUE,lw=2.0)
    ax.text(28,29,"UDP 5246  ·  CONTROL",ha="center",fontsize=11,fontweight="bold",color=BLUE)
    ax.text(28,22.5,"DTLS-encrypted. Config, keys,\nAP management, RRM.",ha="center",fontsize=9,color=INK)
    box(ax,54,16,36,18,"","",fc="#E8F7EE",ec=TEAL,lw=2.0)
    ax.text(72,29,"UDP 5247  ·  DATA",ha="center",fontsize=11,fontweight="bold",color=TEAL)
    ax.text(72,22.5,"Client traffic tunnelled to the WLC\n(centralized mode).",ha="center",fontsize=9,color=INK)
    ax.text(50,9,"Memorise both port numbers — they are directly examinable.",
            ha="center",fontsize=10,fontweight="bold",color=AMBER)
    return save(fig,"capwap-join.png")

# ---------------------------------------------------------------- 7. VXLAN header
def vxlan_header():
    fig,ax=new_fig()
    title(ax,"The VXLAN Header — 50 Bytes of Overhead",
          "Which is why the underlay MTU must be at least 1550")
    fields=[("Outer\nEthernet","14 B",TEAL),("Outer IP","20 B",BLUE),
            ("Outer UDP\ndst 4789","8 B",VIOLET),("VXLAN\n24-bit VNI","8 B",AMBER),
            ("Original Layer 2 Frame","varies",GREY)]
    widths=[12,15,15,15,35]
    x=6
    for (name,size,col),w in zip(fields,widths):
        box(ax,x,52,w,22,"","",fc=LIGHT,ec=col,lw=2.0)
        ax.add_patch(Rectangle((x,70),w,4,facecolor=col,edgecolor="none",zorder=3))
        ax.text(x+w/2,72,size,ha="center",va="center",fontsize=9,fontweight="bold",color=WHITE,zorder=4)
        ax.text(x+w/2,61,name,ha="center",va="center",fontsize=9.5,color=INK,fontweight="bold")
        x+=w+0.8
    # brace
    line(ax,6,48,53.4,48,color=RED,lw=2.2)
    ax.text(29.7,44,"50 BYTES OF ENCAPSULATION OVERHEAD",ha="center",fontsize=10.5,
            fontweight="bold",color=RED)
    facts=[("UDP port 4789","Identifies VXLAN. The outer source port is a hash of the inner flow, which is what enables ECMP across the underlay."),
           ("24-bit VNI","16,777,216 segments, against 4,094 for 802.1Q VLANs — the segment ceiling problem solved."),
           ("MTU ≥ 1550","1500 payload + 50 overhead. An underlay left at 1500 silently fragments or drops."),
           ("No spanning tree","Layer 2 is carried over a routed underlay, so STP does not extend across the fabric.")]
    y=34
    for t,d in facts:
        ax.add_patch(Circle((9,y+1.2),1.1,facecolor=AMBER,edgecolor="none",zorder=3))
        ax.text(12,y+1.2,t,fontsize=10,fontweight="bold",color=INK,va="center")
        ax.text(30,y+1.2,d,fontsize=8.8,color=GREY,va="center")
        y-=8
    return save(fig,"vxlan-header.png")

# ---------------------------------------------------------------- 8. STP protection
def stp_protection():
    fig,ax=new_fig(12,7.0)
    title(ax,"Spanning Tree Protection — Each Feature Defends a Different Failure",
          "Know which one responds to which event, and how")
    feats=[("PortFast","Edge ports only","Skips listening and learning so a host gets an instant link","Port forwards immediately",TEAL),
           ("BPDU Guard","PortFast ports","Any BPDU on an edge port means someone plugged in a switch","Port goes ERR-DISABLED",RED),
           ("Root Guard","Distribution uplinks","A superior BPDU tries to move the root bridge","Port goes ROOT-INCONSISTENT",AMBER),
           ("Loop Guard","Point-to-point links","BPDUs stop arriving on a non-designated port (unidirectional link)","Port goes LOOP-INCONSISTENT",VIOLET)]
    y=64
    for name,where,when,then,col in feats:
        box(ax,6,y,88,15,"","",fc=LIGHT,ec=col,lw=2.0)
        ax.add_patch(Rectangle((6,y),2.2,15,facecolor=col,edgecolor="none",zorder=3))
        ax.text(11,y+10.4,name,fontsize=12,fontweight="bold",color=col,va="center")
        ax.text(11,y+4.6,where,fontsize=8.5,color=GREY,va="center",style="italic")
        ax.text(30,y+10.4,when,fontsize=9.5,color=INK,va="center")
        ax.text(30,y+4.6,"→  "+then,fontsize=9.5,color=col,va="center",fontweight="bold")
        y-=17.5
    ax.text(6,-2,"Exam point: BPDU guard ERR-DISABLES the port (it must be recovered). Root guard puts it in "
                "root-inconsistent,\nwhich clears by itself once the superior BPDU stops. That difference is examined directly.",
            fontsize=9.5,color=GREY,va="top")
    return save(fig,"stp-protection.png")

# ---------------------------------------------------------------- 9. AAA flow
def aaa_flow():
    fig,ax=new_fig(12,7.0)
    title(ax,"AAA and 802.1X — Who Talks to Whom",
          "EAPOL runs supplicant-to-authenticator; RADIUS carries it onward")
    box(ax,6,50,22,26,"","",fc="#E8F0FE",ec=BLUE,lw=2.0)
    ax.text(17,71,"SUPPLICANT",ha="center",fontsize=11,fontweight="bold",color=BLUE)
    ax.text(17,60,"The client device\nwith an 802.1X\nsoftware supplicant",ha="center",fontsize=8.5,color=INK,linespacing=1.6)
    box(ax,39,50,22,26,"","",fc="#E8F7EE",ec=TEAL,lw=2.0)
    ax.text(50,71,"AUTHENTICATOR",ha="center",fontsize=11,fontweight="bold",color=TEAL)
    ax.text(50,59,"The switch or WLC.\nKeeps the port closed\nuntil authentication\nsucceeds",ha="center",fontsize=8.5,color=INK,linespacing=1.6)
    box(ax,72,50,22,26,"","",fc="#F3EDFE",ec=VIOLET,lw=2.0)
    ax.text(83,71,"AUTH SERVER",ha="center",fontsize=11,fontweight="bold",color=VIOLET)
    ax.text(83,60,"RADIUS / Cisco ISE.\nHolds the identity\nstore and the policy",ha="center",fontsize=8.5,color=INK,linespacing=1.6)
    arrow(ax,28.5,63,38.5,63,color=BLUE,lw=2.4); ax.text(33.5,66,"EAPOL",ha="center",fontsize=9.5,fontweight="bold",color=BLUE)
    arrow(ax,61.5,63,71.5,63,color=VIOLET,lw=2.4); ax.text(66.5,66,"RADIUS",ha="center",fontsize=9.5,fontweight="bold",color=VIOLET)
    # AAA definitions
    aaa=[("Authentication","Who are you?","Verify the identity — password, certificate or MAC",BLUE),
         ("Authorization","What may you do?","Apply the privilege level, VLAN or SGT the policy grants",TEAL),
         ("Accounting","What did you do?","Record the session and the commands run, for audit",AMBER)]
    x=6
    for n,q,d,col in aaa:
        box(ax,x,18,29,26,"","",fc=LIGHT,ec=col,lw=1.8)
        ax.text(x+14.5,39,n,ha="center",fontsize=11,fontweight="bold",color=col)
        ax.text(x+14.5,33.5,q,ha="center",fontsize=9.5,color=INK,style="italic")
        ax.text(x+14.5,26,wrap(d,30),ha="center",fontsize=8,color=GREY,
                va="center",linespacing=1.7)
        x+=30.5
    box(ax,6,2,88,10,"","",fc="#FFF8E6",ec=AMBER,lw=1.8)
    ax.text(50,8.5,"ALWAYS KEEP A LOCAL FALLBACK",ha="center",fontsize=10,fontweight="bold",color=AMBER)
    ax.text(50,4.5,"aaa authentication login default group tacacs+ local   —  create the local user BEFORE 'aaa new-model'.",
            ha="center",fontsize=9.3,color=INK,family="monospace")
    return save(fig,"aaa-flow.png")

# ---------------------------------------------------------------- run
if __name__=="__main__":
    print(f"Writing diagram assets to {OUT}")
    campus_tiers()
    three_planes()
    forwarding_tables()
    sdwan_planes()
    sdaccess_stack()
    capwap_join()
    vxlan_header()
    stp_protection()
    aaa_flow()
    print("done")
