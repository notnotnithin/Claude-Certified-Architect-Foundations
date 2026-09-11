---
hovernotes-transcript-of: doc_0ddc68bd-a45a-4b66-996d-ddeaba5096d2
hovernotes-transcript-version: 2
note: "[[06-Claude-Code-In-CI-CD]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57479755#overview"
updated: 2026-09-10T16:08:23.808Z
---

# 06-Claude-Code-In-CI-CD — Transcript

**0:00 → 0:40**

So across this whole domain, we have been configuring Cloud code. Its memory, its commands, its rules, plan mode and iteration. Now we take the final step. We put Cloud onto the assembly line. This is Cloud code in CICD. So that it can run automatically with no human at the keyboard at all. So six things in this lecture. Number one, headless mode. Number two, the dashed P flag. Number three, structured output. Number four, safety guards. Number five, Cloud.md as CIContact.

**0:40 → 1:14**

And number 6, self-review isolation. Alright, so the first topic, headless mode. And the subtitle tells you what it means. No keyboard, no terminal, just a pipeline step. So look at what headless mode is. Cloud code runs unattended. Right inside your CICD. So it runs on every pull request or on a schedule or inside a script. There is no interactive terminal and no human clicking approved.

**1:14 → 1:59**

It is just another automated stage. So please notice the shift here. Everything we have done so far, assumed you were sitting right there at the keyboard, headless mode removes you entirely. Cloud becomes one more automatic step in your pipeline, like running the tests or building the code. Now here is the picture for it. It is like an automated night shift. It is the same cloud running your task without anyone watching. So think about that night shift for a second. The work still gets done on every pull request, all through the night, but nobody is there to guide it or to catch a problem in the moment. So that unattended nature is the whole point

**1:59 → 2:44**

headless mode. And as we will see, it is also exactly why the safety guards matter so much. Alright, so the second topic, the dash P flag. And the subtitle sums up its whole behavior. One prompt in, one result out, and then it exits. So, look at how you use it. You run, cloud, dash P and then your prompt. So, it runs to completion, it prints the result, and then it exits. And it exits with a status code that your pipeline can branch on. So, there is no interactive session, and no REPL, that is no live back and forth prompt. So, notice why that suits a pipeline

**2:44 → 3:29**

A pipeline step needs to start, do its job and finish cleanly. So Dash B does exactly that. It takes your one prompt, produces one result and then gets out of the way. Now here is the key point and the exam loves this. Dash B or print mode is the headless switch. It is the foundation of every CI step, every cron job and every GitHub action. So please make sure you know this one. If a question asks how you run cloud code without a human in an automated pipeline, the answer is the Dash B flag. It is the single switch that turns interactive cloud into an automated step. All right.

**3:29 → 4:05**

So the third topic, structured output and the subtitle tells you why. You want JSON that your script can actually read. So look at the two flags. The output format flag set to JSON and the JSON schema flag. So output format JSON gives you a structured result plus metadata, which you can pass with a JSON tool like JQ and JSON schema forces an exact shape into a structured output field. And the formats you can choose are text, which is the default JSON and stream JSON.

**4:04 → 4:47**

JSON and stream JSON which is real time. So notice what this gives your pipeline. Instead of a blob of prose that a script cannot easily read, you get clean structured data in a shape that you control. Now here is when you really need a schema. Is a downstream step going to branch on the result, then you use JSON schema so the shape is guaranteed and not just hope for. So think about why that matters. If your next pipeline step reads a field and decides what to do, then that field absolutely has to be there in the right place every single time. So the schema forces it, you are no longer hoping the output looks right.

**4:47 → 5:32**

guaranteeing it and here is one more useful detail the json format returns the result plus metadata things like the cost and the session id and you pass it with jq so notice the bonus in that you do not just get the answer you also get useful facts about the run itself like how much it costs and because it is all clean json a small tool like jq can pull out exactly the piece you need all right so the fourth topic and this one is essential safety guards and the subtitle tells you why. Unattend it means you set the limits.

**5:32 → 6:17**

So look at the guards, you cap the run before you walk away. So there is max turns to cap the amount of work and allow tools to narrow the permissions and max budget USD to cap the cost in dollars. And you check the output content, not just the exit code. So notice that these are all limits set in advance because nobody will be there to stop it later. So you decide upfront how many turns, which tools and how much money. And then the run simply cannot go past those lines. And here is the warning and it is a serious one. No human is watching.

**6:17 → 7:03**

Without turn and budget, caps, a stuck run can burn time and money quietly at 3 in the morning. So please take this to heart. Picture a run that gets stuck in a loop in the middle of the night. With you at the keyboard, you would just stop it. But headless and alone, it keeps going turn after turn, quietly running up a bill until morning. So the caps are what protect you when nobody is there to hit stop. Alright, so the fifth topic, Claude.md as CI context. Your project rules ride along into the pipeline. So look at what happens. The same Claude.md loads.

**7:03 → 7:48**

in CI. So your conventions become the reviewer's context automatically. You write your rules once and CI inherits them. So there is no extra setup to teach the pipeline your standards. So notice how much you get for free here. The rules you already wrote for your daily work are the very same rules the automated reviewer uses. You do not write them twice. They just come along. Now here is the connection. This is lecture 3.1's claude.md doing double duty. You write your rules once and CI inherits them for free. So remember back in 3.1 we set up that file as project memory for your sessions.

**7:48 → 8:33**

So here is the payoff, that exact same file with no changes at all, now also guides Claude inside the pipeline, one file teaching Claude your project both at your desk and out on the assembly line. Alright, so the sixth and final topic, self-review isolation. And the subtitle nails the idea, you want a fresh reviewer, not the author grading its own homework. So look at the technique, you run the reviewer as a separate instance. So it has an independent context and it did not write the code. So there is no bias from justifying its own choices and what you get is an author.

**8:33 → 9:18**

second opinion. So please notice why this is so important. If the same cloud that wrote the code also reviews it, it carries all the reasoning it used to write it. So it is naturally inclined to defend its own work. A fresh instance has none of that baggage. Now here is the point stated plainly. A separate instance gives you an unbiased second opinion. It is not the same session justifying its own choices. So think about that phrase grading its own homework. We all know that a student marking their own test will go easy on themselves. So it is exactly the same here. The author is the wrong

**9:18 → 10:03**

to judge the work. So you bring in a fresh reviewer that sees the code cold with no reason to defend it. And here is a pointer to what is coming. The full multi-instance review architecture is taught in domain 4 in lecture 4.6. Here it is simply the CI mechanic. So just note this, for now, using a fresh independent reviewer is a big idea and it has a whole lecture waiting for it. So in this lecture we are just using it as the practical way to review code in your pipeline and we will study the full architecture later in domain 4. Alright.

**10:03 → 10:48**

takeaways from this lecture, Claude code in CI CD in 3 lines 1-P is headless, Claude-P runs unattended, prompt in result out and an exit code 2- Shape and guard, to output format JSON and JSON's schema flags give your scripts a reliable shape and you kept the turns, the tools and the budget 3- Context and isolation, your Claudey.md loads in CI and you run self review as a separate unbiased instance, so that brings domain 3 to a close Look back at the whole journey. We taught Claude our project.

**10:48 → 11:34**

once with cloud.md. We saved our workflows as commands and skills. We aimed our rules precisely with path-specific loading. We learned to plan before risky work and to refine in passes. And now we have put cloud onto the assembly line. So that is cloud code configuration and workflows. It is all about shaping how cloud works from your own desk all the way out to your pipeline. Alright, that completes domain 3, cloud code configuration and workflows. In the next domain, we move on to prompt engineering and structured output. So with this, I am going to end domain 3.

**11:34 → 11:37**

and I will catch you in the next one.
