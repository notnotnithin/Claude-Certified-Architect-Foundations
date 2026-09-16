---
title: "Course: Claude Certified Architect: Foundations Exam Guide - 2026 | Udemy"
description: Agentic architecture, MCP tools, Claude Code, prompt engineering & context management for the CCA Foundations exam
author: 2026 | Udemy
source: https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview
created: "2026-09-10"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/03-Model-Driven-And-The-Anti-Patterns (transcript)|Transcript]]"
hovernotes-id: doc_3a6cd5cf-c9ac-4a3d-bf1f-4295754b3014
---

![00:00:00](hover-notes-images/screenshot-01M25E5BJCF219WJ6MJMBZV18S.png)
[00:00:00](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

## Model-Driven & the Anti-Patterns

- Let Claude steer — and avoid the classic mistakes.

### In This Lecture

1. Model-driven vs. hardcoded

    - A fundamental question of who is in charge of the logic

2. The three anti-patterns

![00:00:42](hover-notes-images/screenshot-01M25E66Y75V6SE8B7R2NRY27D.png)
[00:00:42](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

![00:01:09](hover-notes-images/screenshot-01M25E66Y75398Z2SHHWY0370P.png)
[00:01:09](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

### Model-Driven vs. Hardcoded

- The core decision is whether the AI reads the situation or if you write out every logic branch in advance
- **[Advice]** Let Claude decide — don't script every branch

#### Model-driven

- Claude picks the next tool from context
- Flexible because it handles surprises
    - Similar to how a sat nav reacts to real-world driving conditions

![00:01:45](hover-notes-images/screenshot-01M25E74MDA8A3X0NA4JBHEQVY.png)
[00:01:45](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

#### Hardcoded

- **[Why it's brittle]** Because you have to write every single `if/else` branch in advance
    - It breaks on the unforeseen
    - Like a printed sheet of directions: it works until you encounter a change that isn't on the paper

| Feature | Model-driven | Hardcoded |
| --- | --- | --- |
| Logic | Claude picks the next tool from context | You write every if/else branch |
| Resilience | Flexible — handles surprises | Brittle — breaks on the unforeseen |

![00:02:27](hover-notes-images/screenshot-01M25E83ZHAN9YCAXX9TT6CDD7.png)
[00:02:27](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

![00:02:55](hover-notes-images/screenshot-01M25E83ZHWZ43BJT7TBMTATQY.png)
[00:02:55](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

### Choosing the Right Approach

- **[Exam Tip]** The exam favors model-driven loops for anything non-trivial
    - Hardcoded trees cannot handle cases you didn't foresee
- When to use each:
    - **Hardcoded**: Genuinely fine for tiny, fixed jobs
    - **Model-driven**: The expected answer the moment a task has any real variety in it

![00:03:16](hover-notes-images/screenshot-01M25E90GQ00KK6HNJQDR2WJ83.png)
[00:03:16](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

## The Three Anti-Patterns

- Three ways to break your loop.
- **[Definition]** An anti-pattern is a solution that looks reasonable but reliably causes trouble.

### Ignoring `stop_reason`

- You never know when to stop
    - Claude provides a signal every turn to indicate if the job is finished
    - **[The Risk]** If you ignore this signal, you are essentially guessing when the task is done
    - It is like asking a colleague to check something and walking away before they can give you their answer; you miss the outcome regardless of what they found

![00:04:13](hover-notes-images/screenshot-01M25E9WJKW59YY4ZRPD8Z77Q5.png)
[00:04:13](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

### Never stopping

- No end condition = infinite loop
- **[The Risk]** It is like a tap left running overnight
    - It doesn't necessarily crash the system
    - It quietly costs real money with every single call made in the loop

### Not feeding results back

- Claude "flies blind"
- **[Why it happens]** The tool executes, but the resulting answer is never sent back to the model
    - This breaks the loop's ability to learn from its own actions

![00:04:40](hover-notes-images/screenshot-01M25EAV9PCGZDQPA5PP8MJMXQ.png)
[00:04:40](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

![00:05:07](hover-notes-images/screenshot-01M25EAV9QKW168KQ891KQMGPQ.png)
[00:05:07](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

### Importance of the Anti-Patterns

- **[Production Risk]** These three patterns are the specific bugs that actually take agents down in real systems
- **[Exam Tip]** They are common wrong-answer choices on the exam
    - They often appear as tempting options that look reasonable but are incorrect

### Key Takeaways

- Finishing the loop, in two lines.

![00:05:40](hover-notes-images/screenshot-01M25EC0YFXZW9D4M1TW6R99KF.png)
[00:05:40](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

### Summary: Finishing the Loop

1. **Prefer model-driven**

    - Claude chooses each tool from context
    - You set the destination, and Claude works out the turns one at a time
    - **[Why?]** This allows the system to cope when unexpected turns occur, which is common in real-world systems

2. **Avoid the three traps**

    - Ignoring `stop_reason`
    - Infinite loops
    - Not returning results
    - **[Crucial distinction]** These are all failures in the "plumbing" built around the model, not failures of Claude's intelligence itself

![00:05:58](hover-notes-images/screenshot-01M25ECAV7257YM11S5EZWMJE0.png)
[00:05:58](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview)

- **[Crucial Insight]** The three anti-patterns are failures in the plumbing built around the model, not failures of Claude itself
    - Because they are plumbing issues, they are entirely in your hands to fix

1. Prefer model-driven

    - Claude chooses each tool from context

2. Avoid the three traps

    - Ignoring `stop_reason`
    - Infinite loops
    - Not returning results

---

## Multi-Agent Systems

- Moving beyond a single agent when a job is too big for one model to handle.

---

## Simple Explanation (with Claude Examples)

**The core idea, in one line**: Let Claude decide what to do next based on what it's seeing, instead of pre-writing every possible branch yourself — and watch out for three specific mistakes that quietly break the loop.

**Model-driven vs. hardcoded — an everyday analogy**

A sat nav (model-driven) reacts live to real traffic and reroutes when a road is closed. A printed sheet of directions (hardcoded) works great — until something on the road doesn't match the paper, and then it's useless. Model-driven logic handles surprises; hardcoded `if/else` trees break the moment reality doesn't match what you predicted.

*Claude Code example*: If you ask me to "fix the failing tests," I don't follow a fixed script — I look at *which* tests are failing, decide what to check first, and adjust based on what I find. If the first fix reveals a second, unrelated bug, I handle that too — a hardcoded script that only knew "run tests, apply fix A" would have no way to react to that surprise.

**When hardcoded is actually fine**: for genuinely tiny, fixed jobs with no real variation. The moment a task has any real variety, model-driven is the safer bet.

**The three anti-patterns — ways to break the loop**

1. **Ignoring `stop_reason`** — walking away before Claude tells you it's actually done, like asking a colleague to check something and leaving before they answer. You end up guessing when the task finished instead of knowing.

2. **Never stopping** — no end condition, so the loop runs forever. *Everyday analogy*: a tap left running overnight — it won't crash anything, but it quietly costs money with every single call.

3. **Not feeding results back** — the tool runs, but its answer never reaches Claude, so it's "flying blind" and can't learn from its own actions (this is the exact failure covered in the previous note in this domain).

*Claude Code example*: If a session capped my tool calls at a fixed number regardless of what `stop_reason` said, or silently dropped a tool's result before showing it to me, I'd either stop too early on a real multi-step task, or keep re-requesting the same information forever — neither is a failure of my reasoning, it's a failure in the "plumbing" around me.

**Recap in 3 lines**

1. **Prefer model-driven** — Claude picks the next step from context; you set the goal, not every turn.
2. **Avoid the three traps** — ignoring `stop_reason`, infinite loops, and not feeding results back.
3. **These are plumbing failures, not intelligence failures** — and because they're plumbing, they're entirely fixable by you.