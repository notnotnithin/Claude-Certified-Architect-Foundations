---
hovernotes-transcript-of: doc_7cba8b3e-54b0-4389-88fa-ca9bc3fbf3c3
hovernotes-transcript-version: 2
note: "[[01-Explicit-Criteria-And-False-Positives]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57493847#overview"
updated: 2026-09-11T05:18:52.464Z
---

# 01-Explicit-Criteria-And-False-Positives — Transcript

**0:00 → 0:43**

Alright everyone, welcome back. So we are now starting domain 4 and this domain is about prompt engineering and structured output. In simple terms, it is about getting reliable and precise results out of Claude. And the very first lecture is about being clear. This lecture is explicit criteria and false positives, which really means telling Claude exactly what good looks like. So six things in this lecture. Number one, why criteria matter? Number two, vague versus specific. Number three, severity levels. Number four, the false positive problem. fight.

**0:43 → 1:28**

noise erodes trust and number six tuning the noisy categories all right so the first topic why explicit criteria matter and the subtitle gives you the core idea claude judges against the yardstick you give it so look at the vague ask on the left it is something like is this code good and the problem is claude has to invent a standard of its own so it drifts so please notice what goes wrong here good is not a fixed thing what counts as good code to one person is different to another So when you ask, is this good, Claude has to make up its own definition of

**1:28 → 2:13**

on the spot and it might make up a slightly different one every time you ask. Now look at the other side. Explicit criteria. Here you give Claude a clear checklist to judge against and because of that you get the same standard every single time. So notice the difference. Instead of leaving good up to Claude, you hand it the exact list of things to check. So there is nothing left to invent. It checks your list the same way on every run. And here is the idea in one line. A vague ask means Claude invents a standard that drifts from run to run but explicitly

**2:13 → 2:58**

criteria means the same standard every time. So this is the whole lesson of the slide. Consistency does not come from a cleverer question. It comes from giving Claude a fixed yardstick, so it is not guessing at what you meant. Alright, so now let's make that sharper, vague versus specific. And the subtitle draws the line beautifully. Check for security issues is a wish, but a specific rule is testable. So look at the vague version first. It is a wish. Something like check for security problems. And the trouble is Claude has to guess what you actually matter.

**2:58 → 3:43**

So notice why that is weak. Security problems could mean a hundred different things. So Claude is left guessing which ones you care about. And guessing means it will be inconsistent. Catching one thing today and a different thing tomorrow. Now look at the specific version. It is testable. Something like flag any SQL query that is built with string concatenation. So that is specific, it is observable and it is testable. So let me unpack that example simply. String concatenation just means gluing bits of text together to build the query. And that is a well-known security risk.

**3:43 → 4:28**

So this rule is precise. Claude does not have to guess at all. It just looks for that one exact pattern and it flags it. And you could check its work by hand. And here is the rule to remember. A criterion that Claude cannot test objectively will be applied inconsistently. So you write rules that you yourself could check by hand. So please hold on to that little test. Before you give Claude a rule, ask yourself, could I check this myself with a clear yes or no? If yes, it is a good testable rule. But if it is fuzzy and open to opinion, then Claude will apply it.

**4:28 → 5:14**

unevenly. Alright, so the second topic Severity Levels and the subtitle keeps it light. Not every issue is a 5 alarm fire. So look at the first level, critical. It is marked in red. This is something that blocks the release. For example, a hard coded password. So notice why this is the top level. A hard coded password is a serious security hole. You cannot ship the code until it is fixed. So critical means stop. This must be dealt with now. Now the second level, major. It is marked in orange. This is something to fix soon. For example.

**5:14 → 5:59**

Missing error handling. So notice the difference from critical. Missing error handling is a real problem. But it is not going to stop the release today. So major means this matters and you should fix it soon. But it is not an emergency. And the third level, minor, it is marked in grey. This is just nice to fix. For example, an inconsistent name. So notice how low the stakes are here. An inconsistent name is a bit untidy but it does not break anything. So minor means fix it if you have time but it can happily wait. And here is why this matters so much. without severity, a typo and

**5:59 → 6:44**

security hole look equally urgent and so the important issue gets buried. So think about that for a second. If every finding is just an issue with no level attached, then a tiny typo sits right next to a serious security flaw, looking exactly as important. So the real danger gets lost in the crowd. Severity is what makes the important things stand out. Alright, so the third topic, the false positive problem. And the subtitle says exactly what it is, flagging things that aren't actually problems. So look at the definition. false positive is when Claude flags something that

**6:44 → 7:29**

So, over-broad criteria lead to many false alarms. It is like a smoke alarm going off at toast. And opposite of this is a false negative which is missing a real issue. So let me make both of this clear. Simply, a false positive is a false alarm. It shouts about a problem that is not there. A false negative is the reverse. It stays silent about a problem that is real. So the smoke alarm going off at your toast is the false positive. Loud and wrong. Now here is the key point. Both of this hurt. But false positives are the real trust cases.

**7:29 → 8:14**

as the next slide will show. So notice that this is a little bit surprising. You might think that missing a real issue, the false negative is the worst one and it is certainly bad. But as we are about to see, it is the constant false alarms that quietly destroy trust in the whole system. Alright, so the fourth topic, why noise erodes trust? And the subtitle is an old proverb. A reviewer who cries wolf gets ignored. So look at what happens. Too many false alarms and people just stop reading the output. So imagine 18,

**8:14 → 8:59**

nonsense flags, burying the two real ones. Users start clicking dismiss, dismiss, dismiss, and then they scroll straight past the one genuine critical flag. So please picture that clearly, when almost everything is a false alarm, people stop paying attention entirely, they dismiss everything on autopilot. And so the one flag that really mattered, gets dismissed too, without a second look. And here is the hard truth, a noisy reviewer is worse than no reviewer at all, because users tune it out entirely, so even its correct flags stop working.

**8:59 → 9:45**

that for a moment because it is a strong claim. You might think that a reviewer, which is sometimes wrong, is still better than nothing. But it is not. Once people learn to ignore it, its good flags and its bad flags are ignored alike. So all of its value is gone. Alright. So the fifth topic. Tuning disable the noisy categories. And the subtitle gives you the move. Turn off what you can't make precise. So look at the approach. You narrow it or you switch it off. So if a category, for example, style nitpicks is mostly false positives, then you tighten its rule. Or you

**9:45 → 10:30**

disable that category completely because fewer high precision flags beat many noisy ones. So notice what you are doing here. You are being honest about which checks actually work. If a whole category is mostly noise, you do not keep it and just hope you either make its rule much tighter or you turn it off so it stops drowning the good flags. And here is the exam worthy point. If you have an over flagging problem, you tighten or you disable the noisy category. You do not just add be more careful to the prompt. So please notice this one carefully because it is a very common wrong answer.

**10:30 → 11:09**

When a reviewer flags too much, the tempting fix is to write, please be more careful or only report high confidence issues. But that vague plea does not work. The real fix is specific. You tighten the rule for that category or you switch that category off. Alright, so the sixth and final topic and it ties everything together. A worked example, two review prompts and the subtitle sets it up. The same code but two very different reviewers. So look at the...

**11:09 → 11:51**

look at the first prompt it just says review this code and the result is 15 flags mostly style noise so the team ignores it so notice what happened here a vague prompt produced a flood 15 findings and most of them trivial and because it is mostly noise the team learns to ignore the whole thing so all 15 flags the useful ones and the useless ones get thrown away together now look at the second prompt this one has criteria plus severity plus tuning and the result is just three flags one critical and two major and all three

**11:51 → 11:55**

are real, so the team acts on it. So notice the contrast.

**11:54 → 12:37**

So notice the contrast. This reviewer says much less only 3 things. But every one of them is genuine and it comes with a severity. So the team trusts it and it actually does something about it. And here is the punchline and it is a little surprising. The tuned reviewer finds fewer things. And that is exactly why the team acts on it. So please hold on to this because it flips the usual instinct. More flags, feels like more thoroughness but it is not. The reviewer that found 15 things got ignored. The one that found 3 got trusted. So in review, fewer real things.

**12:37 → 13:22**

beat many noisy ones every single time. Alright, so let's pull this together. The key takeaways from this lecture. Explicit criteria in three lines. Number one, specific and testable. You give Claude specific testable criteria, not vague wishes. So remember a rule you could check by hand gets applied consistently. A fuzzy wish does not. Number two, add severity. Severity levels prioritize your findings. So the important ones surface. So remember without levels, a typo and a security hole look equally urgent. But with them the serious things stand.

**13:22 → 13:54**

and number three control your false positives you tune or you disable the noisy categories to keep the reviewer trusted so remember a noisy reviewer gets ignored entirely and fewer real flags are what the team actually acts on all right so that is how you tell claude exactly what good looks like in the next lecture we will look at few short prompting so with this i am going to end this one and i will catch you in the next one
