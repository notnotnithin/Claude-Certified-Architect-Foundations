---
title: "Course: Claude Certified Architect Foundations: Complete Course | Udemy"
description: Pass the Claude Architect exam and build production-style AI apps with tools, agents, MCP, Claude Code, and evals.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview
created: "2026-09-04"
tags:
  - hover-notes
  - udemy
hovernotes-id: doc_bf3f982c-23f1-4b6f-aca8-a254968cf939
transcript: "[[hover-notes-transcripts/ClaudeApp-vs-ClaudeAPI-vs-ClaudeCode-vs-MCP-vs-AgentSDK (transcript)|Transcript]]"
---

[00:00:00](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![Captured video screenshot](hover-notes-images/screenshot-01M1P0C4JWA9EXVFA4ZGECM3NY.png)

![00:00:14](hover-notes-images/screenshot-01M1P0C4JW17DW4YHJ3W74ARRY.png)
[00:00:14](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

## Five Concepts to Separate

- Claude app
- Claude API
- Claude code
- Agent SDK
- MCP

### Claude App

- The hosted product experience
    - Accessed directly through a browser, desktop app, or mobile app
    - Ideal for interactive work
    - **[Note]** It is not your production runtime; you do not own the application state, backend orchestration, tool execution, validation, or deployment model
    - For this course, it serves mostly as a reference point

[00:00:22](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:00:47](hover-notes-images/screenshot-01M1P0DCZ8SY31Z6M663H41QJY.png)
[00:00:47](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

[00:00:52](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:01:02](hover-notes-images/screenshot-01M1P0DZBT8DX95V4PPJHCH2GW.png)
[00:01:02](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

### Claude API

- The model interface inside your own application
- **Communication Flow**
    - Your backend sends: messages, system instructions, model parameters, tool definitions, and structured output requirements
    - Claude returns: a response, structured data, or a tool use request
- **[Critical]** The API does not remove your responsibility as an architect
    - While Claude can reason, classify, extract, generate, and request tools, it should not be the only enforcement layer for critical rules
    - Your backend must still own:
        - Conversation state & auth
        - Permission checks
        - Tool execution
        - Output validation & retries
        - Observability & business rules

[00:01:22](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:01:24](hover-notes-images/screenshot-01M1P0F87MFKV7KJDNF9V97TGX.png)
[00:01:24](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:01:29](hover-notes-images/screenshot-01M1P0F87NHSA5F3YTF7Y4NVD1.png)
[00:01:29](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

### Claude API: The Verification Gate

- **[The Problem]** Relying solely on a system prompt to enforce critical rules is unsafe
    - An AI might decide to call a sensitive tool (e.g., `process_refund`) without proper authorization
- **The Solution: Programmatic Prerequisite Gates**
    - The backend must explicitly verify conditions before allowing a tool call to proceed
    - This ensures rules are enforced in code, not just in the model's reasoning

#### Refund Request Workflow

```mermaid
sequenceDiagram
    participant C as Customer
    participant S as Our Server (gate)
    participant A as Claude API

    C->>S: Refund request ("Refund my order")
    S->>A: Forward to model
    A->>S: Tool-use request (`process_refund`)

    Note over S: GATE: is customer verified?

    alt If not verified
        S->>C: Ask to verify first (user verification, not possible)
    else If verified
        S->>A: Allow `process_refund` (tool executes)
    end
```

[00:01:52](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:01:53](hover-notes-images/screenshot-01M1P0FTY549YKDBVC0RC1GQ9Y.png)
[00:01:53](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:02:07](hover-notes-images/screenshot-01M1P0FTY6FMWR199F0NVPEHFD.png)
[00:02:07](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

## Claude Code

- A developer workflow tool
- **[Usage]** Used inside a codebase to:
    - Inspect files
    - Understand architecture
    - Make edits
    - Write tests
    - Refactor code
    - Generate documentation
    - Review changes
- **The Simple Distinction**
    - Claude API belongs to the application runtime
    - Claude Code belongs to the development workflow

### When to use Claude Code

- Engineers maintaining the codebase
- Automating code reviews
- Working inside CI/CD
- Addressing runtime questions via API, tools, MCP, or Agent SDK

[00:02:22](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:02:25](hover-notes-images/screenshot-01M1P0H1X670VF3KJY4F7VM7FB.png)
[00:02:25](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:02:50](hover-notes-images/screenshot-01M1P0H1X71H2XTRDCZ5KV9BWB.png)
[00:02:50](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

## Agent SDK

- **[The Distinction]** Unlike a simple API integration (one request, one response), an agentic workflow is multi-step
- **Agentic Workflow Example**
    - A support agent might need to:
        - Classify a request
        - Verify a customer
        - Look up an order
        - Check policy
        - Call a tool
        - Inspect the result
        - Decide whether to continue or escalate
- **[Purpose]** The Agent SDK provides the structure for this orchestration
    - It defines agents, tools, hooks, handoffs, and execution flow
    - **The Key Point: Control**
        - Deciding what the agent can decide
        - Determining what the app must enforce
        - Managing when the loop should stop or escalate
        - Identifying which actions require deterministic validation

### Agent SDK — Multi-Step Loop

```mermaid
sequenceDiagram
    participant S as Our Server
    participant L as Agent Loop
    participant A as Claude API

    Note over L: Start workflow
    L->>A: Classify request (what to do?)
    A-->>L: response
    L->>S: Verify customer (prerequisite gate)
    L->>A: Look up order (via MCP tool)
    A-->>L: response
    L->>A: Check policy (what is eligible?)
    A-->>L: response

    alt Continue or escalate?
        L->>L: Resolve
    else Escalate to human
        L->>S: Escalate to human (low confidence/edge case)
    end
```

[00:02:52](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:03:07](hover-notes-images/screenshot-01M1P0J07G1HXJ552B9SPR1PHH.png)
[00:03:07](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:03:14](hover-notes-images/screenshot-01M1P0J07HAMN2B1P7666A1YYM.png)
[00:03:14](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

## MCP — Model Context Protocol

- **[Definition]** A standard way to expose tools and context to Claude-compatible clients
- **[Concept]** Acts as an integration boundary
    - It is more than just "tool calling"
    - Designed to make tools easy to understand and hard to misuse
- **Characteristics of a good MCP tool**
    - A clear name & description
    - A typed input schema
    - Structured output
    - Useful error handling
    - Appropriate permissions

[00:03:23](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:03:24](hover-notes-images/screenshot-01M1P0JZ7YN7YZ508PH2HZFK3Q.png)
[00:03:24](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:03:52](hover-notes-images/screenshot-01M1P0JZ7Z67738PNR45RPKHV8.png)
[00:03:52](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

### Putting the Map Together: ShopAssist AI

- The pieces connect into one single runtime flow

```mermaid
flowchart LR
    Customer["Customer\n(interacts with our frontend)"] --> ClaudeAPI["Claude API\n(our backend calls the model)"]
    ClaudeAPI --> MCP["MCP tools\n(Claude may request tools, exposed via MCP)"]
    MCP --> AgentSDK["Agent SDK\n(orchestrates the complex workflow)"]

    subgraph Engineering_Workflow [Meanwhile]
        ClaudeCode["Claude Code\n(engineering team uses it to build, test, document, and review)"]
    end
```

[00:03:55](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:04:00](hover-notes-images/screenshot-01M1P0KXGXJJHB8FNFTDYRT8E4.png)
[00:04:00](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:04:19](hover-notes-images/screenshot-01M1P0KXGXJCXR8MZXTC2578R4.png)
[00:04:19](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

### ShopAssist AI — Runtime Flow

- The different components connect into a single runtime flow to process a customer request

```mermaid
sequenceDiagram
    participant F as Frontend
    participant S as Our Server
    participant A as Claude API
    participant M as MCP Tools

    F->>S: User message
    S->>A: + system, tools
    A->>S: Tool-use request (e.g., lookup_order)
    S->>M: Execute tool
    M-->>S: Structured result
    S-->>A: Tool result
    A-->>S: Final response
    S-->>F: Reply to user
```

[00:04:23](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

![00:04:40](hover-notes-images/screenshot-01M1P0MTPTR1KH5EFS5VGNE5RE.png)
[00:04:40](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)

### Summary of the Claude Ecosystem

- **Claude App**: The hosted, consumer-facing product.
- **Claude API**: The model interface used within an application's runtime.
- **Agent SDK**: Used to orchestrate complex, multi-step agentic workflows.
- **MCP (Model Context Protocol)**: The standard layer for exposing tools and context to the model.
- **Claude Code**: The developer workflow tool used for building, testing, documenting, and reviewing the system.

![00:04:48](hover-notes-images/screenshot-01M1P0Q95WVC4JYSVX862TT109.png)
[00:04:48](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview)