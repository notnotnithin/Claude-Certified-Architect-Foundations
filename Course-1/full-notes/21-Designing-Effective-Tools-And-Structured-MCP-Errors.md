---
title: "Designing Effective Tools and Structured MCP Errors — Full Notes"
description: Combined slide notes + transcript + diagrams on writing tool descriptions that guide Claude's routing decisions and returning structured MCP error objects instead of vague failures, for Claude Certified Architect Foundations.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042305#overview
created: "2026-09-06"
tags:
  - hover-notes
  - udemy
  - full-notes
slide-note: "[[21-Designing-Effective-Tools-And-Structured-MCP-Errors]]"
transcript: "[[hover-notes-transcripts/21-Designing-Effective-Tools-And-Structured-MCP-Errors (transcript)|Transcript]]"
---

# Designing Effective Tools and Structured MCP Errors

> Lecture [[03-ClaudeApp-vs-ClaudeAPI-vs-ClaudeCode-vs-MCP-vs-AgentSDK|03]] first listed "clear name & description, typed schema, structured output, useful error handling" as the marks of a good MCP tool, and [[15-ToolSchemas-ToolChoice-And-FirstToolUse|15]] showed how to actually write a schema and read back a `tool_use` block. This lecture goes one level deeper into two of those marks specifically: how a **description** steers Claude toward the *correct* tool when several look similar, and how a tool should shape a **structured error object** so Claude (and the surrounding application) can recover intelligently instead of just seeing "it failed."

![00:00:00](../hover-notes-images/screenshot-01M1PHAVZWM3WRAZG69KPCHN9Z.png)

## The Selection Problem: How Claude Picks a Tool

- Claude sees three things when deciding which tool to call: the **tool name**, the **input schema**, and the **conversation context**.
- The **description** is the piece that explains *when* a tool should be used — not just what it returns.
- If descriptions are too short, too generic, or too similar to each other, Claude can pick the wrong tool.

> **Transcript color:** "How does Claude know which tool to choose? ... Claude can see the tool name, the input schema, and the conversation context, but the description explains when the tool should be used."

## Start Weak: Minimal Descriptions

The lecture opens with a deliberately weak pair of tools — two lookups that sound similar and explain nothing about when to use each one:

```json
weak_tools = [
  {"name": "get_customer",
   "description": "Get customer data.",
   "input_schema": {"email": {"type": "string"}}},

  {"name": "lookup_order",
   "description": "Get order data.",
   "input_schema": {"order_id": {"type": "string"}}}
]
```

- Both descriptions are one-line function summaries — they say *what* the tool returns, never *when* to call it.
- Neither explains the boundary between a customer lookup and an order lookup.
- Neither tells Claude what to do when the user gives only partial information.

![00:00:38](../hover-notes-images/screenshot-01M1PHAVZX6S01W49XPASPRPSS.png)

### The Routing Problem: Partial Information

This is where minimal descriptions actually break in practice:

> **Customer message:** *"Can you check my order? My email is alex@example.com."*

- **The trap:** the user said "order," so Claude may reach for `lookup_order`.
- **The problem:** the user never gave an `order_id` — only an email.
- **The correct path:** call the customer lookup tool first to identify the customer, then continue from there once a verified identity (and, eventually, an order ID) exists.

![00:01:04](../hover-notes-images/screenshot-01M1PHC2EFRZEJPW0DFRKG1RFF.png)

## Improving Tool Design: Specific Names + Guiding Descriptions

The fix has two parts, and both matter:

1. **Specific names** — `get_customer` becomes `get_customer_by_email`; `lookup_order` becomes `lookup_order_by_id`. The name alone now tells Claude what input the tool expects.
2. **Rich descriptions** that go beyond a function summary to cover: **purpose**, **expected inputs/outputs**, **concrete examples**, and — critically — explicit **boundaries** (when *not* to use the tool).

### Tool 1: `get_customer_by_email`

```json
{
  "name": "get_customer_by_email",
  "description": "Find a customer profile by email. Returns identity, account status, and a verified customer ID. Use FIRST when the user gives an email but no order ID. Do NOT use to look up a specific order.",
  "input_schema": {
    "email": {
      "type": "string",
      "description": "e.g. alex@example.com"
    }
  }
}
```

![00:01:25](../hover-notes-images/screenshot-01M1PHC2EF15ENJ713A5W0H2VJ.png)

### Tool 2: `lookup_order_by_id`

```json
{
  "name": "lookup_order_by_id",
  "description": "Retrieve a specific order by order ID (for example ORD-12345678). Do NOT use this tool with an email address. If the user only gives an email, call get_customer_by_email first.",
  "input_schema": {
    "order_id": {
      "type": "string",
      "description": "ORD- followed by 8 digits"
    }
  }
}
```

> **[Gap note]** The slide deck's own screenshots only capture a full-slide view of `get_customer_by_email` (Tool 1) — the video never yields a distinct capture of the `lookup_order_by_id` (Tool 2) slide on its own. The JSON above is reconstructed from the original slide note's text (itself apparently transcribed live from the video) plus the transcript's description of the same boundary rule ("lookupOrder by ID... requires an order ID and should not be used with an email address"), so its *content* is well corroborated even though there's no independent screenshot to verify the exact on-slide formatting of Tool 2.

Notice both descriptions do the same three things: state the **purpose**, give an **input example**, and set an explicit **boundary** ("Use FIRST when...", "Do NOT use..."). That boundary language is what actually prevents the routing mistake from the weak-tools example.

![00:01:57](../hover-notes-images/screenshot-01M1PHDF46K5SJDRYKT2H0VP2S.png)

## The Key Idea: Descriptions Guide Routing

> **[Slide detail]** The lecture's own diagram traces the corrected routing path end-to-end, including the failure branch: if `lookup_order_by_id` is ever reached with an email instead of an order ID, the flow explicitly loops back to `get_customer_by_email` rather than failing silently.

```mermaid
flowchart LR
    User["'Check my order'<br/>(email, but no order ID)"] --> T1["get_customer_by_email<br/>'use FIRST' — by description"]
    T1 --> ID["verified<br/>customer ID"]
    ID --> T2["lookup_order_by_id<br/>(now you have the order)"]

    T2 -.->|"✗ email is not an order ID"| User

    style T1 fill:#f6cfc2,stroke:#b5502f,color:#5c1f0a
    style T2 fill:#c9dff0,stroke:#3b6cb5,color:#0b2a52
    style ID fill:#cde8d5,stroke:#3b8a53,color:#0f3d1e
```

A well-designed interface uses names and descriptions — not just a system prompt — to steer the model through the correct multi-step logic.

![00:02:06](../hover-notes-images/screenshot-01M1PHDF47TJP74B3BCGPY4447.png)

## Tool Granularity: Split vs. Consolidate

> **[The core principle]** Split tools to reduce ambiguity; consolidate tools to reduce complexity.

- **Split for clarity:** one generic tool covering customers, orders, refunds, *and* policy checks becomes too vague for the model to use reliably. Purpose-specific tools give each one a clear, narrow job:
  - `get_customer_by_email`
  - `lookup_order_by_id`
  - `check_refund_eligibility`
  - `create_human_escalation`
- **Consolidate for simplicity:** if several tools are *always* called together, take the same input, and return different parts of one business operation, combining them reduces the number of steps Claude has to manage.

| Direction | Do it when… |
|---|---|
| **Split** | it reduces ambiguity (tools cover genuinely distinct business functions) |
| **Consolidate** | it reduces complexity (tools are always called together, same input, same operation) |

![00:02:18](../hover-notes-images/screenshot-01M1PHDX6G71Q5S9Z0W5F15GJB.png)

---

## Tool Errors: Weak vs. Structured

- **[The problem]** In production, tools fail constantly — invalid IDs, missing permissions, policy violations, backend timeouts.
- **Weak error example:**

```json
{ "error": "Something went wrong" }
```

- **[Why it matters]** A message like this gives Claude nothing to work with. It can't tell whether it should:
  - retry the request,
  - ask the user for better information,
  - explain a specific policy issue, or
  - escalate to a human.

![00:02:59](../hover-notes-images/screenshot-01M1PHETPV4JJZPCF8V5FS0F8Y.png)

### Implementing Structured Errors

The fix is a **structured error object** with a consistent shape: `isError`, `errorCategory`, `isRetryable`, a `customerMessage` (safe to show the end user), and a `developerMessage` (internal detail). Here's `lookup_order_by_id` handling a **validation** failure — a malformed order ID:

```python
def lookup_order_by_id(order_id: str) -> dict:
    if not order_id.startswith("ORD-"):
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "customerMessage": "The order ID does not look valid. Please check the order number and try again.",
            "developerMessage": "Order ID must start with ORD-."
        }
    # ... further logic for empty results, permission, and timeout cases
```

**[Screenshot-verified]** The code screenshot at 00:03:40 shows this exact function in the ShopAssistAI codebase (file `10_tools_errors.ipynb`), confirming every field name (`isError`, `errorCategory`, `isRetryable`, `customerMessage`, `developerMessage`) matches what the slide note claims — no discrepancies found in this lecture's code screenshots.

![00:03:40](../hover-notes-images/screenshot-01M1PHETPVNYXY7KZHS20NYG0E.png)

### Handling Specific Scenarios in `lookup_order_by_id`

The same function distinguishes four outcomes, each requiring a different action from Claude:

| Scenario | `isError` | `errorCategory` | `isRetryable` | Claude's action |
|---|---|---|---|---|
| Malformed order ID (`"ORD-..."` prefix missing) | `True` | `validation` | `False` | Ask the user to check/fix the input |
| Valid ID, no matching record (`ORD-00000000`) | `False` | *(n/a — not an error)* | *(n/a)* | Ask for a different ID or email |
| Valid ID, user doesn't own the order (`ORD-99999999`) | `True` | `permission` | `False` | Don't reveal private data; may escalate |
| Backend timeout (`ORD-TIMEOUT`) | `True` | `transient` | `True` | Retry the same request |

- **[Note]** An **empty result is not an error** — the tool executed correctly, it simply found no matching data. This is an easy category to conflate with a real failure, and the lecture calls it out explicitly.

```python
if order_id == "ORD-00000000":
    return {
        "isError": False,
        "orders": []
    }

if order_id == "ORD-99999999":
    return {
        "isError": True,
        "errorCategory": "permission",
        "isRetryable": False,
        "customerMessage": "I can't access this order with the current account information.",
        "developerMessage": "Authenticated customer does not own requested order."
    }

if order_id == "ORD-TIMEOUT":
    return {
        "isError": True,
        "errorCategory": "transient",
        "isRetryable": True,
        "customerMessage": "I'm having trouble checking the order right now. Please try again in a moment.",
        "developerMessage": "Order service timed out."
    }
```

![00:04:25](../hover-notes-images/screenshot-01M1PHG72SQ2ZW6655E0E6MS5P.png)

## Error Categories and Recovery

The `errorCategory` field is what lets the surrounding system decide how to respond, independent of the specific error message text. `isRetryable` makes the retry decision explicit rather than something Claude has to infer from the category name.

```mermaid
flowchart TD
    E["Tool returns isError: true"] --> C{errorCategory}
    C -->|transient| R["Retry the same request later<br/>(isRetryable: true)"]
    C -->|validation| V["Ask the user to fix the input<br/>(no retry)"]
    C -->|business| B["Explain the situation, or escalate<br/>(no retry)"]
    C -->|permission| P["Don't reveal data; escalate if needed<br/>(no retry)"]
```

| `errorCategory` | Meaning | Recovery action |
|---|---|---|
| **transient** | Temporary system problem (e.g. a timeout) | Retry the same request later |
| **validation** | Input is malformed or incomplete | Ask the user to fix the input — no retry |
| **business** | Request understood, but business rules disallow it | Explain the situation, or escalate — no retry |
| **permission** | User isn't authorized to access or perform the action | Don't reveal private data; escalate if needed — no retry |

![00:04:33](../hover-notes-images/screenshot-01M1PHH55Y1A2MB58FBTM8DXCR.png)

### Example: Refund Eligibility (a Business Error)

`check_refund_eligibility` is the lecture's example of a **business** error: the input is valid, permissions are fine, the backend is healthy — but a policy rule blocks the action. Retrying changes nothing, because the *rule*, not the system state, is what's stopping it.

```python
def check_refund_eligibility(order: dict) -> dict:
    if order["delivered_days_ago"] > 30:
        return {
            "isError": True,
            "errorCategory": "business",
            "isRetryable": False,
            "customerMessage": "This order is outside the standard return window, so I cannot process an automatic refund.",
            "developerMessage": "Refund denied because the order is outside the 30-day return policy."
        }

    return {
        "isError": False,
        "eligible": True,
        "reason": "Order is within the 30-day return window."
    }
```

- **Action:** Claude should use the `customerMessage` to explain the situation, or escalate if the workflow allows manual exceptions.

![00:05:05](../hover-notes-images/screenshot-01M1PHH55ZQ6WZMZC93N01SAKK.png)

## Production Pattern: Recover, Then Escalate

Not every error should go straight to a human or a coordinator agent — that wastes the whole point of automating the easy cases. The lecture frames recovery as a filter that runs *before* escalation:

```mermaid
flowchart LR
    A["Tool error<br/>(don't escalate yet)"] --> B["Try local recovery:<br/>• transient → retry locally<br/>• messy input → normalize it<br/>• missing info → ask the user"]
    B --> C{Resolved?}
    C -->|Yes| D["Continue the conversation"]
    C -->|No| E["Escalate<br/>(recovery failed, or needs human judgment)"]
```

- **Transient errors:** if the backend times out once, retry locally.
- **Messy input:** extra whitespace or lowercase in an ID — normalize it (strip, uppercase) instead of failing.
- **Missing information:** Claude can just ask the user for the missing field directly.
- **Escalation** only happens once local recovery has failed, or the error specifically needs human judgment (e.g. a `permission` or unresolvable `business` error).

This pattern reduces the burden on human operators by letting the application quietly resolve the mechanical failures (timeouts, sloppy formatting) and reserving escalation for cases that actually need it.

---

## Beyond Schemas

Tool design isn't finished once a schema validates. A strong tool interface has to help Claude:

- choose the right tool,
- send the right input,
- understand the result, and
- recover safely from errors.

For ShopAssist, that means: better names, better descriptions, clear input boundaries, and structured MCP errors. The payoff is **less room for the model to guess**, **more control for the backend**, and **a better experience for the customer** when something does go wrong.

![00:05:57](../hover-notes-images/screenshot-01M1PHJ26ZPTBG0HH2C61KRV87.png)

---

## In Plain English

Here's the whole file in plain, everyday language:

**The big picture:** two very practical, very exam-relevant skills — writing tool descriptions good enough that Claude never confuses one tool for another, and designing error messages good enough that Claude (and your app) can actually recover instead of just seeing "it failed."

**1. Weak descriptions cause real routing mistakes**
If two tools are named/described vaguely ("get customer data" / "get order data"), Claude can pick the wrong one — e.g., a customer only gives an email, but Claude reaches for the order lookup because the message mentioned "order."

**2. The fix is simple but very effective**
Rename tools to be specific (`get_customer_by_email`, `lookup_order_by_id`) and write descriptions that explicitly say *when* to use it AND *when not to* ("use this first if only an email is given, don't use this for orders").

**3. When to split tools vs. combine them**
Split into separate tools when it makes each one's job clearer; combine several tiny tools into one only when they're always used together anyway — splitting reduces confusion, consolidating reduces unnecessary extra steps.

**4. Bad error handling gives Claude nothing to work with**
A reply like `{"error": "something went wrong"}` doesn't tell Claude whether to try again, ask the customer for better info, or give up and escalate.

**5. The fix: return a structured error every time, with a category**
Is it a broken input (fix and retry), a permission problem (don't retry, maybe escalate), a business rule blocking it (explain, don't retry), or a temporary glitch (safe to just retry)? Each category tells Claude — and your code — exactly what to do next.

**6. An empty result is NOT an error**
If a valid order ID simply doesn't exist in the system, that's a normal "no results," not a failure — mixing these up would make your app retry things that will never succeed.

**7. Don't escalate to a human immediately**
First let the system try to recover on its own (retry a one-off glitch, clean up messy input, just ask the user for a missing field) — only escalate once that quiet recovery attempt has failed or the situation genuinely needs a person's judgment.

**One-sentence summary:** Specific tool names + descriptions that state clear boundaries stop Claude from picking the wrong tool, and structured, categorized error messages let both Claude and your app recover intelligently instead of treating every failure the same way.

---

## Full Walkthrough: One Tool Call, Two Outcomes (With Real JSON)

Everything above can feel abstract until you watch **one tool call** produce a structured error, and then watch a **second, different call to the same tool** produce a completely different kind of structured error. So let's trace both, back to back, with the actual JSON at every stage. Same tool — `lookup_order_by_id` — two different order IDs, two different outcomes.

---

### Outcome 1 — The customer doesn't own this order

**Customer message:**

> "Can you check on order ORD-99999999?"

**Step 1 — Claude requests the tool.** The order ID is well-formed (it starts with `ORD-`), so Claude has no reason to hesitate. It sends a normal `tool_use` request:

```json
{
  "type": "tool_use",
  "name": "lookup_order_by_id",
  "input": {
    "order_id": "ORD-99999999"
  }
}
```

**Step 2 — Your backend runs the real function.** This is the exact `lookup_order_by_id` branch from earlier in this file, run with `order_id = "ORD-99999999"` — the real record exists, but it belongs to a different customer:

```python
if order_id == "ORD-99999999":
    return {
        "isError": True,
        "errorCategory": "permission",
        "isRetryable": False,
        "customerMessage": "I can't access this order with the current account information.",
        "developerMessage": "Authenticated customer does not own requested order."
    }
```

**What comes back to Claude, verbatim:**

```json
{
  "isError": True,
  "errorCategory": "permission",
  "isRetryable": False,
  "customerMessage": "I can't access this order with the current account information.",
  "developerMessage": "Authenticated customer does not own requested order."
}
```

**Step 3 — Claude reads the category, not just the failure.** Per the recovery table earlier in this file, `errorCategory: "permission"` means: *don't reveal private data; escalate if needed — no retry.* So Claude:

- does **not** try calling `lookup_order_by_id` again with the same ID — retrying won't change who owns the order,
- does **not** guess at or reveal any order details,
- uses `customerMessage` directly to explain the situation: *"I can't access this order with the current account information."*
- may offer to escalate, or ask the customer to confirm they're using the right account.

**Now contrast that with the weak version.** If this tool had instead returned the file's own weak-error example —

```json
{ "error": "Something went wrong" }
```

— Claude would have nothing to work with. It couldn't tell whether "something went wrong" meant *retry in a second*, *ask the customer for a different order ID*, *this is a permissions problem*, or *give up entirely*. It would be guessing. The structured version removes the guessing: `errorCategory: "permission"` and `isRetryable: False` together already say exactly what to do.

---

### Outcome 2 — The backend times out

Same tool, same customer, but this time the order ID is `ORD-TIMEOUT` instead.

**Step 1 — Claude requests the tool, again unremarkably:**

```json
{
  "type": "tool_use",
  "name": "lookup_order_by_id",
  "input": {
    "order_id": "ORD-TIMEOUT"
  }
}
```

**Step 2 — Your backend runs the same real function, different branch:**

```python
if order_id == "ORD-TIMEOUT":
    return {
        "isError": True,
        "errorCategory": "transient",
        "isRetryable": True,
        "customerMessage": "I'm having trouble checking the order right now. Please try again in a moment.",
        "developerMessage": "Order service timed out."
    }
```

**What comes back to Claude, verbatim:**

```json
{
  "isError": True,
  "errorCategory": "transient",
  "isRetryable": True,
  "customerMessage": "I'm having trouble checking the order right now. Please try again in a moment.",
  "developerMessage": "Order service timed out."
}
```

**Step 3 — This one is safe to just retry.** `errorCategory: "transient"` plus `isRetryable: True` means the *opposite* recovery action from Outcome 1: this isn't about who owns the order, it's a temporary backend hiccup. So the calling code (or Claude itself) can simply call `lookup_order_by_id` again with the same `order_id: "ORD-TIMEOUT"`, no questions asked. No permissions were violated, nothing about the request was wrong — the system just needs another try.

---

### The two outcomes, side by side

| | Outcome 1: `ORD-99999999` | Outcome 2: `ORD-TIMEOUT` |
|---|---|---|
| `errorCategory` | `permission` | `transient` |
| `isRetryable` | `False` | `True` |
| Correct action | Explain via `customerMessage`, don't retry, maybe escalate | Retry automatically |

Same tool call, same input shape, same tool name — only the **category** differs, and that's all it takes to send the two down completely different paths.

Notice what didn't have to happen anywhere in this walkthrough: no human read `developerMessage` and decided what to do next, and Claude never had to pattern-match on the wording of `customerMessage` to guess whether retrying was safe. The `errorCategory` field alone routed both cases correctly.

**The one thing to hold onto:** `errorCategory` and `isRetryable` are doing all the real work here — they're what let code (and Claude) make the right recovery decision automatically, without a human or the model having to interpret a vague error message.

---

*Sources: [slide notes](../21-Designing-Effective-Tools-And-Structured-MCP-Errors.md) · [[hover-notes-transcripts/21-Designing-Effective-Tools-And-Structured-MCP-Errors (transcript)|full transcript]]*
