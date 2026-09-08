---
hovernotes-transcript-of: doc_6bb9df48-20f8-42cc-bb54-519d6523f08c
hovernotes-transcript-version: 2
note: "[[30-ClaudeCode-Workflows-Commands-Skills-PlanMode-And-Refinement]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042399#overview"
updated: 2026-09-06T11:41:27.362Z
---

# 30-ClaudeCode-Workflows-Commands-Skills-PlanMode-And-Refinement — Transcript

**0:00 → 0:42**

In this lesson, we'll look at practical Cloud Code workflows. Custom commands, skills, plan mode, direct execution, and refinement. The goal is simple. Make Cloud Code useful not only for one developer, but for the whole team. Let's start with slash commands. A project scoped command lives in the project folder called .cloud, then commands. For example, we could create a file called shopassistreview.md inside .cloud commands. Because this file is inside the repository, it can be shared through version control. Every developer on the team can use the same command. a command like slash shopassistreview

**0:42 → 1:27**

tell Claude, review the current changes in ShopAssist, focus on refund logic, escalation behavior, customer messaging, and missing tests. Return findings with file paths, risk level, and suggested fixes. User scoped commands live in the user home folder inside .claude commands. These are personal, they are useful for private workflows, but they are not shared with the team. So, the distinction is, a project command is a shared team workflow, a user command is a personal workflow. Now let's move to skills. Skills live in the project folder called .claude then skills. Each skill has a file called skill.md. A skill is useful when the workflow is more structured than a simple command.

**1:27 → 2:12**

Top assist could have a skill for support workflow analysis. In the skill front matter, we could define the name as support workflow analysis. The description could say analyze, refund, escalation, and customer response behavior. The context field could be set to fork. The allowed tools field could allow read and grab. And the argument hint could say provide the path to the changed workflow or the pull request summary. The description explains when the skill should be used. The argument hint tells the developer what input to provide. The allowed tools field limits what the skill can do. For an analysis-only skill, we may allow reading and searching, but not editing. the

**2:12 → 2:57**

The ContextFork option runs the skill in an isolated context. This is useful when the skill needs verbose exploration, such as reading many files or comparing alternatives. The main conversation receives a useful summary without being filled with all discovery output. Personal skills can also be created in the user home folder inside .cloud skills, but they should use different names so they do not affect teammates or conflict with project skills. Now, when do we use skills vs.cloud.md? Use cloud.md for always loaded project knowledge, coding standards, test commands, architecture rules, and naming conventions. Use skills for on-demand workflows. Thank you.

**2:57 → 3:42**

migration analysis, support workflow review, or release notes. Next, plan mode versus direct execution. Use plan mode when the task is complex, multi-file, architectural, or has multiple possible solutions. For example, refactor the shop assist refund flow so billing disputes, damaged items, and policy exceptions use separate decision paths. That kind of task needs exploration, design, and approval before implementation. Use direct execution for small clear changes. For example, add a validation check so refund amount cannot be negative. That does not need a long plan. A strong workflow is often. First use plan mode to investigate and choose the approach.

**3:42 → 4:28**

plan is approved, use direct execution to implement it. For noisy discovery, use the explore subagent. It can inspect files, trace dependencies and return a compact summary. This keeps the main conversation clean. For example, use an explore subagent to find where refund eligibility is calculated, where customer responses are generated and which tests cover damaged items. The output should be structured. Refund logic is here. Response generation is here. Tests are here. Missing coverage is here. Now let's talk about refinement. The best refinement method is concrete examples. Instead of saying improve refund classification. Give examples. Input. I was charged

**4:28 → 5:13**

expected category billing dispute input the item arrived broken expected category damaged item input I changed my mind after 45 days expected category policy exception examples are stronger than vague descriptions next use test driven iteration write tests first then let Claude implement the change if a test fails share the exact failure for example this input expected escalation required to be true but the actual result was false that gives Claude a precise target for the next iteration another useful workflow is the interview pattern use it when the domain is unclear before implementation ask Claude to interview you for

**5:13 → 5:58**

Ask me the key questions about caching validation, failure behavior, rollout risk, and testing before implementing this change. This helps surface assumptions before code is written. Finally, decide how to send feedback. If issues interact, send them in one message. For example, classification, escalation, and response text may need to be fixed together. If issues are independent, fix them sequentially. For example, a typo, a missing import, and a formatting issue can be handled one at a time. So the practical rule is use project commands for shared team workflows, use user commands for personal workflows, use skills for structured on-demand tasks, use context for

**5:58 → 6:43**

for verbose or exploratory work. Use allowed tools to limit risk. Use argument hint to make invocation clear. Use Claude.md for always loaded standards. Use plan mode for complex work. Use direct execution for simple work. Use explore subagents for discovery. And refine with examples, tests, failures, and focused feedback. For ShopAssist, the workflow could look like this. Run slash ShopAssist review. Invoke the support workflow analysis skill. Use plan mode for multi-file design decisions. Use direct execution for the approved implementation. Run tests. Share failures back to Claude with exact input, expected output, and actual output.

**6:43 → 6:53**

the core idea. Reliable cloud code usage comes from reusable workflows, isolated exploration, good execution mode selection, and tight
