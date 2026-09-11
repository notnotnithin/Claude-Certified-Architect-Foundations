---
title: "Course: Claude Certified Architect: Foundations Exam Guide - 2026 | Udemy"
description: Agentic architecture, MCP tools, Claude Code, prompt engineering & context management for the CCA Foundations exam
author: 2026 | Udemy
source: https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview
created: "2026-09-11"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/04-Context-In-Large-Codebase-Exploration (transcript)|Transcript]]"
hovernotes-id: doc_ee9b94db-413c-4f71-a4c3-6400b292288a
---

![Captured video screenshot](hover-notes-images/screenshot-01M27Q34X6TJZG3T7ATPQ9AMF1.png)
[00:00:37](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

## Context in Large-Codebase Exploration

- Goal: Explore a massive codebase without drowning in it.
- This involves applying the principles of extracting and persisting information and exploring incrementally.

### Lecture Overview

1. The problem
2. Scratchpad files
3. /compact
4. Crash-recovery manifests
5. The Explore subagent

### The Problem: Context Flooding

- Reading a large codebase fills the context window extremely fast
    - This is driven by the act of reading code files
    - Each file read dumps its entire contents into the context
    - Within just dozens of files, the context window becomes full

### The 'Lost in the Middle' Connection

- Context flooding is an extension of the "lost in the middle" problem
    - Instead of being caused by long conversations, the context is filled by file after file of source code
    - This causes the quality of the model's performance to drop mid-task
- **Mindset vs. Tools**
    - **Mindset (from Domain 2):** The habit of "exploring incrementally" (searching first and reading narrowly)
    - **Tools (this lecture):** The actual technical mechanisms used to maintain context and manage long-term exploration sessions

### Scratchpad Files

- **The core move:** Write your findings to disk rather than relying solely on the chat history
    - Instead of keeping everything in the conversation, save key discoveries to a dedicated file
    - Example: Writing a note like "Auth logic lives in `/auth` folder; bug is located in `login()` function"
- **[Why use this?]** To manage the trade-off between information density and context limits
    - **Disk is unlimited:** You can store an infinite amount of observations and findings
    - **Context is limited:** The chat window will eventually fill up and degrade performance
    - **Selective retrieval:** You only re-read the specific note you need at the moment it becomes relevant, keeping the active context clean

### Extract and Persist Made Literal

- **The Connection:** This is the concrete application of the "extract and persist" principle
    - **Previously (Conceptual):** Extract and persist was an abstract idea/principle
    - **Now (Concrete):** It is a physical file on disk where you literally write down findings
- **Maintaining a "Clean" Context**
    - By writing to a file, you ensure the context window stays lean and focused
    - You avoid the clutter of past observations while retaining the ability to retrieve them exactly when needed

### Compact

- **The Goal:** Summarize the session to continue working past the context limit
- **How it works:** It summarizes the existing conversation and replaces the history with that summary
    - This effectively shrinks the number of tokens being used
    - It allows a long-running task to continue without hitting the 'lost in the middle' degradation
- **[Implementation Strategy]:** Treat it as an active command rather than a passive occurrence
    - **Proactive usage:** Run the command when the context window is roughly 70% to 75% full
    - **Control:** You maintain control over what information is kept in the summary and what is discarded

### Proactive Context Control

- **Maintain Agency:** Do not wait for context degradation to force your hand
    - Don't wait until the model starts hallucinating or losing track of details
    - Instead, treat compaction as a tool you trigger on your own terms to ensure the session remains high-quality

![00:04:24](hover-notes-images/screenshot-01M27RB4PE3RC4Q7552N1M353J.png)
[00:04:24](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

### Strategic Timing for Compaction

- **Avoid "Compacting in a Panic"**
    - Do not wait until the context window is completely jammed or forced upon you
    - Waiting until the limit is reached reduces your ability to guide what survives
- **Compact at a Natural Break**
    - Trigger the command during a pause between distinct tasks
    - **[Why?]** A clean moment allows you to calmly ensure important findings are safely carried across into the summary

![00:05:23](hover-notes-images/screenshot-01M27RC24WMFZWHXVR44MK7ASW.png)
[00:05:23](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

## Crash-Recovery Manifests

- **The Core Concept:** If a session dies, you don't have to start over
    - A manifest acts as a safeguard against failure through persistence
- **What a Manifest contains:** It is a running log of the project state
    - The current task
    - What has been done
    - What is next
- **[How it enables recovery]:** A new session can read the manifest and resume immediately
    - This eliminates the need to re-explore the entire project from scratch

![00:05:59](hover-notes-images/screenshot-01M27RD0KJQABY5HREFJNQM7D6.png)
[00:05:59](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

![00:06:32](hover-notes-images/screenshot-01M27RD0KKF8Q9F9Q8NSXWE7Y8.png)
[00:06:32](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

### Manifests in Practice

- **The Safety Net:** Prevents losing all progress during long-running tasks
    - **[Example]:** During a massive refactor that crashes at file 40, a manifest allows a new session to pick up at file 41
    - **Without a manifest:** You would have to restart the entire process from file 1, repeating all previous work

## The Explore Subagent

![00:07:20](hover-notes-images/screenshot-01M27RDX5E7E4X3Z2HXMCQG7QY.png)
[00:07:20](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

### Subagent Delegation Mechanics

- **The Core Move:** Send heavy reading to a separate context
    - The subagent reads in its own context and returns only a summary
    - This delegates the investigation process to an isolated environment
- **[Benefit]:** Keeps the main window clean
    - Large file reads never touch your main window
    - Only the tidy conclusions are brought back to the main session
- **Context Management:** It functions as a tool for isolation
    - By isolating heavy reading, it prevents the main context from being overwhelmed by massive amounts of raw data

![00:07:22](hover-notes-images/screenshot-01M27RESN4V4EZNXQZ5QZKGMTM.png)
[00:07:22](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

![00:07:59](hover-notes-images/screenshot-01M27RESN4W04XVP5ER3ZEFQ10.png)
[00:07:59](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

### The Explore Subagent as a Context Management Tool

- **A Dual Purpose Tool:** While previously used for safe planning (as taught in 3.4), it also serves as a mechanism for isolation
    - **[How it works]:** It acts as a "scout" that performs heavy reading in its own separate context
    - **[The Result]:** This isolation keeps your main window lean and clean by ensuring massive file reads never touch the primary session context

---

## Putting It Together

- **The Goal:** Maintaining one lean session through the use of four specific tools
- **Tool 1: Explore Subagent**
    - Heavy reads happen elsewhere to protect the main context

![00:08:46](hover-notes-images/screenshot-01M27RFS3W987JP2DCT3PK3YAB.png)
[00:08:46](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

- **Tool 2: Scratchpad files**
    - Used to persist findings to disk
    - **[Purpose]:** This keeps what you learn out of the active window context
- **Tool 3:&#32;`/compact`**
    - Shrinks the conversation
    - **[Purpose]:** Makes room when the conversation history itself becomes too long
- **Tool 4: Manifest**
    - Serves as a safety net to survive a crash
    - **[Purpose]:** Protects against the session dying

### The Core Principle of Session Management

All four tools follow the same fundamental workflow established in lecture 5.1:

```mermaid
flowchart LR
    A["Extract (Explore Subagent)"] --> B["Persist (Scratchpad files)"]
    B --> C["Trim (/compact)"]
    C --> D["Just (Manifest)"]
```

![00:08:52](hover-notes-images/screenshot-01M27RGCCQ98XYKXY50R0M78G9.png)
[00:08:52](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

![00:09:34](hover-notes-images/screenshot-01M27RGCCQEH993R01B64WZX7A.png)
[00:09:34](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)

### Key Takeaways: Codebase Context

- **Exploration floods context:**
    - Code-based exploration causes the same "context rot" seen in long text chats
    - Instead of just long dialogue, the context is overwhelmed by dozens of files and their contents
- **Persist and compact:**
    - Use scratchpad files to persist findings
    - Use `/compact` to summarize and make room

![00:09:49](hover-notes-images/screenshot-01M27RHS02E8JECY7D2NKYQ26F.png)
[00:09:49](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview)