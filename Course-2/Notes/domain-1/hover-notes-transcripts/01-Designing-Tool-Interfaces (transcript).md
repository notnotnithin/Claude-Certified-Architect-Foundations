---
hovernotes-transcript-of: doc_15091248-d393-4757-9aec-5c6f62a792d3
hovernotes-transcript-version: 2
note: "[[01-Designing-Tool-Interfaces]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460121#overview"
updated: 2026-09-10T12:51:54.202Z
---

# 01-Designing-Tool-Interfaces — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So we are now starting domain 2 and this domain is all about tools, tool design and mcp integration. And you might remember, right at the end of the last domain I said something. An agent is only as good as the tools you give it. So now we make good on that and the very first lecture is about how you describe those tools. This is designing tool interfaces because the tool is only as good as the way you describe it. So 6 things in this lecture. Number 1, tools are Claude's hands. Number 2, the description is how Claude picks.

**0:42 → 1:27**

3. The anatomy of a great description. 4. Naming to kill ambiguity. 5. Split vs. Consolidate. 6. The cost of a vague tool. Alright, so the first topic. Tools are Claude's hands. And the subtitle puts it nicely. Talk is cheap, but tools let Claude act. So look at the definition. A tool is a function that Claude can call to do something like look up an order, send an email, or query a database. Because without tools, Claude can only talk. And each tool is one action that Claude can reach for. So please notice.

**1:27 → 2:12**

gift here on its own. Claude is a very clever thing that can only produce words. A tool is what turns those words into actions in the real world. So each tool you give it is one more thing it can actually do instead of merely describe. Now here is a connection straight back to domain 1. Remember the loop from lecture 1.1. Claude asks for a tool and your code runs it. And a tool is exactly that thing that Claude can ask for. So this ties the two domains together. Back then we said Claude requests and your code executes. So a tool is simply one of the things it is a lot.

**2:12 → 2:57**

request and in this domain we are going to design those requests properly all right so the second topic the description is how claude picks and the subtitle reveals the key limitation claude can't see your code it can only see your description so look at how selection actually works claude selects a tool from its name and its description it cannot see inside your function at all so a vague description means the wrong tool gets picked or no tool at all it is like a shopkeeper reading only the the label on each box.

**2:57 → 3:43**

please sit with that limitation because it is the heart of this whole lecture. Claude has no idea what your code does inside. It cannot peek in. All it has to go on is the little label you wrote. So if that label is unclear, Claude is choosing blind. Now, here is the big idea and the exam tests this directly. The description is the selection mechanism. So you write it for Claude and not for yourself. So notice that last part especially. It is tempting to write a description as a quick note to yourself, the developer. But Claude is the one reading it to make a choice. so you

**3:43 → 4:28**

write it as instructions to Claude. What is this for and when should you pick it? That is what the description is really for. Alright, so the third topic, the anatomy of a great description. And the subtitle lists the parts. Say what it does, when to use it, and what to pass. So look at the four parts of a good description. First, what it does, the action in one clear line. Second, when to use it. And just as importantly, when not to use it. Third, each parameter explained in plain words. And fourth, a short example, one tiny sample call. So,

**4:28 → 5:13**

Notice that this 4 cover everything Claude needs to choose well and to call correctly. What the tool is for, when it is the right pick, what to put in each field, and what a real call actually looks like. Now here is the one that matters most and it is the one people skip. When to use it and really when not to use it. Because that is exactly what stops Claude reaching for the wrong tool. So think about why. Most descriptions say what a tool does and that is fine. But two tools can both sound reasonable for a job. So the line that says use this one when and not that other one is

**5:13 → 5:58**

Let's Claude tell them apart. So never skip the when to use it part. Alright, so the four topics name your tools to kill ambiguity. And the subtitle warns you why. If two tools sound the same Claude will mix them up. So look at the vague confusing vague first. You have got get data versus fetch data. And honestly which one does what. So notice the problem instantly. Get data and fetch data mean almost the same thing in plain English. So even you cannot tell them apart from the names alone. And if you cannot then Claude certainly cannot either.

**5:58 → 6:43**

So it ends up guessing between two names that sound identical. Now look at the distinct, clear way. You have got get order by ID and search orders by customer. So notice how much those two names now tell you. The first one fetches a single order when you already know its ID. The second one searches for many orders by a customer. There is no overlap left between them. So just from the names alone, Claude knows exactly which one fits the job in front of it. And here is the warning. Overlapping names and overlapping descriptions are a top cause of wrong tool errors. So you make.

**6:43 → 7:28**

Each tool's job obvious and non-overlapping. So please take this one seriously because it is a very common mistake. When two tools blur into each other, Claude will sometimes pick the wrong one quietly. So the fix is in your hands right at design time. Give each tool a name that could only ever mean one thing. Alright, so the fifth topic, Split vs Consolidate. And the subtitle poses the question, one giant tool or many small ones. So here is the guiding idea. You size your tools around the choices that Claude has to make.

**7:28 → 8:14**

So you split when the jobs are distinct because that gives clearer selection. And you consolidate steps that always go together because that means fewer round trips. So you avoid both extremes, too many tiny tools and also one do everything tool. So notice that this is a balance and not a hard rule. You are trying to match the shape of your tools to the actual decisions that Claude needs to make. Now here is why both extremes hurt you. Too many tiny tools overwhelm the selection and one do everything tool becomes too vague to describe. Think about each failure on one.

**8:14 → 8:59**

On the other side, if you have 50 little tools, Claude has too many look-alike options and selection gets unreliable. On the other side, if you have one giant tool that does everything, its description has to be so broad and so woolly that Claude can never be sure what it really does. So you aim for the sensible middle. Alright, so let's make that concrete with a worked example, Booking Travel. And the subtitle sets it up. The same feature designed two ways. So look at the first design, one mega tool. it is called handle travel and it takes an action parameter

**8:59 → 9:44**

And the problem is Claude must guess the action string. So notice what that means in practice. Claude has to somehow know that it should pass, book, or search, or cancel as a kind of magic word inside that action field. And if it guesses that string wrong, the whole call goes wrong. So you have pushed the hard decision down into a field where Claude is just guessing. Now look at the second design. Three clear tools. Search flights, book flight, and cancel booking. And each one does exactly one job. So notice how the guessing has completely

**9:44 → 10:29**

There is no mysterious action string to get right. If Claude wants to book, it calls book flight. So the choice is now made by picking the tool itself, which is exactly the thing Claude is good at. And here is the lesson. Distinct actions should become distinct tools. So Claude picks book flight unambiguously instead of guessing an action value. So this is the whole split idea made real. Three genuinely different actions became three genuinely different tools. And a decision that used to be a risky guess is now just a clean obvious tool choice.

**10:29 → 11:14**

So the sixth and final topic, the cost of a vague interface. And the subtitle carries a real warning. Bad design doesn't crash. It quietly misbehaves. So look at how these failures actually show up. They are silent, not loud. Maybe the wrong tool gets chosen or the wrong parameters get filled in or Claude just gives up and answers in plain text instead. And it all shows up as a subtly wrong behavior in production. So please notice why this is so dangerous. A vague interface does not give you a nice red error. It gives you an agent that mostly works but is

**11:14 → 11:59**

wrong here and there and that is a great deal harder to catch and here is the warning stated plainly you won't see a neat error you will see subtly wrong behavior so you invest in the interface before the logic so notice that piece of advice because it flips the usual instinct most people rush straight to the clever logic inside the tool but if the description and the names are vague claude will call your perfect logic at the wrong time with the wrong inputs so get the interface right first. It is the thing everything else depends on. Alright, so the key

**11:59 → 12:45**

from this lecture tool design in three lines number one the description is the interface Claude picks tools from their name and their description so you write for Claude number two clear and distinct you say what it does when to use it the parameters and an example and distinct names kill ambiguity and number three right size your tools you split distinct actions and you consolidate steps that always go together so notice the one idea holding this whole lecture together Claude cannot see your code it only ever sees

**12:45 → 13:30**

interface you wrote. So the name and the description are not documentation you tack on at the end. They are the actual control panel that Claude uses to choose. So get them clear, get them distinct, and get them right sized, and Claude reaches for the right tool every time. But get them big and it quietly reaches for the wrong one. Alright, in the next video we'll look at what happens when a tool fails. Because when it does, your error message is Claude's only clue. This is structured error responses. That means how errors are Claude's window into failure, the isError flag, error categories, Yes.

**13:30 → 13:42**

is retrieval, empty result versus a real failure, and writing a genuinely useful error. So with this, I'm going to end this one, and I will catch you in the next one.
