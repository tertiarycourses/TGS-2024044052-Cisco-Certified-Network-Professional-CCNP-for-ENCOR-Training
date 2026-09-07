# Lab 32 — Construct and Validate JSON-Encoded Files

**Topic 06: Network Automation** · 15% of the exam · Skills Framework K6, A5 (ICT-DIT-3009-1.1)

## Exam Objective

Construct valid JSON-encoded files (ENCOR 6.2).

## Scenario

Every REST API you will touch speaks JSON, and the exam presents you with JSON that is subtly invalid and asks you to spot why. As the automation engineer you construct a valid device inventory in JSON, deliberately break it in each of the classic ways, and learn to read a parser error back to the exact character that caused it.

## What You'll Build

A valid nested JSON device inventory that passes validation, a set of four broken variants each demonstrating a different classic error, and a Python script that parses the valid file into a dictionary.

## Tools and Devices

Python 3.10+, a text editor, json module, sample API payloads.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-32-json.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Field | JSON Type | Example Value | Valid | Common Error |
| --- | --- | --- | --- | --- |
| hostname | string | "R1-CORE" | yes | Single quotes instead of double |
| mgmt_ip | string | "10.1.1.1" | yes | Unquoted key |
| uptime_days | number | 412 | yes | Quoting a number is legal but changes the type |
| enabled | boolean | true | yes | Capitalised True — that is Python, not JSON |
| last_error | null | null | yes | Using None — that is Python, not JSON |
| interfaces | array | [{...},{...}] | yes | Trailing comma after the last element |
| location | object | {"site":"HQ"} | yes | A // comment anywhere in the file |

## Steps

1. Open lab-32-json/ and review the six JSON value types — string, number, boolean, null, array, object
2. Write a JSON object describing one device with hostname, IP, uptime and an enabled flag
3. Extend it into an array of three device objects
4. Nest an interfaces array inside each device to make the structure realistic
5. Validate the file with Python's json module

   ```text
   python3 -m json.tool devices.json
   ```

6. Break it variant 1 — add a trailing comma after the last element and re-validate

   ```text
   python3 -m json.tool broken_trailing_comma.json
   ```

7. Read the parser error and note it names the line and column
8. Break it variant 2 — use single quotes instead of double quotes

   ```text
   python3 -m json.tool broken_single_quotes.json
   ```

9. Break it variant 3 — add a // comment, which JSON does not allow

   ```text
   python3 -m json.tool broken_comment.json
   ```

10. Break it variant 4 — leave a key unquoted

   ```text
   python3 -m json.tool broken_unquoted_key.json
   ```

11. Parse the valid file in Python and confirm it becomes a dictionary

   ```text
   python3 parse_json.py
   ```

12. Navigate the nested structure to print the second device's first interface name

   ```text
   python3 -c "import json; d=json.load(open('devices.json')); print(d['devices'][1]['interfaces'][0]['name'])"
   ```

13. Serialise a Python dictionary back out to a JSON string with indentation

   ```text
   python3 write_json.py
   ```

14. Compare a real Cisco DNA Center response payload with your own structure

## Validation

devices.json validates cleanly with 'python3 -m json.tool', all four broken variants fail with a parser error you can explain, and your navigation command prints the correct nested interface name.

## Checkpoint Questions

1. Name the six JSON value types.
1. Why is a trailing comma invalid in JSON?
1. What is wrong with True and None in a JSON file?
1. What Python type does a JSON object become when parsed?

## Exam Focus

The classic invalid-JSON traps are a trailing comma, single quotes, an unquoted key, a comment, and Python's True/None instead of JSON's true/null. Keys are ALWAYS in double quotes.
