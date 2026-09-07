"""
Domain 6 — Network Automation (ENCOR 6.0, 15%).  Labs 31–35.
"""

DOMAIN6 = [
    dict(
        num=31, topic=6,
        title="Interpret Python Components and Scripts",
        objective="Interpret basic Python components and scripts (ENCOR 6.1).",
        desc=(
            "The ENCOR exam does not ask you to write an application — it shows you a script and asks what it "
            "prints. As the network engineer moving into automation, you work through the Python that actually "
            "appears in network scripts: lists and dictionaries holding device inventories, loops that iterate "
            "them, conditionals that branch on state, and functions that return values."
        ),
        build="A set of correctly predicted script outputs, a working device-inventory script that loops a list of dictionaries, and a written explanation of the one deliberate bug you fix.",
        services="Python 3.10+, VS Code or any editor, devices.py sample scripts",
        steps=[
            ("Open lab-31-python/ and read devices.py before running anything", ""),
            ("Predict the output of the first script on paper, then run it and compare", "python3 predict_01.py"),
            ("Examine the list of device dictionaries that models the inventory", ""),
            ("Access a single value by its key and print it", "python3 -c \"d={'host':'R1','ip':'10.1.1.1'}; print(d['ip'])\""),
            ("Loop the inventory and print each device's hostname and IP", "python3 loop_inventory.py"),
            ("Add a conditional that flags any device whose status is not 'up'", "python3 check_status.py"),
            ("Read the function that returns a filtered list and note what it returns", ""),
            ("Predict what happens when a key that does not exist is accessed", "python3 predict_02.py"),
            ("Fix it using .get() with a default so the script does not raise KeyError", ""),
            ("Use the requests library to call a REST endpoint and print the status code", "python3 api_call.py"),
            ("Read the response object — note .status_code, .headers and .json() are different things", ""),
            ("Find and fix the deliberate indentation bug in buggy.py", "python3 buggy.py"),
            ("Explain in a comment what the bug was and why Python cared", ""),
            ("Run the full inventory report script and check the output matches your prediction", "python3 inventory_report.py"),
        ],
        test="Your written predictions match the actual output of every script, inventory_report.py runs without error and prints one line per device, and buggy.py runs correctly after your fix with a comment explaining the indentation error.",
    ),
    dict(
        num=32, topic=6,
        title="Construct and Validate JSON-Encoded Files",
        objective="Construct valid JSON-encoded files (ENCOR 6.2).",
        desc=(
            "Every REST API you will touch speaks JSON, and the exam presents you with JSON that is subtly "
            "invalid and asks you to spot why. As the automation engineer you construct a valid device "
            "inventory in JSON, deliberately break it in each of the classic ways, and learn to read a parser "
            "error back to the exact character that caused it."
        ),
        build="A valid nested JSON device inventory that passes validation, a set of four broken variants each demonstrating a different classic error, and a Python script that parses the valid file into a dictionary.",
        services="Python 3.10+, a text editor, json module, sample API payloads",
        steps=[
            ("Open lab-32-json/ and review the six JSON value types — string, number, boolean, null, array, object", ""),
            ("Write a JSON object describing one device with hostname, IP, uptime and an enabled flag", ""),
            ("Extend it into an array of three device objects", ""),
            ("Nest an interfaces array inside each device to make the structure realistic", ""),
            ("Validate the file with Python's json module", "python3 -m json.tool devices.json"),
            ("Break it variant 1 — add a trailing comma after the last element and re-validate", "python3 -m json.tool broken_trailing_comma.json"),
            ("Read the parser error and note it names the line and column", ""),
            ("Break it variant 2 — use single quotes instead of double quotes", "python3 -m json.tool broken_single_quotes.json"),
            ("Break it variant 3 — add a // comment, which JSON does not allow", "python3 -m json.tool broken_comment.json"),
            ("Break it variant 4 — leave a key unquoted", "python3 -m json.tool broken_unquoted_key.json"),
            ("Parse the valid file in Python and confirm it becomes a dictionary", "python3 parse_json.py"),
            ("Navigate the nested structure to print the second device's first interface name", "python3 -c \"import json; d=json.load(open('devices.json')); print(d['devices'][1]['interfaces'][0]['name'])\""),
            ("Serialise a Python dictionary back out to a JSON string with indentation", "python3 write_json.py"),
            ("Compare a real Cisco DNA Center response payload with your own structure", ""),
        ],
        test="devices.json validates cleanly with 'python3 -m json.tool', all four broken variants fail with a parser error you can explain, and your navigation command prints the correct nested interface name.",
    ),
    dict(
        num=33, topic=6,
        title="Explore YANG Models and Call the DNA Center API",
        objective="Describe the principles and benefits of YANG, describe APIs for Cisco DNA Center and vManage, and interpret REST API response codes (ENCOR 6.3, 6.4, 6.5).",
        desc=(
            "Your team is scripting against Cisco DNA Center, and the first attempts are failing with codes "
            "nobody can interpret. As the automation engineer you walk the YANG model that defines the data, "
            "authenticate correctly to obtain an X-Auth-Token, then work through the response codes "
            "deliberately — including the 401 versus 403 distinction that decides whether you fix the token "
            "or the account's permissions."
        ),
        build="A YANG model walkthrough naming containers, lists and leaves, a successful token request, a device inventory retrieved with that token, and a completed response-code interpretation table.",
        services="Python 3.10+, requests library, curl or Postman, DNA Center sandbox or provided mock API",
        steps=[
            ("Open lab-33-yang-dnac/ and read the ietf-interfaces YANG model extract provided", ""),
            ("Identify the container — the node that groups related data but does not repeat", ""),
            ("Identify the list and its key — the node that repeats, one entry per interface", ""),
            ("Identify the leaves and their types — name is a string, enabled is a boolean", ""),
            ("State the benefit: one model drives both NETCONF XML and RESTCONF JSON", ""),
            ("Request an authentication token from DNA Center using Basic auth", "curl -k -X POST -u devnetuser:Cisco123! https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token"),
            ("Read the JSON response and extract the Token value", ""),
            ("Use that token in the X-Auth-Token header to list network devices", "curl -k -H 'X-Auth-Token: <token>' https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"),
            ("Confirm the response code is 200 and count the devices returned", ""),
            ("Now send the same request with no token and record the response code", "curl -k -i https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device"),
            ("Send it with a deliberately corrupted token and record the code", ""),
            ("Interpret the difference: 401 means unauthenticated, 403 means authenticated but not permitted", ""),
            ("Request a URL that does not exist and record the 404", ""),
            ("Run the provided Python script that automates token then inventory", "python3 dnac_inventory.py"),
            ("Note how vManage differs — a session cookie from /j_security_check plus an XSRF token", ""),
            ("Complete response-codes.csv with each code, its meaning and the action you would take", ""),
        ],
        test="The token request returns 200 with a Token value, the authenticated inventory call returns 200 with a device list, the unauthenticated call returns 401, and response-codes.csv correctly distinguishes 401 (fix the token) from 403 (fix the permissions).",
    ),
    dict(
        num=34, topic=6,
        title="Construct an EEM Applet to Automate Response",
        objective="Construct an EEM applet to automate configuration, troubleshooting or data collection (ENCOR 6.6).",
        desc=(
            "A critical WAN interface flaps at night and nobody captures the state before it recovers, so the "
            "cause is never found. As the engineer you make the device investigate itself: an EEM applet that "
            "triggers on the syslog message, runs the diagnostic commands, writes the output to a file and "
            "logs a summary — automation with no external server involved."
        ),
        build="Two working EEM applets — one syslog-triggered applet that collects diagnostics on an interface down event, and one timed applet that logs a periodic health snapshot.",
        services="Cisco Packet Tracer, Cisco IOS CLI, R1 router",
        steps=[
            ("Open lab-34-eem/lab-34-eem.pkt and confirm you can see the interface down syslog message", "R1# show logging | include LINEPROTO"),
            ("Create the applet and give it a descriptive name", "R1(config)# event manager applet INTERFACE-DOWN"),
            ("Define the syslog event detector matching the interface down pattern", "R1(config-applet)# event syslog pattern \"Interface Serial0/0/0, changed state to down\""),
            ("Add the first action — enter privileged mode, since the applet starts unprivileged", "R1(config-applet)# action 1.0 cli command \"enable\""),
            ("Collect the interface state", "R1(config-applet)# action 2.0 cli command \"show interfaces Serial0/0/0\""),
            ("Collect the routing table at the moment of failure", "R1(config-applet)# action 3.0 cli command \"show ip route\""),
            ("Write a syslog message recording that the applet ran", "R1(config-applet)# action 4.0 syslog msg \"EEM: Serial0/0/0 down - diagnostics collected\""),
            ("Note the numbering convention — 1.0, 2.0, 3.0 sorts lexically, whereas 1, 2, 10 does not", ""),
            ("Trigger the applet by shutting the interface", "R1(config-if)# shutdown"),
            ("Read the log and confirm the applet's message appears", "R1# show logging | include EEM"),
            ("Verify the applet registered and check its run count", "R1# show event manager policy registered"),
            ("Check the statistics for how many times it has fired", "R1# show event manager statistics policy"),
            ("Now create a second applet on a timer for a periodic health snapshot", "R1(config)# event manager applet HEALTH-CHECK"),
            ("Set the timer event to fire every 300 seconds", "R1(config-applet)# event timer watchdog time 300"),
            ("Add the CPU check action", "R1(config-applet)# action 1.0 cli command \"show processes cpu | include CPU\""),
            ("Log the snapshot", "R1(config-applet)# action 2.0 syslog msg \"EEM: periodic health snapshot taken\""),
            ("Bring the interface back and confirm both applets are registered", "R1(config-if)# no shutdown"),
        ],
        test="'show event manager policy registered' lists both applets, shutting Serial0/0/0 produces the 'EEM: Serial0/0/0 down' syslog entry, and 'show event manager statistics policy' shows a non-zero run count for the triggered applet.",
    ),
    dict(
        num=35, topic=6,
        title="Compare Agent and Agentless Orchestration Tools",
        objective="Compare agent versus agentless orchestration tools such as Chef, Puppet, Ansible and SaltStack (ENCOR 6.7).",
        desc=(
            "Your organisation must pick one configuration management tool for a network of 300 Cisco devices "
            "that cannot run third-party agents. As the engineer making the recommendation you compare the "
            "four tools on architecture, transport, language and network-device suitability, then write and "
            "read a small Ansible playbook to prove the agentless model works on IOS."
        ),
        build="A completed four-tool comparison matrix, a written recommendation justified on the agent constraint, and an annotated Ansible playbook that configures an IOS interface idempotently.",
        services="Python 3.10+, Ansible, a text editor, tool comparison worksheet",
        steps=[
            ("Open lab-35-orchestration/ and read the requirement: 300 IOS devices, no agents permitted", ""),
            ("Record Puppet's architecture — agent-based, pull model, Ruby DSL, master/agent", ""),
            ("Record Chef's architecture — agent-based, pull model, Ruby recipes and cookbooks", ""),
            ("Record Ansible's architecture — agentless, push model, YAML playbooks over SSH or API", ""),
            ("Record SaltStack's architecture — minion-based by default, but supports agentless SSH mode", ""),
            ("Mark which transports each uses and which port", ""),
            ("Apply the constraint: eliminate any tool that requires an agent on the network device", ""),
            ("Read the provided Ansible inventory file and identify the group and host variables", ""),
            ("Read the playbook and identify the hosts, tasks and module in use", ""),
            ("Run the playbook in check mode first so nothing is changed", "ansible-playbook -i inventory configure_interface.yml --check"),
            ("Run it for real and read the changed count in the play recap", "ansible-playbook -i inventory configure_interface.yml"),
            ("Run it a second time and observe the changed count is now zero", "ansible-playbook -i inventory configure_interface.yml"),
            ("Explain in your notes what idempotency means and why it makes re-running safe", ""),
            ("Complete orchestration-comparison.csv with all four tools across every dimension", ""),
            ("Write your recommendation with the constraint that decided it", ""),
        ],
        test="orchestration-comparison.csv correctly classifies Puppet and Chef as agent-based pull and Ansible as agentless push, the playbook reports changed=1 on the first run and changed=0 on the second, and your recommendation names Ansible with the no-agent constraint as the reason.",
    ),
]
