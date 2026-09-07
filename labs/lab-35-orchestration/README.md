# Lab 35 — Compare Agent and Agentless Orchestration Tools

**Topic 06: Network Automation** · 15% of the exam · Skills Framework K6, A5 (ICT-DIT-3009-1.1)

## Exam Objective

Compare agent versus agentless orchestration tools such as Chef, Puppet, Ansible and SaltStack (ENCOR 6.7).

## Scenario

Your organisation must pick one configuration management tool for a network of 300 Cisco devices that cannot run third-party agents. As the engineer making the recommendation you compare the four tools on architecture, transport, language and network-device suitability, then write and read a small Ansible playbook to prove the agentless model works on IOS.

## What You'll Build

A completed four-tool comparison matrix, a written recommendation justified on the agent constraint, and an annotated Ansible playbook that configures an IOS interface idempotently.

## Tools and Devices

Python 3.10+, Ansible, a text editor, tool comparison worksheet.

## Lab Files

| File | What it is |
| --- | --- |
| `lab-35-orchestration.pkt` | The Cisco Packet Tracer topology for this lab |
| `addressing-table.csv` | Every device, interface and address used here |
| `topology.md` | The topology diagram in text form |

## Addressing Table

| Tool | Architecture | Model | Transport | Language | Agent on Device? | Suitable for IOS? |
| --- | --- | --- | --- | --- | --- | --- |
| Puppet | Master / agent | Pull | TCP 8140 | Ruby DSL | Yes | No — requires an agent |
| Chef | Server / client | Pull | HTTPS | Ruby recipes | Yes | No — requires an agent |
| Ansible | Control node only | Push | SSH / NETCONF / API | YAML playbooks | No | Yes — agentless |
| SaltStack | Master / minion | Push | ZeroMQ (or SSH) | YAML states | Yes by default | Only in agentless salt-ssh mode |

## Steps

1. Open lab-35-orchestration/ and read the requirement: 300 IOS devices, no agents permitted
2. Record Puppet's architecture — agent-based, pull model, Ruby DSL, master/agent
3. Record Chef's architecture — agent-based, pull model, Ruby recipes and cookbooks
4. Record Ansible's architecture — agentless, push model, YAML playbooks over SSH or API
5. Record SaltStack's architecture — minion-based by default, but supports agentless SSH mode
6. Mark which transports each uses and which port
7. Apply the constraint: eliminate any tool that requires an agent on the network device
8. Read the provided Ansible inventory file and identify the group and host variables
9. Read the playbook and identify the hosts, tasks and module in use
10. Run the playbook in check mode first so nothing is changed

   ```text
   ansible-playbook -i inventory configure_interface.yml --check
   ```

11. Run it for real and read the changed count in the play recap

   ```text
   ansible-playbook -i inventory configure_interface.yml
   ```

12. Run it a second time and observe the changed count is now zero

   ```text
   ansible-playbook -i inventory configure_interface.yml
   ```

13. Explain in your notes what idempotency means and why it makes re-running safe
14. Complete orchestration-comparison.csv with all four tools across every dimension
15. Write your recommendation with the constraint that decided it

## Validation

orchestration-comparison.csv correctly classifies Puppet and Chef as agent-based pull and Ansible as agentless push, the playbook reports changed=1 on the first run and changed=0 on the second, and your recommendation names Ansible with the no-agent constraint as the reason.

## Checkpoint Questions

1. Which of the four tools are agent-based, and which are agentless?
1. Why does the no-agent constraint rule out Puppet and Chef for IOS?
1. What does idempotency mean, and how did the playbook demonstrate it?
1. What is the difference between a push and a pull model?

## Exam Focus

Puppet and Chef are agent-based pull; Ansible is agentless push over SSH/API; SaltStack is minion-based unless run in salt-ssh mode. Network devices that cannot run an agent are why Ansible dominates network automation.
