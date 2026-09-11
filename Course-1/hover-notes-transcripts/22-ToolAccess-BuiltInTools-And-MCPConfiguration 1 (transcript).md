---
hovernotes-transcript-of: doc_593607eb-1ce8-446e-9d3b-903314fe2774
hovernotes-transcript-version: 2
note: "[[22-ToolAccess-BuiltInTools-And-MCPConfiguration 1]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview"
updated: 2026-09-04T16:17:42.102Z
---

# 22-ToolAccess-BuiltInTools-And-MCPConfiguration 1 — Transcript

**0:00 → 0:43**

In the previous lesson, we improved individual tools. Now we need to decide which tools an agent should actually have. A common mistake is giving one agent access to everything. That sounds flexible, but it can make tool selection less reliable. Let's start with an over-provisioned ShopAssist support agent. This agent has too many tools. Some are useful for support. Some belong to refunds, inventory marketing, reporting, or internal operations. And some are risky, like run SQL query or write internal policy. The issue is not only security, it is also reliability. When Claude sees too many tools, especially tools with overlapping purposes, it has more

**0:43 → 1:28**

to choose the wrong one. For a normal return conversation, the main support agent does not need inventory updates, marketing emails, SQL access, or policy writing. A better design is scoped tool access. This agent can identify the customer, look up an order, check refund eligibility, and escalate when needed. That is enough for the main support role. Other tools can belong to specialized agents. This prevents cross-specialization misuse. The support agent should not accidentally update inventory. The inventory agent should not issue refunds, and the policy agent should not modify customer orders. Some tools can still be shared across roles. For

**1:28 → 2:13**

Both the support agent and the refund agent may need lookup order by ID. The goal is not to make every tool exclusive. The goal is to give each agent the smallest useful set of tools for its job. Now let's connect this to tool choice. In tool workflows, tool choice controls how much freedom Claude has. Use auto for normal flexible conversations. Use any when the workflow requires some tool call before continuing. For example, every refund decision may need back-end order data. Use force tool selection when the application already knows the exact next step. But do not overuse force tool choice. If the application forces the wrong tool, Claude cannot choose a better one. Now let's talk about built-in tools.

**2:13 → 2:58**

In Cloud code style workflows, Cloud may have tools like read, write, edit, bash, grab, and globe. These are development tools, not shop assist business tools. Read inspects a file. Write creates or overwrites a file. Edit makes targeted modifications. Bash runs shell commands. Grab searches inside file contents. Globe matches file paths. For example, if Cloud needs to find refund logic, use grab. If Cloud needs to find policy files by path, use globe. The difference is simple. Grab searches content. Globe matches paths. For code changes, edit is usually best when there is a unique text match. but if edit cannot match the target,

**2:58 → 3:44**

text uniquely, Claude may need a safer fallback. Read the file, understand the current content, modify the content carefully, write the updated version back. This is why incremental codebase understanding matters. Claude should search, inspect, understand the surrounding code, and then make the smallest save change. Now let's move to MCP configuration. MCP servers expose external capabilities to Claude. These capabilities can be tools or resources. An MCP tool is something Claude can call to perform an action. Get customer by email, lookup order by ID, process refund. An An MCP resource is content Cloud can read as context.

**3:44 → 4:29**

policy MD, shipping policy MD, support macro catalog MD. So the distinction is tools do work. Resources provide content. For ShopAssist, customer lookup, order lookup, and refund processing should be MCP tools. Policy documents and support playbooks can be MCP resources. A project can define MCP servers in a project-scoped MCP JSON file. This configuration belongs to the project. It lets the project define which MCP servers are available. Notice the environment variable expansion. We do not hard code credentials in the config. The config references an environment variable, and the actual secret comes from the developer's environment. There can also be user

**4:29 → 5:14**

MCP configuration in Cloud JSON. The difference is scope. MCP JSON belongs to the project. Cloud JSON belongs to the individual developer's local cloud setup. Multiple MCP servers can be available at the same time, but that does not mean every agent should use every tool from every server. The servers expose capabilities. The agent design still decides which tools are allowed for each role. Finally, MCP servers can be community built or custom built. Community MCP servers are useful for common integrations like file systems, GitHub, databases, or developer tools. Custom MCP servers are better for business specific systems. For Shopify,

**5:14 → 5:59**

we would likely build custom MCP servers for customers, orders, refunds, and support policies, because those systems have specific permissions, schemas, and error behavior. So the main lesson is, do not give every agent every tool. Give each agent the smallest useful tool set for its role. Use tool choice to control whether Claude may call tools, must call a tool, or must call a specific tool. Use built-in development tools, carefully for reading, searching, editing, and running commands. Use MCP tools for actions. Use MCP resources for content catalogs. And configure MCP servers at the right scope, project level for shared project capabilities and user level for

**5:59 → 6:16**

personal local setup. For ShopAssist, the main support agent gets a small set of support tools. Specialized sub agents handle refunds, inventory, or policy work. And backend systems are exposed through MCP servers with
