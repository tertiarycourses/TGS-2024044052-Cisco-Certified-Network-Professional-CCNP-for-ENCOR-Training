# Lab 31 — Interpret Python Components and Scripts

**Topic 06: Network Automation** · 15% of the exam · Skills Framework K6, A5 (ICT-DIT-3009-1.1)

## Exam Objective

Interpret basic Python components and scripts (ENCOR 6.1).

## Scenario

The ENCOR exam does not ask you to write an application — it shows you a script and asks what it prints. As the network engineer moving into automation, you work through the Python that actually appears in network scripts: lists and dictionaries holding device inventories, loops that iterate them, conditionals that branch on state, and functions that return values.

## What You'll Build

A set of correctly predicted script outputs, a working device-inventory script that loops a list of dictionaries, and a written explanation of the one deliberate bug you fix.

## Tools and Devices

Python 3.10+, VS Code or any editor, devices.py sample scripts.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-31-python.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Device | Hostname | Management IP | Platform | Status | Uptime (days) |
| --- | --- | --- | --- | --- | --- |
| 1 | R1-CORE | 10.1.1.1 | ISR4451 | up | 412 |
| 2 | R2-EDGE | 10.1.1.2 | ISR4331 | up | 287 |
| 3 | SW1-ACC | 10.1.2.11 | C9200-24P | up | 198 |
| 4 | SW2-ACC | 10.1.2.12 | C9200-24P | down | 0 |
| 5 | SW3-DIST | 10.1.2.1 | C9300-48U | up | 365 |
| 6 | WLC1 | 10.1.3.1 | C9800-CL | up | 145 |

## Steps

1. Open lab-31-python/ and read devices.py before running anything
2. Predict the output of the first script on paper, then run it and compare

   ```text
   python3 predict_01.py
   ```

3. Examine the list of device dictionaries that models the inventory
4. Access a single value by its key and print it

   ```text
   python3 -c "d={'host':'R1','ip':'10.1.1.1'}; print(d['ip'])"
   ```

5. Loop the inventory and print each device's hostname and IP

   ```text
   python3 loop_inventory.py
   ```

6. Add a conditional that flags any device whose status is not 'up'

   ```text
   python3 check_status.py
   ```

7. Read the function that returns a filtered list and note what it returns
8. Predict what happens when a key that does not exist is accessed

   ```text
   python3 predict_02.py
   ```

9. Fix it using .get() with a default so the script does not raise KeyError
10. Use the requests library to call a REST endpoint and print the status code

   ```text
   python3 api_call.py
   ```

11. Read the response object — note .status_code, .headers and .json() are different things
12. Find and fix the deliberate indentation bug in buggy.py

   ```text
   python3 buggy.py
   ```

13. Explain in a comment what the bug was and why Python cared
14. Run the full inventory report script and check the output matches your prediction

   ```text
   python3 inventory_report.py
   ```


## Validation

Your written predictions match the actual output of every script, inventory_report.py runs without error and prints one line per device, and buggy.py runs correctly after your fix with a comment explaining the indentation error.

## Checkpoint Questions

1. What is the difference between a list and a dictionary in Python?
1. How do you safely access a dictionary key that may not exist?
1. What does .json() return when called on a requests response?
1. Why does Python raise an error on inconsistent indentation?

## Exam Focus

You will be shown a script and asked what it prints — not asked to write one. Practise reading list-of-dictionary structures, loops and conditionals, and know that .get() avoids a KeyError.
