---
hovernotes-transcript-of: doc_9cfbcd9d-2346-40a9-8ea4-dae7e45f213d
hovernotes-transcript-version: 2
note: "[[05-Orchestration-In-Practice]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908975#overview"
updated: 2026-09-10T10:56:12.126Z
---

# 05-Orchestration-In-Practice — Transcript

**0:00 → 0:35**

Alright everyone, welcome back. So last lecture we met the pattern itself, one coordinator sitting at the hub and specialist sub-agents arrange around it. But we never really asked what that coordinator spends its day doing. So this lecture is called Orchestration in Practice and the subtitle sets the question for us, what the coordinator actually does. So four things in this lecture. Number one, the coordinator's jobs. to sequential versus parallel.

**0:35 → 1:20**

Number 3, Iterative Refinement And Number 4, the Narrow Decomposition Trap Which is the mistake to watch for Alright, so the first topic is the coordinator's jobs And the subtitle lists all 4 of them Root, Manage, Select, Synthesize So we are going to take these one at a time Because each one is a genuinely different piece of work So look at the first job, Route Which means, send work to the right sub-agent So that is your head chef handing the fish to the fish station And the pastry to the pastry section Somebody has to decide which pair of hands

**1:20 → 2:06**

each piece of work belongs to. And notice that this is a judgment made fresh each time based on what the job actually needs. Now the second job, manage errors, which means decide what to do if one fails. So when a subagent comes back empty or simply breaks, the coordinator is the one who has to react. It might try again. It might take a different route entirely. But the decision sits with the hub. And this is exactly why we said last lecture that one hub means one place to catch a failure. Now the third job, select, which means choose which subagents to run.

**2:06 → 2:51**

So notice that this is subtly different from routing. Routing is about where a piece of work goes. Selecting is deciding which helpers are needed at all. Because not every job needs every specialist you happen to have. A simple request might only wake up one station and leave the rest untouched. And the fourth job, synthesize, which means combine results into one answer. So all those separate pieces come back from their stations and somebody has to turn them into a single coherent plate. That actually makes sense to the person who ordered it. Three good components arriving separately are not yet an answer.

**2:51 → 3:36**

to assemble them and now here is the line that ties all four together the coordinator is a manager not a worker because it decides and combines and it doesn't do the task itself so please hold on to that because it is easy to get wrong the head chef at the pass is not working the moment your coordinator starts doing the research itself you have thrown away the focus that made this pattern worth using all right now the second topic sequential versus parallel and the subtitle gives you the choice in one line, one after another or all.

**3:36 → 4:21**

So once you have several helpers available, you have to decide how they run and that decision is not a matter of taste. So look at the first option and it comes up with ticks, sequential steps in order where each one feeds the next. And the example given is research then analyze then write. So notice why that order cannot be shuffled. You cannot analyze material you have not gathered yet and you cannot write up an analysis that does not exist. The work itself has a shape. Now look at the other option which the slide sets against it as a straight versus parallel independent sub-agents at the same time. at the same time.

**4:21 → 5:06**

and faster. So that is three cooks making three different starters at once. Nobody is waiting on anybody. And three dishes finish in roughly the time it would take one. And now here is the rule for choosing between them. Parallel when parts don't depend on each other and sequential when each part needs the previous result. So please notice that you do not choose by what sounds quicker. You look at the work and you ask one question. Does this piece need the answer from that piece? If yes, it is sequential. And if no, run them together.

**5:06 → 5:51**

Third topic, Iterative Refinement, and the subtitle describes it neatly. The coordinator can send work back for another pass. So this is the difference between a coordinator that simply collects and one that actually takes responsibility for the quality of what it hands over. So look at the rule at the top. A quality loop, not a one shot. And then the three points underneath. After synthesizing, the coordinator judges the result. Not good enough, then it redelegates for another round. So the cycle runs, delegate, then synthesize, then check, and then maybe delegate again. notice that checking step.

**5:51 → 6:37**

because that is what turns this into a loop at all. And now, here is the point stated simply. A good coordinator checks the result and asks for more if it falls short. So that is your head chef tasting the sauce before the plate ever leaves the kitchen. And if it is not right, it goes straight back to the station. Notice how much this echoes the agentic loop itself from our very first lecture. You do something, you look at the result, and then you decide whether to go round again. Alright, now the fourth topic, the narrow decomposition trap, and the subtitle

**5:59 → 6:44**

while a brigade with clean stations keeps every single disc sharp. And that is the whole reason we split in the first place. Now number two, hub and spoke, everything flows through the coordinator. So remember, the spokes never talk to each other and that is deliberate. One hub means one place where you can see the whole job and one place to catch a failure. And number three, isolated context, use it when parts are separable. So remember to ask that question honestly before you reach for this pattern. Because a simple single threaded job is genuinely better off with one agent and adding a

**6:37 → 7:22**

is a warning. Don't shrink the question when you split it. So splitting work is powerful and we have spent two lectures on why, but there is one way to split badly and it is worth knowing by name. So look at the rule at the top. The pieces must add up to the whole and then the three points underneath splitting too narrowly loses part of the request. So somebody asked you to research the creative industries and you spawn only a visual arts subagent which then misses music, film, design and more. So notice what actually went wrong there. Nothing failed and nobody threw an error. It is as if somebody asked you to

**6:44 → 7:00**

to it buys you nothing at all. Alright, in the next video, we look at orchestration in practice. So with this, I'm going to end this one and I will catch you in the next one.

**7:22 → 8:07**

or a seafood menu and you came back with an excellent prawn dish. Genuinely good work, but it is not what was asked for. And now here is the warning stated properly. When you decompose, the pieces must still add up to the whole question, or you will answer a smaller one. So please take this seriously because it is a quiet failure. That visual arts research might be excellent, and the answer comes back confident and well written. It is simply an answer to a much smaller question than the one you were actually asked. Alright, so let us pull this together. The key takeaways from this lecture.

**8:07 → 8:52**

orchestration in practice in three lines. So number one, four jobs, route, manage errors, select and synthesize. So remember the head chef at the pass, deciding, checking and combining, but never actually cooking the dish himself. The moment your coordinator starts doing the work, the pattern stops paying for itself. Now number two, parallel or sequential. Independent goes parallel, dependent goes sequential and you refine iteratively. So remember, the dependency decides that for you and not your preference for speed. Ask whether one piece needs the answer from another and the shape

**8:52 → 9:29**

the work will tell you. And number three, don't narrow. Don't decompose so narrowly that you lose part of the question. So remember to check your pieces against the original request because a confident answer to a smaller question is still the wrong answer. And it is the hardest kind to spot precisely because it reads so well. Alright, in the next video we look at spawning sub-agents. So with this I am going to end this one and I will catch you in the next one.
