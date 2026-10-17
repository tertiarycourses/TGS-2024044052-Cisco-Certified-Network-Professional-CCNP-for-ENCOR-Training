# Cisco Certified Network Professional (CCNP) for ENCOR Training

**WSQ Course Code:** TGS-2024044052 · **Duration:** 5 days (40 hours) · **Version:** v6.0

Courseware for the WSQ course *Cisco Certified Network Professional (CCNP) for ENCOR Training*, delivered by
**Tertiary Infotech Academy Pte Ltd** (UEN 201200696W). The course prepares learners for the Cisco
**350-401 ENCOR v1.1** exam — *Implementing Cisco Enterprise Network Core Technologies* — the core exam for
both CCNP Enterprise and CCIE Enterprise.

**[Register for this course →](https://www.tertiarycourses.com.sg/wsq-cisco-certified-network-professional-ccnp-for-encor-training.html)**

**Funding:** up to 70% course-fee funding for eligible learners and SMEs. Eligibility and terms apply — see the registration page.

---

## What learners can do by the end

| | Learning outcome |
| --- | --- |
| **LO1** | Translate organizational networking needs into technical configurations by selecting appropriate network components, considering their functions and interdependencies. |
| **LO2** | Identify and choose key network components for configuration, utilizing techniques in server and device implementation aligned with technical requirements. |
| **LO3** | Implement a variety of servers and devices effectively, following the organizational network blueprint to enhance network performance and reliability. |
| **LO4** | Manage network access, ensuring compliance with organizational guidelines and specifications to maintain secure and efficient user connectivity. |
| **LO5** | Select and deploy network management tools effectively, optimizing network performance and user experience in line with organizational needs. |
| **LO6** | Conduct regular network reporting and administration, employing assessment tools to ensure network stability and alignment with organizational objectives. |

## Course structure — the six ENCOR exam domains

The six topics **are** the six exam domains, in blueprint order and with the published weightings, so class
time is proportional to exam time.

| Topic | Exam domain | Weighting | Labs | TSC |
| --- | --- | --- | --- | --- |
| 1 | Enterprise Architecture | 15% | 1–5 | K1, A1 |
| 2 | Virtualization Technologies | 10% | 6–9 | K2, A2 |
| 3 | Network Infrastructure | 30% | 10–21 | K3, A3 |
| 4 | Network Assurance | 10% | 22–25 | K5, A4 |
| 5 | Network Security | 20% | 26–30 | K4, A6 |
| 6 | Network Automation | 15% | 31–35 | K6, A5 |

**Skills Framework:** TSC *Network Configuration* — `ICT-DIT-3009-1.1`

## Courseware

| Artifact | File |
| --- | --- |
| Trainer slides (211 slides) | [`courseware/Cisco Certified Network Professional (CCNP) for ENCOR Training-v6.0.pptx`](courseware/) |
| Learner slides (PDF) | [`courseware/Cisco Certified Network Professional (CCNP) for ENCOR Training-v6.0.pdf`](courseware/) |
| Lesson Plan | [`courseware/LP-Cisco Certified Network Professional (CCNP) for ENCOR Training.docx`](courseware/) |
| Learner Guide | [`courseware/LG-Cisco Certified Network Professional (CCNP) for ENCOR Training.docx`](courseware/) |
| Learner Guide (Markdown mirror) | [`LG-Cisco Certified Network Professional (CCNP) for ENCOR Training.md`](LG-Cisco%20Certified%20Network%20Professional%20%28CCNP%29%20for%20ENCOR%20Training.md) |
| Labs (35) | [`labs/`](labs/README.md) |

> The assessment papers are **confidential** and are distributed through Google Drive and the LMS only.
> They are deliberately excluded from this repository.

## Labs

35 hands-on labs, one folder each, covering every objective in the blueprint. Every folder carries its own
Cisco Packet Tracer topology, an addressing table, a mock data set and a README with the full procedure,
validation checks, checkpoint questions and an exam-focus note.

Start at the **[labs index](labs/README.md)**; the environment setup is in **[labs/tools.md](labs/tools.md)**.

## Lab environment

- **Cisco Packet Tracer 8.2+** (free from the [Cisco Networking Academy](https://www.netacad.com)) — the primary lab environment
- **Cisco IOS / IOS XE CLI** — every command transfers directly to real 9200/9300 switches and ISR/Catalyst routers
- **Wireless LAN Controller (WLC)** GUI — for the WLAN, WPA2-Enterprise and wireless troubleshooting labs
- **Python 3.10+**, **Postman or curl** — for the automation and REST API labs

## Assessment

| Instrument | Duration | Format |
| --- | --- | --- |
| Written Assessment (WA) — Short-Answer Questions (SAQ) | 1 hour | Individual, summative, open book |
| Practical Performance (PP) — hands-on configuration tasks | 1 hour | Individual, summative, open book |

A minimum **75% attendance** is required to be eligible for assessment and funding.

## Practice exam

Practise against the matching exam bank before sitting 350-401:
**<https://exams.tertiaryinfotech.com/practice-exams/cisco/cisco-ccnp-encor>** — 200 original questions across
two full 100-question exams, 120 minutes each, weighted to the same six domains. A free sample exam is
available.

## Rebuilding the courseware

All artifacts are generated from one source (`course_data.py` + `data_domain1..6.py`), so the slides, Lesson
Plan, Learner Guide and labs can never drift apart:

```bash
bash .claude/skills/courseware-build/build/build_courseware.sh   # PPT + LP + LG + PDFs
python3 .claude/skills/courseware-build/build/build_labs.py      # the labs/ tree
python3 .claude/skills/courseware-build/build/build_assets.py    # the diagram assets
```

---

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · [www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)
