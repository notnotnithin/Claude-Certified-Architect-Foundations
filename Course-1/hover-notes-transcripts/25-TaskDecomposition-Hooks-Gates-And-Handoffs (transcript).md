---
hovernotes-transcript-of: doc_35f8bf49-a689-4275-9590-400f2c0bc6e6
hovernotes-transcript-version: 2
note: "[[25-TaskDecomposition-Hooks-Gates-And-Handoffs]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042363#overview"
updated: 2026-09-04T16:53:08.767Z
---

# 25-TaskDecomposition-Hooks-Gates-And-Handoffs — Transcript

**0:00 → 0:42**

In the previous lesson, we looked at coordinator and sub-agent architecture. Now let's go one level deeper. How do we design the work itself? In agentic systems, not every task should be handled the same way. Sometimes we know the exact steps in advance. Sometimes we only know the goal, and Claude needs to investigate dynamically. That is the difference between a fixed workflow and adaptive decomposition. For ShopAssist, a predictable refund workflow might look like this. This is a fixed sequential pipeline. Each step depends on the previous step. This is a good design when the business process is known. Verify the customer. Check the order.

**0:42 → 1:27**

then decide. This is also called prompt chaining when each step uses Claude and passes its output to the next step. For example, in this case, chaining keeps each call focused. Claude does not need to classify, extract, validate, decide, and write the final answer all inside one massive prompt. But not every task is predictable. If a customer says something is wrong with my account, I was charged, but I don't see my order and support told me something different yesterday. We may not know the exact path yet. That is where dynamic decomposition is useful. The coordinator can first map the situation, then decide what to investigate. This pattern is especially important in unfamiliar code bases or large,

**1:27 → 2:12**

review tasks. Before acting, the agent should map the structure. For example, in a code base review, do not immediately edit files. First identify the relevant modules, entry points, dependencies, and risk areas. In ShopAssist, the same idea applies to business workflows. First map the issue, then act. For large reviews, we can also split the work into local and integration passes. Local passes focus on one area. The integration pass checks how the findings fit together. This is more reliable than asking one prompt to inspect everything at once. Now let's talk about enforcement. Prompts are useful for guidance, but prompts are not enough when deterministic compliance is required. For example, we

**2:12 → 2:57**

Tell Claude, never process a refund unless the customer has been verified. That instruction is important. But for production support system, it is not enough. If the rule must always be enforced, it belongs in code. This is where prerequisite gates come in. Here, process refund cannot run unless getCustomer confirms the customer. This is not just a prompt instruction. It is a programmatic gate. The same idea applies to refund thresholds. If ShopAssist policy says refunds above $100 require human approval, then the backend must block automatic refund processing above that threshold. Claude can recommend escalation, but the application must enforce it. In agentic systems, we can enforce these rules with hooks.

**2:57 → 3:42**

Hooks let us intercept or normalize agent behavior around tool calls. A common example is a post-tool use hook. After a tool runs, the hook can normalize the result before Claude sees it. This keeps tool results consistent. Instead of letting every downstream prompt deal with messy formats, the hook standardizes the output once. Hooks can also intercept tool calls before execution. For example, before process refund runs, we can check whether the action violates policy. This gives us deterministic enforcement. The model may choose tools dynamically, but the application still controls what is allowed. If the requested action is unsafe or policy violating, the hook blocks it. the case needs judgment, the hook

**3:42 → 4:27**

redirects to human escalation. Now let's connect this to handoffs. A handoff is not just send this to another agent or send this to a human. A good handoff has a structured protocol. For shop assist, a refund escalation should include the facts needed by the next reviewer. This is much better than a vague escalation like please review this refund. The human reviewer, another agent or another workflow should receive enough context to continue without reconstructing the entire conversation. For the exam, remember the design rule. Use fixed sequential pipelines when the steps are known. Use dynamic decomposition when the task is open-ended or investigative. Use local and integration passes

**4:27 → 5:02**

large reviews. Use prompts for guidance but use programmatic gates when compliance must be guaranteed. Use hoops to normalize tool results, intercept tool calls, block unsafe actions, and redirect to escalation. And use structured handoff protocol so work can move safely between agents, tools, and humans. In ShopAssist, this means Claude can be flexible in how it investigates a customer problem. But customer verification, refund limits, policy enforcement, and escalation rules are controlled by
