---
title: "Course: Claude Certified Architect: Foundations Exam Guide - 2026 | Udemy"
description: Agentic architecture, MCP tools, Claude Code, prompt engineering & context management for the CCA Foundations exam
author: 2026 | Udemy
source: https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908993#overview
created: "2026-09-10"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/10-Task-Decomposition-The-Strategies (transcript)|Transcript]]"
hovernotes-id: doc_d9de2c7b-03a7-44fe-bb2f-989283eab54c
---

![Captured video screenshot](hover-notes-images/screenshot-01M25J1QGRN12J9X7V02NQRKR2.png)
[00:00:00](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

## Task Decomposition: The Strategies

- The process of breaking a big job into the right-shaped pieces
- Serves as the underlying thinking scale for agentic machinery
    - Loops
    - Coordinators and subagents
    - Gates and hooks

![Captured video screenshot](hover-notes-images/screenshot-01M25J2MHX0DH7PJ580B9H03B6.png)
[00:00:37](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

![Captured video screenshot](hover-notes-images/screenshot-01M25J2MHXXSBN6TBD45D7DXCX.png)
[00:01:00](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### Task Decomposition Strategies

- Aim: Break a big job into the right-shaped pieces
- Core components of the study:
    - Why decompose?
    - Sequential & parallel (the two basic shapes)
    - Adaptive (also called dynamic) for jobs that cannot be planned in advance

### Why Decompose?

- **[Primary Reason]** Smaller pieces are easier to get right

![Captured video screenshot](hover-notes-images/screenshot-01M25J3N6Y8AH4KNCKRH36V0N6.png)
[00:01:22](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### Benefits of Decomposition

- **Focused, checkable, reliable**
    - Breaking a task into subtasks makes each one focused
    - Makes tasks easier to check and more reliable
    - Independent pieces can run in parallel
- **[The importance of checkability]** Because a giant task is a "solid block," if it fails, you cannot see inside to identify the cause
    - Subtasks allow you to pinpoint exactly which part let you down

![Captured video screenshot](hover-notes-images/screenshot-01M25J587JMB80TNB3TD880Q9W.png)
[00:02:05](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### The Core Principle: Small & Clear vs. Big & Vague

- **The recurring principle of focus**
    - Small, clear sub-tasks consistently outperform one giant, vague task
    - This mirrors the logic of sub-agents: splitting work across specialists (e.g., a kitchen) ensures each part is manageable
- **Decomposition as a tool for understanding**
    - Being able to describe a job in small, discrete pieces is a sign that you genuinely understand the task

![Captured video screenshot](hover-notes-images/screenshot-01M25J685TM3YA4CX1BQ7JW00Q.png)
[00:02:43](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

## Sequential & Parallel

- Represented by two mental pictures: a **chain** or a **fan**

### Sequential

- Follows a fixed order where each task feeds the next
- **[The shape of the work]** The order is often non-negotiable because of the dependencies between steps
    - Example: `extract` $\rightarrow$ `validate` $\rightarrow$ `format`
        - You cannot validate data that hasn't been extracted yet
        - You cannot format an analysis that does not yet exist

![Captured video screenshot](hover-notes-images/screenshot-01M25J8C98QY565CHB03ZTV99G.png)
[00:03:40](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### Sequential & Parallel

- **Sequential (A Chain)**
    - Fixed order where each step feeds the next
    - Driven by dependencies: you cannot perform a step until the previous one is complete
    - Example: `extract` $\rightarrow$ `validate` $\rightarrow$ `format` (you can't validate data that hasn't been extracted yet)
- **Parallel (A Fan)**
    - Independent steps performed at once
    - No dependency between steps; one step does not need the answer from another
    - Example: `check 5 files simultaneously`
    - **[The payoff]** Because they don't have to queue up, parallel execution finishes in roughly the time it takes to complete a single step

```mermaid
flowchart LR
    subgraph Sequential["Sequential (Chain)"]
        direction LR
        A[Extract] --> B[Validate] --> C[Format]
    end

    subgraph Parallel["Parallel (Fan)"]
        direction LR
        P1[Check File 1]
        P2[Check File 2]
        P3[Check File 3]
        P4[Check File 4]
        P5[Check File 5]
    end
```

![Captured video screenshot](hover-notes-images/screenshot-01M25J8461JXH1QQTZB949HSGC.png)
[00:04:13](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

![Captured video screenshot](hover-notes-images/screenshot-01M25J8461A12NR9M1KERDZ6X1.png)
[00:04:54](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### Choosing Between Sequential and Parallel

- **The decision rule**
    - Do not choose based on what sounds faster
    - Instead, look at the work and ask: "Does this piece need the answer from that piece?"
- **Sequential (The Chain)**
    - Use when steps depend on each other
- **Parallel (The Fan)**
    - Use when steps are independent

### Adaptive (Dynamic) Decomposition

- **Figure out the pieces as you go**
- **[How it works]** The plan grows as the work reveals it
    - You don't know all the subtasks upfront
    - An agent (e.g., Claude) discovers them as it works
    - Example flow: `investigate` $\rightarrow$ `find leads` $\rightarrow$ `spawn follow-ups`

![Captured video screenshot](hover-notes-images/screenshot-01M25J8J83H692ADR1W6CRN2ZQ.png)
[00:05:37](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### Adaptive (Dynamic) Decomposition

- **[Core Concept]** The plan grows as the work reveals it
    - Unlike sequential or parallel shapes, you do not know all subtasks upfront
    - The agent (e.g., Claude) discovers subtasks as it works
    - The second step depends on whatever the first step turns up
- **The shape of adaptive work**

```mermaid
flowchart LR
    A[investigate] --> B[find leads] --> C[spawn follow-ups]
```

- **[When to use it]** Use adaptive decomposition when steps cannot be known in advance
        - Research
        - Debugging
        - Exploration

![Captured video screenshot](hover-notes-images/screenshot-01M25J8QQH27ND8VAPDRV87KJ8.png)
[00:05:43](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

![00:05:44](hover-notes-images/screenshot-01M25JYBA3F0DCR5RXB7XJJG6S.png)
[00:05:44](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

![00:06:20](hover-notes-images/screenshot-01M25JYBA348D676MYX76V01X5.png)
[00:06:20](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### Adaptive Decomposition and the Agentic Loop

- **[The nature of adaptive work]** It is like following a trail through a woods
    - You take one step
    - You look at what is actually there
    - Only then can you decide where the next step goes
- **Connection to the Agentic Loop**
    - Adaptive decomposition perfectly fits the core agentic pattern:
    - Act $\rightarrow$ Observe $\rightarrow$ Decide what comes next

## Key Takeaways

- Decomposition strategies can be summarized in three lines (Sequential, Parallel, and Adaptive)

![00:07:02](hover-notes-images/screenshot-01M25JZ81YVBXZV68WSBYWMPMB.png)
[00:07:02](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)

### Summary of Decomposition Strategies

- **Why decompose?**
    - Each piece becomes focused and reliable
    - **[The benefit of granularity]** A giant task can hide its own failures, whereas five small pieces tell you exactly which one went wrong
- **Sequential or parallel?**
    - The decision is driven by dependency, not a preference for speed
    - Dependent tasks $\rightarrow$ sequential (a chain)
    - Independent tasks $\rightarrow$ parallel (a fan)
- **Adaptive**
    - Used when steps cannot be known upfront
    - The work itself reveals the plan

![00:07:13](hover-notes-images/screenshot-01M25JZNA1S93X8MB9KZMRGSF8.png)
[00:07:13](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview)