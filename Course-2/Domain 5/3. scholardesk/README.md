# Part 2 — Escalation & Ambiguity

### Domain 5: Context Management & Reliability · Task 5.2

---

## Where we are

- **Part 1** (`2. scholardesk`) — kept the important findings alive across a long
  session.
- **Part 2** (`3. scholardesk`, this folder) — knowing **when to hand off to a human
  expert**, and what to do when a query is **ambiguous**.

> **Read** in **VS Code**. **Run** in **cmd**. The two escalation demos need your API
> key (Part 0); the ambiguity demo doesn't.

---

## The one big idea of Part 2

> **Escalate for the right reasons — and when a question could mean several things,
> ask.**

A good research assistant answers what its sources support and hands off what they
don't. The trick is deciding *which is which* correctly — and not making confident
guesses when a query is ambiguous.

---

## Half 1 — escalation: the wrong signals vs the right ones

### The wrong signals: difficulty and tone

`escalate_vague.py` tells ScholarDesk to escalate when a question *seems hard* or the
user *sounds demanding*. It misfires:

- An **urgent-but-covered** question (running cost per km) gets **escalated** — the
  bot bounced an easy, well-sourced answer to a human just because it was phrased
  forcefully.
- A **not-covered** question (5-year resale value — no source mentions it) gets
  **answered with a made-up number** — it didn't "seem hard," so the bot didn't
  escalate a genuine coverage gap.

**The exam's point:** difficulty and self-judged confidence are **unreliable proxies**
for whether a question actually needs a human.

### The right signals: explicit triggers

`escalate_criteria.py` uses explicit criteria, with few-shot examples marking the
boundary. Escalate to a human expert only when:

1. **the user explicitly asks for one** — honor it immediately, no first attempt;
2. **the sources don't cover the question** — a **coverage gap** (the research version
   of the exam's "policy gap"); not just "hard" questions, but ones the sources are
   silent on;
3. ScholarDesk **genuinely can't make progress** — e.g. sources conflict and it can't
   resolve which is right.

Otherwise, **answer** it from the sources. And a question that's fully covered but
phrased forcefully still just gets answered — **tone is not a trigger.**

With those triggers, the three questions sort correctly:

| Question | Right call |
|----------|-----------|
| Urgent "running cost per km?" (covered) | **ANSWER** — tone doesn't matter |
| "5-year resale value?" (no source) | **ESCALATE** — coverage gap |
| "Have a human expert look into this" | **ESCALATE** — explicit request |

> **An honest note on fit:** escalation is a slightly more natural fit for a customer-
> support bot (which escalates to a human agent all the time) than for a research
> tool. But the mapping is clean and real: a research assistant escalates to a **human
> expert** when the sources can't answer or conflict unresolvably. The *principle* the
> exam tests — escalate on explicit triggers, not on difficulty or tone — is identical.

---

## Half 2 — ambiguity: ask, don't guess

`ambiguity.py` shows a different reliability trap. A user asks **"What's the cost?"** —
but the sources cover several distinct costs: the vehicle's **purchase price**, the
**running cost per km**, and **battery replacement**. The query matches more than one.

- **The wrong move (a heuristic guess):** pick one meaning — say, whichever appears
  first — and answer it. If the user meant a different cost, the answer is confidently
  about the **wrong thing**, and they may not notice.
- **The right move:** recognise the ambiguity and **ask which cost they mean**, briefly
  listing the options the sources can answer.

**The rule:** when one query maps to several distinct answers, **ask for clarification**;
never pick a meaning by heuristic. One short question is a tiny cost; a confidently
wrong answer is not.

---

## The demo

```cmd
python escalate_vague.py       # escalate on difficulty/tone -> misfires
python escalate_criteria.py    # explicit triggers + few-shot -> correct
python ambiguity.py            # ambiguous query -> ask which meaning (no API key)
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
3. scholardesk/
├── escalate_vague.py       ← NEW: ❌ escalate on difficulty/tone
├── escalate_criteria.py    ← NEW: ✅ explicit triggers + few-shot
├── ambiguity.py            ← NEW: ambiguous query -> ask, don't guess
├── DEMO-PROMPTS.md, README.md
├── scholardesk/, sources/  ← unchanged
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 5.2 — Design effective escalation and ambiguity resolution patterns**

- ✅ Appropriate escalation triggers (explicit human request, coverage/policy gaps,
  can't make progress): `escalate_criteria.py`.
- ✅ Escalating immediately on explicit request vs answering when covered: the
  "have a human look into this" case vs the running-cost case.
- ✅ Difficulty / self-reported confidence are unreliable proxies: `escalate_vague.py`
  demonstrates the misfire; criteria fixes it.
- ✅ Ambiguous queries require clarification, not heuristic selection: `ambiguity.py`.
- ✅ Explicit escalation criteria with few-shot examples: the criteria system prompt.
- ✅ Honoring explicit human requests immediately: honored without a first attempt.
- ✅ Answering when within capability despite forceful tone: the urgent-but-covered
  case is answered.
- ✅ Escalating on coverage gaps (sources silent on the question): the resale-value
  case.
- ✅ Asking for clarification on ambiguous queries: `ambiguity.py`.

---

## What's next

**Part 3 — Error propagation (Task 5.3).** When one of ScholarDesk's sources fails to
load, how should that failure travel back? We'll see why a generic "something went
wrong" hides vital context, and how structured error information lets the assistant
recover intelligently.

See you in Part 3.

---

*CCAR-F · Domain 5 · Part 2 — ANKIT MISTRY*
