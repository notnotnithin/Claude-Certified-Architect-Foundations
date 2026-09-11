---
hovernotes-transcript-of: doc_6b67e196-3b6e-4c80-bbd2-68e4e87d904a
hovernotes-transcript-version: 2
note: "[[08-Enforcement-And-Handoffs]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908987#overview"
updated: 2026-09-10T11:25:06.796Z
---

# 08-Enforcement-And-Handoffs — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So everything we have built so far has trusted Claude to make good decisions. It picks its own tools, it decides when to stop, and we have deliberately given it that freedom. But some rules are different. Some rules have to hold every single time. So this lecture is called Enforcement and Handoffs, and the subtitle sets the tone. Some rules can't be left to chance. So four things in this lecture. Number one, programmatic versus prompt, which is the core distinction. to.

**0:42 → 1:27**

when you need enforcement and how to decide. Number three, prerequisite gates. And number four, handoffs and escalation for when a human has to step in. Alright, so the first topic is programmatic versus prompt. And the subtitle gives you the choice in one line. Ask nicely or guarantee it in code. So these are your two ways of making Claude follow a rule and they are not remotely equal. So look at the first option and notice it comes up with a tick and a cross. Prompt guidance, you ask Claude to follow a rule. But it is probabilistic, which means it usually holds.

**1:27 → 2:13**

So sit with that word, usually. Most of the time, Claude will do exactly what you asked and honestly it will do it very well. But usually it is not the same thing as always. And for most of what your agent does, usually is perfectly fine. The trouble starts with a small number of rules where it simply is not. Now look at the other option which the slide sets against it. As a street versus programmatic and this one gets two ticks, code guarantees it. And it is deterministic which means it always holds. So this is not a request that Claude might follow. It is a wall. The rule sits outside the model.

**2:13 → 2:58**

So there is nothing there to slip past and no clever argument that can talk it around. And now here is the line to carry with you. Prompts give probable compliance and code keeps guaranteed compliance. Remember it. So please genuinely memorize that pairing because it is one of the most testable ideas in this entire domain. Probable versus guaranteed. And when you meet a question about a rule that must never break, that word guaranteed is what points you straight at code. Alright, now the second topic. When you need enforcement. And,

**2:58 → 3:43**

Subtitle gives you the test. If breaking the rule is unacceptable, enforce it. So look at the rule at the top, four rules that must hold 100%, and then the three examples underneath it. Identity checks before payments, refund limits, and safety and compliance gates. So notice what all three of those have in common. Every one of them protects against real damage, money living wrongly, a limit being breached, or somebody actually getting hurt. None of them is about the answer being nicely worded, or the tone being right. These are the things that must never happen, no matter how the conversation went,

**3:43 → 4:28**

Now here is a question you can genuinely use at work. Ask, what happens if Claude ignores this once? And if the answer is serious harm, then it's a code rule and not a prompt rule. So please carry that question around with you because it settles the argument quickly. Once is the key word. Not usually and not most of the time. Because if a single slip causes real damage, then probable compliance was never good enough. Alright, now the third topic, prerequisite gates. And the subtitle describes the mechanism. action until the condition is met.

**4:28 → 5:13**

So, we have agreed that some rules belong in code. This slide shows you the commonest shape that ticks. So, look at the rule at the top. No refund until identity is verified. And then the three points underneath it. A gate blocks an operation until a required step is done. It is enforced in code and not requested in a prompt. And the action literally can't run until the gate opens. So, notice how physical that is. This is not a polite reminder sitting in the prompt. The refund simply refuses to happen while identity is unverified.

**5:13 → 5:58**

And now here is the lovely part, the gate makes the order impossible to get wrong, because Claude can't skip ahead. So think of the barrier at a car park. You do not ask drivers nicely to pay before leaving. The barrier stays down until the ticket is paid, and then nobody has to remember the rule, because the rule is simply how the place works. And that is exactly what you have done to your refund flow. Claude does not have to remember the correct order, and it does not have to resist a persuasive customer. Even if it tried to jump straight to the refund, then the gate would simply not open.

**5:58 → 6:44**

Alright, now the fourth topic, handoffs and escalation. And the subtitle says when. When Claude should stop and call a human. So gate stop the wrong thing happening. But sometimes the right answer is that this case should not be automated at all. So look at the rule at the top. Escalate with a structured handoff summary. And then the three points underneath it. Too risky or unclear means escalate to a human. The summary carries the customer, the issue and what's been done. And also the recommended action. So notice that is four things going into that summary. Who it is, what is wrong, what has already happened and what you suggest doing.

**6:44 → 7:29**

And now here is why the structure matters so much. A good handoff means the human doesn't re-read everything, because they get the situation and a recommendation at a glance. So think about the cost of a lazy escalation. If you simply dump the whole conversation on somebody, then you have saved them nothing at all. They still have to read the whole thing and work out what is going on before they can lift a finger. Whereas a structured summary means they can act almost immediately. Alright, so let us pull this together. The key takeaways from this lecture, Enforcement and Handoffs.

**7:29 → 8:14**

lines. So number one, code versus prompt. Prompts give probable compliance and code gives guaranteed compliance. So remember, usually is not always and that gap is exactly where the trouble lives. When a rule genuinely cannot wait, the prompt is the wrong place for it. Now number two, gate the must-holds. Enforce 100% rules in code and use prerequisite gates. So remember the car park barrier. Nobody has to remember the rule because the rule is built into how the place works. And number three, escalate cleanly, hand risky cases to a human with a structured summary. So,

**8:14 → 8:37**

Remember, give them the situation and a recommendation, and not a transcript to wait through the customer, the issue, what has been done, and what you suggest next. Alright, in the next video, we look at Agent SDK hooks. So, with this, I'm going to end this one, and I will catch you in the next one.
