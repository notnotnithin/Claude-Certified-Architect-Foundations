---
hovernotes-transcript-of: doc_8b9aed11-021e-40e6-a5bf-09c7394f2130
hovernotes-transcript-version: 2
note: "[[03-Structured-Output-With-Tool-Use]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57493851#overview"
updated: 2026-09-11T05:45:09.053Z
---

# 03-Structured-Output-With-Tool-Use — Transcript

**0:00 → 0:43**

Alright everyone, welcome back. So in the last lecture, we made Claude's output more reliable by showing it examples. But for real automation, reliable is not quite enough. Your code needs a guarantee. Clean data in a fixed shape that it can trust every single time. This lecture is structured output with tool use, so that you get back clean JSON that your code can trust every time. So 7 things in this lecture. Number 1. Why free text is unreliable. Number 2. How tool use forces structure. Number 3. The JSON schema. Number 4. Thank you.

**0:05 → 0:00**

teammate clods out

**0:43 → 1:28**

required, optional and nullable 5. Enums and the other escape hatch 6. Tool choice 7. What it does not fix Alright, so the first topic, why free text is unreliable? and the subtitle says it plainly Your code cannot depend on a paragraph So look at the problem, usually valid is just not good enough for automation because Claude might add a little phrase like here's the data or it might wrap the output in markdown fences or it might quietly rename a field and then one stray sentence and you are passed away

**1:28 → 2:13**

So please notice the real issue here. A human reading the reply would not care about a friendly hears the data. But a program trying to read it automatically is very fragile. One unexpected word and the whole thing falls over. Now here is the key distinction. For a chat reply all of that is perfectly fine. But for a pipeline feeding a database it fails. So we need a guarantee and not a hope. So notice those two words at the end. Guarantee versus hope. Free text is a hope. It usually works. But feeding a database automatically you cannot run on usually.

**2:13 → 2:58**

that works every single time. Alright, so the second topic, how tool use forces structure. And the subtitle reveals a neat trick. Claude has no dedicated JSON mode. So it uses tools instead. So look at how this works. You define a tool, and then Claude's answer is that tools input. So you give a tool an input schema describing your fields. And Claude calls that tool with structured data. So you get back a clean tool use block, and not prose. So let me make that concrete. Normally calling a tool is about doing an app.

**2:58 → 3:43**

But here, we use it in a clever way. The tool is just the shape that you define. And when Claude fills in that tool's inputs, those inputs are your structured answer. And here is the pattern to remember. Anthropics structured output pattern is forced tool use. You define the shape as a tool schema and Claude fills it in. So please lock this in because it is the core idea of the whole lecture. There is no special give me JSON button. Instead you describe your desired shape as a tool. And getting Claude to call that tool is how you get guaranteed structure back. Alright. So the third thing is,

**3:43 → 4:29**

topic, the JSON schema and the subtitle gives you the picture. The schema is your blueprint for the answer. So look at the schema. It is called an input schema and it names every field with its type. So for example, take a tool called extract claim. Its input schema might have a claim ID, which is a string and amount, which is a number and a date, which is a string. So it names every field, its type and which ones are required. So notice what the schema is doing. It is a blueprint. It lays out exactly what fields you expect, what type each one is.

**4:29 → 5:14**

whether it is text or a number and which ones must be there and here is a practical tip a malformed schema is rejected upfront you get a 400 error before cloud even runs so you validate your schema first so notice the useful thing here if you make a mistake in your schema itself the system catches it immediately and cheaply before spending anything on running cloud so it pays to get the blueprint right first all right so the fourth topic and this one is really important field types required versus nullable. And the subtitle contains

**5:14 → 5:59**

the warning make a field required and Claude will invent it when it is missing. So this whole slide is the root cause fix for fabricated fields. So notice that phrase root cause, we are not patching a symptom here, we are fixing the actual reason that Claude invents data and it comes down to how you mark your fields. So look at the first case, required leads to fabrication. Imagine a phone field typed only as a string, so it is marked as required. Now what happens if the document has no phone number? Well, because the field is required, Claude

**5:59 → 6:44**

it must produce one. So it invents a number. So notice the trap. By insisting the field is always there, you have accidentally forced Claude to make one up when it isn't. Now look at the better case, nullable stays honest. Here the phone field is typed as string or null. So now if the phone number is missing, Claude can simply return null, which just means nothing there. So notice the difference this makes. By allowing null, you have given Claude a truthful option. It no longer has to invent a number. It can honestly say there wasn't one.

**6:44 → 7:29**

Here is the rule spelled right out. The root cause fix is to make the fields that the document might not have, optional or nullable. You do not just say, don't guess, and you mark only the always present fields as required. So please take this to heart because it is heavily tested. The wrong fix is to add, please don't make things up to the prompt. The right fix is structural. If a field might genuinely be missing, you make it nullable. So Claude has a legal way to leave it empty. Alright, so the fifth topic, enums and the other escape hatch.

**7:29 → 8:15**

subtitle explains the balance. You constrain a field to a fixed list, but with a safety valve. So look at the idea. You use an enum for consistency, and you add an other plus a detail field for honesty. So let me unpack that. An enum is just a fixed list of allowed values. So for a claim type, you might allow auto, home, health, and other, plus a detail field, a string that gets used when the type is other. So notice both parts. The fixed list keeps things consistent. Claude must pick from your options. And the other plus detail is the safety valve for anything that doesn't fit.

**8:15 → 9:00**

And here is why that escape hatch matters. An Anum with no escape forces Claude to jam an odd input into the closest wrong option. But Other plus detail keeps it honest. So think about what happens without it. Say a claim doesn't fit any of your categories. If the only options are auto, home and health, then Claude has to pick one of them and it will be wrong. So by adding Other, you give it an honest place to put the unusual cases. And the detail field captures what it actually was. Alright, so the sixth topic.

**9:00 → 9:45**

Guaranteeing the call and the subtitle tells you the goal. You make sure Claude actually uses the tool. So look at the first mode, Auto. With auto Claude may just reply in text. So there is no guarantee. So notice the danger. On auto calling your tool is optional. For Claude it might do it. Or it might just answer in prose. And prose is exactly what we were trying to avoid. Now the second mode, Any. This one forces some tool. So you use this one for structured output. So notice why this is the safe choice. With any Claude must call a tool. It cannot wander off into prose.

**9:45 → 10:30**

So for guaranteed structured output, this is usually the mode you want. And the third mode, tool. This forces one specific named tool. So notice the difference from any. With any, Claude must call some tool, but it chooses which. With tool, you name the exact one it must call. So when you have one specific extraction tool and you want to guarantee that one gets used, this is the mode. And here is a connection back to domain 2. We taught the four modes back in lecture 2.3. And here we are applying them. So remember this.

**10:30 → 11:15**

on auto, Claude can skip the tool and hand you prose. So this is where that earlier lesson plays off. You already learned these modes and now you can see exactly why they matter. For structured output, you do not leave it on auto. You force it with any or tool. Alright, so the seventh and final topic. What structured output does not fix? And the subtitle is a crucial warning. Valid JSON can still be wrong. So look at the first half. Syntax. This is solved. So malformed JSON is guaranteed gone. don't

**11:15 → 12:00**

always returns well-formed data. So let me explain. Syntax simply. Syntax is about the shape being correct. Are the brackets closed? Are the fields named properly? And tool use guarantees all of that. The shape will always be valid. Now look at the second half. Semantic, this is not solved. So you can still get numbers that don't add up. Or a value in the wrong field. Or a fabricated value. So let me explain. Semantic simply. Semantic is about the meaning being correct. And that structured output does not touch. So the JSON can be perfect.

**12:00 → 12:46**

well-formed and still contain wrong numbers. And here is the line to remember above all, structured output guarantees the shape, but never the truth, and checking that meaning is exactly what the next lecture is about. So please hold on to this because it is a very common misunderstanding. People think if the JSON is valid, then the data must be right. But no, valid only means well-shaped. Whether the values are actually correct is a completely separate question. And that is where we go next. Alright, so let's pull this together, the key takeaways from this lecture.

**12:46 → 13:31**

Structured output in three lines 1. Force the shape You use tool use plus a JSON schema And you use tool choice either any or a name tool to guarantee the call So remember there is no JSON mode You force the shape through a tool 2. Design against fabrication You make uncertain fields optional or nullable And you use anums with an other and detailed escape So remember the root cause fix for invented data is structural It is in how you mark your fields Not in a plea in the prompt And number 3. Syntax not meaning Structured

**13:31 → 14:02**

output kills syntax errors but it never guarantees that the values are correct so remember valid json can still be wrong the shape is guaranteed the truth is not all right so that is how you get clean guaranteed json in the next lecture we will look at validation and retry loops so with this i am going to end this one and i will catch you in the next one
