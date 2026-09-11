---
hovernotes-transcript-of: doc_3cff9542-0c9f-4635-8b0e-6698f44d9e06
hovernotes-transcript-version: 2
note: "[[03-Tool-Distribution-And-ToolChoice]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460127#overview"
updated: 2026-09-10T13:09:00.274Z
---

# 03-Tool-Distribution-And-ToolChoice — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So in the last two lectures, we have been perfecting a single tool, describing it clearly and handling it well when it fails. Now we zoom out to the whole toolbox. How many tools should Claude have all at once? And can you ever take the choice out of its hands? So this lecture is tool distribution and tool choice. Because more tools isn't better. You want the right tools and sometimes a forced choice. So six things in this lecture. Number one, the too many tools problem.

**0:42 → 1:27**

scoping tools to the job number 3 the tool choice lever number 4 the 4 modes number 5 when to use each and number 6 a worked example alright so the first topic the too many tools problem and the subtitle is blunt about it give Claude 60 tools and watch it fumble so look at the two sides on the left 60 tools with that many the selection accuracy drops and all the overlapping tools just confuse it now on the right 6 sharp tools with those the choices are faster and more accurate it has the right view

**1:27 → 2:13**

for the job. So notice what is really happening here. It is not that Claude is not clever enough for 60 tools. It is that every extra tool is one more look-alike option to weigh up on every single decision. So more tools does not mean more power. Past a point, it means worse choices. Now here is the warning. Overloading the toolset is a silent quality killer because Claude picks slower and less accurately. So notice that word silent again. Nothing crashes. There is no error. Your agent just quietly gets a little worse at choosing the right tool as the toolbox grows.

**2:13 → 2:49**

So, this is a real design decision. Fewer, sharper tools is not a compromise. It is very often the better system. Alright, so the second topic, scope your tools to the job and the subtitle gives you the rule, every agent gets only the tools that its role needs. So look at the idea, you don't hand every agent every tool. A read-only reporter needs read tools only. A refund agent needs the refund tools.
