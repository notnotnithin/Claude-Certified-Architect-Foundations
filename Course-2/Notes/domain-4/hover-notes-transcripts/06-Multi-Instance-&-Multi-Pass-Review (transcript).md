---
hovernotes-transcript-of: doc_8cc56a7d-0c26-4bbc-9ca5-5ab9eb57d2a3
hovernotes-transcript-version: 2
note: "[[06-Multi-Instance-&-Multi-Pass-Review]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57493861#overview"
updated: 2026-09-11T06:41:34.505Z
---

# 06-Multi-Instance-&-Multi-Pass-Review — Transcript

**0:00 → 0:42**

All right everyone, welcome back. So, all through this domain, we have made Claude's output reliable and structured. And now for the final piece, we turn to reviewing work thoroughly, not with one quick glance, but with fresh independent eyes looking more than once. This lecture is multi-instance and multi-pass review. And the subtitle says it well. Two sets of fresh eyes beat one tired glance. So, five things in this lecture. Number one, why one pass isn't enough? Number two, the independent reviewer. Number three, per file and cross file passes.

**0:42 → 1:28**

Number 4 Confidence-Anitated Passes And Number 5 Aggregating the Passes Alright, so the first topic, why one pass isn't enough and the subtitle states the problem. A single reviewer in one sweep misses things. So look at the two problems, limited attention plus self-review bias. So one sweep over many files means the focus spreads thin and the author reviewing its own work is biased to approve. So we fix both with independence and with multiple passes. So notice there are really two separate issues here.

**1:28 → 2:13**

First is just attention. Over a big task, in one pass the focus gets stretched too thin. And the second is bias. When the same Claude that wrote the code reviews it, it tends to approve its own work. Now here are those two problems named clearly. One limited attention across a big task and two bias when the reviewer also wrote the work. So please hold board in mind because the rest of the lecture fixes them one by one. The independent reviewer will fix the bias and the multiple passes will fix the thin attention. Two problems and two fixes.

**2:13 → 2:58**

Alright. So the second topic, the independent reviewer. And the subtitle tells you the core idea of fresh instance that didn't write the work. So look at what this is. It is a separate Claude instance with its own context. So it never saw the author's reasoning or its excuses. So it judges the work purely on its merits. So one instance builds and a different one reviews. So notice why the fresh context matters so much. The reviewer has no memory of why the code was written that way. It cannot defend choices it never made. So it looks at the work cold.

**2:58 → 3:43**

exactly as an outside reviewer would and here is the connection and it runs right through the course this is the isolation idea from lecture 3.6 the self-review and from the sub-agents of lectures 1.2 and 1.3 a clean context gives an unbiased opinion so please notice how many times this idea has come up back in domain 1 sub-agents worked in isolated contexts in domain 3 the CI reviewer was a separate instance and here it is the same principle once more a fresh separate context is what makes the the

**3:43 → 4:28**

honest. Alright, so the third topic, Per file and cross file passes and the subtitle explains the two views. You look closely at each part and then at how they fit together. So look at the first pass, the Per file pass, here you review each file on its own and deeply and that catches the local bugs and the style issues. So notice what this pass is good at. By focusing on just one file at a time, the review goes deep. It spots the small local problems inside that single file, the bugs and the messy style that live in one place. Now look at the second pass

**4:28 → 5:13**

The cross file pass, here you look at how the files work together and that catches integration problems and mismatched interfaces. So notice what this pass sees that the other cannot. Some bugs do not live inside any single file. They live in the gaps between them where two files are supposed to connect but do not quite line up. And only a cross file view can catch those. And here is why you need both. A per file only review misses the integration bugs. And a cross file only review misses the local ones. So multipass means

**5:13 → 5:59**

both so please hold this clearly because it is exactly what gets tested neither pass alone is enough look only at each file and you miss how they connect look only at the connections and you miss the bugs inside so you do both passes and between them you catch everything all right so the fourth topic confidence annotated passes and the subtitle tells you the extra step each finding says how sure it is so look at the idea you attach a confidence to every finding so that is high

**5:59 → 6:44**

each flag and then a high confidence finding you act on but a low confidence one you route to a human so notice what the confidence adds it is not enough just to know that something was flagged you also want to know how sure the reviewer is because a thing it is certain about anything it is only half sure about deserve very different treatment and here is the powerful part confidence turns a flat list into a routing signal so the sure things auto apply and unsure things get human eyes so please notice what that does for you without confidence

**6:44 → 7:29**

Every finding looks the same and a human has to check all of them. But with it, the high confidence ones can be handled automatically and only the genuinely uncertain ones need a person. So you save your human effort for exactly where it is needed. Alright, aggregating the passes and the subtitle tells you the goal. You combine all the passes into one clean verdict. So look at how you combine them. You merge, you do not just stick them end to end. So you deduplicate the overlapping findings. you keep the high severity when they

**7:29 → 8:14**

overlap and you group by confidence for routing. So notice the keyword merge, two passes will often flag the same issue. So you do not want two copies of it, you want to combine them intelligently. One entry per real issue at its true severity and here is the warning and it loops right back to the start of the domain. Two passes flagging the same issue should appear once at its true severity or you are back to the trust problem from lecture 4.1. So please see why this matters. If you just pile up both passes then every duplicate issue shows up twice.

**8:14 → 8:59**

And suddenly your clean review is noisy again And we know from 4.1 that a noisy review gets ignored So the merge is what keeps the whole thing trusted Alright, so let's see the whole thing in a worked example Reviewing a feature branch and the subtitle promises the full picture The whole architecture on one change So look at the full flow in order First independent, a fresh reviewer instance Then perfile, reviewing each changed file Then crossfile, checking the integration Then confidence, annotating each file

**8:59 → 9:44**

And finally, Aggregate, where you deduplicate and root. So, notice how every piece of this lecture snaps into place here. A fresh instance does two passes, scores its findings, and merges them into one clean verdict. And here is the lovely payoff. This is the architecture that lectures 1.6 and 3.6 pointed to. It is decomposition, that is the per file and cross file passes, meeting independent, confident, scored review. So, please appreciate this moment way back in domain 1, when we split big work into pieces. we

**9:44 → 10:30**

this comes together later and in domain 3 when we ran a self-review in isolation we said the same so this right here is that promise kept every thread tied together all right so let's pull this together the key takeaways from this lecture multi-pass review in three lines and with it domain 4 is wrapped number one the independent reviewer a separate instance kills self-review bias so remember the reviewer that did not write the code has no reason to defend it number two 2 passes plus confidence.

**10:30 → 11:15**

a per file and a cross file pass and you annotate each finding with the confidence so remember per file catches local bugs cross file catches integration ones and confidence tells you what to trust and number three aggregate and root you de duplicate you keep the top severity and you send the low confidence findings to humans so remember merge don't just concatenate or the review gets noisy again so that brings domain four to a close look back at the whole journey we told claude exactly what good looks like with explicit creative

**11:15 → 12:00**

We showed it with few short examples. We forced clean structured output. We validated the meaning and required with feedback. We ran huge jobs cheaply in batches. And now we review that work with fresh independent eyes. So that is prompt engineering and structured output. It is everything that turns a clever but unpredictable model into a reliable production system. Alright, that completes domain 4, prompt engineering and structured output. In the next domain, we move on to context management. So with this, I'm going to end domain 4 and I will catch you in the next one.
