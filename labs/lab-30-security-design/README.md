# Lab 30 — Analyse Wireless Security, REST API Security and Security Design

**Topic 05: Network Security** · 20% of the exam · Skills Framework K4, A6 (ICT-DIT-3009-1.1)

## Exam Objective

Describe REST API security, configure wireless security features, and describe the components of network security design (ENCOR 5.3, 5.4, 5.5).

## Scenario

You are reviewing three security designs before sign-off: the wireless authentication model for a new floor, the API integration a vendor has proposed, and the overall segmentation design. As the engineer you evaluate each against the exam's criteria — walking the 802.1X and 4-way handshake exchanges, finding the flaws in the vendor's API design, and placing each defence layer.

## What You'll Build

A completed wireless authentication comparison, an annotated 4-way handshake walkthrough, a REST API security review naming every flaw in the vendor proposal, and a layered security design map.

## Tools and Devices

Cisco Packet Tracer, WLC GUI, Postman or curl, security review worksheets.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-30-security-design.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `api-security-review.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Use Case | Recommended Method | Why | Notes |
| --- | --- | --- | --- |
| Corporate laptops | 802.1X with EAP-TLS | Certificate-based, strongest identity, no shared secret | Requires PKI and a supplicant |
| Guest Wi-Fi | WebAuth captive portal | No credential distribution, acceptable-use acceptance | Weak identity — segment guests away |
| Contractor devices | 802.1X with PEAP-MSCHAPv2 | Username and password against RADIUS/AD | Simpler than EAP-TLS, no client certificate |
| IP cameras and printers | MAB with device profiling | Cannot run a supplicant | MAC is spoofable — always pair with profiling |
| Small branch, no RADIUS | WPA2/WPA3 PSK | No server infrastructure needed | Rotate the key; every device shares it |

## Steps

1. Open lab-30-security-design/ and read the three review packs provided
2. Compare the wireless authentication methods in wireless-security.csv — PSK, 802.1X, WebAuth and MAB
3. Identify the three 802.1X roles: supplicant, authenticator and authentication server
4. Note that EAPOL carries EAP between supplicant and authenticator, and RADIUS carries it onward
5. Walk the 4-way handshake: the AP sends ANonce, the client replies with SNonce and a MIC
6. Continue the handshake: the AP sends the GTK, and the client acknowledges
7. State what the handshake proves — both sides hold the PMK, without ever transmitting it
8. Recommend an authentication method for each of the four use cases in the worksheet
9. Move to the vendor's API proposal and check whether it uses HTTP or HTTPS
10. Check how it authenticates — look for embedded credentials rather than a token
11. Check whether the token is scoped, whether it expires, and where the vendor stores it
12. Check for rate limiting and input validation on the exposed endpoints
13. List every flaw you found with the fix in api-security-review.csv
14. Now map the security design layers: threat defence, endpoint security and next-generation firewall
15. Place segmentation in the map — TrustSec SGTs for policy and MACsec for link encryption
16. Place network access control with 802.1X, MAB and WebAuth at the access edge
17. Complete security-design-map.csv naming each layer, its control and what it defends against

## Validation

Your wireless comparison recommends 802.1X for corporate, PSK or WebAuth for guest and MAB with profiling for headless devices; your 4-way handshake walkthrough has all four messages in order; and api-security-review.csv names the HTTP transport, the embedded credentials and the absent rate limiting as flaws with concrete fixes.

## Checkpoint Questions

1. What are the three roles in an 802.1X exchange?
1. What does the 4-way handshake prove, and what does it never transmit?
1. Why is MAB weak, and what is normally paired with it?
1. What is the difference between a 401 and a 403 in REST API terms?

## Exam Focus

802.1X roles: supplicant, authenticator, authentication server. EAPOL runs supplicant-to-authenticator; RADIUS carries it onward. The 4-way handshake derives PTK/GTK from the PMK without ever transmitting the key.
