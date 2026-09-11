---
hovernotes-transcript-of: doc_6199c5e3-35c6-4821-9b6b-40a6def0a1d9
hovernotes-transcript-version: 2
note: "[[04-Coordinator-Subagent-The-Pattern]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908971#overview"
updated: 2026-09-10T10:48:34.752Z
---

# 04-Coordinator-Subagent-The-Pattern — Transcript

**0:00 → 0:43**

Alright everyone, welcome back. So across the last three lectures, we built the Argentic Loop and we now have one agent that can loop away calling tools until a job is done and for plenty of tasks that is genuinely enough. So this lecture is called Coordinator and Subagent the Pattern and the subtitle captures it, one agent in charge and many doing the work. So three things in this lecture. Number one, why one agent isn't enough once a job gets large. to hub and spoke which is the shape this pattern ticks

**0:43 → 1:28**

And number three, isolated context, and when you should actually reach for all of this. Alright, so the first topic is why one agent isn't enough. And the subtitle names the problem for us. Big many part jobs overwhelm a single agent. So the question here is simply, what happens when the work grows beyond what one agent can hold in its head? So look at the first site, and notice it comes up with crosses against it. One agent, everything. Research plus analysis plus writing all at once, and a cluttered context that loses focus. So picture a restaurant kitchen with one cook. He

**1:28 → 2:13**

making the starters and the main courses and the desserts all at the same time. He is skilled and he knows every one of those dishes properly. But things start slipping, simply because there is too much on his bench at once. Nothing fails dramatically. The food just quietly gets worse. Now look at the other side, which the slide sets against it, as a straight versus. Split across specialists. Each helper handles one part, and focused and sharp. So that is a proper kitchen brigade. One station does starters, another does mains, another does desserts. each cook has a clean

**2:13 → 2:58**

with only the ingredients for their own dish sitting in front of them. Same people, same skills. But now nobody is juggling three jobs at once. And now here is the idea that this whole slide rests on. More work crammed into one context equals worse results. And splitting keeps each agent focused. So please notice what is really going wrong in that first picture. It is not that Claude is not clever enough. It is that the research notes and the half-finished analysis and the draft text are all piled into one place and things get lost in the pile. Alright.

**2:58 → 3:43**

The second topic, hub and spoke and the subtitle tells you the shape of it in one line. Everything flows through the coordinator. So if we are splitting work across helpers, then something has to sit in the middle and hold it all together. So look at the picture that comes up. There is a research subagent, an analysis subagent and a writing subagent. And then sitting right in the middle of them, the coordinator. So notice the shape that makes. It is a wheel. The coordinator is the hub at the center. And each subagent is a spoke connected only to that middle and not to each other. And now here is the rule that makes this work. Subagents don't

**3:43 → 4:29**

talk to each other, they report to the coordinator, and one hub means one place to see everything and to handle errors. So, that is your head chef standing at the pass. The starter station does not shout across to the desert station. Everything comes back to one person who knows what the finished plate should look like and who spots it when something is missing. Alright, now the third topic, isolated context and when to use it, and the subtitle says it plainly. Each subagent gets a clean, focused workspace. So, this is where we find out what the real prices and just as importantly when you should leave this pattern

**4:29 → 5:14**

So look at the rule at the top, a clean workspace equals better work. And then the three points underneath. Each subagent sees only its task and not the whole job. You use the pattern when a task has several separable parts. And simple single threaded jobs don't need a coordinator. So notice that last one carefully because it is the slide warning you off. If your job is one straight line of work, then adding a coordinator just gives you more parts that can break. And now here is the benefit stated directly. Isolated context is the benefit because a subagent focused on one job does

**5:14 → 5:59**

job better. So please pay attention to that word separable. Ask yourself can this job genuinely be cut into pieces that stand on their own? Writing a market report splits nicely into research then analysis then writing but editing a single paragraph does not. There is simply nothing there to split. Alright so let us pull this together. The key takeaways from this lecture the orchestration pattern in three lines. So number one split the work big multi-part jobs go to specialist sub-agents. So remember the kitchen one cook doing everything gets slower ends lobbying.
