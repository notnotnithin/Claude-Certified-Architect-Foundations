---
title: "Course: Claude Certified Architect Foundations: Complete Course | Udemy"
description: Pass the Claude Architect exam and build production-style AI apps with tools, agents, MCP, Claude Code, and evals.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview
created: "2026-09-06"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/29-ClaudeCode-SessionManagement-Resume-Compact-Forks-And-Scratchpads (transcript)|Transcript]]"
hovernotes-id: doc_48cac08c-1ec8-4952-a42f-e64959cc1e54
---

![00:00:00](hover-notes-images/screenshot-01M1V7PFAA47YN3ED7GWP5QH5R.png)
[00:00:00](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

![00:00:26](hover-notes-images/screenshot-01M1V7PFAB9KR9192DTQ1K3504.png)
[00:00:26](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

## Managing Long Cloud Code Sessions

- Long sessions (exploring files, running tests, etc.) require active management
    - Poor management can cause Claude to rely on stale context
    - It can lead to lost details or a mix of exploration and implementation
- **Four practical techniques for session management:**
    - Resume: Continue a clean, ongoing task
    - Compact: Shrink a session that has grown too large
    - Scratchpads: Keep facts outside the chat
    - Forks: Compare approaches in isolation
    - Structured findings: Ask for evidence, not transcripts

### Technique 1: Resume

- Claude Code saves sessions automatically so you can continue later
- Ways to resume a session:
    - **Most recent**:
        - `claude --continue`
    - **Pick from a list**:
        - `claude --resume`
    - **By session ID**:
        - `claude --resume <id>`
    - **Name it up front**:
        - `claude -n return-validation`
    - **Resume by name**:
        - `claude --resume return-validation`
    - **Rename inside a session**:
        - `/rename return-validation`

![00:00:40](hover-notes-images/screenshot-01M1V7QC77PKWRGSRYCZR70CDN.png)
[00:00:40](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

![00:01:17](hover-notes-images/screenshot-01M1V7QC7B1PN3AYJ55YGWSH57.png)
[00:01:17](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

### Resume Techniques

- Claude Code allows resuming sessions beyond just the most recent one
- **Methods for resuming**:
    - **Most recent**: `claude --continue`
    - **Pick from a list**: `claude --resume`
    - **By session ID**: `claude --resume <id>`
    - **By custom name**:
        - To name a session upfront: `claude -n <name>` (e.g., `claude -n return-validation`)
        - To resume by that name: `claude --resume <name>`
- **Renaming active sessions**:
    - Use the `/rename <name>` command inside an active session to give it a readable name

### Session Storage and Management

- Session transcripts are stored locally under the `cloud projects` directory
- The file path follows this structure:

```text
~/.claude/projects/<project>/<session-id>.jsonl
```

- **Best practices for serious work**:
    - Use meaningful session names so they are easy to find and resume
    - Use `/export` to create a readable transcript for record-keeping
    - Avoid using non-persistent runs for work that you intend to resume later

![00:01:26](hover-notes-images/screenshot-01M1V7R9K9581G2422R7RSTH0Q.png)
[00:01:26](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

![00:01:47](hover-notes-images/screenshot-01M1V7R9K93XV3E9ZR1T65TAYN.png)
[00:01:47](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

### Session Transcript Storage

- Transcripts are saved locally as JSON lines files
    - Path pattern: `~/.claude/projects/<project>/<session-id>.jsonl`
- **[Caution]** Do not rely solely on chat history for serious work

### Protecting Against Lost State

- To ensure work durability, use these strategies:
        - Use meaningful session names (makes them findable/resumable by name rather than a random ID)
        - Keep scratchpad notes (durable facts that survive the chat context)
        - Run `/export` for a readable transcript (creates a clean, shareable record)
        - Avoid non-persistent runs for work that requires a future resume

### Technique 1: Resume Safely

- Use `resume` when the task remains the same, but always verify the workspace first
    - The repository may have changed while the session was inactive
- **Recommended Resume Workflow:**

        1. Prompt to re-establish context: `resume the <task-name> task`
        2. Re-check the workspace before editing anything:

                - `git status`
                - `git diff`
                - relevant files
                - failing tests

        1. Summarize the current state to Claude

![00:02:51](hover-notes-images/screenshot-01M1V7V28XDMFESNSRDXXFBBJ1.png)
[00:02:51](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

### Resume Safely

- **The Golden Rule**: Resume the conversation, but verify the code
    - The repository may have changed while the session was inactive
    - Before editing, re-check the workspace using:
        - `git status`
        - `git diff`
        - Relevant files
        - Failing tests
    - Summarize the current state immediately after resuming

### When to Start Fresh Instead of Resuming

- If the previous session context is "noisy," it can hurt more than help
    - **Signs you should start fresh**:
        - You explored multiple conflicting designs
        - You opened many unrelated files
        - You canceled a major refactor mid-way
        - You pasted long, irrelevant logs
- **How to start fresh effectively**:
    - Seed the new session with a clean, structured summary instead of a noisy history
    - **A good summary includes**:
        - The goal
        - Relevant files
        - Important functions
        - Failing tests
        - Decisions made
        - Next steps

```text
Goal: Require photo evidence for damaged-item returns.
Relevant files:
  - app/returns/validation.py
  - tests/test_return_validation.py
Function:
  - validate_return_request()
Failing test:
  - test_damaged_item_requires_photo
Decision:
  - Backend validation only; keep API.
```

### Technique 3: Compact

- Long sessions consume context and can cause the "lost-in-the-middle" problem
    - Key details can get buried as the conversation grows
- Use the `/compact` command to reduce context usage
    - **Caution**: Summaries can drop exact details
    - **Best practice**: Preserve specifics like file paths, function/test names, IDs, dates, error messages, and specific decisions

![00:02:56](hover-notes-images/screenshot-01M1V7T4M179RMBWQ17HEFX5MD.png)
[00:02:56](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

![00:03:42](hover-notes-images/screenshot-01M1V7TJZQE767E4G0BF2ATVWE.png)
[00:03:42](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

![00:04:07](hover-notes-images/screenshot-01M1V7TJZRMYZMTHAFBVQWTG8T.png)
[00:04:07](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

### Technique 4: Scratchpads

- Keep persistent notes in a project file for long tasks
    - This ensures important facts do not live only in the ephemeral chat context
- **[Benefits]**
    - Crash recovery
    - Handoff between people
    - Seeding fresh sessions
    - Acts as a living work manifest
- **Example scratchpad locations**:
    - `.claude/scratchpad.md`
    - `docs/ai_work/session_notes.md`

```markdown

# ShopAssist Session Notes

## Goal
Damaged-item returns require photo evidence.

## Decisions
- Keep public API unchanged
- Backend validation

## Status
- Done: found flow, added test
- In progress: validate_return()
- Next: run focused test suite
```

### Technique 5: Forks

- Use forks to explore divergent designs in isolation
    - This prevents polluting the main session with experimental context
- **Workflow**:

    1. Create forks to explore different paths
    2. Compare the results
    3. Implement only the chosen approach in the main session

| Fork A | Fork B |
| --- | --- |
| Smallest change inside validate_return_request() | A separate ReturnPolicyValidator design |
| Do not edit files, risks, tests | Do not edit files, risks, tests |

![00:04:27](hover-notes-images/screenshot-01M1V7VGHZGGCN3VBN1YZHB6W5.png)
[00:04:27](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

![00:04:47](hover-notes-images/screenshot-01M1V7VGHZSM6G1J9PJA0F43H6.png)
[00:04:47](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

### Sub-agents & Exploration

- **[Avoid]** Requesting long reasoning transcripts
    - Large reasoning dumps add noise and consume unnecessary context
- **[Instead]** Ask for structured findings
    - Tell sub-agents to inspect a flow and return only specific, high-signal data points:
        - Relevant files
        - Relevant functions
        - Current behavior
        - Proposed changes
        - Risks and tests to run
- **Trimming command output**
    - Do not paste full test logs back into the chat
    - Keep the signal by trimming the log to show only what is necessary

```text

# trim the log -- keep signal
Failing test: tests/test_return_validation.py
::test_damaged_item_requires_photo

Expected:
status == "needs_review"
Actual:
status == "approved"

Relevant file: app/returns/validation.py
```

![00:05:11](hover-notes-images/screenshot-01M1V7WDW86ZSF57S2W5RWVG59.png)
[00:05:11](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

![00:05:30](hover-notes-images/screenshot-01M1V7WDW8MKFMPHT0KHY7E83F.png)
[00:05:30](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

### Summary of Cloud Code Techniques

- **[Rule of Thumb]** Choosing the right technique for the situation

| Technique | When to use it |
| --- | --- |
| Resume | When the task is still clean and continuous |
| Name sessions | So you can resume them directly |
| Start fresh | When the old context is noisy |
| /compact | When a session is useful but getting too large |
| Scratchpads | When important facts must survive the conversation |
| Forks | When comparing different implementation strategies |

![00:05:57](hover-notes-images/screenshot-01M1V7WDSSA3JPNTPC74Z2KZQW.png)
[00:05:57](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview)

### Session Management as Correctness

- For high-risk work, proper session management is critical for maintaining correctness
    - **High-risk domains**:
        - Payments
        - Authentication
        - Migrations
        - Production bugs
        - Large refactors
- Effective management ensures Cloud Code remains useful, focused, and safe during long engineering sessions