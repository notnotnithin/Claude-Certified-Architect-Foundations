---
hovernotes-transcript-of: doc_79bf26b0-26ba-4f40-a05d-0d28e4910c59
hovernotes-transcript-version: 2
note: "[[26-SessionState-Forking-Scratchpads-And-LargeContextWorkflows]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042367#overview"
updated: 2026-09-04T16:58:59.819Z
---

# 26-SessionState-Forking-Scratchpads-And-LargeContextWorkflows — Transcript

**0:00 → 0:43**

In short, cloud workflows, we can often pass the recent conversation, tool results, and user requests directly into the next model call. But in long-running workflows, that becomes risky. A real shop assist support case may include customer messages, order lookups, policy checks, refund limits, damaged item photos, duplicate charge investigations, human review notes, and several internal decisions. If all of that lives only in the conversation history, important facts can get buried. So in this lesson, we'll focus on one production rule. The conversation is not your database. For long-running cloud SDK applications, durable states should live outside the model context. Let's start with the fragile

**0:43 → 1:28**

This looks simple, but it does not scale well. As a case grows, the model sees more repeated messages, verbose tool output, old assumptions, and outdated intermediate nodes. Important facts can move into the middle of the context. And that is where models are more likely to miss them. This is often called the lost-in-the-middle problem. The fix is to maintain a structured case-facts block. This is not just a summary for readability. This is persistent working state. IDs, dates, refund amounts, policy versions, percentages, and customer expectations must survive long sessions, retries, handoffs, and human review. Now, the coordinator can load the current case state explicitly. The coordinator is responsible

**1:28 → 2:13**

state. Claude reasons. Tools execute, gates enforce, hooks intercept, handoffs, carry structured state. For example, if the workflow was interrupted, we do not want to guess what happened from a long chat transcript. We want a recovery manifest. Notice the distinction. Drafting a customer response again is usually safe. Processing a refund again is not safe to retry blindly. That decision should not depend on whether Claude remembers the previous step correctly. It should be stored in application state. Now let's look at enforcement. A prompt can tell Claude not to process large refunds automatically. But if the rule must always be followed, the backend must enforce it. Claude may recommend a refund.

**2:13 → 2:59**

But the tool validates the session, checks the amount, applies business rules, and returns a structured result. That is the correct boundary. Prompts guide behavior. Code enforces rules. Now, let's reduce context pressure. A weak order lookup might return the full internal order record. Payment logs, warehouse scans, comments, retry events, and every audit field. For this decision, the agent only needs the relevant facts. The tool output is not vague, but it is trimmed. It gives Claude the facts needed for reasoning without flooding the context window. When we aggregate inputs, we should also place key summaries first. Do not bury the most important facts after pages of logs. matters because longer

**2:59 → 3:44**

text workflows degrade gradually. The model may still sound confident, but it can miss a date, confuse an older refund threshold with the current one, or forget that the customer asked for a refund rather than a replacement. Progressive summarization has a similar risk. If every step summarizes the previous summary, small details can disappear over time. So we should preserve critical facts in structured state, not only in natural language summaries. Now let's add sub-agents. Sub-agents are useful when work can be split into independent investigations, but they have isolated context. They do not automatically inherit the parent conversation. coordinator must pass the relevant facts explicitly. We are not asking this obey

**3:44 → 4:29**

for a long reasoning transcript. We are asking for structured findings and metadata. That makes the result easier to verify, store, compare and pass forward. Multiple subagents can run in parallel when the work is independent. But the coordinator still owns the final integration. All customer-facing communication should route through the coordinator. This is a good handoff because it is specific. Another agent, a human reviewer or a later workflow step can continue without reconstructing the entire conversation. For the exam, remember this. Large context work is an architecture problem, not just a prompting problem. Do not rely on a long conversation as your source of truth. Store durable

**4:29 → 4:56**

outside the model context. Use case facts blocks, trim tool outputs, recovery manifests, structured handoffs, and subagent outputs with facts and metadata. And protect the exact details, customer IDs, order IDs, dates, refund amounts, policy versions, percentages, missing information, and customer expectations. In production, those are not small details. They are
