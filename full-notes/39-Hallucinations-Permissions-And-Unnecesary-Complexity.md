---
title: "Hallucinations, Permissions, and Unnecessary Complexity — Full Notes"
description: Combined slide notes + transcript from the Gen AI Revolution Podcast segment on designing around hallucinations, limiting permissions, and avoiding over-engineered agent architectures.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57766027#overview
created: "2026-09-07"
tags:
  - hover-notes
  - udemy
  - full-notes
slide-note: "[[39-Hallucinations-Permissions-And-Unnecesary-Complexity]]"
transcript: "[[hover-notes-transcripts/39-Hallucinations-Permissions-And-Unnecesary-Complexity (transcript)|Transcript]]"
---

# Hallucinations, Permissions, and Unnecessary Complexity

> This is another short segment of the bonus **Gen AI Revolution Podcast**, hosted by **Anton Voroniuk** (SkillsBooster Academy) interviewing **Anton Pavelko**, a Claude Certified Architect. As with the rest of this podcast segment (lectures 33–44), the speakers' names and the podcast branding appear **only in the video-call screenshots** — the on-screen name captions and the "Gen AI Revolution Podcast with Anton Voroniuk" logo. Neither the transcript nor the slide-note bullets ever name the speakers.
>
> The lecture covers three compact, related risk areas an architect has to manage at once: **hallucinations**, **permissions**, and **unnecessary complexity**.

![00:00:00](../hover-notes-images/screenshot-01M1VC917WF27JJFTJSM2RT9JB.png)

---

## 1. Design around hallucinations, don't try to eliminate them

- **[Architectural Approach]** The goal is not to eliminate hallucinations — it's to **design the system around them**.
  - LLMs can produce incorrect answers regardless of how good the prompt is.
  - Systems must be built ready to handle incorrect responses, not built assuming they won't happen.
- **[Security]** It is critical to **limit permissions** to mitigate the risk of an incorrect response causing real damage.

> **Transcript color:** "You should design your system around them because LLM can produce some incorrect answers. And even if you have a great prompt, you cannot rely on LLM response. And you have to be ready to handle incorrect responses. And it's very important to limit permissions."

![Two-person video call: Anton Voroniuk (SkillsBooster Academy) and Anton Pavelko, "Gen AI Revolution Podcast" branding top right](../hover-notes-images/screenshot-01M1VC917WFGP11TMFHPHNMMQA.png)

---

## 2. Mitigating Hallucination Risks

- **[Risk Management]** Avoid allowing LLMs to perform risky operations without high confidence.
  - Examples given: processing refunds, financial transactions.
  - Use **human review** to validate sensitive actions before they are finalized.
- **[Complexity Control]** Do not use AI if a deterministic software solution can solve the problem.
  - Adding AI to a system where it isn't needed can actually make the system worse.
  - Avoid the mistake of over-orchestrating.
- **[Simplifying Agentic Approaches]** Prefer simplicity over complex multi-agent systems.
  - If a difficult multi-agent architecture can be replaced by a single function making several requests to an LLM, choose the simpler method.

> **Transcript color:** "if deterministic software solves the problem, use it. So there's no need to use AI everywhere and orchestration. It's a big mistake, yeah. The agentic approach, if you can replace that difficult multi-agent system just with one function and several requests to LLM... it should be as simple as possible."

**[Transcript inconsistency, slide wins]** The raw transcript reads "**allow** some risky operations like refunds, some transactions before you 100% sure that it's allowed" — missing the negation. This is a transcript chunk-boundary artifact: the previous chunk ends mid-sentence on "it's very important to limit permissions," and the following chunk drops the implied "avoid/don't." The slide note's phrasing — "**Avoid allowing** LLMs to perform risky operations without high confidence" — is the correct, coherent version and is used above.

![Two-person video call, same frame — Pavelko mid-sentence](../hover-notes-images/screenshot-01M1VC9Z909R1Q735VZV4ZWX10.png)

---

## Risk summary

| Risk | What it looks like | Mitigation |
|---|---|---|
| **Hallucinations** | LLM gives a confidently wrong answer — even with a well-engineered prompt | Design the system to expect and handle bad output; never treat model output as ground truth |
| **Unchecked permissions** | The model attempts a risky, high-stakes action (refund, financial transaction) without full confidence it's warranted | Limit what the model is permitted to do; require human review before finalizing sensitive actions |
| **Unnecessary complexity** | A multi-agent architecture is adopted for a problem a single deterministic function (or one function making a few LLM calls) could solve | Default to the simplest solution that works; don't add AI or agent orchestration where it isn't needed |

---

## 3. Complexity vs. Agents

- **[Core Philosophy]** Not anti-agent, but **anti-unnecessary complexity**.
  - Avoid adopting complex architectures simply because they are new or trendy.
  - Prioritize the simplest solution that effectively solves the problem.

The podcast host presses on this point with a direct, practical question — his own company's over-engineering:

> **Transcript color (host):** "Our company is currently over-engineering AI agents."
>
> **Transcript color (Pavelko):** "I see that, yes. But you are deeper in the topic... sometimes people want to learn something and they want to apply their knowledge even in places that it's not necessary. And I saw some systems like multi-agent systems that can be replaced just by one function."

Asked directly which AI architecture he'd "ban" if he could, given how it's being blindly adopted:

> **Transcript color:** "If you could ban one AI architecture that companies are blindly adopted in 2026, what would it be? — Multi-agent systems for everything... I'm not anti-agent, no. Anti-unnecessary complexity."

![Two-person video call, same frame — Voroniuk smiling, Pavelko mid-sentence with eyes closed](../hover-notes-images/screenshot-01M1VCB61RRFB1C7G42911FVB3.png)

---

## Summary

- **Hallucinations** are not a solvable-once problem — architect the system to expect and gracefully handle wrong answers, regardless of prompt quality.
- **Permissions** are the practical backstop: don't let the model perform risky/financial operations without high confidence, and keep a human in the loop for sensitive actions before they're finalized.
- **Unnecessary complexity** — specifically over-adopted multi-agent architectures — is called out as the single AI architecture pattern most worth banning in 2026. The stance is explicitly *not* anti-agent; it's anti-complexity-for-its-own-sake. If one function with a few LLM calls solves the problem, use that instead of a multi-agent system.

**Duplicate/near-duplicate screenshots noted but not kept:** two additional talking-head frames at 00:02:11 and 00:02:16 (`screenshot-01M1VCB15E79Z3BK2G95R7KJD3.png`) were visually identical to the 00:01:27 frame kept above (same pose, same expressions) — dropped per the dedup pass. The lecture's closing frame reused the plain title card (`screenshot-01M1VCB15EX3JBEX018SP9FT32.png`, no play-button overlay) — omitted here since it's a near-duplicate of the intro title card already shown at the top.

---

*Sources: [slide notes](../39-Hallucinations-Permissions-And-Unnecesary-Complexity.md) · [[hover-notes-transcripts/39-Hallucinations-Permissions-And-Unnecesary-Complexity (transcript)|full transcript]]*
