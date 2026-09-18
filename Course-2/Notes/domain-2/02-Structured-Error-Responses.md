---
title: "Course: Claude Certified Architect: Foundations Exam Guide - 2026 | Udemy"
description: Agentic architecture, MCP tools, Claude Code, prompt engineering & context management for the CCA Foundations exam
author: 2026 | Udemy
source: https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460121#overview
created: "2026-09-10"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/02-Structured-Error-Responses (transcript)|Transcript]]"
hovernotes-id: doc_56d1795b-9c02-433d-882c-52fc9f03567e
---

![00:00:00](hover-notes-images/screenshot-01M25P8AB05GBB17W5SPZS6FEK.png)
[00:00:00](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

## Structured Error Responses

- When a tool fails, the error message is Claude's only clue to what went wrong
    - Even perfectly described tools can fail due to external issues like:
        - Payment bounces
        - Database downtime
        - Missing data (e.g., an order simply isn't there)

![00:00:45](hover-notes-images/screenshot-01M25P9B23VGGFWAXV2PW9T4AT.png)
[00:00:45](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:01:10](hover-notes-images/screenshot-01M25P9B23WGF0HZXMYF8R2AVR.png)
[00:01:10](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### Errors Are Claude's Window Into Failure

- Generic messages like "Something went wrong" provide no information to the model
- **[The Useless Error Example]**
    - Error: `"Booking failed."`
    - Result: Claude is stuck with nothing to act on
    - Why: It doesn't specify the cause (e.g., was it a credit card issue?)

![00:02:13](hover-notes-images/screenshot-01M25PA4D4AM474PZDRJBJV4DC.png)
[00:02:13](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### Actionable vs. Useless Errors

- **[Useless Error]**
    - Example: `'Booking failed.'`
    - Problem: Does not explain the cause (e.g., was the card declined, was the flight full, or was the service down?)
    - Result: Claude is stuck because it has no information to act upon
- **[Actionable Error]**
    - Example: `'Payment failed: insufficient balance. Refund in 3 days. Try another method.'`
    - Benefit: It identifies exactly what broke and hints at the next move
    - Result: Claude can take sensible actions, such as:
        - Telling the customer their balance is low
        - Suggesting a different payment method

![00:02:14](hover-notes-images/screenshot-01M25PBD5T7CF5XJ2EVWCYFTG1.png)
[00:02:14](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:02:58](hover-notes-images/screenshot-01M25PBD5T6FRBY7X53D45GEHP.png)
[00:02:58](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### The Importance of Error Specificity

- Claude can only act on what the error message actually says
    - It is not sitting inside your system watching what happened
    - The error text is the entire window it has into what went wrong
- **[The Core Principle]**
    - Vague errors force the model to guess
    - Specific errors let the model recover

### The isError Flag

- A single boolean value (true/false)
    - Indicates that a tool ran, but the execution failed

![00:03:41](hover-notes-images/screenshot-01M25PCC87C1DSNNB833J6KGA0.png)
[00:03:41](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### Implementing Readable Failures

- **The Technical Distinction**
    - The tool call itself should succeed at the technical level to prevent a system crash
    - Instead of throwing a raw exception, return a response containing `isError: true`
- **Why Avoid Raw Exceptions?**
    - Claude handles raw exceptions poorly, often treating them as low-level protocol errors
    - By returning a structured error within a successful response, you provide a "readable failure" that Claude can interpret and act upon

![00:03:44](hover-notes-images/screenshot-01M25PCW1JDYXF1YB8XVRAN5R2.png)
[00:03:44](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:04:27](hover-notes-images/screenshot-01M25PCW1JWQTS8371XAZD4B1E.png)
[00:04:27](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### Exception vs. Structured Error

- **[The Problem with Exceptions]**
    - A thrown exception becomes a low-level protocol error
    - This happens at the "plumbing" level, below the conversation
    - Result: Claude cannot see, reason about, or act upon the failure
- **[The Solution: Handing Failures Gently]**
    - Return `isError: true` along with specific details inside a normal response
    - This arrives as a message Claude can actually read and interpret
    - **[Why this works]** It transforms a system crash into actionable data

## Error Categories

- Not all failures are the same kind of failure
- **Common categories include:**
    - `validation`: Bad input — fix it and retry
    - `auth / permission`: Not allowed — escalate
    - `not_found`: Nothing there to return
    - `rate_limit / transient`: Service busy — wait, then retry

![00:05:10](hover-notes-images/screenshot-01M25PE5TFJEW38WECBJV5NKRX.png)
[00:05:10](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### Error Tagging for Recovery

- **[The Core Strategy]**
    - To ensure Claude takes the correct path, every error should be explicitly tagged with its specific category
    - This transforms a simple error message into a set of instructions for the next move
- **[Mapping Failures to Actions]**
    - The goal is to ensure the response points to a distinct recovery strategy:
        - **Bad input** $\rightarrow$ Fix and retry
        - **Not allowed** $\rightarrow$ Escalate
        - **Nothing there** $\rightarrow$ Accept/End
        - **Service busy** $\rightarrow$ Wait and retry

![00:05:14](hover-notes-images/screenshot-01M25PF1YHDVC4TFT8HPF91G3G.png)
[00:05:14](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:05:55](hover-notes-images/screenshot-01M25PF1YHD7QM3R69JJ7MCWTA.png)
[00:05:55](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### The Power of Error Categorization

- Tagging every error with an `errorCategory` provides a clear decision path for Claude
- **[The Benefit]**
    - Without a tag, every failure looks identical, forcing the model to guess how to react
    - With a tag, a vague failure is transformed into a clear, actionable decision

## isRetryable: Should Claude Try Again?

- Described as the single most useful field in an error response
- A single boolean value (`true` or `false`) that prevents "blind retry loops"
- **[How it guides behavior]**
    - `isRetryable: true` $\rightarrow$ used for `transient` or `rate_limit` errors (wait, then retry)
    - `isRetryable: false` $\rightarrow$ used for `validation`, `auth`, or `business` errors (retrying is pointless)
- **[Example: Business Errors]**
    - A "business error" (e.g., a refund that exceeds a limit) is never retryable

![00:06:38](hover-notes-images/screenshot-01M25PFYYPJ7ZADHE0R36BTGC5.png)
[00:06:38](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:06:45](hover-notes-images/screenshot-01M25PGZ40PKZA8SFADVN8CJK2.png)
[00:06:45](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:07:25](hover-notes-images/screenshot-01M25PGZ407KDXVVP38QW4XF19.png)
[00:07:25](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### The Cost of Blind Retries

- **[The Risk]** Without an `isRetryable` flag, an agent may enter a loop of repeating the same unsuccessful action
    - If input is invalid, it remains invalid on every retry
    - If a business policy is violated (e.g., a refund limit), it will continue to fail on every attempt
- **[Consequence]** This wastes both time and money (API calls) on operations that can never succeed

---

## Empty Result vs Real Failure

- **[Core Principle]** "Found nothing" is a success, not an error
- **[Success, but empty]** When a search or query returns no results, it should be reported as a successful operation with an empty set
    - Example response structure:

```json
{
        "isError": false,
        "resultCount": 0
      }
```

    - This provides a real answer: "no orders found" rather than triggering error recovery logic

![00:07:55](hover-notes-images/screenshot-01M25PJ9G3CJV250ZC4VW1HT4P.png)
[00:07:55](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### Distinguishing Success from Connectivity Failures

- **[Success, but empty]** The tool performed its task perfectly and correctly reported that no data exists
    - Example: Searching for orders and finding none
    - Response structure:

```json
{
        "isError": false,
        "resultCount": 0
      }
```

    - **[Key takeaway]** This is a complete and successful answer, not a failure
- **[Real Failure: Access Failed]** The tool was unable to perform its task because it couldn't reach the necessary data source
    - Example: "Couldn't reach the database"
    - Response structure:

```json
{
        "isError": true,
        "isRetryable": true
      }
```

    - **[Why it differs]** Unlike an empty result, the tool never actually got to look at the data, meaning it doesn't know if orders exist or not

![00:08:21](hover-notes-images/screenshot-01M25PJR0Z93WV4PTKKTNEXTAA.png)
[00:08:21](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:08:56](hover-notes-images/screenshot-01M25PJR10FGPMYWCZBV5K0JEJ.png)
[00:08:56](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### The Distinction Between Empty Results and Failures

- **[The Canonical Trap]** An agent retrying a successful empty query
    - This occurs if an empty result is mistakenly reported as an error
    - The agent will continuously hunt for data that does not exist, wasting resources
- **[Comparison]**

| Scenario | isError | retryable | Meaning |
| --- | --- | --- | --- |
| Success, but empty | false | N/A | The tool worked perfectly; the answer is simply "nothing found" |
| Access failed | true | true | A genuine failure (e.g., database unreachable) that is worth retrying |

- **[Key Rule]** "Empty is an answer; failure is not"
        - An empty result must explicitly communicate: "I succeeded, and the answer is nothing"

## Writing a Useful Error Message

- To be effective, an error message should cover:
        - What was attempted
        - What failed
        - What to do next

![00:09:00](hover-notes-images/screenshot-01M25PKPR5T4HBJBNKNW54D6CK.png)
[00:09:00](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:09:14](hover-notes-images/screenshot-01M25PKPR59NX2MT6E3WNFFBTM.png)
[00:09:14](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### The Error Message Balance

- **[Core Principle]** Say enough to recover — nothing that leaks
- **[The Recipe]** A useful message should cover:
    - What was attempted
    - What failed
    - What to do next
- **Comparison of Error Quality**
    - **Good:** Provides context and guidance
        - *Example:* "Couldn't fetch order #4471: DB timed out after 5s. Transient — safe to retry."
    - **Bad:** Provides no utility
        - *Example:* A bare "Error."
    - **Dangerous:** Leaks system internals
        - *Example:* Returning a raw stack trace
- **Sanitization**
    - **[Why sanitize?]** Raw technical errors leak your internal implementation details to the LLM/user
    - **[How to sanitize]** Wrap specific, low-level errors into safe, high-level descriptions
        - *Instead of:* `no such table: users_v2`
        - *Use:* `The requested resource could not be accessed.`

![00:09:58](hover-notes-images/screenshot-01M25PM83MKEPNV1Y59H6J2NJB.png)
[00:09:58](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### The Dual Purpose of Masking Errors

- **[Goal 1] Help the LLM**
    - A raw stack trace acts as "noise" to Claude
    - This noise makes it significantly harder for the model to identify and understand the actual problem
- **[Goal 2] Protect the System**
    - Raw technical errors reveal the internal structure of your system
    - They can act as a "free map" for outsiders, exposing sensitive details like:
        - Database table names
        - Internal file paths
- **[The Solution] One clean, sanitized message fixes both issues**

![00:10:32](hover-notes-images/screenshot-01M25PNG7P01P0V8EHQGVJT9QF.png)
[00:10:32](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

![00:10:34](hover-notes-images/screenshot-01M25PNG7P1P687D0F8K7Z5ZAQ.png)
[00:10:34](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

## Key Takeaways: Structured Errors

- **[Core Philosophy]** When a tool fails, Claude is not in the room; it relies entirely on the structured data you return to understand the situation.

### 1. Return, Don't Throw

- **[The Problem]** A thrown exception provides no actionable information to the LLM.
- **[The Solution]** Return an error response containing specific details
    - This provides Claude with its only clue to resolve the issue

### 2. Category + Retryable

- **[The Mechanism]** Tag every error with an `errorCategory` and an `isRetryable` flag
- **[The Goal]** This gives Claude a clear decision path so it knows whether to:
    - **Fix** (e.g., bad input)
    - **Wait** (e.g., transient error/rate limit)
    - **Escalate** (e.g., permission denied)
    - **Stop** (e.g., business rule violation)

### 3. Empty is Not Failure

- **[The Distinction]** An empty result is a successful query that found nothing
- **[Implementation]** Use `isError: false` with a `resultCount: 0`
    - **[Why?]** This ensures the agent never incorrectly retries a successful operation as if it were a failure

![00:11:16](hover-notes-images/screenshot-01M25PPDNZHQB71QRPJ9RMPMV9.png)
[00:11:16](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

### The Role of the Error Message

- **[Core Reality]** Claude cannot see your logs, exceptions, or database
    - The error message is the *only* window it has into what went wrong
- **[The Goal]** A good error is a small, structured note that tells the model:
        - What happened
        - What to do about it
- **[Consequences of Poor Design]**
        - **Good error:** The agent recovers gracefully
        - **Bad error:** The agent guesses or enters an infinite loop

---

## Tool Distribution and Tool Choice

![00:12:01](hover-notes-images/screenshot-01M25PPD2NWD12B6RCSZ6K79JG.png)
[00:12:01](https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview)

## Tool Distribution and Tool Choice

- **[Focus]** Moving from how to describe a single tool to determining how many tools to provide to Claude and how to steer those choices.
- **Upcoming Topics**
    - Scoping tools to the job
    - The four modes of tool choice
    - When to use each mode
    - Real-world work examples

---

## Simple Explanation (with Claude Examples)

**The core idea, in one line**: When a tool fails, the error message is Claude's *entire* window into what went wrong — a vague "something went wrong" leaves it stuck, while a specific, structured error lets it actually recover.

**Useless vs. actionable errors**

- **Useless**: `"Booking failed."` — Claude has nothing to act on. Was it the card? The flight being full?
- **Actionable**: `"Payment failed: insufficient balance. Refund in 3 days. Try another method."` — Claude now knows exactly what happened and what to suggest next.

*Everyday analogy*: it's the difference between a doctor saying "you're sick" versus "you have a mild fever caused by X, rest and drink fluids." One gives you nothing to act on; the other gives you a clear next step.

**Return, don't throw**

Raw exceptions get treated as low-level "plumbing" errors Claude can't reason about — they happen below the conversation, invisible to the model. Instead, return a structured response with `isError: true` plus specifics. This turns a system crash into readable, actionable data Claude can actually interpret.

*Claude Code example*: If a `Bash` command I run fails, I don't just see a raw crash — I get back the actual stderr output as a normal tool result. That's exactly this principle: a "readable failure" I can read and reason about, instead of an opaque low-level exception.

**Error categories — tell Claude what kind of failure this is**

Tag every error so Claude knows the right response:
- `validation` → fix input, retry
- `auth/permission` → escalate
- `not_found` → nothing there, accept it
- `rate_limit/transient` → wait, then retry

**`isRetryable` — probably the single most useful field**

A `true`/`false` flag that prevents "blind retry loops." Transient errors (server busy) → `true`, retry makes sense. Business errors (a refund that violates policy) → `false`, retrying will *never* succeed no matter how many times you try — it just wastes time and money.

*Claude Code example*: If I tried to run a command and got permission denied, retrying the exact same command five times in a row would be pointless — `isRetryable: false` tells me (or would tell an automated system) to stop retrying and instead escalate or try a different approach entirely.

**Empty result ≠ failure**

"Found nothing" is a successful answer, not an error:
```json
{ "isError": false, "resultCount": 0 }
```
vs. a real failure where the tool never even got to look:
```json
{ "isError": true, "isRetryable": true }
```
Mixing these up causes an agent to endlessly retry a search that correctly found nothing — hunting forever for data that was never there.

**Writing a good error message — and sanitizing it**

A good message says what was attempted, what failed, and what to do next — *without* leaking internals. `no such table: users_v2` becomes `The requested resource could not be accessed.` This protects two things at once: it removes noise that confuses Claude, and it stops your internal database structure from leaking to whoever's reading the output.

**Recap in 3 lines**

1. **Return structured errors, never raw exceptions** — Claude only sees what you explicitly hand it back.
2. **Tag with category + `isRetryable`** — gives Claude a clear decision: fix, wait, escalate, or stop.
3. **Empty is a success, not a failure** — `isError: false, resultCount: 0` prevents pointless infinite retries.

---

## Exam Objective Note: CCAR-F 2.2 — Structured Error Responses

**The one question that matters after a failure: "should I try again?"**

This is the most important thing an agent needs to know after something goes wrong. The answer has to be spelled out in the error itself — a field like `isRetryable` — not something Claude has to guess from the wording of the message.

**Three kinds of failure, three different answers**

- **A timeout** — the server was briefly busy. Try again and it might work. Retryable.
- **A bad argument** — the input itself is wrong. Retrying with the same input will never work. The input needs fixing, not another attempt.
- **A closed account** — a permanent fact. No amount of retrying changes it. What's actually useful here isn't "try again," it's a clear reason, like "this account was closed on March 3."

*Everyday analogy*: a shop closed for lunch — come back in an hour and it's open. A shop closed down for good — coming back never helps. What you need there is someone telling you plainly "they've closed for good," not a vague "try later."

**Don't mix up "found nothing" with "couldn't check"**

- **"Nothing found"** — Claude looked, and there was genuinely nothing there. A complete, successful answer.
- **"Could not look"** — Claude never got to check at all (database down, access blocked). An unfinished, failed attempt.

If a tool returns an empty list for both cases, Claude can't tell them apart. But the two cases need completely different next steps: accept "nothing found" and move on, or retry/escalate "couldn't check."

*Claude Code example*: if I search a codebase with `Grep` and it finds zero matches, that's a successful search with an empty result — I should report "no matches" and move on. If instead the search failed because a file couldn't be read, that's a real failure — I should retry or tell you what broke, not quietly report "no matches" as if the search actually ran.

**Recap in 3 lines**

1. Say clearly in the error whether trying again would help — don't make Claude guess from the wording.
2. Not every failure is the same: a timeout may fix itself, but a bad input or a closed account never will, however many times you retry.
3. Keep "found nothing" and "couldn't check" separate — collapsing them into one empty response stops Claude from reacting the right way to either one.