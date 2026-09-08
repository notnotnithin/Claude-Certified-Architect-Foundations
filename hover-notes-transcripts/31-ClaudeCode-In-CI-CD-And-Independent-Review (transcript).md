---
hovernotes-transcript-of: doc_da88b49e-a2a7-47de-940f-c907c5f84f37
hovernotes-transcript-version: 2
note: "[[31-ClaudeCode-In-CI-CD-And-Independent-Review]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042405#overview"
updated: 2026-09-06T11:49:16.796Z
---

# 31-ClaudeCode-In-CI-CD-And-Independent-Review — Transcript

**0:00 → 0:42**

In this lesson, we'll look at how to run Cloud Code safely inside CI CD pipelines. Interactive Cloud Code is useful when a developer is working in the terminal, asking questions, approving edits, and refining the result. But CI is different. A CI job cannot wait for a conversation. It must start, run, produce output, and finish. That is why Cloud Code supports non-interactive mode. The command is cloud-p. You can also write the same thing as cloud-print. This prevents CI jobs from hanging. In a pull request workflow for ShopAssist, the prompt could say, review this ShopAssist pull request. Focus on refund logic.

**0:42 → 1:27**

escalation behavior, customer messaging, security issues and missing tests. Return only structured findings. The key point is simple. In CI, do not start an interactive Cloud Code session. Use print mode so the job finishes automatically. Now let's talk about output. Plain text is fine for humans, but it is fragile for automation. If we want to post pull request commands, create annotations, fail a build or skip duplicate findings, we need structured output. Cloud Code can return JSON. The command option is dash dash output format, JSON. For stricter automation, we can also provide a JSON schema. The command option is dash dash JSON schema.

**1:27 → 2:12**

CI command means run Claude code in print mode. Use JSON output format. Apply this JSON schema. Review the pull request. Return an array of findings. Each finding should include file path, line number, severity, categories, message, suggested fix, and a stable fingerprint. The fingerprint is important because CI may run more than once. A developer can push another commit. A workflow can be rerun. The same review can happen again. If Claude posts the same comment every time, the pull request becomes noisy. So the workflow should generate a stable fingerprint for each finding. For example, the fingerprint can be based on file path, line number,

**2:12 → 2:57**

and normalize message. Before posting a new pull request command, the CI script checks whether that fingerprint already exists. If it already exists, skip it. If it is new, post the comment. Now let's talk about context. Cloud code in CI still needs to understand the project. That context can come from the cloud.md file. For ShopAssist, this file may explain how refund workflows are organized, where support fixtures live, which tests must be run, what counts as an escalation, and what customer messaging rules must be followed. Existing tests and fixtures are also useful context. If ShopAssist already has refund policy tests, escalation fixtures, and customer message snapshots,

**2:57 → 3:42**

Claude can compare the pull request against real project behavior. That makes the review more grounded. Now we need to decide how strict the CI review should be. There are two common modes. First, blocking pre-merge checks. This is useful for high confidence issues, security problems, broken tests, schema violations, missing required fixtures, or dangerous production behavior. If Claude returns a critical finding, the CI check can fail. Second, non-blocking reports. This can run overnight or on demand. They are useful for broader review, code quality, missing edge cases, test suggestions, duplication, or architecture concerns. These reports should help the job.

**3:42 → 4:28**

but they do not need to block every pull request. For shock assist, a good pattern is block only critical and high severity structured findings. Post medium and low findings as pull request comments. Run a deeper review overnight for broader improvements. Finally, let's talk about independent review. The same cloud session that generated code is not always the best reviewer of that code. The implementation session may remember the intention behind the change. That can be useful, but it can also make review weaker. A reviewer should ask, does the code actually do what it claims? Are tests missing? Did the implementation introduce a regression? Would this behavior be clear to another developer?

**4:28 → 5:13**

That is why independent review instances matter. In CI, the review should run in a separate Cloud Code invocation with a clean session. It should read the repository, the pull request diff, cloud.md, tests, and fixtures. But it should not inherit the implementation conversation. This gives us session isolation. One Cloud session can help build the feature. A separate Cloud Code run can review it independently. For the ShopAssist pull request workflow, the full idea is run Cloud Code with Cloud-P, use JSON output. Constrain the result with a JSON schema. Ask for structured findings, generate stable fingerprints, skip duplicate comments, post

**5:13 → 5:58**

to the pull request, fail the check only for serious issues. This is the key difference between interactive cloud code and cloud code in CI. Interactive mode is for collaboration. CI mode is for repeatable automation. For the exam, remember the core pattern. Use cloud-p or cloud-dash-print for non-interactive execution. Use structured JSON output for automation. Use JSON schemas when the output must be machine-parseable. Use project contexts such as cloud.md tests and fixtures. Avoid duplicate findings on repeated runs. Choose carefully between blocking checks and non-blocking reports and use an independent review

**5:58 → 6:03**

instead of asking the same coding session to judge its own work.
