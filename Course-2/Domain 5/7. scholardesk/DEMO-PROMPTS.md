# Part 6 — Live Demo Guide

### Task 5.6 — Provenance in Multi-Source Synthesis

---

## Read this first — the map of Part 6

Three scripts, run in cmd. Two call the API (the synthesis demos); one runs on its own
(the rendering demo). You need your API key (from Part 0) for the two synthesis scripts.

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 5.6** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 5.6** | ✅ Yes |
| Demo 3 | cmd | ◆ **Task 5.6** | ❌ No |

Start in the project folder:

```cmd
cd C:\path\to\7. scholardesk
```

**The setup:** two of ScholarDesk's sources deliberately **disagree** on one thing —
Pune's public charging-point count. The newer adoption report (`ev_adoption_report.txt`,
published 2026-03-10) says **~480**; the older charging note (`ev_charging_note.txt`,
published 2026-02-05) says **~350**. That built-in conflict is what these demos hinge
on.

---

## Demo 1 ◆ Task 5.6 — The anti-pattern: synthesis with no provenance

Run the no-provenance version:

```cmd
python synth_no_provenance.py
```

**What it does:** blends all the sources into one smooth answer about charging and
adoption.

**What to look for:** two failures:
- the answer **cites no sources** — you can't tell which document any fact came from,
- the two sources **disagree** on the charging count, but the blended answer just states
  **one** number (usually whichever it read last) as if it were settled, **hiding the
  conflict** entirely.

---

## Demo 2 ◆ Task 5.6 — The fix: preserve claim-source mappings

Run the with-provenance version:

```cmd
python synth_with_provenance.py
```

**What it does:** each source is labelled with its filename **and publication date**
(pulled automatically from the source header), and ScholarDesk returns a **structured**
answer (via tool use) where:

- every **claim is tied to its source document** (claim-source mapping), and
- the **conflict is flagged** — both values, both sources, both dates — then **resolved
  by recency**.

**What to look for:**
- **Claims** each show their source file — attribution survived the synthesis.
- The charging-count **conflict** is reported openly:
  `~480 [ev_adoption_report.txt, 2026-03-10]` vs
  `~350 [ev_charging_note.txt, 2026-02-05]`,
  with a resolution: the newer source wins, so **~480 is current**.

The **dates are the key**. Without them, "480" and "350" look like a contradiction.
With them, you can see one simply **updated** the other as new sites opened. Temporal
metadata turns a scary "contradiction" into a clear "this replaced that."

---

## Demo 3 ◆ Task 5.6 — Render each content type appropriately

Run the rendering demo (no API key needed):

```cmd
python render_by_type.py
```

**What it does:** shows the same kind of research output rendered three ways — a cost
comparison as a **table**, an adoption finding as **prose**, charging advice as a
**numbered list**.

**What to look for:** each content type gets the format that reads best. Numeric
comparisons belong in a table; a narrative finding reads best as prose; a how-to as
steps. Forcing everything into one uniform block would make it harder to read. Matching
format to content type is the final piece of presenting synthesised information well.

---

## Why this matters (the one-line takeaway)

> **Keep every claim tied to its source, flag conflicts instead of hiding them, and use
> dates to tell an update apart from a contradiction.**

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 5.6 | `synth_no_provenance.py` | Blended answer loses sources, hides a conflict |
| 2 | ◆ 5.6 | `synth_with_provenance.py` | Claim-source mappings + conflict flagged + dated resolution |
| 3 | ◆ 5.6 | `render_by_type.py` | Table vs prose vs list by content type |

---

*CCAR-F · Domain 5 · ScholarDesk · ANKIT MISTRY*
