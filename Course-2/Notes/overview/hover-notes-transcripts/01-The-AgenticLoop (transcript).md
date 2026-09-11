---
hovernotes-transcript-of: doc_84c048d0-e21c-4ea2-a0a4-37ac02ce9092
hovernotes-transcript-version: 2
note: "[[01-The-AgenticLoop]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908961#overview"
updated: 2026-09-10T09:14:26.343Z
---

# 01-The-AgenticLoop — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So we are now starting domain 1. And this domain is about agentic architecture and orchestration. And the very first lecture is called the agentic loop. What it is and why. So this one asks the question that everything else in this course is built on top of. And the subtitle says it in one line. What turns a chatbot into an agent? So three things in this lecture. Number one, one call versus a loop. Number two, the four steps. And number three, the stop reason, which is the signal that keeps you in the loop.

**0:42 → 1:28**

the whole thing turning. Slide 2. Alright. So the first topic is one call versus a loop and the subtitle puts it in a single line. A chatbot answers once and agent keeps going. So look at the first side. This is the chatbot. You ask, it replies and it is done and it can only talk. So think about what that really means. Picture phoning a friend who has read every company handbook ever written. She knows the refund policy by heart, but she is sitting in a room with no computer and no way to check anything.

**1:28 → 2:13**

working days and that is genuinely useful but she cannot open your actual order. Now look at the other side. This is the agent. It uses tools, it sees the result and it keeps going and it can act until the job is finished. So walk into that room and hand your friend a laptop. Now she does not have to guess. She looks up your real order. She sees it was delivered and she checks whether a refund was ever issued and that laptop in our world is what we call a tool which simply means an action that we allow Claude to take out in the real world. And now here is the line that this whole slide is

**2:13 → 2:58**

around the loop is the difference without it Claude can only talk and with it Claude can act. So please notice what did not change in that little story. Not her intelligence. She was exactly as sharp in both rooms. What changed was whether she could reach out and check something real before answering you. Now the second topic the four steps of the loop and the subtitle names all four of them perceive then reason then act then observe and then repeat. So look at all four steps together on the screen perceive which is

**2:58 → 3:43**

request, then reason, which is decide what to do, then act, which is call a tool, and then observe, which is read the result, and look. So rather than define those one by one, let us just watch an agent actually do that, and I will use a customer who is asking, where is my refund? So the agent reads her question, and that is perceived. Then it thinks, I cannot answer this without her order, so I will look it up, and that is reason. Then it calls the order, lookup tool, and that is act, and back comes the answer delivered three weeks ago, and no refund issued. So it reads that, and that is observe. and

**3:43 → 4:28**

notice what it does not do. It does not stop there. It goes straight back to the beginning and starts again. And now here is the key point on this slide. Each loop, Claude gets new information from the tool. So its next decision beats a blind guess. So please notice what the second lap looks like. Our agent now knows that no refund was ever issued. So the next question almost asks itself. Is this customer even entitled to one? And that question could not have been written in advance. It came out of what the first lookup actually written. All right. Now the third topic.

**4:28 → 5:13**

and how it drives the loop. And the subtitle tells you its job in one line. One field tells you keep going or stop. And before we look at it, here is a question worth sitting with. If this loop keeps going round and round, what actually tells it to stop? So look at the rule at the top. Tool use means loop and end turn means stop. And then the three points underneath it. Every reply carries a stop reason. Tool use means run the tool, feed the result back and loop. And end turn means clawed is done. So you stop. Now this next bit is where people usually get stuck. So let us go slowly.

**5:13 → 5:59**

Every time Claude replies, that reply comes back with a few labels attached to it, and a field simply means one of those labels. So the stop reason is the label that tells you why Claude stopped talking. And now here is the whole loop written as one rule. While the stop reason is tool use, you keep looping. And when it is end turn, you stop. So notice the answer to the question I asked you a moment ago. Claude decides, not your code. And that is exactly why capping the agent at three tool calls sounds careful, but quietly breaks things. Because our refund agent needs the order, then the policy, then the code.

**5:59 → 6:44**

record and her actual answer would have come on the fourth all right so let us pull all of this together the key takeaways from this lecture the agentic loop in three lines so number one loop equals action the loop is what makes an agent act and not just talk so remember our friend with the laptop same mind same knowledge but a completely different reach once she could go and check something now number two four steps perceive then reason then act then observe and repeat so keep that cycle in your head because every agent you ever built is the

**6:44 → 7:29**

it underneath and each lap begins better informed than the one before it. And number three, the stop reason drives it. Tool use equals loop and end turn equals stop. So remember the model tells you when the work is finished. Your job is to listen to that signal and not to gas at it with a counter. So notice how much of this lecture really comes down to one idea. A chatbot produces words. An agent produces words, looks at what happened and then decides what to do next. And that single difference, the going round again, is what the entire rest of this domain is built on. Alright, in the next video

**7:29 → 7:49**

we watch a real loop run from start to finish. That means seeing how you feed results back into the conversation and then walking through a full work trace of that refund question. So with this, I'm going to end this one and I will catch you in the next.
