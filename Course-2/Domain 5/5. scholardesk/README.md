# Part 4 — Large Codebase Exploration

### Domain 5: Context Management & Reliability · Task 5.4

---

## Where we are

- **Parts 1–3** — context, escalation, and error handling, all with the **API**.
- **Part 4** (`5. scholardesk`, this folder) — exploring a codebase without losing
  track. **This part uses Claude Code, not the API.**

> **This is the one part of Domain 5 that switches tools.** Task 5.4 is about
> scratchpads, subagents, `/compact`, and manifests — all **Claude Code** features,
> like Domain 3. So you'll type prompts inside Claude Code (using your Claude Pro
> login), not run Python scripts. We flag this openly because it genuinely is a
> different flavour of task from the rest of the domain.

> **Read** in **VS Code**. **Do** the demos in **Claude Code**.

---

## The one big idea of Part 4

> **Long exploration sessions decay — so write your findings down.**

When you explore a big, unfamiliar codebase in one long Claude Code session, the
conversation fills up. As it does, the model starts **losing the specifics** it found
earlier and falling back on generic "typical patterns" instead of the actual modules
and functions it discovered. The whole task is about fighting that decay.

Four tools do the fighting:

1. **Scratchpad files** — write key findings to disk so they survive a long session.
2. **Subagents** — send noisy investigations off to their own context; get a summary.
3. **`/compact`** — condense a filling-up conversation to free room.
4. **Manifests** — a structured state file so you can resume after a crash.

---

## Why context degrades (the problem)

Imagine exploring for an hour. Early on, Claude noted that `search_sources` lives in
`retrieval.py` and returns a structured result. An hour later, buried under everything
since, it might answer a question about searching with a vague "typically, a function
like this would..." — having lost the *specific* thing it already knew.

That's context degradation. It's not that the model got worse; it's that the specific
detail scrolled out of reliable reach. The fix isn't a bigger brain — it's **writing
the detail somewhere durable.**

---

## Scratchpads — durable findings (Demo 1)

`exploration/SCRATCHPAD.md` is a file Claude fills in **as it explores** — what each
module does, how data flows, where key functions live. Because it's on disk, those
findings survive no matter how long the conversation runs or whether it gets compacted.
Open it in VS Code after Demo 1 and you'll see the exploration captured in a form that
won't decay.

---

## Subagents — isolate the noise (Demo 2)

Some questions ("find every place we load or search a source") produce a wall of file
output. Run that in the **main** session and it clogs everything. Delegate it to a
**subagent**: the digging happens in the subagent's own context, and your main session
gets back a clean summary. (Same idea as `context: fork` from Domain 3.)

---

## `/compact` — free up room (Demo 4)

When a long session fills with verbose output, `/compact` condenses the conversation so
far, making space while keeping the thread. Your scratchpad file is untouched by this —
which is *exactly* why the scratchpad matters: durable findings live in the file, not
only in the conversation that just got compacted.

---

## Manifests — crash recovery (Demo 5)

A **manifest** (`exploration/MANIFEST.json`) is a small structured record of your
exploration state: modules reviewed, data flow, key findings, what's left. If the
session crashes or you close it, a **fresh** session can load the manifest and resume —
instead of re-exploring from scratch. See `exploration/MANIFEST.example.json` for the
shape.

This is the "structured state persistence" the exam describes: each session exports
state to a known place, and the next one loads that manifest on resume.

---

## The demo

All in Claude Code (`claude` from this folder). Follow **`DEMO-PROMPTS.md`**:

1. explore + write to the scratchpad,
2. delegate a noisy question to a subagent,
3. summarise before the next phase,
4. `/compact` when context fills,
5. write a manifest for crash recovery.

---

## Your folder layout

```
5. scholardesk/
├── exploration/
│   ├── SCRATCHPAD.md            ← NEW: findings file (Claude fills it in)
│   └── MANIFEST.example.json    ← NEW: example crash-recovery manifest
├── scholardesk/
│   ├── retrieval.py             ← NEW: source lookups (more code to explore)
│   ├── ask.py, _shared.py       ← from earlier parts
├── sources/                     ← unchanged
├── DEMO-PROMPTS.md, README.md
├── requirements.txt, .env.example, .gitignore
```

(`retrieval.py` was added so ScholarDesk's codebase is realistic enough to explore — a
few modules that call each other.)

---

## Exam objective coverage

**◆ Task 5.4 — Manage context effectively in large codebase exploration**

- ✅ Context degradation in extended sessions (referencing "typical patterns" instead
  of specifics): the "why context degrades" section.
- ✅ Scratchpad files for persisting key findings: `SCRATCHPAD.md` + Demo 1.
- ✅ Subagent delegation for isolating verbose exploration: Demo 2.
- ✅ Structured state persistence for crash recovery via a manifest: `MANIFEST` +
  Demo 5.
- ✅ Spawning subagents to investigate specific questions while the main agent keeps
  the high-level view: Demo 2.
- ✅ Maintaining scratchpad files and referencing them for later questions: Demo 1 +
  the `/compact` note.
- ✅ Summarising a phase before spawning the next: Demo 3.
- ✅ Crash recovery using structured state exports the coordinator loads on resume:
  Demo 5.
- ✅ Using `/compact` to reduce context usage during extended exploration: Demo 4.

---

## What's next

**Part 5 — Human review & confidence (Task 5.5).** Back to the API. We give ScholarDesk
a way to **score its own confidence** in an answer, so low-confidence answers get routed
to a human — and we see why one aggregate accuracy number can hide a weak spot.

See you in Part 5.

---

*CCAR-F · Domain 5 · Part 4 — ANKIT MISTRY*
