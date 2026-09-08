---
hovernotes-transcript-of: doc_ecee4f59-3dd1-4256-8e03-c6f36ac5dc49
hovernotes-transcript-version: 2
note: "[[27-BUILD-ShopAssist-Becomes-An-Agentic-System 1]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042371#overview"
updated: 2026-09-04T17:13:26.665Z
---

# 27-BUILD-ShopAssist-Becomes-An-Agentic-System 1 — Transcript

**0:00 → 0:32**

In this build lesson, ShopAssist becomes an agentic support system. Not just one prompt, not just one tool call. A controlled loop where Claude reads the customer request, chooses tools, reviews tool results, continues when more information is needed, and stops when the case is ready for a response or human escalation. The architecture rule is the same. Claude reasons, tools execute, gates enforce, hooks intercept, and handoffs carry structured state. our backend tools return more

**0:32 → 1:17**

In production, the same functions would call your customer database, order API, payment provider, refund service, or ticketing system. Here is the customer case. Customer message. Hi, I received my blue jacket yesterday and it arrived damaged. I also think I was charged twice. I want a full refund, not a replacement. My order number is 77819. This is a multi-concern request. The customer has a damaged item issue, a refund request, and a possible duplicate charge. A fixed pipeline could miss one of those concerns. An identity workflow is useful because Claude can decide which tools are needed and in what order. But Claude does not execute business actions directly. It receives tools

**1:17 → 2:02**

with typed inputs. In this demo, these tools map to backend functions. Verify customer checks the authenticated session. Lookup order retrieves, order fax using customer ID and order ID. Check return policy checks a specific item and reason. Investigate duplicate charge checks, payment records. Process refund can create a refund, but only if gates and hooks allow it. An escalate to human creates a structured handoff. Now we create persistent case facts. This case facts block is memory for the workflow. It protects important details like order IDs, item IDs, refund amounts, evidence, missing information, and escalation reasons. Now let's look at the backend functions.

**2:02 → 2:48**

This is the customer verification gate. Before ShopAssist can process a refund, the backend must confirm the customer session. Claude can request verification, but the backend decides whether verification passes. Next order lookup. The tool receives explicit typed arguments, customer ID and order ID. It does not guess everything from the raw customer message. Now the policy check. The item is eligible, but the refund amount is above the automatic limit. That limit will matter in the refund hook. Now duplicate charge investigation. This is a separate concern from the damaged item. In a larger system, the coordinator could run the policy check and payment investigation in parallel because they do not depend

**2:48 → 3:33**

each other. Now the refund tool. This is the refund limit hook. Claude may decide that a refund makes sense, but the backend still blocks automatic refund processing above the threshold. Prompts guide behavior. Code enforces rules. Now we need a tool runner. This function is the backend execution layer. Claude requests a tool, the backend executes it. Then the backend returns structured success, blocked or error results. Now let's look at the agentic loop. This is the core pattern. When stop reason is tool use, Claude is asking the application to run one or more tools. The backend executes those tools, updates case facts, sends the tool results back, and continues the loop. When stop reason is tool use, Claude is asking

**3:33 → 4:18**

turn, Claude has finished the response. If the stop reason is unexpected, the system does not improvise. It escalates safely. The update case fax function keeps the important facts outside the model context. This is simple but important. The case fax block survives the loop. It gives the coordinator a stable view of the case. Now let's walk through what happens. First, Claude reads the customer message and sees multiple concerns. It should request verification and order lookup. The backend verifies the customer and retrieves the order. Then Claude can request a return policy check and duplicate charge investigation. Those are independent concerns. The damaged item may may qualify for refund.

**4:18 → 5:03**

The requested amount is $149. The automatic refund limit is $75. So if Claude requests process refund, the refund hook blocks it and returns a structured error. This error is not a failure of the agent. It is the system working correctly. The tool tells Claude what happened and what the next safe step is. Then Claude should call Escalate to Human. This is a structured human escalation handoff. It includes the customer, order, root cause, refund amount, evidence, missing information, and escalation reason. Finally, ShopAssist drafts a customer response from verified state, not from scattered intermediate reasoning, not from unverified assumptions, from case

**5:03 → 5:48**

and tool results. For the exam, remember the pattern. An agentic system is not let the model do anything. It is a controlled loop. Claude chooses steps and reasons over tool results. The backend executes tools with typed arguments. Stop reason controls whether the loop continues or ends. Gates verify identity and permissions. Hooks block unsafe or policy-sensitive actions. Structured errors guide recovery. Case facts preserve important context. Parallel investigation handles independent concerns. And human escalation is a structured handoff, not a vague fallback. That is how ShopAssist becomes an agentic system without giving up production control.
