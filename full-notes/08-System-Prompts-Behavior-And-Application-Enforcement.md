---
title: "System Prompts, Behavior, and Application Enforcement — Full Notes"
description: Combined slide notes + transcript + diagrams on giving ShopAssist AI a system prompt, and why guidance from a prompt is not the same as enforcement in code.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview
created: "2026-09-06"
tags:
  - hover-notes
  - udemy
  - full-notes
slide-note: "[[08-System-Prompts-Behavior-And-Application-Enforcement]]"
transcript: "[[hover-notes-transcripts/08-System-Prompts-Behavior-And-Application-Enforcement (transcript)|Transcript]]"
---

# System Prompts, Behavior, and Application Enforcement

> The previous lecture gave ShopAssist AI **context** (a `messages` list carrying conversation history). This lecture gives it **behavior** — a `system` prompt that defines persona, scope, tone, and hard constraints. It closes with the architectural point the exam keeps coming back to: a system prompt can *steer* a rule, but only application code can *guarantee* it. That's the same "which layer guarantees this behavior" question from the Claude App/API/Code/MCP/Agent SDK lecture — here it shows up one layer down, inside a single API call.

![Give It Behavior, Not Just Context](../hover-notes-images/screenshot-01M1P4EKVP4PST256V16BNQ060.png)

**[Slide detail]** The slide's own tagline: *"History tells Claude what's been said. The system prompt tells it how to act."*

---

## 1. Context vs. Behavior — two different jobs in the API request

- **`messages`** — what has been said so far
  - The running conversation history
  - Every user and assistant turn, appended and resent on each request
- **`system`** — how the assistant should behave
  - Durable instructions that set the assistant's role, tone, and behavior rules
  - Independent of any single message
- **[API Structure]** The system prompt is **not** just another user message — it has its own dedicated slot in the API request.

> **Transcript color:** "In the previous lesson, we built a basic multi-turn conversation... That gave ShopAssist context. Now we need to give it behavior. We do not want a generic chatbot."

![Recap: previous lesson's conversation history](../hover-notes-images/screenshot-01M1P4FV6WYWXAKKJ2FWEVP7Z8.png)

*This screenshot is the tail end of the prior lecture's notebook (a "return my order" conversation with no system prompt yet) — the video briefly recaps it before introducing `system_prompt`.*

---

## 2. Defining ShopAssist AI's behavior

- **[The Goal]** Transform the assistant from a generic chatbot into a specialized customer support agent for an online store, via a `system_prompt` variable.

```python
system_prompt = """
  You are ShopAssist AI, a helpful customer support assistant for an online store.

  Your job is to help customers with order questions, returns, refunds, shipping issues,
  Be concise, polite, and practical.

  Do not promise a refund until the order is checked.

  If you need more information, ask one clear question at a time.
  """
```

| Piece | What it establishes |
|---|---|
| **Persona** | Who the assistant is — ShopAssist AI |
| **Scope** | What it handles — order questions, returns, refunds, shipping, product support |
| **Tone** | Style — concise, polite, practical |
| **Constraints** | Hard rules — don't promise refunds prematurely; ask only one question at a time |

- **[Strategic Communication]** Two of these instructions specifically head off common chatbot failure modes:
  - **Preventing premature commitments** — the refund constraint forces a verification workflow before any promise is made.
  - **Optimizing user experience** — the single-question rule avoids overwhelming the customer during information-gathering.

![system_prompt defined in the notebook](../hover-notes-images/screenshot-01M1P4GRZCJNXV6R30X9NZ6F2N.png)

---

## 3. Wiring the system prompt into the chat function

- **[Implementation]** The `chat` function is updated to pass `system=system_prompt` alongside the existing `messages` argument.

```python
def chat(messages):
    message = model.messages.create(
        model=model,
        max_tokens=300,
        system=system_prompt,
        messages=messages
    )
    return message.content[0].text
```

- **[Impact]** Claude now sees not just the message history but its identity and operational constraints on *every single turn*.

> **Transcript color:** "The important difference is this line — system was set as a system prompt. That means every request will now include the ShopAssist AI instructions."

![chat() function updated with system=system_prompt](../hover-notes-images/screenshot-01M1P4J8ZDMQ7GSJAWF292EKZ8.png)

### The role split, restated

| | Answers |
|---|---|
| **System Prompt** | "How should the assistant behave?" |
| **Messages List** | "What has been said so far?" |

---

## 4. Testing it — does the constraint actually show up?

- Reset `messages` to `[]` and simulate a real customer interaction.

```python
messages = []
add_user_message(messages, "Hi, I bought headphones last week and they do not work. I want my money back.")
answer = chat(messages)
print("ShopAssist:", answer)
```

![Test setup: fresh messages list, add_user_message](../hover-notes-images/screenshot-01M1P4J8ZEE9G43CCRRHKX5PRY.png)

- **[Test Scenario]** User input: *"Hi, I bought headphones last week and they do not work. I want my money back."*
- **[Observed Behavior]** Because the system prompt forbids promising a refund before the order is checked:

| ShopAssist DOES | ShopAssist does NOT |
|---|---|
| Acknowledge the issue | Say **"Your refund is approved."** |
| Ask for the order number | |
| Explain the next step | |

- **[Key Insight]** This cautious, helpful tone is driven **entirely by the system prompt** — no business logic has been written yet.

![Careful by Design — ShopAssist does / does not](../hover-notes-images/screenshot-01M1P4KH6AGF5XV5KRDNVNVZ6R.png)

**[Slide detail]** The slide is titled *"Careful by Design"* (not named in the narration) and its footer states explicitly: *"All driven by the system prompt — **no business logic written yet**."* — a sharper way of putting the point than either the transcript or the original bullets stated it.

![Continuing the test: printing ShopAssist's reply](../hover-notes-images/screenshot-01M1P4KH6BJVF1ZVC3DSNB5HJ5.png)

---

## 5. Conversation state and history

- The feeling of continuity comes entirely from **resending the full history** with every request — it is not hidden model memory.
- **[The Conversation Flow]** A typical multi-turn interaction alternates roles:
  1. `user` — initial problem/question
  2. `assistant` — response shaped by the system prompt
  3. `user` — follow-up (e.g., order number)
  4. `assistant` — response acknowledging the new context

```python
messages = [
    {'role': 'user', 'content': 'Hi, I bought headphones last week and they do not work. I want my money back.'},
    {'role': 'assistant', 'content': "I'm sorry to hear your headphones aren't working! ... Could you please share your **order number**..."},
    {'role': 'user', 'content': 'The order number is 12345.'},
    {'role': 'assistant', 'content': "Thank you! Let me look up order #12345 for you..."}
]
```

![Full conversation history: two user/assistant turns](../hover-notes-images/screenshot-01M1P4ME5B4QZSCWR2JFTA03GH.png)

- **[Storage in Production]** This `messages` list can't just live in a local Python variable — it must persist externally (database, session storage) so it survives between requests.
- **[Context Responsibility]** The application owns the conversation; Claude simply responds based on the context the application sends it.

---

## 6. Guidance is not enforcement

- A prompt **steers** behavior; it does not **guarantee** it.

| Feature | Prompt (Guidance) | Code (Enforcement) |
|---|---|---|
| Nature | Soft | Hard |
| Function | Shapes tone, persona, and intent; sets sensible defaults | Backend verifies before it acts; financially critical rules live here |
| Reliability | Can be nudged, ignored, or slip | Cannot be talked out of by a user |

- **[Why this matters]** If a rule is financially or operationally important (e.g., "do not issue refunds before verification"), the **application code** must enforce it programmatically — the LLM following the prompt is not sufficient on its own.

> **Transcript color:** "A system prompt can guide behavior, but it is not the same as a guaranteed business rule... The prompt is guidance. The application code is enforcement. This distinction will become more important later when we add tools like lookup order, process refund, and escalate to human."

![Guidance Is Not Enforcement — prompt (soft) vs code (hard)](../hover-notes-images/screenshot-01M1P4P9HMFABBXBJ2B3A5AMCA.png)

The slide's own footer previews exactly where this is going: **"Coming up — real enforcement via tools: `lookup order` · `process refund` · `escalate to human`"** — i.e., the next lectures wire these into actual tool calls with a backend gate in front of them, the same shape as the Verification Gate pattern from the Claude App/API/Code/MCP/Agent SDK lecture.

### Today (prompt-only) vs. what's coming (programmatic gate)

```mermaid
flowchart TD
    U["Customer: 'I want my money back'"] --> Q{"How is the rule\n'don't promise a refund before verification'\nactually enforced?"}

    Q -->|"Right now — system prompt only"| SP["System prompt instruction:\n'Do not promise a refund until the order is checked'"]
    SP --> M1["Claude reasons over the instruction —\nsoft: can be nudged, ignored, or slip"]
    M1 --> R1["Claude usually stays cautious...\nbut nothing in code stops it if it doesn't"]

    Q -->|"Coming up — real tools + a backend gate"| GATE["Backend verifies the customer/order\nbefore process_refund is allowed to run"]
    GATE --> R2["Tool call is physically blocked until verified —\nhard: cannot be talked out of by a user"]

    classDef soft fill:#fde7c8,stroke:#b5793b,color:#52340b
    classDef hard fill:#dbe9ff,stroke:#3b6cb5,color:#0b2a52
    class SP,M1,R1 soft
    class GATE,R2 hard
```

---

## 7. Putting it together — the application loop

- **[The Application Loop]**
  1. Define the system prompt
  2. Maintain a `messages` list for conversation history
  3. Append each new user message with the `user` role
  4. Send both the system prompt and the `messages` list to Claude
  5. Append Claude's response back with the `assistant` role
  6. Repeat

```mermaid
sequenceDiagram
    participant App as Application
    participant C as Claude API

    Note over App: system_prompt defined once\n(persona, scope, tone, constraints)
    App->>App: messages = []
    App->>App: append user turn (role: user)
    App->>C: system=system_prompt, messages=messages
    C-->>App: assistant response
    App->>App: append response (role: assistant)
    Note over App: repeat each turn —\nthe app owns state, Claude only sees what's sent
```

- **[Scaling Conversation History]** Unlimited raw history is impractical in production — longer context means higher cost, more latency, more complexity. Production strategies:
  - Summarize older turns
  - Store key facts separately
  - Keep structured state (e.g., `customer`, `order`, `intent` as distinct fields)

![Putting It Together — the loop and scaling strategies](../hover-notes-images/screenshot-01M1P4PER7G9PC4DBVSJMKT59A.png)

**[Slide detail]** Footer line: *"**Claude app** handles history for you. **API** — you build that behavior yourself."* — a reminder that the convenience of the consumer Claude App (from the earlier "five concepts" lecture) disappears once you're the one calling the API; your backend is now responsible for the loop above.

---

## Summary

- **`messages`** answers "what's been said" (context); **`system`** answers "how should it behave" (behavior) — they occupy separate, dedicated slots in the API request.
- A well-built system prompt combines **persona, scope, tone, and constraints** — and constraints like "don't promise refunds before verification" visibly shape the model's replies even with zero business logic written.
- **Guidance vs. enforcement**: a system prompt is soft — it can be nudged, ignored, or slip. Code is hard — it verifies before acting and cannot be talked out of by a user. Financially or operationally critical rules belong in code, not just the prompt.
- The application owns conversation state end-to-end: building the `messages` list, persisting it externally in production, and managing its growth (summarization, key-fact extraction, structured state) as conversations scale.
- **Exam framing to remember:** this is the same question as "which layer guarantees this behavior" from the five-concepts lecture, now applied inside a single API call — the system prompt guides; the backend (in the upcoming tools lectures) enforces.

---

*Sources: [slide notes](../08-System-Prompts-Behavior-And-Application-Enforcement.md) · [[hover-notes-transcripts/08-System-Prompts-Behavior-And-Application-Enforcement (transcript)|full transcript]]*
