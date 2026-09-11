---
hovernotes-transcript-of: doc_de3b5c3f-dcc0-466d-a1fb-8dea99acacf6
hovernotes-transcript-version: 2
note: "[[13-Session-State-Resume]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57909007#overview"
updated: 2026-09-10T12:28:42.836Z
---

# 13-Session-State-Resume — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So everything we have built so far has quietly assumed one continuous run. The agent starts, it loops away and then it finishes. But real work is not like that. You close your laptop, you come back tomorrow or a long job gets interrupted halfway through. So this lecture is called Session State Resume and the subtitle says it. Picking up where you left off. So three things in this lecture. Number one, what a session actually is. Number two, resume and continue, which are your two ways of coming back and number three

**0:14 → 0:16**

It's not like that. You close your laptop.

**0:42 → 1:27**

the stale transcript trap which is the thing to watch for all right so the first topic is what is a session and the subtitle defines it for us the saved memory of an agent's work so before we can pick anything up we need to know what is actually being kept so look at the rule at the top the agent's memory on disk and then the three points underneath it the saved record of a conversation and its work messages tool calls and results and save it and you can come back later so notice what what is genuinely being stored there. Not only what you type,

**1:27 → 2:12**

what every tool called the agent made and every result that came back. And on disk simply means written into a file. So it survives after the program closes. And now here is why that matters. Without a saved session, closing the window means starting over from nothing. So remember from our context lectures that everything Claude knows on a given turn is whatever sits in that conversation. So if the conversation is gone, then all of it is gone. Every file it read and every lookup it did would have to happen all over again. And for a long job, that is not merely annoying.

**2:12 → 2:57**

every one of those tool calls pass you something alright now the second topic resume and continue and the subtitle describes what they do reopen a session and keep going so look at the rule at the top keep the full prior context and then the three points underneath it resume reopens a specific saved session continue picks up the most recent one and the agent keeps its entire prior context so notice the difference between those two resume is for when you know exactly which session you want and continue is the convenient one which simply takes you back to

**2:57 → 3:43**

wherever you last were. So in practice, continue is what you reach for most days and resume is what you use when you are juggling several pieces of work at once. And now here is the idea in one line. Resume equals keep the whole history and carry on. Perfect when the earlier context is still valid. So please notice those last four words. Still valid because that is a condition and it is doing a great deal of quiet work in that sentence. Resume is the right choice when nothing important has changed since you were last here. And that is exactly where the next topic comes in.

**3:43 → 4:28**

because resume does not check anything. It does not go and see whether the world moved on. It simply hands the old history straight back to Claude. Alright, now the third topic, the stale transcript trap and the subtitle warns you plainly. Old tool results can lie to the model. So look at the rule at the top. Resumed is not the same as fresh. And then the three points underneath it. A resume session still holds old tool results. Claude trusts them even if the world changed. And a file was edited, then Claude may act on stale information. So notice why that happens.

**4:28 → 5:13**

precisely what you ask. It is restoring the full history and that history contains results that were perfectly true yesterday. But Claude has no way of knowing that any of them have since gone out of date. Because a tool result is just an entry in the conversation. It does not carry a little label saying this might be old now. And now here is the warning. If earlier results are now out of date, then resuming can make Claude confidently wrong. So please take that in because confidently wrong is the dangerous kind. Claude will not hesitate and it will not flag any doubt.

**5:13 → 5:58**

It read that file yesterday, the contents are sitting right there in its history and so it simply carries on. It is like coming back from holiday and acting on a note you wrote a fortnight ago without once checking whether anything moved. So the practical habit is to ask yourself before resuming. Has anything changed since I was last year? And if files were edited or data was updated, then treat that old context with real suspicion. Alright, so let us pull this together. The key takeaways from this lecture. Resume in three lines. So, number one.

**5:58 → 6:43**

memory, the agents saved messages, tools and results. So remember it is the entire working history and not just a check you can see. Now number two, resume or continue, reopen our session with full context. So remember resume names our specific session and continue simply takes the most recent one. And number three, beware still resume isn't fresh and old tool results can mislead. So remember the history comes back exactly as it was, even though the world did not stay that way. Alright, in the next video, we look at session state fork.

**6:43 → 6:50**

With this, I am going to end this one and I will catch you in the next one.
