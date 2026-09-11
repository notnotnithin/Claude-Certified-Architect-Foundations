---
hovernotes-transcript-of: doc_3a6cd5cf-c9ac-4a3d-bf1f-4295754b3014
hovernotes-transcript-version: 2
note: "[[03-Model-Driven-And-The-Anti-Patterns]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908967#overview"
updated: 2026-09-10T10:38:56.322Z
---

# 03-Model-Driven-And-The-Anti-Patterns — Transcript

**0:00 → 0:40**

Alright everyone, welcome back. So in the last lecture, we watched a real loop run. Claude looked up the order, it read what came back and it chose its next tool from that result. So this lecture is called Model Driven and the Anti-Patterns and the subtitle tells you the plan. Let Claude steer and avoid the classic mistakes. So two things in this lecture. Number one, Model Driven vs Hard Coded which is really a question about who is in charge And number two, the three anti-patterns, which are the

**0:40 → 1:25**

ways that people break a loop in real systems. Alright, so the first topic is model-driven vs. hard-coded. And the subtitle gives you the advice in one line. Let Claude decide and don't script every branch. So this is about who chooses the next step. Is it Claude reading the situation or is it you writing it out in advance? So look at the first side. This is model-driven and it has two ticks against it. Claude picks the next tool from context and it is flexible because it handles surprises. So think of a sat nav in your car.

**1:25 → 2:10**

You tell it where you want to go and then it works out the turns as it drives. And if a road is closed, it simply finds another way without you doing anything at all. That is Claude, picking each tool from what it has just learned. Now look at the other side. This is hard-coded and the slide sets it against the first one as a straight versus and it has two crosses. You write every if and else branch and it is brittle because it breaks on the unforeseen. So that is a printed sheet of directions. Turn left, then right, then left and you have arrived. which works beautifully right up until one

**2:10 → 2:56**

those roads is shut. And then that sheet of paper has absolutely nothing to offer you. It cannot think, it can only repeat what somebody wrote down earlier. And now here is a note that matters for your exam. The exam favors model-driven loops for anything non-trivial, because hard-poured trees cannot handle cases you did not foresee. So please keep that leaning in mind because it is tested directly. For a tiny fixed job, a script is genuinely fine and nobody will mark you down for it. But the moment a task has any real variety in it, the expected answer is to let Claude decide.

**2:56 → 3:41**

Now the second topic, the three anti-patterns, and the subtitle is blunt about what these are. Three ways to break your loop. So an anti-pattern simply means a solution that looks reasonable, but which reliably causes trouble. And each of these three has broken real systems. So look at the first one, ignoring the stop reason, and then you never know when to stop. So remember from lecture one that Claude tells you every single turn whether the job is finished. So if you ignore that signal, you are simply guessing. And it is like asking a colleague to check something and then walking off before they have answered. Whatever they found, you will never hear it.

**3:41 → 4:26**

Now the second one, never stopping, because no end condition means an infinite loop. So notice this is the opposite failure. Here, nothing ever tells the loop to halt. So it just keeps calling tools round and round. And that is a tap left running overnight. Nothing dramatic happens and nothing crashes. But every single call is quietly costing you real money the entire time. And the third one, not feeding results back. And then Claude flies blind. So this is our mistake from last lecture. The tool runs, but the answer never reaches Claude. And honestly, this one is the national

**4:26 → 5:11**

of the three because nothing crashes. The agent looks busy, it looks like it is working hard, and it simply never arrives anywhere. But now look at the warning underneath, these three break loops in production, and they are common wrong answer choices on the exam. So please learn all three by name because they earn their keep twice over. In real systems, these are the bugs that actually take agents down, and in your exam, they are the tempting options that are sitting there waiting for you. Alright, so let us pull this together, the key takeaways from this lecture.

**5:11 → 5:56**

finishing the loop in two lines. So number one, prefer model driven. Claude chooses each tool from context. So remember the set now, you set the destination and Claude works out the turns one at a time. And that is exactly what lets it cope when something unexpected turns up along the way, which in real systems is most days. And number two, avoid the three traps, ignoring the stop reason, infinite loops and not returning results. So remember all three of those are failures in the plumbing that you built around the model. Not one of them is Claude getting something wrong.

**5:56 → 6:25**

Which is good news because it means all three are entirely in your hands to fix. Alright, in the next video, we move on from a single agent and ask what happens when one agent is not enough. That means looking at why a big job overwhelms one agent, then hub and spoke, and then isolated context, and when you should actually use it. So with this, I'm going to end this one, and I will catch you in the next one.
