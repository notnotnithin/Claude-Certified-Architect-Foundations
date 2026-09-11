---
hovernotes-transcript-of: doc_a53f73dc-9a79-44fd-a17b-a13010605f9a
hovernotes-transcript-version: 2
note: "[[06-Spawning-Subagents]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908977#overview"
updated: 2026-09-10T11:10:49.073Z
---

# 06-Spawning-Subagents — Transcript

**0:00 → 0:42**

All right, everyone, welcome back. So over the last two lectures, we learned why big jobs get split across helpers and what the coordinator actually does with them. But we have quietly skipped a very practical question. How do you actually create one of these helpers? So this lecture is called Spawning Sub-Agents and the subtitle tells you the goal, how you actually create a helper agent. So three things in this lecture. Number one, the task tool, which is the mechanism itself. Number two, defining an agent, which is the four things you have to specify. Number three.

**0:42 → 1:27**

scoping tools and spawning in parallel. Alright, so the first topic is the task tool and the subtitle gives you a rather neat idea. Spawning a sub-agent is itself a tool call, so that is worth sitting with for a second because it means there is no new machinery to learn here. So look at the rule at the top, hand off a job to a fresh agent and then the three points underneath it. The coordinator spawns a sub-agent using the task tool. The new agent runs its own loop and reports back. So it has its own loop from lecture 1.1 and its own isolated context from

**1:27 → 1:57**

and notice how neatly those two earlier ideas come together right here everything we learned about the loop applies inside each sub-agent and that click in workspace we placed last time is exactly what the new agent gets and now here is the whole thing in plain words spawning is just the coordinator saying through a tool call here's a job go run your own loop on it so

**1:57 → 2:42**

Remember from our very first lecture that a tool is simply an action, cloud and tick. And the coordinator already knows how to call tools. So creating a helper is only one more tool call. It just happens that this particular tool hands over an entire job, rather than fetching a single fact. Alright, now the second topic, defining an agent and the subtitle counts them for us. Four things describe a sub-agent. So this is really the job advert for any helper you want to create. Four fields and then that helper exists and can be called upon. So look at the four fields.

**2:42 → 3:27**

at the top. Description, prompt, tools, and model. And then what each one does. Description is what it's for. Prompt is how it behaves. Tools are what it can use. And model is optional, meaning which clot to run it on. And then a genuinely useful note. A cheaper model can power a simple sub-agent. So if a helper's job is straightforward, then you do not need your most powerful model sitting behind it. A sub-agent that simply tidies up some text does not need the same horsepower as one doing genuinely hard analysis. And now, here is the point about that very first field. The description is how the code

**3:27 → 4:06**

knows when to use this sub-agent, so write it clearly. So please take that one seriously because it is easy to rush past. Remember that routing was the coordinator's first job and it is reading those descriptions to decide who gets the work. So think of the description as the job title and the prompt as the job instructions. The title is how you get chosen and the instructions are how you do it once you have Alright, now the third topic scoping tools and spawning

**4:06 → 4:51**

and the subtitle covers both halves of it. Give each subagent only its tools and fire several at once. So, having created our helpers, we now decide what they are allowed to touch and how many run together. So look at the rule at the top. Minimal tools, parallel launches, and then the three points underneath it. Give a subagent only the tools, its job needs. A research agent gets search and not the refund tool. And several task calls in one turn means the subagents run in a parallel. So notice those are really two separate ideas. Sitting together on one slide. The first one is about safety.

**4:51 → 5:36**

keeping each helper's toolkit tight. And the second is about speed, because if you spawn several helpers in the same turn, they all get going at once. And now, here is why each half matters. Scope tools equals safer and clearer, and parallel task calls in a single turn equals real speed. So think about that research agent. If it simply does not have the refund tool, then it cannot issue a refund. Not by accident, and not by being talked into it. You have not asked it politely to behave. You have simply removed the option entirely. And on the speed side, this is exactly

**5:36 → 6:21**

you get the parallel running that we discussed last lecture. Alright, so let us pull this together. The key takeaways from this lecture, spawning in three lines. So number one, task tool, the coordinator spawns sub-agents with the task tool. So remember, spawning is not special machinery at all. It is one more tool call which happens to hand over a whole job rather than fetching a single fact for you. Now number two, define four things, description, prompt, tools, and optional model. So remember that the description is the field doing the routing

**6:21 → 7:06**

because that is exactly what the coordinator reads when it is deciding who gets a job. A vague description and it cannot route properly. And number three scope and parallelize. Tight tools and several task calls in one turn for parallelism. So remember a tool your sub-agent does not have is a mistake that it can never make and several task calls in one turn is how you actually get that parallel speed in practice. Alright in the next video we look at context passing between agents. So with this I'm gonna end this one and I will catch you in the
