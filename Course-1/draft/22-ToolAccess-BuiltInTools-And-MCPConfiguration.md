---
title: "Course: Claude Certified Architect Foundations: Complete Course | Udemy"
description: Pass the Claude Architect exam and build production-style AI apps with tools, agents, MCP, Claude Code, and evals.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042305#overview
created: "2026-09-04"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/22-ToolAccess-BuiltInTools-And-MCPConfiguration 1 (transcript)|Transcript]]"
hovernotes-id: doc_593607eb-1ce8-446e-9d3b-903314fe2774
---

![00:00:16](hover-notes-images/screenshot-01M1PK5H41ATS2EGG892HFTJGF.png)
[00:00:16](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

## Tool Access Scoping

- **[The Goal]** Deciding which specific tools an agent should actually have access to
- **[The Anti-Pattern]** Over-provisioning an agent with too many tools
    - While it seems flexible, it makes tool selection less reliable

### Over-provisioned ShopAssist Support Agent

- An example of an agent with fifteen tools that include inappropriate or risky functions:

```python
main_support_agent_tools = [
      get_customer_by_email, lookup_order_by_id, check_refund_eligibility,
      process_refund, create_human_escalation, update_shipping_address, cancel_order,
      create_discount_code, search_product_catalog, update_product_inventory,
      read_internal_policy, write_internal_policy, run_sql_query, send_marketing_email,
      create_support_report
  ]
```

    - **Risky tools included:** `run_sql_query` and `write_internal_policy` (belong to internal operations/policy)
    - **Irrelevant tools included:** Tools belonging to refunds, inventory, marketing, reporting, or internal operations

### Why Over-provisioning Backfires

- **Reliability, not just security:** The primary issue is that too many tools make selection less reliable
    - Overlapping purposes give the model (e.g., Claude) more chances to pick the wrong tool
    - For example, a normal return conversation needs none of the inventory, marketing, SQL, or policy-writing tools

![00:00:45](hover-notes-images/screenshot-01M1PK6E4Z94PPCWFJG6GW9QZY.png)
[00:00:45](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:01:08](hover-notes-images/screenshot-01M1PK6E50XMRAVRGF3ZP06EQ0.png)
[00:01:08](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:01:25](hover-notes-images/screenshot-01M1PK6E50NV99RVB155DDG72Z.png)
[00:01:25](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

### Multi-Agent Design with Scoped Access

- **[The Strategy]** Instead of one agent with all tools, use specialized agents that only receive the tools required for their specific role
    - This prevents cross-specialization misuse (e.g., a support agent accidentally updating inventory)

#### Specialized Agent Tool Sets

```python
refund_agent_tools = ["lookup_order_by_id", "check_refund_eligibility", "process_refund"]

inventory_agent_tools = ["search_product_catalog", "update_product_inventory"]

policy_agent_tools = ["read_internal_policy", "create_support_report"]
```

#### Scoped Tool Distribution

To maintain functionality while minimizing risk, tools are distributed based on the agent's primary responsibility. Some tools, like `lookup_order_by_id`, can be shared across multiple roles to ensure they have the necessary context.

![00:01:29](hover-notes-images/screenshot-01M1PK7C4KR927JYDNAS3CFVW7.png)
[00:01:29](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:01:43](hover-notes-images/screenshot-01M1PK7C4KEGYJC9BR2Y7DH4HA.png)
[00:01:43](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:01:56](hover-notes-images/screenshot-01M1PK7C4K5RZS898RBTYQYPXQ.png)
[00:01:56](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

### Multi-Agent Tool Sharing

- **[The Goal]** Provide each agent with the smallest useful set of tools for its specific job
    - This does not mean every tool must be exclusive to one agent
    - For example, both a `main_support_agent` and a `refund_agent` might need access to `lookup_order_by_id` to function effectively

### Controlling Agent Freedom with `tool_choice`

`tool_choice` determines how much autonomy Claude has in deciding whether or when to call a tool.

| Mode | Behavior | Use Case |
| --- | --- | --- |
| auto | May answer directly OR call a tool | Normal, flexible conversations |
| any | Must call ONE of the available tools | When a tool call is required before continuing (e.g., needing backend order data for a refund) |
| tool (forced) | Must call a SPECIFIC tool | When the application already knows the exact next step |

- **[Warning on Forced Selection]** Do not overuse forced tool choice
    - If the application forces the wrong tool, the model is blocked from choosing a better, more appropriate one

![00:02:39](hover-notes-images/screenshot-01M1PK88SPBQ4ZG5F6R5X0V35P.png)
[00:02:39](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:02:53](hover-notes-images/screenshot-01M1PK88SPEPJCKSF1M38R8R1S.png)
[00:02:53](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

## Built-in Development Tools

- These tools act on a codebase rather than being business-specific tools (like ShopAssist tools)
- **Key Development Tools:**
    - `Read`: Inspects a file
    - `Write`: Creates or overwrites a file
    - `Edit`: Makes targeted modifications
    - `Bash`: Runs shell commands
    - `Grep`: Searches inside file contents
    - `Glob`: Matches file paths

### Searching the Code: Grep vs. Glob

- **[The Distinction]** Use `grep` to find specific text within files, and `glob` to find files based on their path patterns

| Tool | Purpose | Example Command |
| --- | --- | --- |
| grep | Search content | grep -R "refund" ./shopassist |
| glob | Match paths | shopassist/**/*.policy.md |

### Making Safe Changes with Edit

- `Edit` is best used when there is a unique text match to target a modification
- **[Fallback Strategy]** If no unique match is found, do not force an edit
    - Instead, follow a safe sequence: `Read` $\rightarrow$ `understand` $\rightarrow$ `modify` $\rightarrow$ `Write`
    - This involves inspecting the surrounding code to make the smallest safe change possible

![00:03:00](hover-notes-images/screenshot-01M1PK96FNXDQGEQ2A68DH12RE.png)
[00:03:00](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:03:20](hover-notes-images/screenshot-01M1PK96FNZTT4SA9BZG302EC8.png)
[00:03:20](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

### Safe Code Modification Fallback

If the `edit` tool cannot find a unique text match to target a change, a safer fallback sequence should be used to ensure incremental codebase understanding:

1. **Read**: Inspect the file to see the current state.
2. **Understand**: Analyze the surrounding code to ensure context is correct.
3. **Modify**: Plan the smallest safe change possible.
4. **Write**: Write the updated version back to the file.

```python

# Example of an edit attempt
EDIT(
    file_path="shopassist/refunds.py",
    old_text="RETURN WINDOW DAYS = 14",
    new_text="RETURN WINDOW DAYS = 30"
)
```

---

## MCP Capabilities

Model Context Protocol (MCP) servers expose external capabilities to Claude, which are categorized into tools and resources.

### MCP Tools vs. MCP Resources

| Feature | Definition | Examples |
| --- | --- | --- |
| MCP Tools | Actions Claude can call to perform a task | get_customer_by_email, lookup_order_by_id, process_refund |
| MCP Resources | Content Claude can read for context | refund-policy.md, shipping-policy.md, support-macro-catalog.md |

> **Summary**: Tools **do work**, while resources **provide content**.

![00:03:45](hover-notes-images/screenshot-01M1PKA45GF6GZ08SJ34KDCEPN.png)
[00:03:45](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:04:04](hover-notes-images/screenshot-01M1PKA45HD8MKGCTFDC4FXPNS.png)
[00:04:04](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

### Project-Scoped MCP Configuration

- MCP servers can be defined at the project level using an `.mcp.json` file
    - This configuration belongs specifically to that project
    - It defines which MCP servers are available for that specific codebase
- **[Security Best Practice]** Use environment variable expansion for secrets
    - Never hardcode credentials directly in the `.mcp.json` file
    - Instead, reference an environment variable that expands from the developer's environment

```json
// .mcp.json
{
  "mcpServers": {
    "shopassist-orders": {
      "command": "python",
      "args": ["mcp_servers/orders_server.py"],
      "env": {"ORDERS_API_KEY": "${ORDERS_API_KEY}"}
    },
    "shopassist-policies": {
      "command": "python",
      "args": ["mcp_servers/policies_server.py"]
    }
  }
}
```

### User-Scoped Configuration

- While `.mcp.json` is project-scoped, personal servers can live in a local setup
- **[Scope Distinction]**
        - `.mcp.json` belongs to the project
        - `.claude.json` belongs to the individual developer

![00:04:29](hover-notes-images/screenshot-01M1PKB13NVDNCNWBT8Q26K2BX.png)
[00:04:29](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

![00:04:55](hover-notes-images/screenshot-01M1PKB13PZ10WZSRJ27PQNRE2.png)
[00:04:55](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

### MCP Configuration Scopes

- **[Scope Distinction]**
    - `.mcp.json` belongs to the project
    - `.claude.json` belongs to the individual developer's local setup
- **[Agent Tool Access]**
    - Even if multiple MCP servers are available simultaneously, every agent should not necessarily use every tool from every server
    - The agent design still dictates which specific tools are allowed for each role

### Community vs. Custom MCP Servers

- MCP servers can be either community-built or custom-built depending on the use case

| Type | Best For | Examples |
| --- | --- | --- |
| Community | Common integrations | File systems, GitHub, databases, developer tools |
| Custom | Business-specific systems | ShopAssist servers for customers, orders, refunds, and policies |

![00:05:26](hover-notes-images/screenshot-01M1PKBYRZ77DC1H20VV24W46A.png)
[00:05:26](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

### The Main Lesson: Scoped Tooling

- **[Core Principle]** Do not give every agent every tool
    - Instead, give each agent the smallest useful tool set required for its specific role
- **Tool Choice Control**
    - Use `tool_choice` to dictate how Claude interacts with tools:
        - `may`: Claude can choose to call a tool
        - `must`: Claude is required to call a tool
        - `must call a specific tool`: Claude is forced to use one particular tool
- **Categorizing Tool Usage**
    - **Built-in Development Tools**: Used carefully for reading, searching, editing, and running commands within a codebase
    - **MCP Tools**: Used to perform specific actions
    - **MCP Resources**: Used to access content catalogs
- **[Implementation Strategy]** For complex systems like ShopAssist, use specialized sub-agents (e.g., for refunds, inventory, or policies) with clear boundaries enforced by MCP servers

![00:06:01](hover-notes-images/screenshot-01M1PKCA7K4A38DBW4QVJRTS98.png)
[00:06:01](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042309#overview)

### Summary of Effective Agent Design

- **[The Main Lesson]** Do not give every agent every tool
    - Provide each agent with the smallest useful set for its specific role
- **Control with&#32;`tool_choice`**
    - Use this to dictate whether Claude **may**, **must**, or **must call a specific** tool
- **Tool Categorization**
    - **Built-in Development Tools**: Use carefully for reading, searching, editing, and running commands
    - **MCP Tools**: Used for performing actions
    - **MCP Resources**: Used for accessing content catalogs
- **[Architecture Example]** ShopAssist Implementation
    - Main support agent: Receives a small, dedicated set of support tools
    - Specialized sub-agents: Handle specific domains like refunds, inventory, or policy
    - Backend systems: Exposed via MCP servers with clear boundaries