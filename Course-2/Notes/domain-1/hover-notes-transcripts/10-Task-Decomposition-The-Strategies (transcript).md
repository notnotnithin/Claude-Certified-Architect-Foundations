---
hovernotes-transcript-of: doc_d9de2c7b-03a7-44fe-bb2f-989283eab54c
hovernotes-transcript-version: 2
note: "[[10-Task-Decomposition-The-Strategies]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908997#overview"
updated: 2026-09-10T11:59:23.935Z
---

# 10-Task-Decomposition-The-Strategies — Transcript

**0:00 → 0:26**

Alright everyone, welcome back. So we have spent this domain building machinery, the loop, then coordinators and subagents, and then gates and hooks. But underneath every one of those sits a thinking scale that we have not yet looked at directly. Because when a big job lands on your desk, somebody has to decide how to cut it up. So this lecture is called

**0:26 → 1:12**

Task decomposition, the strategies. And the subtitle sets the aim. Break a big job into the right shape pieces. So three things in this lecture. Number one, why decompose at all? And what it actually buys you. Number two, sequential and parallel which are your two basic shapes. And number three, adaptive, which is also called dynamic. For the jobs, you cannot plan out in advance. Alright, so the first topic is why decompose? And the subtitle gives you the reason in one line. Smaller pieces are easier to get right.

**1:12 → 1:57**

But before we look at the shapes, it is worth being clear about what splitting actually buys you. So look at the rule at the top, focused, checkable, reliable. And then the three points underneath it, breaking a task into subtasks makes each one focused, easier to check and more reliable. And independent pieces can run in parallel. So notice that middle word, checkable, because that is the one people under it. A giant task either works or it doesn't. And when it fails, you have no idea which part let you down. It is one solid block and you cannot see inside it. five small pieces can

**1:57 → 2:42**

each be checked on their own. So a failure tells you exactly where to look. And now, here is a connection you have already met. It is the same focus benefit as sub-agents because a small clear sub-task beats one giant vague one. So please notice how the same principle keeps returning. It applied to agents when we split work across specialists in a kitchen. And it applies here to the work itself. Small and clear beats big and vague every single time. And notice that this is not only about correctness. A job you can describe in small pieces is a job that you genuinely understand

**2:42 → 3:27**

yourself. Alright, now the second topic, sequential and parallel. And the subtitle gives you two pictures to hold, a chain or a fan. So look at the first shape, and it comes up with two ticks, sequential, fixed order, where each one fits the next. And the example is extract, then validate, then format. So notice why that order cannot be shuffled around. You cannot validate data that you have not extracted yet, and you cannot format an analysis that does not exist. The work itself has a shape, and you are simply following.

**3:27 → 4:12**

So you are not choosing to be slow here. The dependency is choosing for you and arguing with it just breaks the job. Now look at the other shape which the slide sets against it as a straight versus. Parallel and it also gets two ticks. Independent steps at once. And the example is check five files simultaneously. So notice the key word there. Independent file once check does not need file 2's answer. So there is no reason at all to make them queue up. And the payoff is real. Five checks running together finish in roughly the time it would take to do one of them. one of them. And now here is the rule for

**4:12 → 4:57**

between them sequential when steps depend on each other and parallel when they're independent so please notice that you do not choose by what sounds faster you look at the work and ask one question does this piece need the answer from that piece if yes it is a chain and if no it is a fan all right now the third topic adaptive decomposition which is also called dynamic and the subtitle describes it plainly figure out the pieces as you go so look at the rule at the top the plan goes as the work reveals it and then

**4:57 → 5:43**

three points underneath it. You don't know all the subtasks up front. Claude discovers them as it works. And the shape looks like investigate, then find leads, then spawn follow-ups. So notice how different that is from the first two shapes. With a chain or a fan, you knew the pieces before you started. Here, you genuinely do not. The second step depends on whatever the first one turns up. So the plan is being written while the work happens. And now, here is when to reach for it. Use adaptive when the steps can't be known in advance. Which means research Yes.

**5:43 → 5:43**

bugging.

**5:44 → 6:27**

So think about what those three have in common. You cannot plan a debugging session in advance because you do not yet know what is broken. It is like following a trail through a wood. You take one step, look at what is actually there and only then can you tell where the next step goes. And notice how well that fits the Argentic loop from our very first lecture. Act, observe and then decide what comes next. Alright, so let us pull this together, the key takeaways from this lecture. composition

**6:27 → 7:12**

strategies in three lines. So number one, why decompose? Each piece becomes focused and reliable. So remember, a giant task hides its own failures, whereas five small pieces tell you exactly which one went wrong. Now number two, sequential or parallel? Dependent goes sequential and independent goes parallel. So remember, a chain or a fan and the dependency decides that for you, not your preference for speed. And number three, adaptive, when the steps can't be known up front. So remember, the work itself reveals the plan, which is

**7:12 → 7:28**

bugging so naturally. Alright, in the next video, we look at mapping decomposition to patterns. So with this, I'm going to end this one and I will catch you in the next one.

**8:08 → 0:00**

So last lecture we said that some rules must be guaranteed in code and not merely requested in a prompt. Alright everyone, welcome back. So we have spent this domain building machinery, the loop, then coordinators and sub-agents, and then gates and hooks. But underneath every one of those sits a thinking scale that we have not yet looked at directly. Because when a big job lands.
