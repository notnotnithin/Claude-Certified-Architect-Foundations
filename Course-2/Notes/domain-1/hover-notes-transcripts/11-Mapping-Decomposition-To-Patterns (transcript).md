---
hovernotes-transcript-of: doc_58d87a96-1839-46ab-99ef-81077ba4dea7
hovernotes-transcript-version: 2
note: "[[11-Mapping-Decomposition-To-Patterns]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57909001#overview"
updated: 2026-09-10T12:09:50.587Z
---

# 11-Mapping-Decomposition-To-Patterns — Transcript

**0:00 → 0:43**

Alright everyone, welcome back. So, last lecture, we learned 3 ways to cut up a job, sequential, parallel and adaptive. But we stopped just short of the genuinely useful part, because once you know the shape of your split, that shape actually tells you which architecture to build. So this lecture is called Mapping Decomposition to Patterns, and the subtitle captures the whole idea. The right split points to the right pattern. So two things in this lecture, number 1, fixed vs dynamic and how that points to the architecture, and number 2, prompt chaining vs.

**0:43 → 1:28**

orchestrator workers, which are two names worth knowing properly. Alright, so the first topic is fixed vs dynamic and architecture. And the subtitle asks the question for us, do you know the steps or discover them? So everything on this slide follows from that one honest answer. So look at the first case, and it comes up with two ticks, fixed steps, known upfront, which points to a simple pipeline or a prompt chain. So notice why that fits. If you already know every step and the order they run in, then you do not need anything clever sitting on top.

**1:28 → 2:13**

need to run them in order and adding a coordinator there would be paying for decision making when there are no decisions left to make. Now look at the other case which the slide sets against it as a straight versus dynamic steps and this one also gets two ticks discovered as you go which points to a coordinator with subagents. So notice why you need more here somebody has to work out what comes next and that judgment can only be made in the moment once you see what the last step actually turned up and now here is the deciding question and it is a good one can you list the steps in advance yes

**2:13 → 2:59**

means a chain and no means an orchestrator. So please make that your habit because it settles the choice in seconds. And do answer it honestly because it is tempting to say yes when what you really mean is mostly. If there are real branches where the path depends on what you find then that is a no. Alright, now the second topic prompt chaining vs orchestrator workers and the subtitle tells you exactly why this slide exists. Two names the exam wants you to know. So look at the first name and it comes up with two ticks prompt chaining a fixed name

**2:59 → 3:44**

line of steps where the output becomes the input of the next one and it is simple and predictable. So notice that word predictable, you know before you run it exactly what will happen, which makes it easy to test and easy to debug. Because when something goes wrong, there was only ever one part it could have taken. Now look at the second name which the slide sets against it as a straight versus orchestrator workers and it also gets two ticks, a coordinator directing sub-agents and it is flexible and adaptive. Notice that this is our hub and spoke pattern from lecture 1.2 now wearing its formal name.

**3:44 → 4:29**

The coordinator is the orchestrator and the sub-agents are the workers. So the vocabulary is new but the machinery is exactly what we already built. And now here is the mapping to memorize and I mean word for word. Fixed known steps equals prompt chaining and a coordinator directing workers equals orchestrator workers. So please drill that pairing because exam questions often use precisely this vocabulary. And note that they may not say coordinator at all. They might say a lead agent or a manager agent. So listen for the shape and not only for the exact word. Alright.

**4:29 → 5:14**

pull this together. The key takeaways from this lecture, mapping to patterns in two lines. So number one, fix versus dynamic. Fix points to prompt chaining and dynamic points to orchestrator workers. So remember the shape of your split decides the architecture and not the other way around. You do not pick a pattern first and then bend the work to fit it. And number two, the test. Can you list the steps upfront? So remember that single question settles it and it is worth asking honestly every time because the cost of getting it wrong runs in both directions.

**5:14 → 5:36**

A chain on dynamic work simply breaks, and an orchestrator on fixed work is expensive complexity you never needed. Alright, in the next video, we look at passes and picking the fit. So with this, I am going to end this one and I will catch you in the next one.
