---
hovernotes-transcript-of: doc_e32fe6bc-bf22-4784-be96-25c99359f1ac
hovernotes-transcript-version: 2
note: "[[05-Built-In-Tools]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460133#overview"
updated: 2026-09-10T14:07:51.954Z
---

# 05-Built-In-Tools — Transcript

**0:00 → 0:44**

So, in the last lecture, we connected external tools through MCP. But Cloud Code also comes with its own small set of tools built right in. And knowing them well is what makes it feel fast and precise. So this lecture is about those built-in tools, the toolkit that Cloud Code ships with, and how to pick the right one. So six things in this lecture. Number one, the six built-in tools. Number two, grep versus glob. Number three, read, edit, and write. Number four, read before edit. Number 5, preferring built-ins over bash and number 6,

**0:42 → 1:27**

bash and number six exploring incrementally all right so the first topic the six built-in tools and the subtitle sets the tone a small toolkit where each tool has one clear job so look at the first three read which opens and views a file write which creates or overwrites a file and edit which changes just part of a file so notice already that these three are all about files one to look at a file one to replace a whole file and one to change a piece of a file so three very different jobs and we will come back to exactly

**0:44 → 1:30**

exploring incrementally. Alright, so the first topic, the six built-in tools and the subtitle sets the tone. A small toolkit where each tool has one clear job. So look at the first three, read which opens and views a file, write which creates or overwrites a file, and edit which changes just part of a file. So notice already that these three are all about files. One to look at a file, one to replace a whole file, and one to change a piece of a file. So three very different jobs, and we will come back to exactly how they differ. Now look at the next three.

**1:27 → 2:12**

how they differ. Now look at the next three bash which runs shell commands, grep which searches inside files and glob which finds files by their name. So notice that these three are about searching and running. Grep looks inside your files for text, glob finds files by their names and bash is the general one for running commands. So six tools in total and each one with a single narrow purpose and here is the point of learning them well. These are the tools you will see most in cloud code. Each one has a single job.

**1:30 → 2:15**

bash which runs shell commands grep which searches inside files and glob which finds files by their name so notice that these three are about searching and running grep looks inside your files for text glob finds files by their names and bash is the general one for running commands so six tools in total and each one with a single narrow purpose and here is the point of learning them well these are the tools you will see most in cloud code each one has a single job and the wrong pick wastes tokens and time.

**2:12 → 2:57**

and the wrong pick wastes tokens and time. So please take this seriously because it is very practical. These six come up constantly. So knowing exactly which one fits, which job is not just trivia. It is the difference between a quick, clean action and a slow, wasteful one. All right, so the second topic, and this is the big one. Grap versus Glob, the number one confusion. And the subtitle tells you the split. Search inside files or find files by name. So look at the first one. Grap is for contents. It searches inside your files, for example.

**2:15 → 3:01**

So, please take this seriously because it is very practical. These six come up constantly. So knowing exactly which one fits, which job is not just trivia. It is the difference between a quick clean action and a slow wasteful one. Alright, so the second topic and this is the big one. Grap vs. Glob. The number one confusion. And the subtitle tells you the split. Search inside files or find files by name. So look at the first one. Grap is for contents. It searches inside your files. For example, find where process order is called.

**2:57 → 3:42**

Find where process order is called. So notice what grep is really doing. It is opening up your files and looking at the text inside them. So whenever your question is about what is written in the code, that is a grep job. Now look at the second one. Glob is for file names. It matches file parts and names. For example, find every star.test.js file. So notice the difference clearly. Glob does not care what is inside the files at all. It only looks at their names and their parts. So, whenever your question is about which files exist, buy

**3:01 → 3:46**

So, notice what grep is really doing. It is opening up your files and looking at the text inside them. So whenever your question is about what is written in the code, that is a grep job. Now look at the second one. Glob is for file names. It matches file parts and names. For example, find every star.test.js file. So notice the difference clearly. Glob does not care what is inside the files at all. It only looks at their names and their parts. So whenever your question is about which files exist by name, that is a glob job and here is why.

**3:42 → 4:28**

that is a glob job and here is why this matters so much the exam test this directly and it penalizes mixups so remember it simply contents means crap file names means glob so please burn that one line into your memory if you are searching for text inside files it is grab if you are finding files by their names it is glob contents grab file names glob get those two the wrong way round and the exam will catch you alright so the third topic read edit and write together and the subtitle explains the three jobs see a file change

**3:46 → 4:31**

matters so much. The exam tests this directly and it penalizes mixups. So remember it simply contents means grep, file names means glob, so please burn that one line into your memory. If you are searching for text, inside files it is grep, if you are finding files by their names it is glob, contents grep, file names glob, get those two the wrong way round and the exam will catch you. Alright, so the third topic, read, edit and write together and the subtitle explains the three jobs, see a file, change part of it or replace the whole thing.

**4:28 → 5:13**

part of it or replace the whole thing. So look at the three in order. First read, you view the file, then edit. That is a precise change and exact string replace and then write. That creates or overwrites the whole file. So notice how they grow in false. Read touches nothing, it just looks. Edit changes one exact piece and write replaces everything. So three levels from looking to a small change to a full rewrite. Now here is the key habit. For a small change, you use edit and not write. Because edit shows a clean diff while write rewrites everything.

**4:31 → 5:16**

the three in order first read you view the file then edit that is a precise change an exact string replace and then write that creates or overwrites the whole file so notice how they grow in false read that is nothing it just looks edit changes one exact piece and write replaces everything so three levels from looking to a small change to a full rewrite now here is the key habit for a small change you use edit and not write because edit shows a clean diff while write rewrites everything so think about why that matters if you only

**5:13 → 5:58**

why that matters. If you only want to change one line, edit changes exactly that line and you can see precisely what moved, but write throws away the whole file and lays down a fresh one so you cannot easily see what actually changed. So, for small changes, edit is both safer and clearer. Alright. So, the fourth topic, the golden rule, read before edit. And the subtitle states it plainly. Claude must see a file before it can change it. So, look at the rule and its details. Edit requires a prior read. So, the target text must match exactly

**5:16 → 6:01**

change one line edit changes exactly that line and you can see precisely what moved but write throws away the whole file and lays down a fresh one so you cannot easily see what actually changed so for small changes edit is both safer and clear all right so the fourth topic the golden rule read before edit and the subtitle states it plainly claude must see a file before it can change it so look at the rule and its details edit requires a prior read so the target text must match exactly and it must be unique. Not unique, then you watch

**5:58 → 6:43**

must be unique. Not unique, then you widen the surrounding text or you use replace all. And if you can't get a clean match at all, then read plus write is your last resort fallback. So notice why the read has to come first. Edit works by finding an exact piece of text and swapping it out. So Claude has to have actually read the file to know that exact text is there and to know that it appears only once. And here is the warning. A non-unique or a stale match fails. So you pin one spot by widening the text. So think about what goes wrong. If the text you are matching appears in five places.

**6:01 → 6:47**

the surrounding text or you use replace all and if you can't get a clean match at all then read plus write is your last resort fallback so notice why the read has to come first edit works by finding an exact piece of text and swapping it out so claude has to have actually read the file to know that exact text is there and to know that it appears only once and here is the warning a non-unique or a stale match fails so you pin one spot by widening the text so think about what goes wrong if the text you are matching appears in five places edit cannot know which one you meant So we just...

**6:43 → 7:28**

edit cannot know which one you made so it just fails and the fix is to include more of the surrounding lines until your match points at one single unmistakable spot and one more important point read plus write is the fallback it is not the default so you always prefer a precise edit so please notice this because it is easy to get lazy here rewriting the whole file with write feels simpler but it is heavier and it hides what actually changed so you only fall back to read plus write when a clean edit is genuinely not possible the precise edit is always

**6:47 → 7:32**

fails and the fix is to include more of the surrounding lines until your match points at one single unmistakable spot and one more important point read plus write is the fallback it is not the default so you always prefer a precise edit so please notice this because it is easy to get lazy here rewriting the whole file with write feels simpler but it is heavier and it hides what actually changed so you only fall back to read plus write when a clean edit is genuinely not possible the precise edit is always the first choice

**7:28 → 8:14**

the first choice. Alright, so the fifth topic. Prefer the built-ins over bash and the subtitle gives two quick examples. Use read not cat. Use the built-in grep tool not the raw grep command. So look at the built-in tools first. Read, grep, glob and edit and these give you better permissions, a clearer trail and results that can be cached. So notice those three advantages. The built-ins fit properly into the permission system. They leave a clean record of what happened and the results can be reused from a cache.

**7:32 → 8:17**

Alright, so the fifth topic, prefer the built-ins over bash and the subtitle gives two quick examples. Use read, not add. Use the built-in grep tool, not the raw grep command. So look at the built-in tools first. Read, grep, glob and edit. And these give you better permissions, a clearer trail and results that can be cached. So notice those three advantages. The built-ins fit properly into the permission system. They leave a clean record of what happened and the results can be reused from a cache. So they are simply better behaved inside CloudCon.

**8:14 → 8:59**

So they are simply better behaved inside cloud code. Now look at the bash one liners, things like cat, grep, find and said. And the problem is, these bring extra permission prompts that cannot be cached. So notice the cost. Every time cloud reaches for a raw shell comment like cat, it can trigger another permission prompt and none of that work can be cached and reused. So doing by hand in bash what a built-in already does for you, just adds friction. And here is the balance advice, you save bash for what it is uniquely good at, which is

**8:17 → 9:02**

Now look at the bash one liners, things like cat, grep, find and said. And the problem is, these bring extra permission prompts that cannot be cached. So notice the cost. Every time Claude reaches for a raw shell command like cat, it can trigger another permission prompt and none of that work can be cached and reused. So doing by hand in bash what a built-in already does for you, just adds friction. And here is the balance advice, you save bash for what it is uniquely good at, which is is actually running things. Like your tests,

**8:59 → 9:44**

running things like your tests or a build. So notice that this is not never use bash. Bash is essential for the things that only it can do. Running your tests with kicking off a build, executing a real command. So use the built-ins for reading and searching and editing and save bash for actually running things. Alright, so the sixth and final topic. Explore incrementally and the subtitle gives you a lovely image. Don't read the whole library. Use the catalog. So look at the approach. You find first and then you read only what matters.

**9:02 → 9:47**

or a build. So, notice that this is not never use bash. Bash is essential for the things that only it can do. Running your tests with kicking off a build, executing a real command. So use the built-ins for reading and searching and editing. And save bash for actually running things. Alright, so the sixth and final topic. Explore incrementally and the sub-petal gives you a lovely image. Don't read the whole library. Use the catalog. So, look at the approach. You find first and then you read only what matters. So you use grep.

**9:44 → 10:29**

So you use grep or glob to locate the few files that actually matter and then you read only those and you never read every file upfront. So notice the order here. First you search to narrow things down then you read but only the handful that the search pointed you to. So you do not open everything and hope. Now here is why this discipline matters. Reading everything blows your context budget. So you locate first and read narrowly. So think about that library image again. again, reading every single file to find one thing is like reading

**9:47 → 10:32**

to locate the few files that actually matter and then you read only those and you never read every file upfront so notice the order here first you search to narrow things down then you read but only the handful that the search pointed you to so you do not open everything and hope now here is why this discipline matters reading everything blows your context budget so you locate first and read narrowly so think about that library image again reading every single file to find one thing is like reading every book in the library just to answer

**10:29 → 10:57**

every book in the library just to answer one question it is enormously wasteful so you check the catalog first and that is your grep and your glob and then you pull down only the two or three books you actually need and here is a pointer to what is coming managing that context budget properly is the whole of domain 5 but the good habit starts right here

**10:32 → 11:18**

question. It is enormously wasteful. So you check the catalog first and that is your grep and your glob and then you pull down only the two or three books you actually need. And here is a pointer to what is coming. Managing that context budget properly is the whole of domain 5. But the good habit starts right here. So notice that this one small habit is really your first taste of a big theme. Context is limited and it is precious. And domain 5 will go deep on how to protect it. But you begin protecting it now simply by locating first and reading.

**11:18 → 12:03**

narrowly. Alright, so the key takeaways from this lecture, built-in tools in three lines. Number one, six tools with clear jobs, read, write, edit, bash, grep, and glob. And remember, grep is for contents and glob is for file names. Number two, read before edit. Your match must be exact and unique. Otherwise, you use replace all or the read plus write fallback. And number three, built-ins and incremental. You prefer the built-ins over bash and you locate first rather than reading everything. So that brings domain 2 to a close. Look back at what we built.

**12:03 → 12:48**

we started by designing a single tools interface so that Claude could pick it. Then we made its failures speak clearly with structured errors. We learned to distribute tools wisely and to force a choice when we had to. We plugged into the wider world with MCP and now we have mastered the built-in toolkit. So that is tool design and MCP integration. It is all about giving Claude the right hands and then describing them so well that it always reaches for the right one. Alright, that completes domain 2, tool design and MCP integration. So in the next domain,

**12:48 → 13:10**

from the tools themselves to how you set cloud code up around them. This is cloud code configuration and workflows. Because once cloud has good tools, the next question is how you shape its behavior for a whole team and a whole project. So with this, I'm going to end domain 2, and I will catch you in the next one.
