---
hovernotes-transcript-of: doc_ee9b94db-413c-4f71-a4c3-6400b292288a
hovernotes-transcript-version: 2
note: "[[04-Context-In-Large-Codebase-Exploration]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569699#overview"
updated: 2026-09-11T08:15:09.284Z
---

# 04-Context-In-Large-Codebase-Exploration — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So back in lecture 5.1, I made your promise. I said the extract and persist idea would return for code bases. Well, here it is. And we also made the habit, explore incrementally way back in domain 2. So this lecture adds the actual tools for exploring a huge code base over a long session. This lecture is context in large code base exploration. Explore a massive code base without drowning in it. So five things in this lecture. Number one, the problem. Number two, scratch pad files. 3.

**0:42 → 1:22**

4. Crash recovery manifests. 5. The explore subagent. Alright, so the first topic, the problem. Exploration floods the window. And the subtitle states it plainly. Reading a big codebase fills the window fast. So look at what happens. It is the same context rod as in lecture 5.1. But now it is driven by code. So each file read dumps its contents into the context. and within just dozens of files the window is full

**1:22 → 2:07**

the quality drops mid-task. So notice, this is not a new enemy. It is the exact same lost in the middle problem from earlier. Except this time it fills up not with conversation but with file after file of source code. Now here is the connection. We already made the habit level fix back in domain 2 in lecture 2.5. Explore incrementally. But this lecture adds the tools for long sessions. So please notice the difference. Back in 2.5 we learned the good habit, search first and read narrowly. That is the mindset. So this lecture gives you the actual tools to keep

**2:07 → 2:52**

that discipline over a really long exploration session. Alright, so the second topic, scratchpad files and the subtitle gives you the move. You write your findings to disk, not just into the chat. So look at the idea, you save your key findings to a file. So something like auth lives in the auth folder and the bug is in the login function because disk is unlimited. But the context window isn't. So you re-read only the note you need when you need it. So notice the trade you are making. the findings do not have to live in the crowded context

**2:52 → 3:38**

They can live safely on disk where there is endless room and you only hold one back in at the exact moment you actually need it. And here is the connection. This is extract and persist made literal. You persist your findings to a file and you keep the context lean. So please notice this is that core principle from 5.1 but now it is a real file on disk. Back then extract and persist was an idea. Here it is concrete. You literally write the finding into a file and the window stays clean. Clean.

**3:38 → 4:23**

Alright, so the third topic slash compact and the subtitle tells you its purpose. You summarize the session to keep going past the limit. So look at what it does. It summarizes the conversation and replaces the history. So that shrinks the tokens. So a long task can continue. And this is really the progressive summarization from 5.1 but now as a command. So you run it proactively at around 70 to 75% full and you control what it keeps. So notice that last part especially. you

**4:23 → 4:25**

Do not wait for it to be forced on you.

**4:24 → 5:06**

for it to be forced on you. You run it deliberately while there is still room. And because you chose the moment, you can guide what survives. And here is the tip. You compact at a natural break. Not only when you are forced to. Because a clean moment lets you protect what matters. So please notice why that timing matters. If you wait until the window is completely jammed, you are compacting in a panic. But if you do it at a natural pause between tasks, you can calmly make sure the important findings are safely carried across.

**5:06 → 5:51**

Alright, so the fourth topic, Crash Recovery Manifests. And the subtitle is reassuring. If the session dies, you don't start over. So look at the idea, you keep a manifest. That is the task, what's done and what's next. So a new session reads it and resumes. There is no re-exploring the whole project from scratch. So it is persistence protecting you against failure. So notice what a manifest really is. It is a running log of where you are, what the goal is, what you have finished and what is still left.

**5:51 → 6:36**

crashes, a fresh session just reads that log and picks up exactly where you stopped. And here is the concrete case. A long refactor that crashes at file 40 shouldn't restart at file 1. The manifest is the safety net. So please picture that pain. You have 40 files into a big refactor and the session dies. Without a manifest, you are back at the beginning. All that work repeated. But with one, the new session reads it and carries on from file 41. Alright, so the fifth and final topic, the explore subagent.

**6:36 → 7:21**

the subtitle gives you the move. You send the heavy reading to a separate context. So look at what it does. It reads in its own context and it returns only a summary. So you delegate the investigation to the explore sub-agent which we met in lecture 3.4. And so the big file reads never touch your main window. Only the conclusions come home. So notice how clean that is. All the heavy reading, all those huge files get read somewhere else entirely. And what comes back to you is just the tidy answer. And here is the connection. This was taught in lecture 3.4.

**7:21 → 8:06**

3.4 with plan mode but here it is a context management tool the isolation keeps your main window lean so please notice the same tool doing a new job in the 3.4 we use the explore subagent to plan safely and here it is the same scout but we are using it specifically to keep all that reading out of our main context all right so let's put it all together four tools one lean session so look at the first tool the explore subagent with this the heavy reads happen elsewhere so the

**8:06 → 8:52**

defense against the big file reads then the second tool scratchpad files with these you persist your findings to disk so that is how you keep what you learn out of the window then the third tool slash compact with this you shrink the conversation so that is how you make room when the history itself gets long and the fourth tool the manifest with this you survive a crash so that is your safety net against the session dying and here is the beautiful part it is the same principle as lecture 5.1. Extract. Persist. Trim. Just.

**8:52 → 9:37**

expressed through code specific tools. So please see the Unity here, 4 different tools, but one single idea underneath. Everything we did for a long conversation, we are now doing for a long code-based exploration. Same principle, new clothes. Alright, so let's pull this together. The key takeaways from this lecture. Code-based context in three lines. Number one, exploration floods context. It is the same context rot as long chats. Now driven by code. So remember, dozens of files and the window is full. Number two, persist and compact. You use.

**9:37 → 10:20**

scratchpad files to persist, slash compact to summarize, and a manifest to survive crashes. So remember, disk is unlimited, the window is not. And number three, delegate the heavy reads. The explorer subagent's separate context keeps your window lean. So remember, the big reads happen elsewhere, and only the summary comes home. All right, so that is how you explore a massive code disk without drowning in it. In the next lecture, we will look at human review and confidence calibration. So with this, I am going to end this one, and I will catch you in the next one.
