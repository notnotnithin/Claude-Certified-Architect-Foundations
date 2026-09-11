---
hovernotes-transcript-of: doc_a7c13a8d-bf3e-4b22-ace7-8e74814c2057
hovernotes-transcript-version: 2
note: "[[03-Error-Propagation-In-Multi-Agent-Systems]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57561047#overview"
updated: 2026-09-11T07:28:48.999Z
---

# 03-Error-Propagation-In-Multi-Agent-Systems — Transcript

**0:00 → 0:42**

So this lecture brings two earlier ideas together Back in domain 1, we built coordinator and subagent teams And in domain 2, we made a single tools errors Speak clearly So now we combine them What happens when a subagent inside a team fails? This lecture is error propagation in multi-agent systems Because when one worker fails, the team shouldn't collapse So four things in this lecture Number 1, the problem Number 2, the structured error handback Number 3, failure type partial results

**0:42 → 1:27**

and access vs empty and number 4 recovery strategies alright so the first topic the problem a subagent fails and the subtitle names the real danger a silent failure is the worst failure so look at what goes wrong if a subagent returns nothing then the coordinator can't tell what broke so it may build the final answer on missing data and then report a confident but incomplete result so the danger is the silence not the failure itself so please notice that carefully the failure on its own is not the disaster the disaster is that the coordinator

**1:27 → 2:13**

does not even know it happened. So it carries on, builds its answer and hands you something that looks complete but quietly isn't. Now here is the key idea. Parts fail, that is normal. The real danger is the coordinator not knowing and hiding the gap. So please take this in. In any big system, some part will occasionally fail. That is expected. That is fine. What is not fine is when that failure is invisible and the missing piece gets papered over silently. So our whole job in this lecture is to make failures loud and visible. All right. So.

**2:13 → 2:58**

Second topic, the structured error hand back. And the subtitle tells you the fix. You report the failure up clearly and in a fixed shape. So look at what the subagent should do. It returns a structured error to the coordinator. So it says what failed, why, and what it did get, not silence. And it passes that up so the coordinator can reason about it. So the motto is report, don't swallow. So notice that phrase. A failing subagent has two choices. It can swallow the error and return nothing. Or it can report it honestly upward. And reporting is always the right move.

**2:58 → 3:43**

Here is the connection. You will reuse the error format from lecture 2.2, the is error flag and the category. But here the focus is passing it up to the coordinator. So please notice we are not learning a new error format. We already built one in domain 2. The is, error flag, the category, all of that. So this lecture takes that same structured error and adds one thing. In a team, it does not just sit there. It travels upward to the coordinator who can act on it. Alright, so the third topic, failure type, partial results and access versus error.

**3:43 → 4:28**

and the subtitle tells you the goal. You tell the coordinator exactly what kind of failure this is. So look at the first kind. An excess failure. This is couldn't reach the source and that is a real failure. So it is retrieval. So notice what this means. The sub-agent tried to reach some source and simply could not get to it. Maybe it was down. So that is a genuine failure and because it might just be temporary, it is worth trying again. Now look at the second kind. An empty result. This is reached it, found zero results and that is a valid.

**4:28 → 5:13**

So you do not retry. So notice the crucial difference. Here the sub-agent got through perfectly fine. It looked and there was simply nothing there. So that is not a failure at all. It is a complete correct answer. The answer just happens to be nothing. And here is the rest of it. You also carry the failure type. Plus any partial results. Like got 2 of 5 sources. And this is the same trap as lecture 2.2. Empty is an answer, not a failure. So please notice this is exactly the distinction we drilled.

**5:13 → 5:58**

in domain 2, but now it lives in a team. So a sub-agent that got 2 of 5 sources should say so, and an empty result should never be treated as a failure and retry forever. Alright, so the fourth and final topic, recovery strategies and the subtitle tells you the payoff. Now the coordinator can actually do something. So look at the three strategies in order. First retry, if it was transient, like a timeout, then skip and note. If it is non-critical, you flag the gap and finally escalate. it is critical you hand it to a

**5:58 → 6:44**

So, notice how this all depends on that honest error. Because the sub-agent said clearly, what went wrong, the coordinator can now pick the right response, a transient timeout, retry, a minor missing piece, skip it and note it. A critical failure, bring in a human, and here is the guiding idea for all of it, you report honestly. So, something like findings complete, except news sources which were unavailable, beats a silently incomplete report. So please notice what that gives the user. Instead of a report that looks whole, but quietly has a hole in it, they get one.

**6:44 → 7:29**

That says plainly, here is what I found and here is the one thing I couldn't. And that honesty is far more useful and far more trustworthy. Alright, so let's pull this together. The key takeaways from this lecture, error propagation in three lines. Number one, never fail silently. A sub-agent hands its failures up as a structured error. So remember, the silence is the real danger, not the failure. Number two, name the failure. You carry the failure type plus parcel results and you separate an access failure from an

**7:29 → 8:05**

So remember, empty is an answer, not a failure. And number three, recover and be honest. You retry or skip with a node or escalate. And you report what's missing. So remember, an honest partial report beats a silently incomplete one. All right. So that is how a team survives one worker failing. In the next lecture, we will look at context in large code-based exploration. So with this, I am going to end this one. And I will catch you in the next one.
