---
hovernotes-transcript-of: doc_666d8d08-66a3-45a9-9993-857cd86049d8
hovernotes-transcript-version: 2
note: "[[38-From-Impressive-Demo-To-Production-System]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57766023#overview"
updated: 2026-09-06T12:40:06.291Z
---

# 38-From-Impressive-Demo-To-Production-System — Transcript

**0:00 → 0:41**

Let's talk a little bit about misconceptions. What is the biggest misconception software engineers bring from traditional software architecture in the AI? I believe it's deterministic mindset because in the AI architecture, we have, again, the probabilistic behavior and we never know what LLM can return. And we have to, like, the approach is different. We have to think about permissions and we should also think, like, not only what the model can do but also what

**0:41 → 1:26**

that model should allow it to do, right? And when we need the human in the loop, so we do not allow some risky operations like by mistake, like refunds, et cetera. So I would say it's like another mindset and deterministic mindset, like it's a different approach. It was also about the mistakes. The question of what are the biggest architectural mistakes you see when a team takes an impressive AI demo and tries to turn it into a production system? Well, good demo can prove that the model can do something, right? But if you need to produce, if you need to build production-ready

**1:26 → 2:12**

So in this case, you need to understand what happens when it fails. Let's move to the next question. Yeah, and this is the most important question, and this is the most time-consuming part. Can you describe the situation when AI prototype looked impressive but completely failed when you started thinking about production? The common example, like the prototype works perfectly when we have clean context, well-defined tasks, but in production, users provide some incomplete inputs, tool fails, like we have some issues with permissions, etc. So it's always about

**2:12 → 2:56**

be ready to anything, right? For example, you build system AI assistant for which should process some customer requests, right? But that customer decided to ask your three different questions. So at the same time, the customer ask you, hey, can you please do refund? Then also please check this order. And also, you know, I saw that new product, what price of it, right? And you have to be ready for any kind of situation like that. So instead of one request, customer ask it to you all three requests, right? And they have to be ready and your system have to be ready to process all of them. So this is like what this AI architecture is.
