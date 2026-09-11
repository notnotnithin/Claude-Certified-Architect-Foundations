---
hovernotes-transcript-of: doc_088abcca-bdb7-4c14-8559-40eda7e12f5f
hovernotes-transcript-version: 2
note: "[[07-Context-Passing-Between-Agents]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908983#overview"
updated: 2026-09-10T11:17:46.894Z
---

# 07-Context-Passing-Between-Agents — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So last lecture, we learned how to create a subagent. The task tool, the four fields and keeping its toolkit tight. But there is a catch waiting here that trips up almost everybody the first time. That fresh helper you just created knows absolutely nothing about what has happened so far. So this lecture is called context passing between agents. And the subtitle warns you. Subagents don't read your mind and you must tell them. So four things in this lecture. Number one, no automatic inheritance, which is the problem itself.

**0:42 → 1:26**

Number two, inject context explicitly. Number three, include complete findings. And number four, goals, not steps, which is about how much you should spell out. All right. So the first topic is no automatic inheritance. And the subtitle states it bluntly. A fresh subagent starts blank. So that word blank is doing a lot of work in that sentence. And we should take it seriously. So look at the rule at the top. Isolation cuts both ways. And then the three points underneath it. A subagent does not inherit a coordinator's conversation, nor another subagent's findings.

**1:26 → 2:11**

and it starts completely fresh. So notice that phrase cuts both ways because two lectures ago, we were celebrating isolated context. A clean workspace gives better work. Well, this is the other side of that same coin. Clean also means empty. Nothing at all carries across on its own. And that is by design, not by accident. And now here is the warning. The number one mistake is assuming a subagent already knows. And it doesn't. So please take that seriously because it really is the commonest bug in this whole pattern. In your head, the coordinator has just done a pile of research. So it feels obvious that the writing sub-agent would know about it.

**2:11 → 2:56**

But that helper was created seconds ago and it has never seen a word of it. And notice how this fails. Because it is sneaky. The writer does not throw an error and nothing turns red. It just quietly writes something generic or invents a few details because it had a nothing real to work from. So you only spot it when the output looks oddly thin. Alright, now the second topic, inject context explicitly and the subtitle tells you what to do about it. Put everything the subagent needs into its prompt. So look at the rule at the top. The prompt is the handoff. And then the three points underneath it. Absolutely.

**2:56 → 3:41**

include what the subagent needs in its prompt. That means the goal, the relevant facts, and any prior findings. And there's no shared memory to fall back on. So notice how complete that list is. Not just the task, but also the facts it will need and anything earlier helpers already discovered. And now here is the rule stated plainly. Whatever the subagent needs to know must be written into the prompt. So please notice that phrase, no shared memory. There is no hidden notice board where your agents quietly compare notes behind the scenes. If a fact is not in that prompt,

**3:41 → 4:27**

than for this subagent. That fact simply does not exist. So here is a useful test whenever you write one of these. Read the prompt back to yourself and ask honestly if I knew only this and nothing else at all, could I actually do the job? And if the answer is no, then something important is still missing. Alright, now the third topic include complete findings. And the subtitle says it in one line. Give the whole picture, not a vague summary. So we have agreed that everything must go in the prompt. This slide is about how much and in what shape. So look at the rule at the top.

**4:27 → 5:12**

the structured findings and then the three points underneath it. Pass complete prior findings and not a one-line summary. Use a structured format with clear sections and labels and shrink the context and the subagent's work suffers. So notice that middle point because it matters more than people expect. A wall of unlabeled text is genuinely hard to use whereas clear sections tell the subagent what each part is for. And now here is the whole idea in one image. Give the subagent the whole tidy picture and not a scribbled note. So think about handing work to a colleague while you go on holiday.

**5:12 → 5:57**

with label sections and they can carry on without you. A sticky note saying spoke to the client, it went fine and they are stuck the moment anything unexpected turns up. Alright, now the fourth topic, goals, not steps and the subtitle draws the line for you. Set the destination and not the turn by turn directions. So having said, write everything down. This slide draws the boundary. There is one thing you should not spell out. So, look at the rule at the top. Trust the subagent with the what and then the three points underneath it. Tell the subagent the goal and quality

**5:57 → 6:42**

bar. So that sounds like find the top three, which sources and not a step-by-step script. And let it use its own loop to figure out the how. So notice the difference between those two instructions. One tells you where to arrive and how good it has to be. The other tries to spell out every single move. And now here is why that works. The sub-agent has its own agentic loop. So trust it with the what and not a rigid how. So this brings us right back to our very first lecture. That helper can perceive, reason, act and observe exactly like any other agent. So if you If you script every move for it,

**6:42 → 7:27**

you have thrown away the entire reason you spawned an agent rather than writing a function. Alright, so let us pull this together. The key takeaways from this lecture, context passing in the three lines. So, number one, no inheritance. Subagents start blank and they don't inherit context. So, remember, isolation cuts both ways. The clean workspace you want it arrives completely empty and never assume that a helper already knows something. Now, number two, inject explicitly. Put everything they need in the prompt and pass complete structured findings. So

**7:27 → 8:10**

Remember that colleague going on holiday, you leave them a label folder and not a scribble note, because there is no shared memory for them to fall back on. And number three, goals, not steps. Give a goal and quality bar and not a rigid script. So remember, you spawned an agent precisely because it can work things out for itself. So tell it where to get to and how good the answer needs to be. And then let it find its own way there. Alright, in the next video, we look at enforcement and handoffs. So with this, I'm going to end this one and I will catch you in the next one.
