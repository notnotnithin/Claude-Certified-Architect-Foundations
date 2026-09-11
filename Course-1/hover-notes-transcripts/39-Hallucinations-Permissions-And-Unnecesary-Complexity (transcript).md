---
hovernotes-transcript-of: doc_df763486-399f-4e0c-b12e-38ebfd607a90
hovernotes-transcript-version: 2
note: "[[39-Hallucinations-Permissions-And-Unnecesary-Complexity]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57766027#overview"
updated: 2026-09-06T12:50:57.165Z
---

# 39-Hallucinations-Permissions-And-Unnecesary-Complexity — Transcript

**0:00 → 0:40**

As I remember a lot of questions in the exam, they are associated with hallucinations about how to manage them. So how should an architect think about hallucinations in a production system? Is the goal to eliminate them or to design around them? You should design your system around them because LLM can produce some incorrect answers. And even if you have a great prompt, you cannot rely on LLM response. And you have to be ready to handle incorrect responses. And it's very important to limit permissions.

**0:40 → 1:25**

allow some risky operations like refunds, some transactions before you 100% sure that it's allowed in this case. And of course, human review. What point does adding more AI actually make a system worse? You know, good question, because if deterministic software solves the problem, use it. So there's no need to use AI everywhere and orchestration. It's a big mistake, yeah. The agentic approach, if you can replace that difficult multi-agent system just with one one function and several requests to LLM.

**1:25 → 2:10**

so it should be as simple as possible and that was my next question our company is currently over-engineering AI agents I see that yes but you are deeper in the topic so you have your experience sometimes sometimes sometimes people want you know to learn something and they want to apply their knowledge even in places that it's not necessary and I saw some systems like multi-agent systems that can be replaced just by one function yeah but it is this if you could ban one AI architecture that companies are blindly adopted in 2026 what it would be? multi-agent systems for everything so yeah and I'm not

**2:10 → 2:17**

Anti-agent, no. Anti-unnecessary complexity.
