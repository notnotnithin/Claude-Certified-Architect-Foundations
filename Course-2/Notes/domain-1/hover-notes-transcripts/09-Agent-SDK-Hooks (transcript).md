---
hovernotes-transcript-of: doc_5aad8955-ffc8-4fb7-8c38-4d51aecd38da
hovernotes-transcript-version: 2
note: "[[09-Agent-SDK-Hooks]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908993#overview"
updated: 2026-09-10T11:34:11.799Z
---

# 09-Agent-SDK-Hooks — Transcript

**0:00 → 0:42**

so last lecture we said that some rules must be guaranteed in code and not merely requested in a prompt but that left one obvious question hanging how exactly where does that code actually live in an agent that is looping away on its own so this lecture is called agent sdk hooks and the subtitle tells you why they matter the tool that makes rules deterministic so four things in this lecture number one what a hook is number two pre-tool use which fires before a tool runs number three post tool use which

**0:42 → 1:27**

eyes after it. And number four, deterministic versus probabilistic, which is where all of this pays off. Alright, so the first topic is, what is a hook? And the subtitle defines it very simply. Code that runs around a tool call. So the word around is the important one there. Not inside the tool and not inside cloud, but wrapped around the call itself on either side of it. So look at the rule at the top, runs automatically every time. And then the three points underneath it, your code runs at a set point in the loop. Just before or just after a tool runs.

**1:27 → 2:13**

it can inspect, change or block what happens. So notice all three of those powers. It can look at what is about to happen, it can alter it before it happens, or it can stop the thing entirely. And your code decides which every single time the tool is called. And now here is why hooks are so powerful. Hooks fire every time automatically and that's what makes them a guarantee and not a suggestion. So please sit with those two words every time. There is no path through the loop where the hook gets skipped. Claude cannot forget it and Claude cannot decide to go around it because

**2:13 → 2:58**

Hook is not something Claude chooses. It sits in the loop itself. So if the tool runs at all, then the hook has already run. That is a genuinely different promise from writing a rule into a prompt and hoping. Alright, now the second topic. Pre-tool use before the tool runs. And the subtitle lists what you can do there. Inspect, modify or block before it happens. So look at the rule at the top, your safety checkpoint, and then the three points underneath it. It files before a tool runs. It can allow, modify the input or block the call. and canonical use.

**2:58 → 3:43**

which is block any refund over $500 and route it to a human instead. So notice the timing in all of that. Nothing has happened yet and the money has not moved anywhere. This is the last moment where stopping the action is still free because once the refund has actually gone out, you are no longer preventing a problem. You are cleaning one up. And now here is the key idea. Pre-tool use is the place to stop a dangerous action before it executes. So connect that straight back to last lecture. Remember our prerequisite kit where no refund happens until identity is verified? Well a pre-tool use hook is exactly

**3:43 → 4:28**

you build that gate. It is the code sitting in front of the dangerous action, deciding whether it happens at all. Alright, now the third topic, Post tool use after the tool runs. And the subtitle describes its job. Clean up or check the result before Claude sees it. So if the first hook was about protecting the world from Claude, this one is about protecting Claude from whatever the tool sent back. So look at the rule at the top. Shapes what Claude sees. And then the three points underneath it. It fires after a tool runs but before Claude reads it. It can transform the result, for example,

**4:28 → 5:13**

normalizing messy timestamps. And it is great for logging too, so notice the little window it occupies. The tool has finished, but Claude has not looked yet, so you get one chance to tidy up what came back. And now, here is the cleanest way to hold both of these in your head. Pre-tool use guards what goes out, and post-tool use shapes what comes back in. So please remember it in exactly that pairing, because it makes choosing between them very easy. If you are protecting the world from a dangerous action, that is before, and if you are protecting Claude from a messy result, that is after.

**5:13 → 5:59**

Alright, now the fourth topic, deterministic vs probabilistic And the subtitle is blunt about it Hooks guarantee and prompts only hope So look at the first side and it comes up with two ticks Hooks, deterministic which means the rule always holds And used for anything that must be 100% So notice that word always because it is doing real work There is no distribution here and no usually Either the rule holds or your code is broken And those are the only two outcomes available Now look at the other side which

**5:59 → 6:44**

slide sets against it as a straight versus prompts and this one gets two crosses probabilistic which means the rule usually holds and not for must never break rules so this is the same distinction we drew last lecture between probable and guaranteed compliance only now you know the actual mechanism that delivers it hooks are how deterministic gets built in a real system and now here is a reflex worth drilling for your exam this rule must never break means that's a hook problem and not a prompt problem so please train your ear for that phrasing.

**6:44 → 7:29**

never always or must sitting in an exam question or a signal they are pointing you away from clever prompt wording and straight towards a hook all right so let us pull this together the key takeaways from this lecture hooks in three lines so number one code around tools a hook runs automatically around a tool call so remember automatic is the whole point a rule that runs every single time without cloud choosing it is what turns a hope into a guarantee now number two pre and post pre tool use blocks or modifies before and post tool use blocks

**7:29 → 8:08**

transforms after so remember one guards what goes out and other shapes what comes back in and that single sentence is usually enough to tell you which hook you need and number three deterministic use hooks for any rule that must always hold so remember must always means a hook that is where your non-negotiable rules belong all right in the next video we look at task decomposition the strategies so with this i'm going to end this one and i will catch you in the next one
