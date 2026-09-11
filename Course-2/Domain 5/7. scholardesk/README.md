# Part 6 — Provenance in Multi-Source Synthesis

### Domain 5: Context Management & Reliability · Task 5.6

---

## Where we are

- **Parts 1–5** — context, escalation, errors, codebase exploration, confidence.
- **Part 6** (`7. scholardesk`, this folder) — the finale: when ScholarDesk answers
  from **several sources at once**, keeping track of **which fact came from where**.

This is the task ScholarDesk was born for. A research assistant's core job is combining
sources — so preserving where each fact came from is its most natural lesson of all.

> **Read** in **VS Code**. **Run** in **cmd**. The two synthesis demos need your API key
> (Part 0); the rendering demo doesn't.

---

## The one big idea of Part 6

> **When you combine sources, don't lose track of them.**

Blending several documents into one smooth answer is easy — and it quietly throws away
two things you need: **which source each fact came from**, and **the fact that two
sources sometimes disagree**. Task 5.6 is about keeping both.

---

## The built-in conflict

Two of ScholarDesk's sources disagree on one detail — on purpose:

| Source | Published | Pune charging points |
|--------|-----------|----------------------|
| `ev_adoption_report.txt` | **2026-03-10** (newer) | **~480** |
| `ev_charging_note.txt` | 2026-02-05 (older) | ~350 |

This is the realistic case: figures get updated as new sites open, and an older
document lingers with the old number. How ScholarDesk handles this disagreement is the
heart of the lesson.

---

## The anti-pattern: synthesis with no provenance

`synth_no_provenance.py` blends all sources into one answer. Two things go wrong:

1. **Source attribution is lost.** The answer states facts with no idea which document
   backs each one. Asked "says who?", you can't answer — fatal for a research tool.

2. **The conflict is resolved arbitrarily.** Faced with "480" and "350," the blended
   answer just picks one — often whichever it read last — and states it as settled fact,
   hiding that there was ever a disagreement.

**The exam's point:** when synthesis condenses multiple sources, source attribution is
easily lost, and conflicting values get silently flattened.

---

## The fix: claim-source mappings + conflict annotation

`synth_with_provenance.py` labels each source with its filename **and publication date**
(pulled straight from the source header), and returns a **structured** answer (via tool
use, Domain 4's reliable method) with two parts:

**1. Claims, each tied to a source.** Every fact carries the document it came from — a
*claim-source mapping*. Attribution survives the synthesis instead of dissolving into a
blend.

**2. Conflicts, flagged not hidden.** Where the sources disagree, ScholarDesk records
**both values, with their sources and dates**, and a resolution — rather than silently
picking one:

```
Topic: Pune public charging points
  - ~480  [ev_adoption_report.txt, 2026-03-10]
  - ~350  [ev_charging_note.txt, 2026-02-05]
  Resolution: the newer report (2026-03-10) supersedes; ~480 is current.
```

---

## Why the dates matter: contradiction vs update

This is the subtle, important part. Look at "480" and "350" **without** dates — they
look like a flat contradiction, and you'd have no way to know which to trust. Add the
**publication dates**, and the picture changes completely: the newer document simply
**updated** the count as new charging sites opened. It's not a contradiction at all;
it's a change over time.

**Temporal metadata (publication/collection dates) is what lets you tell a real
contradiction apart from a valid update.** Drop the dates and you'd either trust the
wrong (older) value or waste time "resolving" a conflict that was really just an update.
This is exactly the exam's point about temporal data preventing different-but-valid
values from being misread as contradictions.

> This is why every source carried a date all the way back in **Part 0** — the whole
> project was quietly set up for this moment.

---

## The last piece: render by content type

`render_by_type.py` covers presentation. Synthesised answers often mix content
**kinds** — and each kind reads best in its own format:

- **numeric / comparative data** → a **table** (cost per km),
- **a narrative finding** → **prose** (adoption trends),
- **a how-to** → a **numbered list** (charging steps).

Forcing everything into one uniform format — all prose, or all bullets — makes it harder
to read. Matching format to content type is the final touch on presenting synthesised
information well.

---

## The demo

```cmd
python synth_no_provenance.py     # blended answer -> loses sources, hides conflict
python synth_with_provenance.py   # claim-source mappings + dated conflict resolution
python render_by_type.py          # table vs prose vs list (no API key)
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
7. scholardesk/
├── synth_no_provenance.py      ← NEW: ❌ blended answer, no sources
├── synth_with_provenance.py    ← NEW: ✅ claim-source mappings + conflict + dates
├── render_by_type.py           ← NEW: render each content type appropriately
├── sources/
│   ├── ev_adoption_report.txt  ← now includes the conflicting "~480" (newer)
│   └── ev_charging_note.txt    ← the older "~350"
├── DEMO-PROMPTS.md, README.md
├── scholardesk/                ← unchanged
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 5.6 — Preserve information provenance in multi-source synthesis**

- ✅ Source attribution lost during synthesis: `synth_no_provenance.py`.
- ✅ Structured claim-source mappings preserve attribution: `synth_with_provenance.py`
  (`claims` with `source`).
- ✅ Conflicting values annotated with sources, not arbitrarily picked: the `conflicts`
  block.
- ✅ Temporal data distinguishes contradictions from valid updates: the publication
  dates and the "contradiction vs update" section.
- ✅ Rendering content types appropriately: `render_by_type.py`.
- ✅ Preserving attribution through synthesis, annotating conflicts, using temporal
  metadata, presenting in the right format: all four skills demonstrated.

---

## Domain 5 complete — what you've built

Starting from a simple one-source research tool, ScholarDesk is now **reliable**. Look
back at the seven folders:

| Part | What you added | Task | Tool |
|------|----------------|------|------|
| 0 | Setup + one-source skeleton | — | API |
| 1 | Key-findings block + trimming | 5.1 | API |
| 2 | Escalation & ambiguity criteria | 5.2 | API |
| 3 | Structured error propagation + coverage gaps | 5.3 | API |
| 4 | Codebase exploration (scratchpads, manifests) | 5.4 | Claude Code |
| 5 | Confidence scoring + human routing | 5.5 | API |
| 6 | Provenance + conflict + dates | 5.6 | API |

**All six Domain 5 task statements, on one project.**

And notice the through-line: every part is about **not losing something important** —
findings in a long session (Part 1), the right escalation signal (Part 2), error context
(Part 3), specifics in a long exploration (Part 4), the assistant's own uncertainty
(Part 5), and sources in a synthesis (Part 6). Reliability, across the whole domain, is
the discipline of holding on to the information that matters instead of letting it
quietly slip away. For a research assistant — whose entire value is trustworthy,
traceable answers — that discipline is the whole job.

---

*CCAR-F · Domain 5 · Part 6 — ANKIT MISTRY*
