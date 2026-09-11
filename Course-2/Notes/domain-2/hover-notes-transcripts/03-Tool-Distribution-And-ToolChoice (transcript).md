---
hovernotes-transcript-of: doc_3cff9542-0c9f-4635-8b0e-6698f44d9e06
hovernotes-transcript-version: 2
note: "[[03-Tool-Distribution-And-ToolChoice]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460127#overview"
updated: 2026-09-10T13:23:42.106Z
---

# 03-Tool-Distribution-And-ToolChoice — Transcript

**0:00 → 0:00**

All right, everyone. Welcome back.

**2:49 → 3:07**

So, fewer role appropriate tools give you sharper choices. So notice the simple discipline here. You look at what a particular agent's job actually is and you give it exactly that and nothing more. So, a reporting agent is never even tempted by a

**2:59 → 3:05**

Yes, and you give it exactly that and nothing more.

**3:07 → 3:52**

fun tool because it simply does not have one. Now here is the connection back to domain 1. This is the same scoping idea from lecture 1.3. A subagent's allowed tools should list only what its role needs. So cast your mind back. Back then we said leave the tools field open and a subagent inherits everything which was dangerous. So this is that very same principle now seen from the distribution side. Scope tightly per role and you get both safety and sharper selection at the same time. Alright. So the third topic, now we meet the control level two

**3:10 → 2:49**

Now here

**3:52 → 4:37**

and the subtitle explains why it even exists. By default, Claude decides, but sometimes you cannot allow that. So look at how these two work together. Scoping sets the menu, and Tool choice sets the order. So scoping controls which tools even exist, and Tool choice controls whether and which tool gets called right now. So you use it to take the decision back when you need certainty. So notice that these are two separate levers. One decides what is on offer at all, and the other decides what happens on this particular turn. So together they give you full control. Here is the picture that makes it stick.

**4:37 → 5:22**

scoping is the menu and tool choice is whether Claude may order must order or must order one specific dish so think about that restaurant image because it maps perfectly the menu is the list of dishes available and that is your scoping and tool choice is the waiter's rule for this table you may pick anything or you must pick something or you're having the fish and that is decided so three different levels of control over the very same menu all right so the four topic the four modes and the subtitle names them auto any tool and none so

**5:22 → 6:08**

Put all four in order. First, auto. Claude decides and this is the default. Second, any. Claude must use some tool but it picks which one. Third, tool. Claude must use this one named tool every single time. And fourth, none. No tools at all. This turn text only. So notice how this move along a line from freedom to control. Auto is total freedom. Any forces action but leaves the choice open. Tool removes the choice entirely. And none switches tools off for that turn. Now here is a direct instruction for the exam. Memorize all four. Because the exam asks you to pick.

**6:08 → 6:53**

the right mode for a given scenario so please do actually learn these by name a question will describe a situation and expect you to know whether it needs auto any tool or none so this is not background these four words are the answers to a whole set of questions and here is one technical catch to remember any and tool the forced use modes cannot be combined with extended thinking so notice why this is worth knowing when you force Claude to call a tool you are taking away its freedom to stop and think first so force tool use and extended

**6:53 → 7:38**

do not go together. It is a small detail, but it is exactly the kind of thing an exam likes to check. Alright, so the fifth topic, when to use each, and the subtitle gives you the guiding idea, you match the mode to how much certainty you need. So look at them running from free choice to non-negotiable. Auto is for ordinary check assistance. Any is for you must act, but you choose how. Tool is for guaranteed output or an always save step. And none is for asking without acting or a plain text only turn.

**7:38 → 8:23**

you are choosing based on certainty. If you are happy for Claude to decide freely, you use auto. And the more the outcome simply must be guaranteed, the further along you slide towards tool. Now here is the key one to hold on to. You reach for tool when a step is genuinely non-negotiable. For example, a research agent that must call save report before it finishes. So think about that example. You do not want the agent to sometimes save and sometimes forget. That save has to happen every single time. So forcing the tool is exactly how you turn a hopeful usually into a

**8:23 → 9:08**

guaranteed always. Alright, so let's see that in a worked example, always save the report and the subtitle names the goal exactly. Turning usually saves into always saves. So look at the first design on auto which is risky. Here the agent sometimes just replies in text and when it does the findings are lost. So notice the quiet danger. On auto saving the report is only a strong suggestion. So most of the time it saves. But every so often it decides a text reply is enough and all of that work simply vanishes unsaved. you may not even notice.

**9:08 → 9:52**

until you go looking for a report that was never written. Now look at the second design with a forced tool which is safe. Here you set tool choice to type tool with the name save report and because of that it saves on every single run. So notice what you have done. You have removed the choice entirely. The agent no longer decides whether to save. Saving is simply what this turn does. So usually saves has become always saves with one small setting. And here is a note for the road ahead. forcing a specific tool is the standard trick.

**9:52 → 10:37**

for guaranteed structured output and we will reuse it in domain 4 so tuck this away whenever you absolutely need Claude's answer in a fixed shape you can force the tool that produces that shape so it is not just for saving reports it is a general technique and it comes back when we do structured output properly alright so the key takeaways from this lecture distribution and tool choice in three lines number one fewer scoped tools a giant toolbox hurts selection so you give each role only what it needs number two know the four modes

**10:37 → 11:22**

The simple choice can be auto to decide any for some tool, tool, for this tool or none for no tools. And number three, force it when it must happen. You use tool for an always safe step and for guaranteed structured output. So notice the two levers this whole lecture handed you. The first is scoping that decides which tools even exist for a given agent and fewer sharper tools give better choices. And the second is tool choice that decides what happens on this one turn from letting Claude choose freely all the way to forcing one exact tool. So most of the time you let Claude decide what happens on this one turn from letting

**11:22 → 11:58**

But when a step simply must happen, you now know how to take that decision back completely. Alright, in the next video, we plug Claude into the outside world through one standard connector. This is MCP server integration. That means what MCP actually is, tools versus resources, connecting a server, keeping your secrets safe, the three scopes, precedence, and running multiple servers. So with this, I'm gonna end this one, and I will catch you in the next one.
