# Part 4 — Live Demo Guide

### Task 5.4 — Large Codebase Exploration

---

## Read this first — this part is different

**Part 4 uses Claude Code, not the API.** Every other part of Domain 5 is a Python
script you run in cmd. This one is the exception — because exploring a codebase with
scratchpads, subagents, and `/compact` is a **Claude Code** skill, not an API call.
So here you type prompts **inside Claude Code**, the same tool from Domain 3.

| Step | Where | Task | Needs |
|------|-------|------|-------|
| Demo 1–5 | **Claude Code** | ◆ **Task 5.4** | your Claude Pro login (NOT the API key) |

Start Claude Code from inside this folder:

```cmd
cd C:\path\to\5. scholardesk
claude
```

> **Honest note:** because this is Claude Code, most of this part is *shown live* in
> the session rather than run as a Python file. The two artifacts you'll actually
> create/use — `exploration/SCRATCHPAD.md` and a manifest — are real files. The
> `/compact` and subagent behaviours are demonstrated in the session.

---

## The idea: why long exploration sessions degrade

When you explore a big codebase in one long Claude Code session, something subtle
happens: as the conversation fills up, the model starts **forgetting specifics it
found earlier** and falls back on generic "typical patterns" instead of the actual
modules and functions it discovered. Task 5.4 is about fighting that degradation.

Four tools for it: **scratchpad files**, **subagents**, **`/compact`**, and
**manifests** for crash recovery.

---

## Demo 1 ◆ Task 5.4 — Explore, and write findings to a scratchpad

The scratchpad (`exploration/SCRATCHPAD.md`) is a file where Claude records key
findings **as it explores**, so they survive even as the chat gets long. In Claude
Code:

```
Explore this ScholarDesk codebase. As you go, write your key findings into exploration/SCRATCHPAD.md — what each module does, how data flows, and where the important functions live. Keep updating that file as you learn more.
```

**What to look for:** Claude reads the modules (`ask.py`, `_shared.py`,
`retrieval.py`) and **fills in the scratchpad**. Open `exploration/SCRATCHPAD.md` in
VS Code afterward — those findings are now saved to disk, not trapped in a
conversation that will scroll away.

---

## Demo 2 ◆ Task 5.4 — Delegate a noisy question to a subagent

Some questions produce a wall of output you don't want clogging your main session.
Delegate those to a **subagent** — it investigates in its own space and returns just
a summary:

```
Use a subagent to trace every place a source is loaded or searched in this codebase, and report back just a short summary of what it found — not the full file dumps.
```

**What to look for:** the detailed searching happens in the subagent's context; your
main session receives a **clean summary**. This keeps the main conversation focused on
the high-level picture while the verbose digging happens elsewhere. (If this feels
familiar, it's the same idea as `context: fork` from Domain 3.)

---

## Demo 3 ◆ Task 5.4 — Summarise before the next phase

Before moving to a new area of the code, lock in what you've learned:

```
Summarise what we've established so far in 4–5 bullet points, then we'll explore the error-handling paths in retrieval.py next.
```

**What to look for:** a tight summary you can carry into the next phase. Summarising
between phases — and keeping the scratchpad updated — is how you stop early findings
from decaying as the session grows.

---

## Demo 4 ◆ Task 5.4 — Use `/compact` when context fills up

When a long session starts filling with verbose exploration output, `/compact`
condenses the conversation so far, freeing room while keeping the thread:

```
/compact
```

**What to look for:** Claude Code compresses the earlier conversation. Your scratchpad
file is unaffected — which is exactly why the scratchpad matters: it holds the durable
findings even across a compaction.

---

## Demo 5 ◆ Task 5.4 — A manifest for crash recovery

A **manifest** is a small structured file recording exploration state, so if a session
crashes (or you just close it), you can resume without starting over. Ask Claude to
write one:

```
Write a manifest file exploration/MANIFEST.json capturing our exploration state: which modules we've reviewed and their purpose, the data flow, key findings, and what's still to explore.
```

Compare it with the provided `exploration/MANIFEST.example.json` to see the shape.

**What to look for:** a JSON file you could hand to a **fresh** Claude Code session to
resume: *"Here's the manifest from my last exploration — pick up where it left off."*
That's crash recovery — the coordinator loads the manifest instead of re-exploring
everything.

---

## Why this matters (the one-line takeaway)

> **Long exploration sessions decay — so write durable findings to disk.**
> Scratchpads and manifests keep specifics alive; subagents and `/compact` keep the
> main context clear.

---

## Quick recap

| Demo | Task | In Claude Code | Shows |
|------|------|----------------|-------|
| 1 | ◆ 5.4 | explore + write scratchpad | Persisting findings to a file |
| 2 | ◆ 5.4 | delegate to a subagent | Isolating verbose exploration |
| 3 | ◆ 5.4 | summarise between phases | Preventing early-finding decay |
| 4 | ◆ 5.4 | `/compact` | Freeing context on a long session |
| 5 | ◆ 5.4 | write a manifest | Crash recovery / resume |

---

*CCAR-F · Domain 5 · ScholarDesk · ANKIT MISTRY*
