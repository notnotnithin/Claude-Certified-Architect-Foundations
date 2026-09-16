---
title: "Course: Claude Certified Architect: Foundations Exam Guide - 2026 | Udemy"
description: Agentic architecture, MCP tools, Claude Code, prompt engineering & context management for the CCA Foundations exam
author: 2026 | Udemy
source: https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908977#overview
created: "2026-09-10"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/07-Context-Passing-Between-Agents (transcript)|Transcript]]"
hovernotes-id: doc_088abcca-bdb7-4c14-8559-40eda7e12f5f
---

![00:00:00](hover-notes-images/screenshot-01M25G9CZHRYJZ6R9DZYA8A6Y5.png)
[00:00:00](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

## Context Passing Between Agents

- Subagents don't read your mind — you must tell them.
- **[The Problem]** No automatic inheritance
    - A newly created subagent has no knowledge of the previous conversation or actions taken by the main agent

### Lecture Overview

1. No automatic inheritance
2. Inject context explicitly
3. Include complete findings
4. Goals, not steps

![00:00:42](hover-notes-images/screenshot-01M25GABPWKWH84VNZBEN5NB60.png)
[00:00:42](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

![00:01:14](hover-notes-images/screenshot-01M25GABPXTS12FEKAX7FP90XN.png)
[00:01:14](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### The Mechanics of Isolation

- **[The Rule]** Isolation cuts both ways
    - A subagent does not inherit the coordinator's conversation
    - A subagent does not inherit another subagent's findings

![00:01:53](hover-notes-images/screenshot-01M25GB9DYNEE7767GV1ZWDY1S.png)
[00:01:53](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### The Double-Edged Sword of Isolation

- **[The Trade-off]** Isolation provides a clean workspace for better work, but "clean" also means "empty"
    - Nothing carries across on its own by design
- **The #1 Mistake**
    - Assuming a subagent "already knows" what the coordinator has done
    - For example, assuming a writing subagent is aware of the research conducted by the coordinator

![00:02:13](hover-notes-images/screenshot-01M25GC4N6N2S4YN21DYR0ZRGT.png)
[00:02:13](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

![00:02:53](hover-notes-images/screenshot-01M25GC4N7XSWKNFEGJ3G21J5J.png)
[00:02:53](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### The Silent Failure of Missing Context

- **[The Risk]** Missing context is "sneaky"
    - Subagents won't throw an error or cause a system crash when they lack information
    - Instead, they will quietly produce generic content or invent (hallucinate) details to fill the gaps
    - The failure is often only detectable when the output appears thin or lacks substance

### Inject Context Explicitly

- **[The Rule]** The prompt IS the handoff
- Put everything the subagent needs directly into its prompt
    - Include the specific goal
    - Include relevant facts
    - Include any prior findings
- **[Why?]** There is no shared memory to fall back on; the subagent starts completely blank.

![00:03:23](hover-notes-images/screenshot-01M25GDB7A1Y3Y9TD0QYH9P0FP.png)
[00:03:23](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### Prompting for Success

- **[The Rule]** Whatever the subagent needs to know must be written into the prompt
- **What to include in the prompt:**
    - The specific goal
    - Relevant facts
    - Any prior findings from previous helpers
- **[The Reality]** There is no shared memory to fall back on
    - There is no hidden notice board where agents quietly compare notes behind the scenes
    - If a fact is not in the prompt, the subagent does not have access to it

![00:03:44](hover-notes-images/screenshot-01M25GDZ0X93TTMMEAK5RQZWZY.png)
[00:03:44](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

![00:04:25](hover-notes-images/screenshot-01M25GDZ0XTV23MN6423XSGPWH.png)
[00:04:25](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### Prompt Completeness Test

- **[The Heuristic]** To ensure a prompt is sufficient, read it back to yourself and ask:
    - "If I knew only this and nothing else at all, could I actually do the job?"
    - If the answer is no, critical context is still missing

### Include Complete Findings

- **[The Rule]** Give the whole picture, not a vague summary
- **[The Goal]** Provide full, structured findings to the subagent
    - Pass COMPLETE prior findings instead of a one-line summary
    - Use a structured format with clear sections and labels
- **[The Risk]** Shrinking the context causes the subagent's work to suffer

![00:05:02](hover-notes-images/screenshot-01M25GFCMQ4J0JEJM1JH8WMCF2.png)
[00:05:02](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### Structuring for Clarity

- **[The Importance of Structure]** A wall of unlabeled text is genuinely hard for an agent to use
    - Clear sections tell the subagent exactly what each part of the data is for
    - Without labels, the agent may struggle to parse the relevance of the information

### The Handoff Analogy

- Think of passing findings to a subagent like handing work over to a colleague before you go on holiday
    - You wouldn't leave them a scribbled, incomplete note
    - You would provide a tidy, complete picture so they can function effectively in your absence

```mermaid
flowchart LR
    A["Scribbled Note\n(Vague Summary)"] --> B["Subagent Performance Drop"]
    C["Tidy Picture\n(Structured Findings)"] --> D["Successful Handoff"]
```

![00:05:13](hover-notes-images/screenshot-01M25GFVQ03BYGKV0TDX5PZVD0.png)
[00:05:13](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

![00:05:47](hover-notes-images/screenshot-01M25GFVQ1TQV288ZS2BFJSATZ.png)
[00:05:47](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### Goals, Not Steps

- **[The Rule]** Set the destination — not the turn-by-turn directions
- **Trust the subagent with the \*what**\*
    - Tell the subagent the goal and the quality bar
    - Avoid providing a step-by-step script
        - Instead of: "Find the top 3, with sources"
        - Focus on the outcome and let the subagent use its own loop to figure out the *how*

```mermaid
flowchart LR
    A[Coordinator/Main Agent] -->|"Goal + Quality Bar (The What)"| B[Subagent]
    B -->|"Reasoning Loop (The How)"| C[Final Task Output]
```

![00:06:21](hover-notes-images/screenshot-01M25GH1QTPBWVMC8ZCFYNHA0Y.png)
[00:06:21](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### The Agentic Loop Advantage

- **[The Core Reason]** Subagents are not just scripts; they are autonomous entities
- **[Capabilities]** Like any other agent, a subagent can:
    - **Perceive** the provided context
    - **Reason** through the requirements
    - **Act** upon the information
    - **Observe** the results of its own actions
- **[The Risk of Over-Scripting]** Providing a rigid, step-by-step script prevents the subagent from utilizing this internal loop to handle nuances or unexpected turns in the task.

![00:06:44](hover-notes-images/screenshot-01M25GHSJE91418HHJKY7FEHY1.png)
[00:06:44](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

![00:07:21](hover-notes-images/screenshot-01M25GHSJEC68VH7VR2Z2YPXAC.png)
[00:07:21](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

### Key Takeaways: Context Passing

- **[1. No inheritance]** Subagents start blank and do not inherit context from the main agent
    - Because isolation cuts both ways, the clean workspace you want arrives completely empty
    - Never assume a helper already knows something
- **[2. Inject explicitly]** Put everything the subagent needs directly into the prompt
    - This includes passing complete, structured findings to ensure the agent has all necessary data

![00:07:39](hover-notes-images/screenshot-01M25GKESD0ACMYW6YSDXN324P.png)
[00:07:39](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview)

---

## Simple Explanation (with Claude Examples)

**The core idea, in one line**: A subagent starts completely blank — it doesn't automatically know anything you or another agent discussed, so whatever it needs has to be written directly into its prompt.

**Isolation cuts both ways — an everyday analogy**

A clean, isolated workspace is great for focus — but "clean" also means "empty." It's like handing a new employee a private office with no files in it: great, distraction-free space, but they genuinely know nothing until you brief them. Assuming a subagent "already knows" what the coordinator did is the #1 mistake here — there's no hidden notice board where agents secretly compare notes.

*Claude Code example*: In this session, when I use the `Agent` tool, the prompt itself literally warns: "Brief the agent like a smart colleague who just walked into the room — it hasn't seen this conversation, doesn't know what you've tried, doesn't understand why this task matters." That's this exact principle, word for word.

**Why missing context is dangerous — it fails silently**

A subagent lacking context doesn't crash or throw an error. It just quietly produces generic, thin content — or worse, invents details to fill the gap. You often only notice something's wrong because the output feels vague, not because anything visibly broke.

*Claude Code example*: If I spawned an `Explore` agent and only told it "find the bug" without saying *which* bug or *where* to look, it might wander broadly and return a shallow, generic summary — not because it's incapable, but because I never gave it the specific context it needed.

**The prompt IS the handoff**

Put the specific goal, relevant facts, and any prior findings directly into the subagent's prompt — full and complete, not a one-line summary. A vague summary causes real performance drops; a complete, structured handoff lets the subagent work properly.

*Everyday analogy*: Think of it like leaving a colleague a note before you go on holiday. You wouldn't scribble "handle the Johnson account" — you'd leave a tidy, complete brief: what's been done, what's pending, and what decisions were already made.

**The completeness test**

Read your prompt back and ask: *"If I knew only this and nothing else, could I actually do the job?"* If the answer is no, something critical is still missing.

**Goals, not steps**

Tell the subagent the destination and the quality bar — not a turn-by-turn script. A subagent is a full agent with its own Perceive-Reason-Act-Observe loop; over-scripting it strips away its ability to handle nuances or unexpected turns on its own.

*Claude Code example*: When I brief an `Agent`, good practice is saying "find every file that handles user authentication and report back which ones are outdated" (the goal) — not "first open file A, then check line 12, then open file B..." (a rigid script). The subagent uses its own reasoning loop to figure out *how*.

**Recap in 3 lines**

1. **No automatic inheritance** — subagents start completely blank; never assume they "already know" something.
2. **Inject context explicitly and completely** — the prompt is the only handoff; vague summaries quietly hurt output quality.
3. **Give goals, not step-by-step scripts** — trust the subagent's own reasoning loop to figure out the how.