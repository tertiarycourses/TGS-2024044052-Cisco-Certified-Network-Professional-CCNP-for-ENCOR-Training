# Lab 33 — Explore YANG Models and Call the DNA Center API

**Topic 06: Network Automation** · 15% of the exam · Skills Framework K6, A5 (ICT-DIT-3009-1.1)

## Exam Objective

Describe the principles and benefits of YANG, describe APIs for Cisco DNA Center and vManage, and interpret REST API response codes (ENCOR 6.3, 6.4, 6.5).

## Scenario

Your team is scripting against Cisco DNA Center, and the first attempts are failing with codes nobody can interpret. As the automation engineer you walk the YANG model that defines the data, authenticate correctly to obtain an X-Auth-Token, then work through the response codes deliberately — including the 401 versus 403 distinction that decides whether you fix the token or the account's permissions.

## What You'll Build

A YANG model walkthrough naming containers, lists and leaves, a successful token request, a device inventory retrieved with that token, and a completed response-code interpretation table.

## Tools and Devices

Python 3.10+, requests library, curl or Postman, DNA Center sandbox or provided mock API.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-33-yang-dnac.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `yang-model-extract.csv` | The mock data set this lab works with |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| HTTP Code | Meaning | What Went Wrong | What To Do |
| --- | --- | --- | --- |
| 200 | OK | Nothing — the request succeeded | Parse the response body |
| 201 | Created | The resource was created | Read the Location header for its URI |
| 204 | No Content | Succeeded, nothing to return | Common after a DELETE |
| 400 | Bad Request | Malformed syntax or invalid JSON | Validate the payload before sending |
| 401 | Unauthorized | Token missing, wrong or expired | Request a new token |
| 403 | Forbidden | Token is valid but the account lacks permission | Fix the account's role, not the token |
| 404 | Not Found | The URI does not exist | Check the endpoint path and the API version |
| 429 | Too Many Requests | You exceeded the rate limit | Back off and retry, honouring Retry-After |
| 500 | Internal Server Error | The server failed | Retry; if persistent, it is not your script |

## Steps

1. Open lab-33-yang-dnac/ and read the ietf-interfaces YANG model extract provided
2. Identify the container — the node that groups related data but does not repeat
3. Identify the list and its key — the node that repeats, one entry per interface
4. Identify the leaves and their types — name is a string, enabled is a boolean
5. State the benefit: one model drives both NETCONF XML and RESTCONF JSON
6. Request an authentication token from DNA Center using Basic auth

   ```text
   curl -k -X POST -u devnetuser:Cisco123! https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token
   ```

7. Read the JSON response and extract the Token value
8. Use that token in the X-Auth-Token header to list network devices

   ```text
   curl -k -H 'X-Auth-Token: <token>' https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device
   ```

9. Confirm the response code is 200 and count the devices returned
10. Now send the same request with no token and record the response code

   ```text
   curl -k -i https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device
   ```

11. Send it with a deliberately corrupted token and record the code
12. Interpret the difference: 401 means unauthenticated, 403 means authenticated but not permitted
13. Request a URL that does not exist and record the 404
14. Run the provided Python script that automates token then inventory

   ```text
   python3 dnac_inventory.py
   ```

15. Note how vManage differs — a session cookie from /j_security_check plus an XSRF token
16. Complete response-codes.csv with each code, its meaning and the action you would take

## Validation

The token request returns 200 with a Token value, the authenticated inventory call returns 200 with a device list, the unauthenticated call returns 401, and response-codes.csv correctly distinguishes 401 (fix the token) from 403 (fix the permissions).

## Checkpoint Questions

1. What does a container do in a YANG model, and how does a list differ?
1. Which header carries the DNA Center token, and how do you obtain it?
1. What is the difference between a 401 and a 403?
1. What does a 429 tell you to do?

## Exam Focus

Token flow: POST with Basic auth to get an X-Auth-Token, then send that token in the header. 401 means fix the token; 403 means fix the account's permissions. That distinction is examined directly.
