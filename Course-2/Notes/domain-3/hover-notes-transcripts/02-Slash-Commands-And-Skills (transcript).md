---
hovernotes-transcript-of: doc_c24367dc-785e-44d9-8566-0448e2b8cc1d
hovernotes-transcript-version: 2
note: "[[02-Slash-Commands-And-Skills]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57479743#overview"
updated: 2026-09-10T15:18:42.900Z
---

# 02-Slash-Commands-And-Skills — Transcript

**0:00 → 0:41**

So, in the last lecture, we taught Claude our project once with Claude.md. That was always on memory that Claude reads at the start. Now we do the other half. We save the actions we run again and again, so that we can fire them off with a single word. This is slash commands and skills. Save a workflow once and run it with one word. So six things in this lecture. Number one, the repetition problem. Number two, custom slash commands. Number three, command front matter. Number four, skills.

**0:41 → 1:26**

Number five, the skill front matter that matters. And number six, commands and skills versus Claude.md. All right, so the first topic, the repetition problem and the subtitle names the pain exactly. Stop retyping the same long instruction. So look at the fix. You save it once as a command like slash review because typing the same long paragraph every time quietly drips. One day you forget a step. So you capture it once and then you run it identically every time. So please notice the real problem being solved. When you retype a long instruction,

**1:26 → 2:12**

by hand, it is never quite the same twice. A word changes here, a step gets dropped there. So saving it once freezes it perfectly, so that it runs the same way every single time. Now here is the picture for it. A saved command is like speed dial. It is the same precise instruction under one short name every time. So think about speed dial on a phone. You do not dial the whole number, digit by digit and risk a mistake. You press one button. So a command is exactly that. All of that careful detailed instruction tucked behind one short name that you can find

**2:12 → 2:57**

instantly alright so the second topic custom slash commands and the subtitle tells you how simple they are a markdown file becomes a command so look at how you make one you drop a file into the dot cloud commands folder and that can be project scope in the projects dot cloud commands folder or personal in your home folder so the file name becomes the command and the body of the file becomes the prompt and you use a placeholder dollar arguments which drops your input straight into the prompt so for example a file called fix issue dot

**2:57 → 3:42**

d gives you the command slash fix issue and if you run slash fix issue one two three then dollar arguments becomes one two three so notice how little they release to it a markdown file its name and its body that is the whole command now here is the scope point to hold on to project scope is committed so the whole team gets the command but the home folder version is just you so notice the parallel with the last lecture it is the same split as claude.md put a command in project scope and commit it and everyone shares it keep it in your home folder and it stays personal to you.

**3:42 → 4:27**

per command, whether it is a team tool or your own. Alright, so the third topic, command front matter, and the subtitle tells you why it is worth it. A few lines of config make the command robust. So, look at the first two fields. First, description, this shows up in slash help, and it lets Claude auto suggest the command. And second, argument hint, this gives an auto complete hint for the input. So notice what these two do for you. The description makes the command discoverable, both to you in the help list and to Claude. And the argument has to be used.

**4:27 → 5:12**

that nudges you on what to type when you call it. So small touches that make the command genuinely easy to use. Now the next two fields, allowed tools which pre-approves the tools that the command needs and model which lets you paint a cheaper faster model. Allowed tools means the command tools are approved upfront so it does not stop mid-run to ask for permission. And model lets you say for this particular command use a lighter quicker model. So the command runs smoothly and it runs efficiently. And here is one more thing the description does. It also lets Claude offer the command automatically.

**5:12 → 5:57**

when your request matches it. So think about how helpful that is. You describe what you want in plain words. And Claude notices, oh there is a save command for exactly this and it offers to run it. So a good description does not just sit in a help menu. It lets Claude reach for your command on your behalf. Alright so the fourth topic, skills, the richer form and the subtitle tells you the story in four words. Commands grew up into skills. So look at what has happened. Commands are now merged into skills. So a skill.md file in the .sql.md file.

**5:57 → 6:43**

Claude skills folder also gives you a slash command by its name, but it adds a whole folder for supporting files, and it brings auto-discovery, so that Claude can invoke it when it is relevant. So notice the two big additions here. A skill is not just a single file, it gets a folder for the extra files it might need, and it can be triggered by Claude itself, not only by you. Now here is the summary, it is the same slash command, but with more power. Skills carry extra files and they can be invoked by Claude and not just by you and on a name clash the

**6:43 → 7:28**

wins so notice that last detail because it is exactly the kind of thing an exam checks if a command and a skill share the same name the skill is the one that runs so the richer form takes priority all right so the fifth topic the skill front matter that matters and the subtitle is very direct these are three fields the exam cares about so look at the three fields first context for which runs the skill in an isolated context second allowed tools which pre-approves tools but and this is important does not really

**7:28 → 8:13**

them and third disable model invocation set to true which means only you can trigger the skill so notice what each one is really for context for keeps a noisy skill from polluting your main conversation allowed tools smooths out the approvals and disable model invocation puts you and only you in charge of firing it and here is the warning and it is the classic trap allowed tools pre-approves the listed tools it does not block the others every other tool stays available so So please read that one very carefully because the name is

**8:13 → 8:58**

Allowed tools sounds like a whitelist that shuts everything else out, but it does not. It simply pre-approves the tools you list so that they run without prompts. Every other tool is still there and still usable. So it is about approval and not restriction. Now here is where that third field really earns its keep. You use disable model invocation for side effect commands, things like slash commit or slash deploy so that cloud never fires them on its own. So think about why that matters so much. Committing code or deploying are actions with real consequences.

**8:58 → 9:43**

You do not want Claude deciding all by itself to deploy. So you set disable model invocation and now those dangerous commands can only be triggered deliberately by you. Alright, so the sixth and final topic, Commands and Skills vs Claude.md. And the subtitle frames the choice, always on rules or on-demand actions. So look at the two sides. On one side, Claude.md. That is passive context that Claude always reads. It is for your standing conventions, on the other side a command or a skill. That is an action that you or Claude invoke.

**9:43 → 10:36**

is for repeatable tasks on demand. So notice the clean split between them. One is always there quietly shaping every session and the other sits waiting and only runs when it is called. Now here is the rule to decide between them. A standing convention goes in cloud.md. A repeatable task becomes a command or a skill and both of them come in project and personal scope. So ask yourself one simple question. Is this a rule that should always be true? Then it belongs in cloud.md. Or is it an action I run now and then, then it is a command or a skill?

**10:36 → 11:14**

So always on vs on demand. That is the whole decision. Alright, so the key takeaways from this lecture, Commands and Skills in 3 lines. Number 1, a file becomes a command. A markdown file in the .cloud commands folder becomes a slash command. And dollar arguments passes your input in. Number 2, skills add power. A skill.md adds supporting files, auto discovery, and the context fork option. And number 3, on demand vs always on. Allow tools pre-approves, it does not restrict. And remember, cloud.md is always on demand.

**11:14 → 11:59**

while commands are on demand. So notice how neatly this sits right next to the last lecture. Claude.md was the always-on memory, the standing rules. And commands and skills are the on-demand actions, the save workflows. So you write a rule when something should always be true. And you save a command when something is a task you keep repeating. So between the two lectures, you now have both halves, what Claude always knows and what Claude can do on command. Alright, in the next video, we look at path-specific rules. So with this, I'm going to end this one and I will catch you in the next one.
