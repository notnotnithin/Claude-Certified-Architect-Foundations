# Demo 2 — Structured Error Responses (DocDesk)

Second demo in **Domain 2: Tool Design & MCP Integration**, continuing DocDesk.
Now our tools don't just succeed or crash — when something goes wrong they
return a **structured error** that tells the agent *what* went wrong and
*whether to retry*.
Maps to **Task Statement 2.2 — Implement structured error responses for MCP tools.**

---

## The concepts (short & simple)

**1. A tool signals failure with an `isError` flag (the MCP pattern).**
Instead of crashing, a tool returns a result that says "this failed."

**2. Not all errors are the same — give each a category.**
Four kinds matter, and each needs a different reaction:

| Category | Meaning | What the agent should do |
|----------|---------|--------------------------|
| `transient` | temporary blip (timeout, busy) | **retry** |
| `validation` | bad input (wrong doc name) | **fix the input**, don't blind-retry |
| `business` | a rule/policy blocks it | **explain**, don't retry |
| `permission` | not allowed to access | **stop / escalate**, don't retry |

**3. Say whether it's retryable (`isRetryable`).**
A retryable flag stops the agent from retrying things that will never succeed
(wasted calls) and from giving up on things that would work on a second try.

**4. Generic errors are the problem.**
A flat `"Operation failed."` tells the agent nothing — so it guesses. That's the
"before" we're fixing.

**5. An empty result is NOT an error.**
"I searched and found nothing" is a *successful* query with zero matches. It
must return `isError: false`, never an error. Confusing the two makes the agent
report false failures.

**6. Recover locally first.**
For a transient blip, the tool can quietly retry once itself before bothering
the agent. Only errors it can't fix locally get passed up.

---

## Before → After

**BEFORE** (`antipattern_tools.py`) — every failure is the same:
```
read a missing doc      -> {"error": "Operation failed."}
read a restricted doc   -> {"error": "Operation failed."}
a timeout               -> {"error": "Operation failed."}
search finds nothing    -> {"error": "Operation failed."}   ← even this!
```
The agent can't tell these apart, so it retries pointlessly or gives up wrongly.

**AFTER** (`tools.py`) — each failure is labelled:
```
missing doc     -> {isError, errorCategory:"validation", isRetryable:false, ...}
restricted doc  -> {isError, errorCategory:"permission", isRetryable:false, ...}
timeout         -> {isError, errorCategory:"transient",  isRetryable:true,  ...}
found nothing   -> {isError:false, matches:[], count:0}   ← a SUCCESS, not an error
```
Now the agent knows exactly how to react.

---

## How the agent works — and where each concept applies

```
You ask a question
      │
      ▼
[1] Model calls a tool (search_documents / read_document)
      │
      ▼
[2] Tool tries the action
      │
      ├─ success            → {isError:false, ...}          ← empty result is still success
      │
      └─ failure → tool builds a STRUCTURED error           ← Concepts 1–3, 5, 6
                    {isError, errorCategory, isRetryable, message}
                    (transient? it retries once locally first)
      │
      ▼
[3] Agent READS the error category + isRetryable            ← this is the whole point
      │
      ├─ transient  + retryable  → tries again
      ├─ validation             → fixes the name / asks
      ├─ business               → explains the rule
      └─ permission             → says it can't access it
      │
      ▼
[4] Agent writes a sensible final ANSWER
```

- Step **2** is where the tool does the work of Task 2.2: labelling the failure
  and recovering locally for transient blips.
- Step **3** is where the *value* shows up: because the error is structured, the
  agent makes the *right* recovery decision instead of guessing.
- With the **bad** tools, step 3 is impossible — every error looks identical, so
  the agent flails.

---

## Files

| File | Job |
|------|-----|
| `documents/` | Sample docs, incl. `internal_pricing.md` (restricted → permission error). |
| `doc_store.py` | Backend that can fail realistically (missing / restricted / flaky timeout). |
| `errors.py` | **The new piece** — the structured error format (category + retryable). |
| `tools.py` | **GOOD** tools — return structured errors + local retry (the AFTER). |
| `antipattern_tools.py` | **BAD** tools — generic `"Operation failed."` (the BEFORE). |
| `agent.py` | **Main demo** — system prompt teaches the agent how to react to each category. |
| `.env.example`, `.gitignore` | Setup helpers. |

`requirements.txt` lives **outside** this folder.

---

## Setup & run

1. Install packages (from the folder with `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the env file and add your key:
   ```bash
   # Windows:  copy .env.example .env
   # mac/Linux: cp .env.example .env
   ```
   Then put your key in `.env`.
3. Run:
   ```bash
   python agent.py          # GOOD tools (structured errors)
   python agent.py --bad    # BAD tools  (generic errors)
   ```

---

## Prompts to try (copy-paste)

Each one triggers a different error category — watch the `[ERROR] category=...`
line, then read how the agent reacts.

**1. Validation (bad document name):**
```
Read the document 'nope.md' and tell me what it says.
```

**2. Permission (restricted document):**
```
Read the document 'internal_pricing.md'.
```

**3. Transient (a flaky read that should be retried):**
```
Read the returns policy document in full.
```
(`returns_policy.md` is flaky in this demo — watch the tool retry locally, and
the agent retry if it still times out.)

**4. Empty result (NOT an error):**
```
Search the documents for 'spaceship'.
```
(Nothing matches — the good agent says "found nothing"; the bad agent calls it
a failure.)

---

## Good vs Bad — what to watch for

- **Good tools:** the agent retries the transient timeout, refuses to retry the
  permission/validation errors, explains business blocks, and treats "no
  matches" as a normal empty result.
- **Bad tools:** every failure is `"Operation failed."`, so the agent can't tell
  a retry-worthy blip from a permanent block — it retries pointlessly or gives
  up, and it wrongly reports an empty search as a failure.

> The lesson: **structured errors let the agent recover intelligently. Generic
> errors force it to guess.**
