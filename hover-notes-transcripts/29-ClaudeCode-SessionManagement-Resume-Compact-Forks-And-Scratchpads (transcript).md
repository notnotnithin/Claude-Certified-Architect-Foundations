---
hovernotes-transcript-of: doc_48cac08c-1ec8-4952-a42f-e64959cc1e54
hovernotes-transcript-version: 2
note: "[[29-ClaudeCode-SessionManagement-Resume-Compact-Forks-And-Scratchpads]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042393#overview"
updated: 2026-09-06T11:32:59.288Z
---

# 29-ClaudeCode-SessionManagement-Resume-Compact-Forks-And-Scratchpads — Transcript

**0:00 → 0:40**

In real projects, Cloud Code sessions can last a long time. You may explore files, run tests, compare approaches, make changes, stop, and continue later. If you manage the session badly, Cloud may rely on stale context, lose exact details, or mix exploration with implementation. So in this lesson, we'll cover four practical techniques. Resume, Compact, Forks, and Scratchpads. First resume. Cloud Code saves sessions as you work so you can continue later. If you run Cloud with dash dash continue, it resumes the most recent session in the current directory. If you run Cloud with dash dash resume, it opens the session.

**0:40 → 1:25**

picker. If you run cloud with dash dash resume followed by a session ID, it resumes that specific session. And for important work, you can give a session a readable name. For example, you can start cloud with dash n and then a name like return validation. Later, you can resume that same session by running cloud dash resume return validation. Inside an active session, you can also rename it with the slash rename command. This is useful for the exam, you are not limited to the last session. You can resume by picker by session ID or by a user defined session name. Cloud code stores session transcripts locally under the cloud projects directory using the project name and session ID.

**1:25 → 2:10**

Transcript is saved as a JSON lines file. Sessions are saved continuously, but for serious work, do not rely only on chat history. Use meaningful session names, scratch pad notes, and export when you need a readable transcript. Also avoid non-persistent runs for work you need to resume later. Use resume when the task is still the same. For example, you were working on ShopAssist return validation and Claude already inspected the relevant files and tests, but after resuming, always verify the current workspace. The repository may have changed while the session was inactive. A good first prompt would say, resume the return validation task. Before editing anything, recheck git status, git diff, relevant file

**2:10 → 2:56**

and failing tests. Then summarize the current state. The rule is simple, resume the conversation, but verify the code. Second, know when not to resume. If the previous session became messy, start fresh. For example, if you explored three designs, looked at unrelated files, canceled the refactor, and pasted long logs, that context may hurt more than help. In that case, start a new session with a structured summary. The summary should include the goal, relevant files, important functions, failing tests, decisions, and next step. Like this one. A clean summary is often better than a noisy old conversation. Third, compact, long sessions consume context. They also become harder for

**2:56 → 3:41**

model to reason over because important details may be buried in the middle of the conversation. This is related to the lost in the middle problem. Cloud code can reduce context usage with a slash compact command. But compaction has a risk. Summaries can lose exact details. So before or during compaction, preserve the information that must remain exact. For example, include the current task, file paths, function names, failing test names, exact error messages, decisions, and next step. A good compact summary might look something like this. Good compaction preserves file paths, function names, test names, IDs, dates, error messages, and decisions. Not just we changed validation.

**3:41 → 4:26**

Scratchpads. For long tasks, keep persistent notes in a project file. For example, a scratchpad file under .cloud or a session notes file under docs. The scratchpad should contain stable facts. A scratchpad helps with crash recovery, handoff, and fresh sessions. It is also useful as a work manifest. The key point is this. Important facts should not live only in the chat. Fifth, forks. Use forks when you want to compare different approaches without polluting the main session. For example, one fork can explore the smallest change inside validate return request. Another fork can explore a separate return policy validator design. Both forks should avoid editing

**4:26 → 5:11**

files at first. They should return the files involved, risks and tests. Then you compare the two results and implement only the chosen approach. Forks are useful for divergent designs. The main session should stay focused on the implementation path. The same principle applies to sub-agents and exploratory work. Do not ask for long reasoning transcripts. Ask for structured findings. For example, tell the sub-agent to inspect the return validation flow and return only relevant files, relevant functions, current behavior, proposed change, risks and tests to run. Also tell it not to edit files. The same idea applies to command output. Do not paste the full test log back

**5:11 → 5:56**

Claude. Trim it to the useful part. For example, failing test. Test damaged item requires photo. Expected status needs review. Actual status approved. Relevant file validation.pi. Claude does not need every line. It needs the right evidence. So the rule is use resume when the task is still clean and continuous. Name important sessions so you can resume them directly. Start fresh when the old context is noisy. Use compact when the session is useful but getting too large. Use scratch pads when important facts must survive the conversation. Use forks when comparing different implementation strategies. For small tasks, this is productivity.

**5:56 → 6:11**

For high risk work like payments, auth, migrations, production bugs, or large refactors, this becomes correctness. Session management is how you keep Cloud Code useful, focused, and safe during long engineering
