---
hovernotes-transcript-of: doc_6a496fcc-2cd5-45cb-b521-4bf5b618a4a7
hovernotes-transcript-version: 2
note: "[[01-CLAUDE-DOT-MD-Hierarchy]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57479739#overview"
updated: 2026-09-10T14:34:59.985Z
---

# 01-CLAUDE-DOT-MD-Hierarchy — Transcript

**5:02 → 5:45**

Closer and the closer rule takes priority. So notice the two ideas here. First they add up, Claude sees all of them together. And second when two of them disagree, the more specific one is the one that wins. Now here is a concrete example of that. Say your personal file asks for 2 space indentation, but the project file asks for 4 space. So which one wins? The project wins because it is the closer more specific rule for this shared work. So think about why that is the right outcome. Your personal preference is perfectly fine in general.

**5:45 → 6:30**

But on this particular team project, the team's shared rule should override your personal taste. So the more specific rule takes priority. Alright, so the fourth topic, nested or directory memory and the subtitle tells you the clever part. Folder rules load only when clod works there. So look at how this works. A clod file inside a folder loads on demand. So a clod file inside your front-end folder kicks in only for front-end files. And that is perfect for large monorepos. Because each area gets exactly the right rules and it ignores all.

**6:30 → 7:15**

the rest. So, notice the efficiency of this. The front-end rules do not clutter things up when Claude is working on the back-end. Each folder's rules appear only when they are actually relevant. Now, here is why this scales so well. A repo with 50 sub-projects won't drown Claude in irrelevant rules because the nested files load only where they apply. So, imagine that huge repo for a moment. If every rule from every sub-project loaded all at once, Claude would be buried under rules that have nothing to do with the task. So, nested files solve exactly that.

**7:15 → 8:01**

only the rules for the folder you are in show up. Alright, so the fifth topic, at import and slash memory, and the subtitle tells you their purpose, keep the file modular and edit it easily. So look at the tools for this. You split the file up and manage it simply. So at import lets you pull in other files, like a shared style file, and slash memory opens your memory files to edit them, and you can type a hash symbol to quick add a rule, and Claude asks which file to put it in. So notice what this gives you, your cloud file does not have to be

**8:01 → 8:46**

one giant block. You can split it, pull pieces in and edit it all quite easily. Now here is an important and honest catch. Imports keep the file organized but everything still loads at launch so it does not actually shrink your context. So please be clear about this because it is a common misunderstanding. Splitting your file into imports makes it tidier for you to read and to manage but cloud still loads all of it when it starts. So imports are for your organization. They are not a way to save context. And here is the handy little habit. You type a hash symbol at the

**8:46 → 9:31**

a message to jot down a rule and then claude asks you which file to save it to so notice how nice this is in the flow up work you spot a new convention mid session so instead of stopping and opening files you just type a hash and your rule and claude files it away for you quick and painless all right so the sixth and final topic what belongs in claude.md and the subtitle gives you the filter. Write what Claude can't guess and skip what it can. So look at what to keep. You

**9:31 → 10:16**

You keep the pitfalls and the conventions that differ from the defaults. And you keep the why behind the rule. So notice the theme. You keep the things that are surprising or particular to your project. The trap that isn't obvious. The convention that isn't standard. And the reason behind it so that Claude understands and does not just blindly obey. Now look at what to cut. You cut the things Claude can figure out for itself. Like the folder layout or the list of dependencies. So notice why you leave those out. Claude can simply look at your project and see the folder structure and read the

**10:16 → 11:01**

So writing those into the file just wastes space on things Claude already knows. So you save the file for what it cannot guess. And here is a firm practical limit. You keep it under about 200 lines because a bloated Claude file actually reduces adherence. Lean high signal files work best. So please take this one seriously because it is counter-intuitive. You might think that more instructions means more control. But the opposite is true. When the file gets bloated, Claude follows it less well. So a short, sharp file full of only the important things is what

**11:01 → 11:46**

gets obeyed. Alright, so the key takeaways from this lecture, cloud.md in three lines. Number one, auto loaded memory. Your cloud file is project memory that cloud reads automatically, so you write it once. Number two, level stack. User, then project, then directory, all combine. And a more specific rule wins. And number three, modular and lean. You use add import to stay modular and slash memory to edit and you keep it rule focused. So notice the single idea underneath this whole lecture. You are teaching cloud your

**11:46 → 12:26**

project once so that it does not have to be re-taught every session so you write down only what Claude cannot guess you put it at the right level user project or directory so the right people and the right folders get it and you keep it lean so that it actually gets followed do that and Claude starts every session already knowing how your project works all right in the next video we look at slash commands and skills so with this I am going to end this one and I will catch you in the next one
