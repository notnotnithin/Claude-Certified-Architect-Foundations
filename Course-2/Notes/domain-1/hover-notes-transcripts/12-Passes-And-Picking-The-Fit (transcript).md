---
hovernotes-transcript-of: doc_19f8ab21-5713-4802-9295-ed8e01b3e172
hovernotes-transcript-version: 2
note: "[[12-Passes-And-Picking-The-Fit]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57909003#overview"
updated: 2026-09-10T12:15:59.593Z
---

# 12-Passes-And-Picking-The-Fit — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So over the last two lectures, we learned the decomposition strategies and then how each shape points to an architecture. Now we finished that thought in two ways. First with a real job that needs more than one shape at once and then with a single decision path that you can run on any task at all. So this lecture is called Passes and Picking the Fit and the subtitle says it, a real example and how to choose. So two things in this lecture. Number one, Perfile and Crossfile passes, which is our work example and number two, Picking the Fit, which is the design.

**0:42 → 1:27**

part itself and the most useful thing in this whole lecture. Alright, so the first topic is per file and cross file passes. And the subtitle introduces our example, a real decomposition example, reviewing code. So imagine somebody hands you a code base and asks you to review it properly. So look at the first pass and it comes up with two ticks. Per file pass, check each file on its own. And it is independent, which means it runs in parallel. So notice why that works. Checking file 1 does not need anything from file 2, so they can all go at the same time.

**1:27 → 2:12**

And with 50 files, that matters enormously because checking them one after another would be 50 times slower. Now look at the second pass, which the slide sets against it as a straight versus. Cross file pass and it also gets two ticks. Check how files fit together and it catches the connections. So notice why one pass alone is not enough. Looking at a single file, you can spot a mistake inside it. But you can never see that this file contradicts another one. So one file might define a value in one way and another file might expect it quite differently. Thank you.

**2:12 → 2:58**

and each of them read on its own looks perfectly fine. And now here is the shape of the answer. One decomposition, two levels, independent per file work in parallel and then a combining cross file pass. So think about what a per file review would report on a genuine cross file bug, nothing at all. Two files, each perfectly correct on its own and the system still broken because the mistake does not live inside either file. It lives between them. So notice that the combining pass is doing something the first pass simply cannot do no matter how carefully you run it.

**2:58 → 3:43**

Now the second topic, picking the fit and the subtitle promises something genuinely useful, one quick decision part for any task. So this is three questions asked in order and together they will settle almost anything. So look at the first question, can you list the steps? And if no, that means adaptive plus an orchestrator. So notice this comes first deliberately because if you cannot even name the steps, then no fixed arrangement is going to survive contact with the work. You need something that can decide as it goes. And that as we learned last lecture is an orchestrator running adaptive decomposition.

**3:43 → 4:28**

Now the second question, yes, and they depend on each other. If yes, then that means a sequential chain. So notice you have already answered the first one. So you do know the steps. Now you are only asking whether they must happen in order. And the test for that is the one we met last lecture. Does this piece need the answer from that piece? If it does, then they are dependent. So they form a chain. And the third question, yes, and they're independent. So no dependency means run them in parallel. So notice how the three questions narrow things down.

**4:28 → 5:11**

First, do I know the steps at all? Then, if I do, do they need each other? And if they do not, run them together. By the third question, there is only one answer left standing. And that is exactly why the order matters. Because each question rules something out. And now, here is why this is worth memorizing. This single decision part answers most domain 1 decomposition questions on the exam. So please learn it in that exact order. And notice that exam questions rarely hand you the pattern name. They describe a situation instead. So your job is to run this part against whatever they describe.

**5:11 → 5:56**

Alright, so let us pull this together. The key takeaways from this lecture, passes and picking the fit in two lines. So number one, combine levels, parallel profile passes and then across file pass. So remember real jobs are rarely purely one shape. It is usually independent work first and then a step that brings it all back together. And number two, pick the fit. Can't list steps means adaptive or an orchestrator. Dependent means a chain and independent means parallel. So remember three questions and you should be able to run them in a few seconds and notice

**5:56 → 6:13**

All three are really asking one thing. What shape does this work actually have? Alright. In the next video, we'll look at session state, resume. So, with this, I'm going to end this one. And I'll catch you in the next one.
