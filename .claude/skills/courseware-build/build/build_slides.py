#!/usr/bin/env python3
"""Generate the Cisco CCNP ENCOR course slide deck (all-white Tertiary house style).

Design helpers are the same set used by the tertiary-course-slides skill that
produced the n8n reference deck (cover, section, content, two_col, cards3,
big_statement, step_slide, test_slide, brk). Content is driven entirely by
course_data.py + data_domainN.py so the deck stays 100% aligned with the LP,
LG and labs.
"""
import os, sys, copy, re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import ChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
from data_domain4 import DOMAIN4
from data_domain5 import DOMAIN5
from data_domain6 import DOMAIN6
ACTIVITIES = DOMAIN1 + DOMAIN2 + DOMAIN3 + DOMAIN4 + DOMAIN5 + DOMAIN6

def _find_repo(start):
    """Locate the course repo (a dir containing both courseware/ and labs/).
    Env COURSE_REPO overrides. Keeps the build working wherever the skill lives."""
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env):
        return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(HERE))
REPO = _find_repo(HERE)
ASSETS = os.path.join(os.path.dirname(HERE), "assets")   # co-located with the skill

# ---------------- palette (matches reference) ----------------
BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81); AMBER=RGBColor(0xF5,0x9E,0x0B)
INK=RGBColor(0x16,0x1B,0x26); GREY=RGBColor(0x5B,0x63,0x72); LIGHT=RGBColor(0xF5,0xF8,0xFC)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0); VIOLET=RGBColor(0x7C,0x3A,0xED)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(1,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
    sp.shadow.inherit=False; return sp
def oval(s,x,y,w,h,color):
    sp=s.shapes.add_shape(9,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    for i,line in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space)
        for t,sz,col,bold in line:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
            r.font.color.rgb=col; r.font.name="Arial"
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
        lvl=it[1] if isinstance(it,tuple) else 0
        text=it[0] if isinstance(it,tuple) else it
        r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
        r.font.size=Pt(size if lvl==0 else size-2); r.font.color.rgb=color if lvl==0 else GREY
        r.font.name="Arial"; r.font.bold=(lvl==0 and isinstance(it,tuple) and len(it)>2 and it[2])
    return tb

# ---------------- motion: restrained transitions + build animation ----------------
# House rule: ONE transition family for the whole deck (morph is unavailable in the
# OOXML PowerPoint 2010 transition set that python-pptx can emit, so we use a short
# push/fade pair). Content slides fade; section dividers push. Nothing else moves.
P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"

def _transition(s, kind="fade", speed="med"):
    """Attach a restrained slide transition. kind: fade | push | wipe."""
    sld = s._element
    for old in sld.findall(qn("p:transition")):
        sld.remove(old)
    tr = etree.SubElement(sld, qn("p:transition"))
    tr.set("spd", speed)
    tr.set("advClick", "1")
    if kind == "fade":
        etree.SubElement(tr, qn("p:fade"))
    elif kind == "push":
        el = etree.SubElement(tr, qn("p:push")); el.set("dir", "l")
    elif kind == "wipe":
        el = etree.SubElement(tr, qn("p:wipe")); el.set("dir", "r")
    # keep the transition last in the slide element (schema order)
    sld.append(tr)
    return tr

# Appear-on-click build for a list of shape ids — used ONLY on process maps so the
# trainer can reveal one stage at a time. No spins, no flying, no sound.
_TIMING = """<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
<p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">
<p:childTnLst>{pars}</p:childTnLst></p:cTn>
<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>"""

_PAR = """<p:par><p:cTn id="{i0}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
<p:childTnLst><p:par><p:cTn id="{i1}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>
<p:childTnLst><p:par><p:cTn id="{i2}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{nt}">
<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{i3}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{i4}" dur="400"/>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"""

def _build_on_click(s, spids):
    """Fade each shape id in on click, in order. Used sparingly (process maps)."""
    if not spids:
        return
    pars, nid = [], 10
    for k, spid in enumerate(spids):
        pars.append(_PAR.format(i0=nid, i1=nid+1, i2=nid+2, i3=nid+3, i4=nid+4,
                                spid=spid, nt="clickEffect" if k == 0 else "afterEffect"))
        nid += 10
    sld = s._element
    for old in sld.findall(qn("p:timing")):
        sld.remove(old)
    sld.append(etree.fromstring(_TIMING.format(pars="".join(pars))))

def connector(s, x1, y1, x2, y2, color, width=Pt(2.0), arrow=True):
    """A REAL PowerPoint connector line (not a typed arrow glyph)."""
    cx, cy = min(x1, x2), min(y1, y2)
    cn = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    cn.line.color.rgb = color; cn.line.width = width
    ln = cn.line._get_or_add_ln()
    if arrow:
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle"); tail.set("w", "med"); tail.set("len", "med")
    return cn

def chevron(s, x, y, w, h, color):
    """A staged chevron shape — the real CHEVRON autoshape, not a text glyph."""
    sp = s.shapes.add_shape(MSO_SHAPE.CHEVRON, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    sp.line.fill.background(); sp.shadow.inherit = False
    return sp

def roundrect(s, x, y, w, h, color, line=None, adj=0.10):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(1.25)
    sp.shadow.inherit = False
    try: sp.adjustments[0] = adj
    except Exception: pass
    return sp

def diamond(s, x, y, w, h, color, line=None):
    sp = s.shapes.add_shape(MSO_SHAPE.DIAMOND, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(1.25)
    sp.shadow.inherit = False
    return sp

def label_in(sp, text, size, color, bold=True):
    """Put centred text inside an autoshape."""
    tf = sp.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = color; r.font.name = "Arial"
    return sp

PAGE={"n":1}   # the cover is slide 1 and carries no number, so numbering starts at 2
def footer(s):
    PAGE["n"]+=1
    txt(s,Inches(0.4),Inches(7.05),Inches(7.5),Inches(0.35),
        [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",9,GREY,False)]])
    txt(s,Inches(5.0),Inches(7.05),Inches(3.3),Inches(0.35),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd",9,GREY,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(12.4),Inches(7.05),Inches(0.6),Inches(0.35),
        [[(str(PAGE["n"]),9,GREY,False)]],align=PP_ALIGN.RIGHT)
def _ellipsis(text,limit):
    """Truncate on a WORD boundary with an ellipsis — never slice mid-word."""
    t=" ".join(str(text).split())
    if len(t)<=limit: return t
    cut=t[:limit]
    sp=cut.rfind(" ")
    if sp>limit*0.55: cut=cut[:sp]
    return cut.rstrip(" ,.;:-—(") + "…"

def _short_cmd(cmd,limit=30):
    """Shorten a shell command for a caption. Paths/URLs have no spaces, so a
    word-boundary ellipsis cuts them mid-token — drop the runner prefix and keep the
    meaningful tail (the script/target) instead."""
    c=" ".join(str(cmd).split())
    for pre in ("uv run python ","uv run ","python3 ","python ","bash ","sh "):
        if c.startswith(pre): c=c[len(pre):]; break
    if len(c)<=limit: return c
    parts=c.split(" ")
    head=parts[0]
    rest=" ".join(parts[1:]).strip()
    if rest:
        # a URL argument → keep the verb and the host, drop the path
        m=re.match(r'https?://([^/\s]+)',rest)
        if m:
            for cand in (f"{head} {m.group(1)}/…", f"{head} {m.group(1)}"):
                if len(cand)<=limit: return cand
        # "git clone …/repo" — keep the verb plus the final path segment
        tail=rest.rstrip("/").split("/")[-1]
        cand=f"{head} …/{tail}" if "/" in rest else f"{head} {tail}"
        if len(cand)<=limit: return cand
        if len(head)+2<=limit: return _ellipsis(head,limit-2)+" …"
    if "/" in c:                   # a bare path → keep the last segment
        tail=c.rstrip("/").split("/")[-1]
        if len(tail)+2<=limit: return "…/"+tail
    return _ellipsis(c,limit)

def _fit_title(title,size=29):
    """Shrink long titles so they never wrap into the hairline rule below."""
    n=len(title)
    if n<=52: return size
    if n<=66: return 25
    if n<=82: return 22
    return 20

def head(s,title,kicker=None,kcolor=BLUE):
    rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),Inches(1.55),kcolor)
    if kicker: txt(s,Inches(0.85),Inches(0.5),Inches(11.6),Inches(0.4),[[(kicker,14,kcolor,True)]])
    txt(s,Inches(0.85),Inches(0.88),Inches(11.9),Inches(0.78),
        [[(title,_fit_title(title),INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
    rect(s,Inches(0.85),Inches(1.7),Inches(11.63),Inches(0.02),LINE)
    return s
def _logo(name):
    """Look in the skill's assets, then the course's own courseware/assets."""
    for p in (os.path.join(ASSETS,name), os.path.join(REPO,"courseware","assets",name)):
        if os.path.exists(p): return p
    return None

# ---------------- slide templates ----------------
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE); rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    org=_logo("tertiary-infotech-logo.png")
    if org: s.shapes.add_picture(org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    # course badge (top-right) — Gemini Agent ADK badge, else text fallback
    badge=_logo("ccnp-encor-badge.png")
    if badge:
        s.shapes.add_picture(badge,Inches(10.35),Inches(0.6),width=Inches(2.2))
    else:
        rect(s,Inches(10.75),Inches(0.66),Inches(1.85),Inches(1.12),BLUE)
        txt(s,Inches(10.75),Inches(0.78),Inches(1.85),Inches(0.52),[[("CCNP",20,WHITE,True)]],align=PP_ALIGN.CENTER)
        txt(s,Inches(10.75),Inches(1.32),Inches(1.85),Inches(0.4),[[("ENCOR 350-401",9,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.85),Inches(12.0),Inches(1.9),[[(C.TITLE,40,INK,True)]])
    rect(s,Inches(0.92),Inches(4.75),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(5.05),Inches(12),Inches(1.4),
        [[(f"WSQ Course Code: {C.COURSE_CODE}",16,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)]],space=6)
    txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),[[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,GREY,False)]])
    txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),[[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

def section(kicker,title,n,sub=""):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,BLUE)
    rect(s,Inches(0.85),Inches(2.5),Inches(0.14),Inches(2.0),TEAL)
    txt(s,Inches(1.25),Inches(2.55),Inches(11),Inches(0.6),[[(kicker,18,BLUE,True)]])
    txt(s,Inches(1.25),Inches(3.0),Inches(11.4),Inches(1.6),[[(title,40,INK,True)]])
    if sub: txt(s,Inches(1.27),Inches(4.55),Inches(11),Inches(0.8),[[(sub,16,GREY,False)]])
    txt(s,Inches(10.0),Inches(0.7),Inches(2.8),Inches(1.6),[[(n,72,RGBColor(0xE2,0xE8,0xF0),True)]],align=PP_ALIGN.RIGHT)
    footer(s)
def content(title,items,kicker=None,size=20):
    s=head(slide(),title,kicker); bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def two_col(title,left,right,kicker=None,lhead="",rhead=""):
    s=head(slide(),title,kicker)
    rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(4.95),LIGHT); rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(4.95),LIGHT)
    if lhead: txt(s,Inches(1.1),Inches(2.15),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
    if rhead: txt(s,Inches(7.2),Inches(2.15),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
    bullets(s,Inches(1.1),Inches(2.66),Inches(5.2),Inches(4.1),left,size=14,gap=7)
    bullets(s,Inches(7.2),Inches(2.66),Inches(5.05),Inches(4.1),right,size=14,gap=7,mcolor=TEAL); footer(s); return s
def cards3(title,cards,kicker):
    s=head(slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
    for i,c in enumerate(cards[:3]):
        x=xs[i]; col=c[0]
        rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT); rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
        txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.6),[[(c[1],19,col,True)]])
        bullets(s,x+Inches(0.25),Inches(2.95),Inches(3.2),Inches(3.4),c[2],size=14,mcolor=col,gap=9)
    footer(s); return s
def big_statement(line1,line2,kicker,color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,color)
    txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[(kicker,16,color,True)]])
    txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(2.4),[[(line1,38,INK,True)]])
    if line2: txt(s,Inches(1.12),Inches(4.9),Inches(11),Inches(1.2),[[(line2,20,GREY,False)]])
    footer(s); return s
import math
PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
    """Grid of light panels, each with a coloured icon/number badge + text.
    items: list of strings (or (title,caption) tuples). Much richer than a bullet list."""
    s=head(slide(),title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    bd=Inches(0.6)
    for i,it in enumerate(items):
        r=i//cols; c=i%cols
        x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,Inches(0.1),ch,col)
        oval(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,col)
        ic=icons[i] if icons else str(i+1)
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        if isinstance(it,tuple):
            txt(s,tx,int(y+Inches(0.14)),tw,int(ch-Inches(0.2)),
                [[(it[0],size+2,INK,True)],[(it[1],size-2,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
        else:
            txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def flow_h(title,steps,kicker=None,color=BLUE):
    """Horizontal numbered flow: coloured chips connected by chevrons."""
    s=head(slide(),title,kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),[[(st,14,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.04)),int(y+ch/2-Inches(0.3)),int(gap+Inches(0.08)),Inches(0.6),
                [[("▶",15,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def process_map(title,stages,kicker=None,color=BLUE,synthesis=None,animate=True):
    """STAGED PROCESS MAP — real rounded-rect stages joined by real connectors with
    arrowheads, each stage numbered, optional synthesis band. stages: list of
    (label, detail). This replaces flow_h wherever a genuine process is taught."""
    s=head(slide(),title,kicker,kcolor=color)
    n=len(stages); X0=Inches(0.85); TOTW=Inches(11.63)
    gap=Inches(0.42); cw=int((TOTW-gap*(n-1))/n)
    y=Inches(2.20); ch=Inches(2.60) if synthesis else Inches(3.20)
    spids=[]
    for i,st in enumerate(stages):
        lbl,detail=(st if isinstance(st,tuple) else (st,""))
        x=int(X0+(cw+gap)*i)
        box=roundrect(s,x,y,cw,ch,LIGHT,line=LINE)
        rect(s,x,y,cw,Inches(0.11),color)
        bd=Inches(0.62)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.34)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.34)),bd,bd,[[(str(i+1),24,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        # Label WRAPS onto up to 3 lines and auto-shrinks — never truncated, because a
        # step the learner cannot read is worse than a smaller font.
        lbl=" ".join(str(lbl).split())
        lsz=13 if len(lbl)<=30 else (12 if len(lbl)<=48 else (11 if len(lbl)<=70 else 10))
        txt(s,x+Inches(0.10),int(y+Inches(0.98)),cw-Inches(0.20),Inches(1.10),
            [[(lbl,lsz,INK,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
        if detail:
            # The command caption is NEVER truncated — it is the thing being taught.
            det=" ".join(str(detail).split())
            dsz=9 if len(det)<=30 else (8 if len(det)<=48 else 7)
            txt(s,x+Inches(0.07),int(y+ch-Inches(0.80)),cw-Inches(0.14),Inches(0.70),
                [[(det,dsz,GREY,False)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=0)
        spids.append(box.shape_id)
        if i<n-1:   # REAL connector in the gap, with an arrowhead
            cy=int(y+ch/2)
            cn=connector(s,int(x+cw+Inches(0.06)),cy,int(x+cw+gap-Inches(0.06)),cy,color)
            spids.append(cn.shape_id)
    if synthesis:
        by=int(y+ch+Inches(0.26))
        rect(s,Inches(0.85),by,Inches(11.63),Inches(1.15),LIGHT)
        rect(s,Inches(0.85),by,Inches(0.11),Inches(1.15),color)
        txt(s,Inches(1.15),int(by+Inches(0.12)),Inches(11.1),Inches(0.32),
            [[(synthesis[0].upper(),11,color,True)]])
        txt(s,Inches(1.15),int(by+Inches(0.46)),Inches(11.1),Inches(0.62),
            [[(synthesis[1],13,INK,False)]])
    if animate: _build_on_click(s,spids)
    footer(s); return s

def decision_map(title,question,yes,no,kicker=None,color=VIOLET,note=None):
    """A real decision diamond with two branches drawn as connectors — used for
    'which pattern do I choose' teaching moments."""
    s=head(slide(),title,kicker,kcolor=color)
    # a diamond's usable text area is ~50% of its box — size generously or text spills
    # past the facets. 4.6 x 2.7 fits 2-3 short lines at 12pt.
    dx,dy,dw,dh=Inches(0.85),Inches(2.75),Inches(4.6),Inches(2.7)
    d=diamond(s,dx,dy,dw,dh,color); label_in(d,question,12,WHITE)
    bx=Inches(6.1); bw=Inches(6.35); bh=Inches(1.5)
    ys=[Inches(2.15),Inches(4.35)]
    for (hdr,items),by,col in zip([yes,no],ys,[TEAL,AMBER]):
        b=roundrect(s,bx,by,bw,bh,LIGHT,line=LINE)
        rect(s,bx,by,Inches(0.11),bh,col)
        txt(s,bx+Inches(0.3),int(by+Inches(0.16)),bw-Inches(0.55),Inches(0.4),[[(hdr,15,col,True)]])
        txt(s,bx+Inches(0.3),int(by+Inches(0.6)),bw-Inches(0.55),Inches(0.82),[[(items,12,INK,False)]])
        connector(s,int(dx+dw),int(dy+dh/2),bx,int(by+bh/2),col)
    if note:
        rect(s,Inches(0.85),Inches(6.15),Inches(11.63),Inches(0.72),LIGHT)
        txt(s,Inches(1.15),Inches(6.28),Inches(11.1),Inches(0.5),[[(note,12,GREY,False)]])
    footer(s); return s

def compare_table(title,headers,rows,kicker=None,accent=BLUE,note=None):
    """A real comparison matrix — the substantive alternative to two bullet columns."""
    s=head(slide(),title,kicker,kcolor=accent)
    X0=Inches(0.85); TOTW=Inches(11.63); ncol=len(headers)
    first=int(TOTW*0.26); rest=int((TOTW-first)/(ncol-1))
    widths=[first]+[rest]*(ncol-1)
    y=Inches(1.95); hh=Inches(0.52)
    x=X0
    for i,h in enumerate(headers):
        col=accent if i==0 else PALETTE[(i-1)%len(PALETTE)]
        rect(s,x,y,widths[i],hh,col)
        txt(s,x+Inches(0.14),y,widths[i]-Inches(0.28),hh,[[(h,13,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
        x+=widths[i]
    # body must end above the note band AND the footer (7.05). Budget it explicitly.
    ry=int(y+hh)
    BOTTOM=Inches(6.88)-(Inches(1.24) if note else Emu(0))
    avail=BOTTOM-ry
    rh=int(min(Inches(0.78),avail/max(len(rows),1)))
    for r,row in enumerate(rows):
        x=X0
        for i,cell in enumerate(row):
            fill=LIGHT if r%2==0 else WHITE
            rect(s,x,ry,widths[i],rh,fill,line=LINE)
            bold=(i==0)
            txt(s,x+Inches(0.14),ry,widths[i]-Inches(0.28),rh,
                [[(cell,11.5,INK if bold else GREY,bold)]],anchor=MSO_ANCHOR.MIDDLE)
            x+=widths[i]
        ry+=rh
    if note:
        rect(s,X0,int(ry+Inches(0.22)),TOTW,Inches(0.92),LIGHT)
        rect(s,X0,int(ry+Inches(0.22)),Inches(0.11),Inches(0.92),accent)
        txt(s,X0+Inches(0.3),int(ry+Inches(0.34)),TOTW-Inches(0.6),Inches(0.66),
            [[("WHEN IT MATTERS  ",11,accent,True),(note,12,INK,False)]])
    footer(s); return s

def worked_example(title,intro,code,explain,kicker=None,accent=TEAL):
    """A worked example: the code on the left, the line-by-line reading on the right.
    This is what turns a decorative lab slide into a teaching slide."""
    s=head(slide(),title,kicker,kcolor=accent)
    txt(s,Inches(0.85),Inches(1.9),Inches(11.63),Inches(0.46),[[(intro,15,GREY,False)]])
    cx,cw=Inches(0.85),Inches(6.5)
    rect(s,cx,Inches(2.5),cw,Inches(4.15),RGBColor(0x0B,0x12,0x20))
    tb=s.shapes.add_textbox(cx+Inches(0.22),Inches(2.62),cw-Inches(0.44),Inches(3.9))
    tf=tb.text_frame; tf.word_wrap=True
    for i,ln in enumerate(code):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(2)
        r=p.add_run(); r.text=ln; r.font.size=Pt(11); r.font.name="Consolas"
        col=RGBColor(0x9C,0xDC,0xFE)
        st=ln.strip()
        if st.startswith("#"): col=RGBColor(0x6A,0x99,0x55)
        elif "=" in ln and not st.startswith(("def","class")): col=RGBColor(0xD4,0xD4,0xD4)
        if st.startswith(("def ","class ","from ","import ")): col=RGBColor(0xC5,0x86,0xC0)
        r.font.color.rgb=col
    ex,ew=Inches(7.65),Inches(4.83)
    for i,(lbl,body) in enumerate(explain[:4]):
        y=int(Inches(2.5)+(Inches(1.0)+Inches(0.05))*i)
        col=PALETTE[i%len(PALETTE)]
        rect(s,ex,y,ew,Inches(1.0),LIGHT); rect(s,ex,y,Inches(0.09),Inches(1.0),col)
        txt(s,ex+Inches(0.26),int(y+Inches(0.1)),ew-Inches(0.45),Inches(0.32),[[(lbl,12,col,True)]])
        txt(s,ex+Inches(0.26),int(y+Inches(0.42)),ew-Inches(0.45),Inches(0.52),[[(body,11,INK,False)]])
    footer(s); return s

def steps_slide(act_title,steps,kicker,accent=TEAL,part=None,start=1):
    """Substantive lab procedure: numbered steps WITH their commands, up to 5 per
    slide. Replaces the old one-sentence step slide."""
    s=head(slide(),act_title+(f" — {part}" if part else ""),kicker,kcolor=accent)
    y0=Inches(1.92); n=len(steps); gapy=Inches(0.1)
    AVAIL=Inches(4.92)          # 1.92 → 6.84, clear of the 7.05 footer
    rh=int(min(Inches(1.12),(AVAIL-gapy*(n-1))/max(n,1)))
    for i,(text,cmd) in enumerate(steps):
        y=int(y0+(rh+gapy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,Inches(0.85),y,Inches(11.63),rh,LIGHT); rect(s,Inches(0.85),y,Inches(0.09),rh,col)
        bd=Inches(0.4)
        oval(s,Inches(1.06),int(y+rh/2-bd/2),bd,bd,col)
        txt(s,Inches(1.06),int(y+rh/2-bd/2),bd,bd,[[(str(start+i),13,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        if cmd:
            txt(s,Inches(1.62),int(y+Inches(0.08)),Inches(10.6),Inches(0.34),[[(text,12.5,INK,True)]])
            rect(s,Inches(1.62),int(y+Inches(0.44)),Inches(10.5),int(rh-Inches(0.54)),RGBColor(0x0B,0x12,0x20))
            one=cmd.split("\n")[0]
            if len(one)>96: one=one[:93]+"..."
            txt(s,Inches(1.78),int(y+Inches(0.44)),Inches(10.2),int(rh-Inches(0.54)),
                [[("$ "+one,10.5,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
        else:
            txt(s,Inches(1.62),y,Inches(10.6),rh,[[(text,12.5,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s

def chart_slide(title,categories,series,kicker=None,accent=BLUE,
                kind="bar",insight=None,number_format='0'):
    """NATIVE PowerPoint chart (fully editable, not a picture) + an insight band.
    kind: bar | column | line | pie | doughnut. series: list of (name, values)."""
    s=head(slide(),title,kicker,kcolor=accent)
    cd=ChartData(); cd.categories=categories
    for nm,vals in series: cd.add_series(nm,vals,number_format)
    ctype={"bar":XL_CHART_TYPE.BAR_CLUSTERED,"column":XL_CHART_TYPE.COLUMN_CLUSTERED,
           "line":XL_CHART_TYPE.LINE_MARKERS,"pie":XL_CHART_TYPE.PIE,
           "doughnut":XL_CHART_TYPE.DOUGHNUT}.get(kind,XL_CHART_TYPE.COLUMN_CLUSTERED)
    ch_h=Inches(3.55) if insight else Inches(4.75)
    gf=s.shapes.add_chart(ctype,Inches(0.85),Inches(1.95),Inches(11.63),ch_h,cd)
    ch=gf.chart
    ch.has_title=False
    ch.font.size=Pt(12); ch.font.name="Arial"; ch.font.color.rgb=INK
    if kind in ("pie","doughnut") or len(series)>1:
        ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout=False; ch.legend.font.size=Pt(11)
    else:
        ch.has_legend=False
    # house palette per point (pie/doughnut) or per series (bar/column/line)
    try:
        if kind in ("pie","doughnut"):
            pts=ch.plots[0]
            for i,pt in enumerate(pts.points):
                pt.format.fill.solid()
                pt.format.fill.fore_color.rgb=PALETTE[i%len(PALETTE)]
        else:
            for i,sr in enumerate(ch.series):
                col=PALETTE[i%len(PALETTE)]
                if kind=="line":
                    sr.format.line.color.rgb=col; sr.format.line.width=Pt(2.5)
                else:
                    sr.format.fill.solid(); sr.format.fill.fore_color.rgb=col
    except Exception:
        pass
    try:
        pl=ch.plots[0]; pl.has_data_labels=True
        dl=pl.data_labels; dl.font.size=Pt(10); dl.font.color.rgb=INK
        dl.number_format=number_format; dl.number_format_is_linked=False
        if kind in ("pie","doughnut"): dl.position=XL_LABEL_POSITION.OUTSIDE_END
    except Exception:
        pass
    if insight:
        by=Inches(5.72)
        rect(s,Inches(0.85),by,Inches(11.63),Inches(1.1),LIGHT)
        rect(s,Inches(0.85),by,Inches(0.11),Inches(1.1),accent)
        txt(s,Inches(1.15),int(by+Inches(0.12)),Inches(11.1),Inches(0.3),
            [[("WHAT THE DATA SHOWS",11,accent,True)]])
        txt(s,Inches(1.15),int(by+Inches(0.44)),Inches(11.1),Inches(0.6),
            [[(insight,12,INK,False)]])
    footer(s); return s

def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    """Profile-card layout: avatar badge + name/role panel on the left, labelled
    info tiles on the right. rows: list of (LABEL, value); blank value → fill-in line."""
    s=head(slide(),"About the Trainer",kicker,kcolor=accent)
    lx=Inches(0.85); lw=Inches(3.65)
    rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
    bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
    oval(s,ax,Inches(2.5),bd,bd,accent)
    txt(s,ax,Inches(2.5),bd,bd,[[(initials,44,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,lx+Inches(0.15),Inches(4.55),lw-Inches(0.3),Inches(0.6),[[(name,21,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,lx+Inches(0.15),Inches(5.2),lw-Inches(0.3),Inches(1.2),[[(role,13,GREY,False)]],align=PP_ALIGN.CENTER)
    rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
    n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
    for i,(label,val) in enumerate(rows):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.1),th,col)
        vruns=[(val,14,INK,False)] if val else [("____________________________________________",13,LINE,False)]
        txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,
            [[(label.upper(),11,col,True)],vruns],anchor=MSO_ANCHOR.MIDDLE,space=3)
    footer(s); return s
def activity_overview(tag,title,desc,build,services,kicker,objective=None,test=None):
    """Lab briefing — now a full teaching slide: the tag chip, the description, and a
    3-tile band covering objective / deliverable / toolchain, plus the success test."""
    s=head(slide(),title,kicker,kcolor=TEAL)
    rect(s,Inches(0.85),Inches(1.88),Inches(1.7),Inches(0.46),TEAL)
    txt(s,Inches(0.85),Inches(1.88),Inches(1.7),Inches(0.46),[[(tag,15,WHITE,True)]],
        align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    if objective:
        txt(s,Inches(2.72),Inches(1.88),Inches(9.7),Inches(0.46),
            [[(objective,12,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,Inches(0.85),Inches(2.5),Inches(11.63),Inches(1.15),[[(desc,17,INK,False)]])
    tiles=[(BLUE,"YOU'LL BUILD",build),(TEAL,"TOOLCHAIN",services),
           (VIOLET,"DONE WHEN",test or "The lab runs end to end without error.")]
    tw=Inches(3.71); xs=[Inches(0.85),Inches(4.81),Inches(8.77)]
    for (col,lbl,body),x in zip(tiles,xs):
        rect(s,x,Inches(3.8),tw,Inches(2.05),LIGHT); rect(s,x,Inches(3.8),tw,Inches(0.1),col)
        txt(s,x+Inches(0.24),Inches(3.98),tw-Inches(0.45),Inches(0.34),[[(lbl,11,col,True)]])
        txt(s,x+Inches(0.24),Inches(4.34),tw-Inches(0.45),Inches(1.4),[[(body,12,INK,False)]])
    footer(s); return s
def step_slide(kicker,act_title,n,total,text,cmd=""):
    s=head(slide(),act_title,kicker,TEAL)
    oval(s,Inches(0.85),Inches(2.5),Inches(1.4),Inches(1.4),TEAL)
    txt(s,Inches(0.85),Inches(2.74),Inches(1.4),Inches(0.9),[[(str(n),38,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.95),Inches(1.95),Inches(11),Inches(0.4),[[(f"STEP {n} OF {total}",13,GREY,True)]])
    txt(s,Inches(2.55),Inches(2.4),Inches(10.1),Inches(1.3),[[(text,23,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    if cmd:
        rect(s,Inches(2.55),Inches(4.15),Inches(10.1),Inches(0.95),RGBColor(0x0B,0x12,0x20))
        txt(s,Inches(2.8),Inches(4.28),Inches(9.7),Inches(0.7),[[("$ "+cmd,13,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def test_slide(act_title,text,kicker,troubleshoot=None):
    """Verification slide — the success criterion PLUS a troubleshooting band, so it
    teaches diagnosis rather than stating one sentence."""
    s=head(slide(),act_title,kicker,TEAL)
    GREEN=RGBColor(0x12,0x7A,0x3E)
    rect(s,Inches(0.85),Inches(1.95),Inches(11.63),Inches(2.15),RGBColor(0xE8,0xF7,0xEE))
    rect(s,Inches(0.85),Inches(1.95),Inches(0.11),Inches(2.15),GREEN)
    txt(s,Inches(1.2),Inches(2.12),Inches(11),Inches(0.44),[[("✅  Expected result",17,GREEN,True)]])
    txt(s,Inches(1.2),Inches(2.62),Inches(11.0),Inches(1.35),[[(text,15,INK,False)]])
    tb=troubleshoot or [
        ("Nothing happens","Check the .env file is in the labs folder and the key has no quotes or spaces."),
        ("Auth or 401 error","Re-copy the API key from AI Studio; confirm GOOGLE_GENAI_USE_VERTEXAI=0."),
        ("ModuleNotFoundError","Run uv sync again, and prefix commands with uv run so the venv is used."),
    ]
    txt(s,Inches(0.85),Inches(4.32),Inches(11.63),Inches(0.34),
        [[("IF IT DOESN'T WORK",11,AMBER,True)]])
    tw=Inches(3.71); xs=[Inches(0.85),Inches(4.81),Inches(8.77)]
    for i,(sym,fix) in enumerate(tb[:3]):
        x=xs[i]
        rect(s,x,Inches(4.7),tw,Inches(1.72),LIGHT); rect(s,x,Inches(4.7),tw,Inches(0.09),AMBER)
        txt(s,x+Inches(0.24),Inches(4.87),tw-Inches(0.45),Inches(0.36),[[(sym,12.5,INK,True)]])
        txt(s,x+Inches(0.24),Inches(5.26),tw-Inches(0.45),Inches(1.05),[[(fix,11,GREY,False)]])
    footer(s); return s
def brk(kind,dur,color=AMBER):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),color); rect(s,0,Inches(7.28),SW,Inches(0.22),color)
    rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
    txt(s,0,Inches(2.75),SW,Inches(1.2),[[(kind,48,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,0,Inches(4.05),SW,Inches(0.8),[[(dur,22,color,True)]],align=PP_ALIGN.CENTER); PAGE["n"]+=1

# ============================================================ BUILD
cover()



def image_slide(title_text, img_name, kicker=None, caption=None, accent=BLUE):
    """Full-bleed diagram slide: a generated PNG from courseware/assets, scaled to fit."""
    from PIL import Image as _PILImage
    path = os.path.join(REPO, "courseware", "assets", img_name)
    s = head(slide(), title_text, kicker, kcolor=accent)
    if not os.path.exists(path):
        txt(s, Inches(0.85), Inches(3.2), Inches(11.6), Inches(1.0),
            [[(f"[missing asset: {img_name}]", 16, GREY, False)]])
        footer(s); return s
    iw, ih = _PILImage.open(path).size
    # available area under the header, above the caption band
    avail_w = Inches(11.9); avail_h = Inches(4.25) if caption else Inches(4.85)
    scale = min(avail_w / iw, avail_h / ih)
    w = int(iw * scale); h = int(ih * scale)
    x = int((SW - w) / 2); y = Inches(1.95)
    s.shapes.add_picture(path, x, y, width=w, height=h)
    if caption:
        cy = Inches(6.32)
        rect(s, Inches(0.85), cy, Inches(11.63), Inches(0.72), LIGHT)
        rect(s, Inches(0.85), cy, Inches(0.1), Inches(0.72), accent)
        txt(s, Inches(1.2), cy, Inches(11.1), Inches(0.72),
            [[(caption, 13, INK, False)]], anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s

# ---------------- ADMIN ----------------
section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
tile_grid("Digital Attendance (Mandatory)",[
 ("Three times a day","Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR","The trainer or administrator displays the digital attendance QR code from the SSG portal."),
 ("Scan and submit","Scan the QR code with your mobile phone camera and submit your attendance."),
 ("75% minimum","A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=15)
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
trainer_slide("YOUR TRAINER",C.TRAINER,"Principal Trainer\nTertiary Infotech Academy Pte Ltd",
 [("Role","Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
  ("Expertise","Enterprise networking, Cisco routing and switching, network security and network automation."),
  ("Delivers","WSQ courses on CCNA, CCNP Enterprise, network security and infrastructure automation."),
  ("Founder","Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
 initials="AA",accent=BLUE)
content("Let's Know Each Other",[
 "Your name, organisation and role.",
 "Your networking experience — CCNA, hands-on with Cisco IOS, or new to enterprise networking.",
 "The network you look after today: campus, branch, data centre or wireless.",
 "What you want to be able to configure or troubleshoot by Friday."],kicker="ICE-BREAKER")
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.","One conversation at a time.",
 "Be punctual; return from breaks on time.","75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
tile_grid("Download Your Course Material",[
 ("1 · Go to the LMS portal","Open https://lms-tms.tertiaryinfotech.com in your browser."),
 ("2 · Log in","Sign in with the account e-mail you used to register for this course."),
 ("3 · Open this course","Select 'Cisco Certified Network Professional (CCNP) for ENCOR Training'."),
 ("4 · Download","Download the Trainer Slides, Learner Guide and Lesson Plan (PDF)."),
 ("5 · Get the labs","Open the labs folder link on the course page for every Packet Tracer topology."),
 ("6 · Keep them open","You may use these materials during the open-book assessment.")],
 kicker="LMS / TMS  ·  lms-tms.tertiaryinfotech.com",cols=2,size=14)
process_map("How to Download Your Course Material",[
 ("Open the LMS","lms-tms.tertiaryinfotech.com"),
 ("Log in","Your registration e-mail"),
 ("Find this course","CCNP ENCOR · TGS-2024044052"),
 ("Open Courseware","Slides · LG · LP · Labs"),
 ("Download the PDFs","Keep them for the open book")],
 kicker="LMS / TMS  ·  STEP BY STEP",color=BLUE,
 synthesis=("BEFORE WE START","Download all four documents now — the assessment is open book, but only these approved materials are permitted."))
tile_grid("Skills Framework Alignment",[
 ("TSC Title", C.TSC_TITLE),
 ("TSC Code", C.TSC_CODE),
 ("K1 / A1","Key network components and their interdependencies; translating organisational to technical requirements."),
 ("K2 / A2","Techniques for implementing and configuring servers, devices and network components."),
 ("K3 / A3","Features of network management tools; implementing devices per the network blueprint."),
 ("K4 / A6","Configuration of network servers and devices; procedures for reporting and stability assessment."),
 ("K5 / A4","Network access management; managing user network access to organisational guidelines."),
 ("K6 / A5","Network tracking and assessment tools; identifying suitable network management tools.")],
 kicker="SKILLS FRAMEWORK  ·  TSC",cols=2,size=13,accent=VIOLET)
tile_grid("Learning Outcomes",[
 ("LO1 · Translate requirements","Translate organizational networking needs into technical configurations by selecting appropriate network components, considering their functions and interdependencies."),
 ("LO2 · Select components","Identify and choose key network components for configuration, utilizing techniques in server and device implementation aligned with technical requirements."),
 ("LO3 · Implement devices","Implement a variety of servers and devices effectively, following the organizational network blueprint to enhance network performance and reliability."),
 ("LO4 · Manage access","Manage network access, ensuring compliance with organizational guidelines and specifications to maintain secure and efficient user connectivity."),
 ("LO5 · Deploy tools","Select and deploy network management tools effectively, optimizing network performance and user experience in line with organizational needs."),
 ("LO6 · Report and assess","Conduct regular network reporting and administration, employing assessment tools to ensure network stability and alignment with organizational objectives.")],
 kicker="WHAT YOU'LL ACHIEVE",cols=2,size=13)
tile_grid("Course Outline — The Six ENCOR Exam Domains",[
 (f"Topic {t['code']} — {t['title']}  ·  {t['weighting']}", t["subtitle"]) for t in C.TOPICS],
 kicker="SIX TOPICS  ·  35 HANDS-ON LABS",cols=1,size=14)
chart_slide("Where Course Time Goes — Exam Domain Weighting",
 [f"{t['code']} {t['title']}" for t in C.TOPICS],
 [("Share of the ENCOR exam (%)",[int(str(t["weighting"]).replace("%","")) for t in C.TOPICS])],
 kicker="ENCOR 350-401 · BLUEPRINT WEIGHTING",accent=BLUE,kind="column",
 insight="Infrastructure carries 30% of the exam — nearly a third — and Security another 20%. Half the exam sits in these two domains, so half your revision time belongs there. Days 3 and 4 are built around that.",
 number_format='0"%"')
two_col("Lesson Plan — 5 Days, 8 hours/day",[
 (f"Day 1 — {C.DAY_THEMES[1]}",0),
 ("Digital Attendance (AM) · Introductions · Learning Outcomes",1),
 ("Topic 1 Enterprise Architecture (Labs 1–5)",1),
 (f"Day 2 — {C.DAY_THEMES[2]}",0),
 ("Topic 2 Virtualization Technologies (Labs 6–9)",1),
 (f"Day 3 — {C.DAY_THEMES[3]}",0),
 ("Topic 3 Network Infrastructure — Layer 2 and Layer 3 (Labs 10–18)",1)],
 [(f"Day 4 — {C.DAY_THEMES[4]}",0),
 ("Topic 3 Network Infrastructure — wireless and IP services (Labs 19–21)",1),
 ("Topic 4 Network Assurance (Labs 22–25)",1),
 ("Topic 5 Network Security (Labs 26–30)",1),
 (f"Day 5 — {C.DAY_THEMES[5]}",0),
 ("Topic 6 Network Automation (Labs 31–35)",1),
 ("Revision · TRAQOM Survey · Digital Attendance (Assessment)",1),
 ("Final Assessment (WA 1 hr + PP 1 hr)",1)],
 kicker="SCHEDULE  ·  40 INSTRUCTIONAL HOURS",lhead="Days 1–3",rhead="Days 4–5")
tile_grid("Your Lab Environment",[(t,d) for (t,d) in C.LAB_TOOLS],
 kicker="SET UP BEFORE WE START",cols=2,size=14,accent=TEAL)
tile_grid("Briefing for Assessment",[
 ("Do · Clear your desk","Place phones and other materials under the table or on the floor."),
 ("Don't · No recording","No photos or recording of assessment scripts."),
 ("Don't · No discussion","Work individually — no discussion during the assessment."),
 ("Do · Black or blue pen","Use a black or blue pen for hard-copy assessments."),
 ("Don't · No correction fluid","No liquid paper or correction tape may be used."),
 ("Do · Stop on time","Scripts are collected when time is up.")],
 kicker="BEFORE YOU START",cols=2,size=14,accent=AMBER)
tile_grid("Final Assessment",[
 ("Written Assessment (WA)","Short-Answer Questions (SAQ) · 1 hour · open book. Tests the underpinning knowledge taught in the slides."),
 ("Practical Performance (PP)","Hands-on Cisco configuration and verification tasks · 1 hour · open book. Tests the ability you built in the labs."),
 ("Open book","You may use the course slides, the Learner Guide and approved materials only."),
 ("Eligibility","A minimum of 75% attendance is required to be eligible for assessment and funding."),
 ("Result","You are assessed as Competent (C) or Not Yet Competent (NYC) on each instrument."),
 ("Appeals","An appeal process is available if you wish to contest an assessment outcome.")],
 kicker="FINAL ASSESSMENT",cols=2,size=14)
process_map("Assessment Flow",[
 ("TRAQOM survey","Scan the QR code on the LMS"),
 ("Digital attendance","Scan the SSG assessment QR"),
 ("Sit WA then PP","Open book · 1 hour each"),
 ("Submit on the LMS","Upload your completed answers"),
 ("Sign the record","Sign the Assessment Summary Record")],
 kicker="ON ASSESSMENT DAY",color=BLUE,
 synthesis=("REMEMBER","All five steps are mandatory for WSQ funding — missing the digital attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Criteria for Funding",[
 ("Attendance","A minimum attendance rate of 75%, based on the SSG Digital Attendance record."),
 ("Assessment","Complete both assessment components and be assessed as 'Competent'."),
 ("Digital attendance","Scan the SSG QR code for AM, PM and Assessment on every training day."),
 ("TRAQOM survey","Complete the mandatory TRAQOM course feedback survey on the LMS.")],
 kicker="WSQ FUNDING",cols=2,size=15,accent=AMBER)
tile_grid("Practice Exam — Cisco CCNP ENCOR 350-401",[
 ("200 original questions","Two full practice exams of 100 questions each, written for this blueprint — not redistributed exam content."),
 ("120 minutes each","The same duration as the real 350-401 exam, so you practise the pacing as well as the content."),
 ("All six domains","Architecture 15% · Virtualization 10% · Infrastructure 30% · Assurance 10% · Security 20% · Automation 15%."),
 ("Practice mode","Answers and full explanations revealed immediately after each question — use this while you learn."),
 ("Exam mode","Timed, answers hidden until you submit, progress saved automatically — use this in the final week."),
 ("Try it free","exams.tertiaryinfotech.com/practice-exams/cisco/cisco-ccnp-encor — a free sample exam needs no payment details.")],
 kicker="PRACTICE EXAM  ·  exams.tertiaryinfotech.com",cols=2,size=14,accent=VIOLET)
big_statement("Practise until the pacing is automatic.",
 "Take the practice exam in Practice mode while you learn, then in Exam mode against the clock. 100 questions in 120 minutes leaves about 72 seconds per question — the pacing is what catches people out, not the content.",
 "exams.tertiaryinfotech.com/practice-exams/cisco/cisco-ccnp-encor",color=VIOLET)

# ---------------- CORE CONCEPTS ----------------
section("CORE CONCEPTS","The Enterprise Network Core, End to End","")
big_statement("ENCOR is one exam across six domains.",
 "350-401 tests whether you can implement core enterprise network technologies — dual-stack architecture, virtualization, infrastructure, assurance, security and automation. This course walks all six, in blueprint order, with a lab for every objective.",
 "WHAT YOU ARE PREPARING FOR",color=BLUE)
tile_grid("The ENCOR 350-401 Exam at a Glance",[
 ("120 minutes","The exam runs two hours and is the core exam for both CCNP Enterprise and CCIE Enterprise."),
 ("Six domains","Architecture, Virtualization, Infrastructure, Network Assurance, Security and Automation."),
 ("Dual stack throughout","IPv4 and IPv6 are both examinable — OSPFv3 and IPv6 addressing appear alongside their v4 equivalents."),
 ("Configure, verify, describe","Read the verb in each objective: 'configure and verify' means hands-on, 'describe' means conceptual."),
 ("Core plus concentration","Passing ENCOR alone earns the Cisco Certified Specialist – Enterprise Core certification."),
 ("Then a concentration","CCNP Enterprise needs ENCOR plus one concentration exam such as ENARSI.")],
 kicker="EXAM STRUCTURE",cols=2,size=14)
compare_table("Read the Verb — What Each Objective Actually Asks",
 ["Verb in the blueprint","What the exam expects","Example objective","How this course covers it"],
 [["Configure and verify","Hands-on configuration and the show command that proves it","Configure and verify eBGP","A full lab with the commands and the verification"],
  ["Troubleshoot","Find and fix a broken configuration","Troubleshoot static and dynamic EtherChannels","A lab that starts broken, not blank"],
  ["Describe","Explain the concept and its components","Describe REST API security","A concept walkthrough and a review worksheet"],
  ["Interpret","Read a given configuration or script and predict the result","Interpret basic Python components","Predict-then-run exercises"],
  ["Compare","State the differences and when to choose each","Compare agent vs agentless tools","A comparison matrix plus a justified recommendation"]],
 kicker="HOW TO STUDY THE BLUEPRINT",accent=TEAL,
 note="The verb tells you how deep to go. 'Describe' will never ask you for a command; 'configure and verify' always will.")
process_map("How a Packet Crosses the Enterprise Core",[
 ("Access","Host attaches, VLAN assigned"),
 ("Distribution","L2 becomes L3, policy applied"),
 ("Core","High-speed transit only"),
 ("WAN edge","NAT, IPsec, SD-WAN"),
 ("Destination","Remote site or cloud")],
 kicker="THE JOURNEY THIS COURSE FOLLOWS",color=BLUE,
 synthesis=("THE POINT","Every topic in this course is one stage of this journey. Keep this picture in mind — the exam questions are almost always about one hop on it."))
tile_grid("The Three Planes — The Idea Behind Every Topic",[
 ("Data plane","Forwards packets. CEF, the FIB and the adjacency table live here, and it runs in hardware at line rate."),
 ("Control plane","Decides where packets should go. Routing protocols, STP and LISP live here, and it runs in software on the CPU."),
 ("Management plane","How you configure and monitor the device. SSH, SNMP, NETCONF and RESTCONF live here."),
 ("Why it matters","CoPP protects the control plane from the data plane, SD-WAN separates them onto different devices, and 'the control plane is down' means something very different from 'the data plane is down'.")],
 kicker="A MODEL YOU WILL USE ALL WEEK",cols=2,size=14,accent=VIOLET)
image_slide("The Three Planes of a Network Device","three-planes.png",
 kicker="CORE CONCEPTS · THE MODEL BEHIND EVERY TOPIC",accent=VIOLET,
 caption="Every topic this week sits in one of these three planes. Know which plane a symptom belongs to and you have already halved the troubleshooting.")
compare_table("Switching Mechanisms — Process, Fast and CEF",
 ["Mechanism","How it decides","Speed","Where the decision is cached"],
 [["Process switching","Every packet examined by the CPU","Slowest","Nowhere — recomputed each packet"],
  ["Fast switching","First packet by CPU, rest from cache","Faster","Route cache, built on demand"],
  ["CEF","FIB built ahead of any traffic","Fastest","FIB + adjacency table, in hardware"]],
 kicker="ENCOR 1.6 · HARDWARE AND SOFTWARE SWITCHING",accent=BLUE,
 note="CEF is the default and the answer to almost every 'which is fastest' question — because it is topology-based, not traffic-driven.")
compare_table("The Forwarding Tables — CAM, TCAM, RIB, FIB and Adjacency",
 ["Table","What it holds","Match type","Populated by"],
 [["CAM","MAC address to port, per VLAN","Exact match","Learning source MACs from frames"],
  ["TCAM","ACL, QoS and policy entries","Ternary (masked)","Compiled ACLs and QoS policies"],
  ["RIB","Best routes from all sources","Longest prefix","Routing protocols and static routes"],
  ["FIB","CEF's forwarding copy of the RIB","Longest prefix","Built from the RIB by CEF"],
  ["Adjacency","Layer 2 rewrite for each next hop","Next-hop lookup","ARP and the neighbour tables"]],
 kicker="ENCOR 1.6 · KNOW WHICH TABLE ANSWERS WHICH QUESTION",accent=TEAL,
 note="An exam question naming a MAC address wants CAM; one naming an ACL wants TCAM; one naming a next hop wants the FIB and adjacency pair.")
image_slide("The Forwarding Tables at a Glance","forwarding-tables.png",
 kicker="ENCOR 1.6 · HARDWARE AND SOFTWARE SWITCHING",accent=TEAL,
 caption="CEF uses the FIB and the adjacency table together — the FIB decides where, the adjacency table builds the new frame header.")
decision_map("Do You Need a Dedicated Core Layer?",
 "More than about\nthree distribution\nblocks?",
 ("YES — build a 3-tier design","Add a dedicated core. Each distribution block gets two uplinks to the core instead of meshing with every other block, so cabling and complexity grow linearly rather than quadratically."),
 ("NO — collapse into 2-tier","Merge core and distribution. Fewer devices, lower cost and less to manage — the right answer for a single building or a small campus."),
 kicker="ENCOR 1.1 · THE DESIGN DECISION",
 note="The trigger is the number of distribution blocks, not the number of users. Four blocks fully meshed need six links; with a core they need four uplinks.")
image_slide("Two-Tier vs Three-Tier Campus Design","campus-tiers.png",
 kicker="ENCOR 1.1.a · ENTERPRISE DESIGN PRINCIPLES",accent=BLUE,
 caption="The design decision is driven by the number of distribution blocks, not the headcount. Beyond roughly three blocks, add the core.")
chart_slide("Why a Core Layer Scales — Links Needed as Blocks Grow",
 ["2 blocks","3 blocks","4 blocks","5 blocks","6 blocks"],
 [("Full mesh, no core",[1,3,6,10,15]),("With a dedicated core",[2,3,4,5,6])],
 kicker="ENCOR 1.1 · THE SCALING ARGUMENT",accent=BLUE,kind="column",
 insight="Without a core, inter-block links grow as n(n-1)/2 — six blocks need fifteen links. With a core they grow linearly: one uplink per block. This is the whole quantitative case for the third tier.")
tile_grid("High Availability — The Three Layers of Redundancy",[
 ("Hardware redundancy","Dual supervisors, dual power supplies and redundant line cards so a component failure is survivable."),
 ("Link redundancy","EtherChannel bundles and redundant uplinks so a cable or port failure does not isolate a block."),
 ("FHRP","HSRP, VRRP or GLBP give hosts one virtual default gateway that survives the failure of the router behind it."),
 ("SSO / NSF","Stateful switchover keeps the standby supervisor in sync; non-stop forwarding keeps forwarding while routing re-converges."),
 ("Graceful restart","Neighbours hold the adjacency during a supervisor switchover instead of tearing routing down."),
 ("Why all four","Each covers a different failure. Redundant hardware without FHRP still leaves hosts pointing at a dead gateway.")],
 kicker="ENCOR 1.1.b · HIGH AVAILABILITY TECHNIQUES",cols=2,size=14,accent=TEAL)
compare_table("First Hop Redundancy Protocols Compared",
 ["","HSRP","VRRP","GLBP"],
 [["Standard","Cisco proprietary","IEEE / RFC 5798","Cisco proprietary"],
  ["Roles","Active / Standby","Master / Backup","AVG / AVF"],
  ["Default priority","100","100","100"],
  ["Preemption","Disabled by default","Enabled by default","Enabled by default"],
  ["Load balancing","No — one active router","No — one master","Yes — across all forwarders"]],
 kicker="ENCOR 3.4.c · FHRP",accent=AMBER,
 note="The preemption default is the classic exam trap: configure HSRP priority without 'standby preempt' and the higher-priority router will never take over.")
tile_grid("QoS — Mark Once, at the Trust Boundary",[
 ("Classification","Identify the traffic — by ACL, by protocol, or by the marking a trusted device already applied."),
 ("Marking","Write the class into the packet: DSCP in the IP header, CoS in the 802.1Q tag. Voice is EF (46)."),
 ("Queuing and scheduling","Decide who transmits next. LLQ gives voice a strict-priority queue; CBWFQ shares the rest by weight."),
 ("Congestion avoidance","WRED drops selectively before the queue is full, so TCP backs off gradually instead of all at once."),
 ("Policing","Enforces a rate by dropping or remarking excess — bursty, no delay added."),
 ("Shaping","Enforces a rate by buffering excess — smooth, but adds delay. Shape towards the provider, police from them.")],
 kicker="ENCOR 1.5 · QoS COMPONENTS",cols=2,size=14,accent=AMBER)
worked_example("Reading a QoS Policy Map",
 "Every QoS configuration you will meet has this same three-part shape — learn to read it once.",
 ["class-map match-all VOICE","  match ip dscp ef","!","class-map match-all VIDEO",
  "  match ip dscp af41","!","policy-map WAN-EDGE","  class VOICE",
  "    priority percent 10","  class VIDEO","    bandwidth percent 30",
  "  class class-default","    fair-queue","!","interface Serial0/0/0",
  "  service-policy output WAN-EDGE"],
 [("class-map","Classifies — it says WHICH packets belong to this class, and nothing else."),
  ("policy-map","Acts — it says WHAT happens to each class: priority, bandwidth or queuing."),
  ("priority percent 10","The strict-priority (low-latency) queue. Voice goes here; it is policed to 10% so it cannot starve everything else."),
  ("service-policy output","Applies the policy to an interface in one direction. Without this line the policy does nothing at all.")],
 kicker="ENCOR 1.5 · WORKED EXAMPLE",accent=AMBER)
tile_grid("Wireless Design Principles",[
 ("Centralized","All client traffic tunnels to a central WLC over CAPWAP. Simple policy, but the WLC is in every data path."),
 ("Distributed / FlexConnect","The AP switches client traffic locally at the branch and only sends control traffic to the WLC — right when the WAN is slow or expensive."),
 ("Controller-less","Mobility Express embeds the controller in an AP. Suits a small site with no room for a separate WLC."),
 ("Cloud-managed","Meraki-style: management in the cloud, data stays local. Lowest operational overhead."),
 ("Location services","RSSI trilateration, Angle of Arrival with Hyperlocation, and BLE beacons — accuracy depends on AP density and placement."),
 ("Client density","High density is a capacity problem: smaller cells, lower transmit power, narrower channels and band steering to 5 GHz.")],
 kicker="ENCOR 1.2 · WIRELESS NETWORK DESIGN",cols=2,size=14,accent=TEAL)
image_slide("The AP Join Process — CAPWAP End to End","capwap-join.png",
 kicker="ENCOR 3.3.c · AP DISCOVERY AND JOIN",accent=TEAL,
 caption="UDP 5246 carries the DTLS-encrypted control tunnel; UDP 5247 carries client data. Both port numbers are directly examinable.")
process_map("How an AP Joins a Controller — CAPWAP",[
 ("Get an address","AP boots and takes DHCP"),
 ("Discover the WLC","Broadcast, option 43, DNS or stored list"),
 ("Select one","By priority, then lowest AP load"),
 ("Join over DTLS","Control tunnel on UDP 5246"),
 ("Download and serve","Image, config, then data on UDP 5247")],
 kicker="ENCOR 3.3.c · AP DISCOVERY AND JOIN",color=TEAL,
 synthesis=("EXAM POINT","Learn the discovery order and both port numbers — 5246 control, 5247 data. 'The AP will not join' questions are almost always option 43, DNS, or a DTLS certificate mismatch."))
image_slide("Cisco SD-WAN — The Four Planes and What Breaks","sdwan-planes.png",
 kicker="ENCOR 1.3 · SD-WAN CONTROL AND DATA PLANES",accent=VIOLET,
 caption="Only vBond must be publicly reachable. A vSmart outage stops NEW route learning — it does not stop traffic already flowing.")
tile_grid("Cisco SD-WAN — The Four Planes",[
 ("vBond · Orchestration","Authenticates every device and introduces them to each other. The only element that must have a public address."),
 ("vSmart · Control","Distributes routes and policy over OMP. It never carries user data."),
 ("vManage · Management","The GUI, the API and the configuration templates. Where you actually operate the fabric."),
 ("vEdge / cEdge · Data","The routers at each site that build the IPsec fabric and forward the traffic."),
 ("If vSmart fails","Existing data plane tunnels keep forwarding — but no new routes or policy are learned."),
 ("If vManage fails","The fabric keeps running; you lose management and monitoring, not forwarding.")],
 kicker="ENCOR 1.3 · SD-WAN CONTROL AND DATA PLANES",cols=2,size=14,accent=VIOLET)
tile_grid("Cisco SD-Access — Underlay, Overlay and Policy",[
 ("Underlay","Any routed IP network that provides reachability between fabric nodes. It carries no client state."),
 ("Overlay data plane","VXLAN. The VNI replaces the VLAN as the segment identifier, lifting the ceiling from 4,094 to 16 million."),
 ("Control plane","LISP. The map server and map resolver answer 'where is this endpoint right now'."),
 ("Policy plane","TrustSec. An SGT is applied at ingress and enforced as an SGACL at egress — policy follows identity, not IP."),
 ("Fabric roles","Control plane node, border node, edge node and the wireless LAN controller."),
 ("Why it matters","Because the endpoint keeps its IP when it roams, policy and mobility both stop depending on the subnet.")],
 kicker="ENCOR 1.4 · SD-ACCESS CONTROL AND DATA PLANES",cols=2,size=14,accent=VIOLET)
image_slide("Cisco SD-Access — The Full Stack","sdaccess-stack.png",
 kicker="ENCOR 1.4 · SD-ACCESS CONTROL AND DATA PLANES",accent=VIOLET,
 caption="LISP resolves where an endpoint is, VXLAN carries the frame there, and TrustSec decides whether it is allowed.")
compare_table("SD-WAN and SD-Access — Do Not Confuse Them",
 ["","Cisco SD-WAN","Cisco SD-Access"],
 [["Where it applies","The WAN, between sites","The campus, inside a site"],
  ["Control plane","OMP via vSmart","LISP via the control plane node"],
  ["Data plane","IPsec tunnels","VXLAN"],
  ["Policy","Centralised and localised policy in vManage","SGTs enforced by TrustSec"],
  ["Managed by","vManage","Cisco DNA Center"]],
 kicker="ENCOR 1.3 AND 1.4",accent=BLUE,
 note="Both are 'software-defined' and both appear in domain 1, but they solve different problems in different places. Exam questions rely on you keeping them apart.")

# ---------------- TOPICS + ACTIVITIES ----------------
TOPIC_ACTS = {t["num"]: [a for a in ACTIVITIES if a["topic"]==t["num"]] for t in C.TOPICS}
CARD_COLORS=[BLUE,TEAL,VIOLET]
for t in C.TOPICS:
    section(f"TOPIC {t['code']}", t["title"], t["code"], t["subtitle"])
    tile_grid(f"Topic {t['code']} — What This Domain Covers",[
      ("Exam domain", t["exam"]),
      ("Exam weighting", f"{t['weighting']} of the ENCOR 350-401 exam"),
      ("TSC mapping", f"Skills Framework {t['tsc']} · {C.TSC_TITLE} ({C.TSC_CODE})"),
      ("Hands-on labs", f"Labs {TOPIC_ACTS[t['num']][0]['num']}–{TOPIC_ACTS[t['num']][-1]['num']} — every objective has a lab")],
      kicker=f"TOPIC {t['code']} · SCOPE",cols=2,size=15,accent=BLUE)
    cons=t["concepts"]
    for ci in range(0,len(cons),4):
        chunk=cons[ci:ci+4]
        suffix="" if ci==0 else f" ({ci//4+1})"
        tile_grid(f"Key Concepts — {t['title']}{suffix}", chunk,
                  kicker=f"TOPIC WEIGHTING {t['weighting']}", cols=2, size=13)
    # topic-specific diagram assets
    if t["num"]==2:
        image_slide("Decoding the VXLAN Header","vxlan-header.png",
         kicker="ENCOR 2.3.b · NETWORK VIRTUALIZATION",accent=AMBER,
         caption="Fifty bytes of overhead is why the underlay MTU must be at least 1550 — an underlay left at 1500 silently drops or fragments.")
    if t["num"]==3:
        image_slide("Spanning Tree Protection Features","stp-protection.png",
         kicker="ENCOR 3.1.c · SPANNING TREE ENHANCEMENTS",accent=AMBER,
         caption="BPDU guard err-disables the port and must be recovered; root guard's root-inconsistent state clears by itself. That difference is examined.")
    if t["num"]==5:
        image_slide("AAA and 802.1X — Who Talks to Whom","aaa-flow.png",
         kicker="ENCOR 5.1.b · AUTHENTICATION AND AUTHORIZATION",accent=BLUE,
         caption="EAPOL runs between supplicant and authenticator; RADIUS carries it onward. Always create the local fallback user BEFORE 'aaa new-model'.")
    acts=TOPIC_ACTS[t["num"]]
    third=(len(acts)+2)//3
    groups=[acts[i:i+third] for i in range(0,len(acts),third)][:3]
    while len(groups)<3: groups.append([])
    cards=[]
    for gi,g in enumerate(groups):
        _lbl=("—" if not g else (f"Lab {g[0]['num']}" if g[0]['num']==g[-1]['num']
                                 else f"Labs {g[0]['num']}–{g[-1]['num']}"))
        cards.append((CARD_COLORS[gi], _lbl,
                      [a["title"] for a in g] if g else ["—"]))
    cards3(f"Hands-On Labs — {t['title']}", cards, kicker="WHAT YOU'LL DO")
    for a in acts:
        activity_overview(f"LAB {a['num']}", a["title"], a["desc"], a["build"], a["services"],
                          kicker=f"TOPIC {t['code']} · HANDS-ON",
                          objective=a.get("objective"), test=a.get("test"))
        stg=[]
        for (stext,scmd) in a["steps"][:5]:
            # Keep the FULL clause and the FULL command — process_map wraps and
            # auto-shrinks. A step or a command the learner cannot read is worse
            # than a smaller font, so nothing here is truncated.
            lbl=" ".join(str(stext).split())
            cap=scmd.split("\n")[0].strip() if scmd else ""
            stg.append((lbl, cap))
        if len(stg)>=3:
            process_map(f"How Lab {a['num']} Runs", stg,
                        kicker=f"LAB {a['num']} · PROCESS MAP", color=TEAL,
                        synthesis=("THE POINT", a["objective"]))
        test_slide(a["title"], a["test"], kicker=f"LAB {a['num']} · VERIFY")
    content(f"Recap — {t['title']}",
            ["You can now: "+a["objective"] for a in {x["objective"]:x for x in acts}.values()][:6],
            kicker="TOPIC RECAP", size=15)

# ---------------- CLOSE ----------------
section("WRAP-UP","Course Summary & Next Steps","")
tile_grid("What You Achieved",[
 ("LO1 · Translated requirements","Turned organisational needs into campus, wireless and WAN designs — 2-tier versus 3-tier, deployment models and QoS policy."),
 ("LO2 · Selected components","Chose and configured the right components: VRFs, tunnels, switches, routers, controllers and their interdependencies."),
 ("LO3 · Implemented devices","Configured trunking, EtherChannel, RSTP, MST, EIGRP, OSPFv2/v3, eBGP, NAT, HSRP and controller-based wireless."),
 ("LO4 · Managed access","Secured device access with SSH and AAA, enforced ACLs and CoPP, and deployed 802.1X and WPA2-Enterprise wireless."),
 ("LO5 · Deployed tools","Deployed syslog, SNMPv3, Flexible NetFlow, SPAN/RSPAN, IP SLA, NETCONF and RESTCONF."),
 ("LO6 · Reported and assessed","Automated reporting and response with Python, JSON, REST APIs, EEM applets and Ansible.")],
 kicker="LEARNING OUTCOMES",cols=2,size=13)
tile_grid("Your Path to CCNP Enterprise",[
 ("1 · Pass ENCOR 350-401","The core exam you have prepared for this week. Passing it alone earns Cisco Certified Specialist – Enterprise Core."),
 ("2 · Choose a concentration","CCNP Enterprise = ENCOR plus one concentration exam. ENARSI (advanced routing) is the most common next step."),
 ("3 · Practise the pacing","Use the practice exam at exams.tertiaryinfotech.com in Exam mode until 100 questions in 120 minutes feels comfortable."),
 ("4 · Rebuild every lab","Redo each of the 35 labs from a blank configuration until the commands come without the guide."),
 ("5 · Read the blueprint again","Walk learningnetwork.cisco.com/s/encor-exam-topics objective by objective and rate your confidence on each."),
 ("6 · Book the exam","Schedule at a Pearson VUE centre once you are consistently scoring above 85% in Exam mode.")],
 kicker="NEXT STEPS",cols=2,size=14,accent=TEAL)
tile_grid("Practice Exam — Book Your Revision Now",[
 ("Where","exams.tertiaryinfotech.com/practice-exams/cisco/cisco-ccnp-encor"),
 ("What","200 original questions across two full 100-question practice exams."),
 ("How long","120 minutes each — the same as the real 350-401 exam."),
 ("Practice mode","Immediate answers and explanations. Use it while the material is still fresh."),
 ("Exam mode","Timed with answers hidden until submission. Use it in your final week."),
 ("Free sample","A free sample exam is available with no payment details required.")],
 kicker="PRACTICE EXAM  ·  exams.tertiaryinfotech.com",cols=2,size=14,accent=VIOLET)
tile_grid("Recommended Courses",[(rc,"") for rc in C.RECOMMENDED_COURSES],
 kicker="CONTINUE WITH TERTIARY INFOTECH",cols=1,size=15)
content("Support",[
 "If you have any enquiries during or after the class, you can contact us below.",
 "Email: enquiry@tertiaryinfotech.com","Tel: +65 6100 0613",
 "Website: www.tertiarycourses.com.sg","LMS / TMS: https://lms-tms.tertiaryinfotech.com"],kicker="WE'RE HERE TO HELP")
tile_grid("Final Assessment",[
 ("Written Assessment (SAQ)","1 hour · open book · short-answer knowledge questions across all six domains."),
 ("Practical Performance (PP)","1 hour · open book · hands-on Cisco configuration and verification tasks."),
 ("Digital attendance","Remember to take the Assessment digital attendance (TRAQOM) before you start."),
 ("Submit on the LMS","Upload your completed answers at https://lms-tms.tertiaryinfotech.com/")],
 kicker="WRAP-UP",cols=2,size=15)
process_map("Assessment Flow",[
 ("TRAQOM survey","Scan the QR code on the LMS"),
 ("Digital attendance","Scan the SSG assessment QR"),
 ("Sit WA then PP","Open book · 1 hour each"),
 ("Submit on the LMS","Upload your completed answers"),
 ("Sign the record","Sign the Assessment Summary Record")],
 kicker="ON ASSESSMENT DAY",color=BLUE,
 synthesis=("REMEMBER","All five steps are mandatory for WSQ funding — missing the digital attendance or the TRAQOM survey can invalidate your claim."))
tile_grid("Digital Attendance (Mandatory)",[
 ("Three times a day","Take the AM, PM and Assessment digital attendance — mandatory for every WSQ-funded course."),
 ("Trainer shows the QR","The trainer or administrator displays the digital attendance QR code from the SSG portal."),
 ("Scan and submit","Scan the QR code with your mobile phone camera and submit your attendance."),
 ("75% minimum","A minimum of 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=15)
big_statement("Thank You!","You can now design, implement, secure and automate the core technologies of a Cisco enterprise network — and you are ready to sit ENCOR 350-401.","GOOD LUCK IN THE EXAM",color=TEAL)

# ---------------- restrained motion pass ----------------
DIVIDER_IDS=set()
for s in prs.slides:
    txts=[sh.text_frame.text for sh in s.shapes if sh.has_text_frame]
    joined=" ".join(txts)
    is_div=any(k in joined for k in ("COURSE ADMINISTRATION","CORE CONCEPTS","WRAP-UP")) or \
           any(t["title"] in joined and f"TOPIC {t['code']}" in joined for t in C.TOPICS)
    _transition(s,"push" if is_div else "fade",speed="fast" if not is_div else "med")

OUT=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
print(f"Saved {OUT}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")
