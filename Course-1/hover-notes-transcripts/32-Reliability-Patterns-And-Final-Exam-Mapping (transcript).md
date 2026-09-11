---
hovernotes-transcript-of: doc_84909f25-15e9-4c3e-94c5-12b7ec4be759
hovernotes-transcript-version: 2
note: "[[32-Reliability-Patterns-And-Final-Exam-Mapping]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042417#overview"
updated: 2026-09-06T11:57:09.833Z
---

# 32-Reliability-Patterns-And-Final-Exam-Mapping — Transcript

**0:00 → 0:40**

In this final lesson, we bring ShopAssist together as a production-style cloud architecture. ShopAssist now has prompts, tools, structured outputs, validation, agentic workflows, cloud code configuration, CI review, and reliability patterns. The final question is, how do we make this system safe and trustworthy in real customer support? Let's start with escalation. A reliable system does not escalate only because the customer sounds angry. Sentiment is useful context, but it is not a reliable signal of case complexity. A frustrated customer may have a simple return request. A calm customer may have a simple return request.

**0:40 → 1:25**

policy exception, identity ambiguity, or financial risk. So, ShopAssist needs explicit escalation triggers. Escalate when the customer explicitly asks for a human. Escalate when the policy is missing, ambiguous, or does not cover the request. Escalate when the agent cannot make meaningful progress. Escalate or ask for clarification when backend results are ambiguous, such as multiple customer matches. For example, if the customer says, I want to speak to a real person. The agent should honor that request immediately. It can summarize the case for the support specialist, but it should not force the customer through more automated investigation first. If the customer says,

**1:25 → 2:11**

I'm frustrated, my package arrived damaged. That alone is not automatic escalation. The agent can acknowledge the frustration, verify the order, check the policy, and resolve the issue if it is within scope. Now, consider ambiguity. If the customer returns two matching customers, the agent should not guess. It should ask for another identifier, such as email address or order number. This is a common exam pattern. When identity permissions or financial actions are involved, do not use heuristics. Clarify, verify, or escalate. Next, error propagation. In a multi-agent system, failures should not disappear. A weak error response says something like this. This gives the coordinator enough context

**2:11 → 2:56**

recover. It can retry, ask the customer for missing information, continue with partial results or escalate. The key pattern is local recovery first, coordinator propagation second. A sub-agent should retry transient failures locally, but if it cannot recover, it should propagate a structured error with what was attempted and what partial results exist. Also remember the difference between an access failure and a valid empty result. A valid empty result means the query succeeded, but no matching record was found. An access failure means the system could not reach the data source. Those require different decisions. Now let's talk about provenance. A reliable system must preserve where important claims came from.

**2:56 → 3:41**

For shop assist, the final answer should keep claim source mappings. For example, like this. This matters because summarization can remove attribution. If a research sub-agent compresses five sources into one summary but drops the sources, the synthesis agent can no longer verify the claims. That is a reliability failure. For conflicting values, the agent should not randomly choose one. If the return policy says 30 days but a newer support memo says damaged item exceptions may be reviewed up to 45 days, the agent should preserve both sources, include publication or collection dates, and escalate if the decision affects money or policy. Temporal context matters. A 2024 policy.

**3:41 → 4:26**

2026 memo may not be a contradiction. The newer source may supersede the older one. The system should also render different content types appropriately. Financial comparisons may work best as tables. Policy reasoning may work best as structured bullets. Customer replies should be clear prose. Technical review findings should include file paths, severity, and suggested fixes. Now let's map ShopAssist to the five exam domains. Domain 1 is agentic architecture and orchestration. ShopAssist uses an agentic loop, tool calls, handoffs, subagents where useful, and deterministic enforcement for critical steps like customer verification before refunds. Domain 2 is tool design and

**4:26 → 5:11**

integration. ShopAssist has tools like GetCustomer, LookupOrder, CheckPolicy, ProcessRefund, and EscalatedToHuman, with clear boundaries and structured errors. Domain 3 is Cloud Code Configuration and Workflows. The project uses cloud.md, slash commands, skills, plan mode, direct execution, session management, and CI review. Domain 4 is prompt engineering and structured output. ShopAssist uses explicit criteria, few short examples, JSON schemas, validation, retry loops, and structured findings. Domain 5 is context management and reliability. Shop Assist preserves context, escalates safely, propagates errors, tracks provenance,

**5:11 → 5:57**

handles uncertainty and routes risky cases to human review. For the exam, remember the weights. Domain 1 is the largest. Domains 3 and 4 are also heavily represented. Domain 2 focuses on tools and MCP. Domain 5 has a smaller percentage, but it appears inside many scenario questions because reliability affects the whole architecture. Let's finish with one exam style scenario. A customer says, I need a refund. Your site said this was eligible, but now your bot says it is not. I want a human if this cannot be fixed. The order exists. The main policy says refunds are allowed within 30 days. The customer is at day 42. A newer internal memo says

**5:57 → 6:42**

The damaged item exceptions may be reviewed up to 45 days, but only by a human specialist. What is the best behavior? Option A. Deny the refund because the main policy says 30 days. Option B. Approve the refund because the newer memo says 45 days. Option C. Explain the conflict, preserve both sources, summarize the case, and escalate to a human specialist. Option D. Ask the model for its confidence score and proceed if confidence is above 80%. The correct answer is C. Option A ignores the newer source. Option B applies an exception without authority. Option D relies on self-reported confidence, which is not enough for business risk. Option C preserves provenance.

**6:42 → 7:07**

handles uncertainty, and escalates with useful context. This is the mindset the exam rewards. The final takeaway is simple. A reliable cloud system is not just a strong prompt. It is an architecture that knows when to act, when to ask, when to stop, and when to escalate. That is what we built with ShopAssist, and that is the mindset to bring into the certification
