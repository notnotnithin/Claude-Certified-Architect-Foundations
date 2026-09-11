---
hovernotes-transcript-of: doc_c00c67e6-97db-4dcc-b263-56cb7b830c9b
hovernotes-transcript-version: 2
note: "[[04-Path-Mode-Vs-Direct-Execution]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57479751#overview"
updated: 2026-09-10T15:42:57.838Z
---

# 04-Path-Mode-Vs-Direct-Execution — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So for the last few lectures, we have been configuring Cloud Code, its memory, its commands and its rules. Now we shift to how you actually work with it day to day. And the very first choice is this. Do you just dive straight in or do you plan first? This is plan mode versus direct execution. Measure twice and cut once. So six things in this lecture. Number one, two ways to work. Number two, what plan mode is. Number three, how to trigger it. Number four, when to use it.

**0:42 → 1:27**

5 the explore sub-agent and number 6 the plan loop. Alright, so the first topic, two ways to work and the subtitle draws the line. Is it a quick errand or a project that needs a plan? So look at the two ways. On one side, direct that is for a small obvious change, you just do it. On the other side, plan mode that is for a big or a risky change. You think first and then you act. So notice the honest split here. Not everything deserves a plan. If the change is tiny and obvious then planning it would just slow you down, but if it is

**1:27 → 2:12**

or risky, then a little thinking first saves you a lot of pain later. Now here is the picture for it. It is like a carpenter. Measure twice, cut once. So cheap changes don't need a plan, but expensive mistakes do. So think about that carpenter for a second. Measuring twice costs a few seconds, but cutting the wood wrong wastes the whole plank. So planning is measuring. You spend a little time up front precisely because the mistake, if you make it, would be expensive to undo. Alright, so the second topic, what plan mode actually is, and the subtitle is the key to the whole thing. It is

**2:12 → 2:57**

only cloud plans but it can't change anything yet so look at what happens in it cloud explores and writes a plan with no edits until you approve so cloud reads it searches and it drops a numbered plan but write and edit are blocked at the tool level so you review every change before it becomes real so please notice the safety in that cloud can look at everything and think hard and lay out exactly what it intends to do but it cannot touch a single file until you have seen the plan and said Yes, now here is the crucial point, so do not miss it.

**2:57 → 3:44**

It is not a polite request. Plan mode blocks the file modifying tools until you say go. So notice that word blocks. This is not Claude being asked nicely to hold off. The write and edit tools are actually switched off at the tool level. So even if Claude wanted to edit a file, it simply could not. It is a hard guarantee and not a gentle suggestion. Alright, so the third topic, how to trigger it. And the subtitle keeps it simple. There are three ways in. So look at the three ways one by one. First press shift plus tab two times. cycles you through default then order

**3:44 → 4:29**

accept then plan second type slash plan right in the prompt and third start the whole session with the permission mode plan flag so notice that this suit different moments the keyboard shortcut is quick mid flow the slash command is nice and explicit and the startup flag launches you straight into plan mode from the very beginning now here is a small practical tip watch the status line it shows plan mode on and that permission mode plan flag also works with headless dash p runs So, notice two useful things there. First, you never have to guess whether plan

**4:29 → 5:14**

is active. The status line tells you plainly. And second, that startup flag works even in headless mode. So you can force planning in an automated run too. Alright, so the fourth topic, when to use it. And the subtitle gives you the rule of thumb. The bigger the blast radius, the more you plan. So look at the guidance. You plan for risk and you skip it for quick edits. So you plan for multi-file changes, refactors, migrations and anything touching out, payment or production. You also plan for unfamiliar repos and for ambiguous tasks

**5:14 → 5:59**

But you skip it for single file tweaks and quick edits. So notice the pattern. The moment a change is large or dangerous or you are unsure of the ground, you plan. And when it is small and clear and safe, you just do it. Now here is a striking little bit of maths that really makes the case. Small decisions compound. Imagine 20 unguided choices. Each one right, 80% of the time. Multiply that all out and the whole thing is right. Only about 1% of the time. So a plan catches the wrong turns before they cost you. So sit with that number.

**5:59 → 6:45**

surprising. 80% per step sounds pretty good. But across 20 steps, those small errors pile up and the odds of getting everything right just collapse. So planning is where you catch those wrong turns early while they are still cheap to fix. Alright, so the fifth topic, the explore sub-agent. And the subtitle gives you a lovely image, send a scout ahead and keep your own desk clean. So look at what it is. It is a read-only scout that reports back a summary. So it has read, grab and club only. It investigates, but

**6:45 → 7:30**

does not modify anything and it works in a separate context window so only the findings come back to your main session so notice the clever bit all the messy verbose work of digging through files happens somewhere else and what returns to you is just a tidy summary not the mountain of files it had to read to get there now here is a connection straight back to domain one this is the same isolation idea as the subagents in lectures 1.2 and 1.3 the exploration happens elsewhere and only the findings come back so you have seen this exact pattern before a specialist goes off does the heavy

**7:30 → 8:15**

on its own separate board and returns just the answer. So the Explorer subagent is that same idea put to work for planning. And here is why it matters so much. For a big project, it keeps a huge code basis file reads out of your main context. So your planning stays focused. So think about a giant repo for a moment. If Claude read 100 files straight into your main session, your context would be swamped and the planning would get muddy. So the Scout absorbs all of that reading elsewhere and hands you back only what matters. and your planning stays sharp.

**8:15 → 9:00**

and clear. Alright, so the sixth and final topic. The plan loop and the subtitle lays out the whole rhythm. Explore, then plan, then approve, then execute, then verify. So look at the five steps in order. First explore which is read only, then plan which is written down. Then approve where you say yes or you edit it. Then execute where the changes are actually made. And finally verify with your tests or a build. So notice the shape of it. Nothing is touched until step four. The first three steps are all looking, writing and

**9:00 → 9:45**

And only after you approve does anything real happen. And then you check that it worked. Now, here is the part that makes this so cheap and so safe. You can edit the plan before you approve it. Because fixing a plan is fast since nothing has been built yet. So, think about why that is such a good deal. If you spot a mistake in the plan, you just change a line of text. Nothing has been coded, so nothing has to be uncoded. So, you catch the problem at its cheapest possible moment on paper before a single file has changed. Alright, so the key takeaways from this

**9:45 → 10:30**

lecture plan mode in three lines number one read-only planning in plan mode cloud plans you approve and then it edits nothing changes until then number two trigger it for risk you use shift plus tab twice or slash plan or the permission mode plan flag and you use it for big or risky work and number three scout with explore the explore sub-agent investigates in a separate context and reports back so notice the single idea underneath this whole lecture for risky work you think first and you act second. So plan mode gives you a safe

**10:30 → 11:01**

Read only space where Claude explores and drafts a plan but cannot touch anything. You review it, you fix it if needed and only then you let it run. So the more expensive a mistake would be, the more that little bit of planning upfront is worth it. Measure twice and cut once. Alright, in the next video we'll look at Iterative Refinement. So with this, I am going to end this one and I will catch you in the next one.
