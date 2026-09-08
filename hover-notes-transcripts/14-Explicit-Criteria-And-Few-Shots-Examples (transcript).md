---
hovernotes-transcript-of: doc_e74ccc1f-f464-4577-9cd8-9117e6bf5854
hovernotes-transcript-version: 2
note: "[[14-Explicit-Criteria-And-Few-Shots-Examples]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042237#overview"
updated: 2026-09-04T14:01:33.183Z
---

# 14-Explicit-Criteria-And-Few-Shots-Examples — Transcript

**0:00 → 0:26**

In the previous lesson we talked about clear and direct instructions. Now let's take the next step. Sometimes we do not just want Claude to follow instructions. We want Claude to make a judgment. For example, is this a normal return? Is this a damaged item? Is this a billing dispute? Should this customer message be escalated? These tasks are harder because they depend on boundaries. And if the boundaries are vague, Claude may behave

**0:26 → 0:57**

consistently. For example, we might write a prompt like this. Classify this customer message. Be conservative. Only escalate serious cases. This sounds reasonable, but it is still vague. What does conservative mean? What counts as a serious case? Should an angry customer always be escalated, or only if they mention a legal issue, a bank dispute, or a safety problem? If we do not define these rules, Claude has to guess. A better approach is

**0:57 → 1:27**

to replace vague judgment words with explicit criteria. Instead of saying, escalate serious cases, we can say, use escalation candidate only when the customer, asks for a manager or human agent, threatens legal action, says they will contact their bank or dispute the charge, reports a safety concern, is extremely upset and also has a billing, legal or policy issue. Now the boundary is clearer. Claude is no longer deciding what serious means on its own.

**1:27 → 1:57**

giving it concrete criteria. Let's apply this to ShopAssist. ShopAssist needs to classify customer messages into one of five categories. Normal return, damaged item, billing dispute, policy exception, escalation candidate. A stronger prompt could define the categories like this. This is much more reliable than simply saying be careful or only escalate when necessary. We defined the categories, we defined escalation triggers, and we added a priority order for

**1:57 → 2:27**

that match more than one category. For example, my package arrived damaged and I was charged twice. This message could be damaged item or billing dispute. But with the priority rule, Claude should classify it as billing dispute. Now let's add few short examples. Few short examples are examples we include directly in the prompt. They help Claude understand the decision boundary and follow the expected output format. These examples do two important things. First, they show

**2:27 → 2:57**

how to classify different cases. Second, they show the exact JSON format we expect. This helps reduce output format drift. Format drift happens when cloud gives a reasonable answer, but not in the structure our application expects. For example, our backend may expect this category, billing dispute, reason, the customer reports a duplicate charge. But without examples, the model might return something like this. Intent, billing,

**2:57 → 3:27**

Hi, a human can understand it, but our application may fail because the field names are different. Few short examples help keep the structure consistent. They are also useful for reducing false positives. A false positive happens when the system flags something as serious when it is not. For example, I do not like the color and want to return it. This customer is unhappy, but this is still a normal return. There is no damage, no billing issue, no policy exception.

**3:27 → 3:57**

and no escalation trigger. So we can add an example like this. This teaches Claude not to over classify normal dissatisfaction as escalation. The same idea applies to code review. A vague code review prompt might say, review this pull request, find serious issues, be conservative, but this can still produce noisy comments. Claude may flag naming preferences, formatting changes or subjective refactoring ideas. A better prompt defines severity criteria.

**3:57 → 4:27**

flag an issue only if it can cause incorrect behavior, failed builds or failed tests, security exposure, data loss, broken user workflows, production errors, do not flag formatting preferences, minor naming suggestions, subjective refactoring ideas, code that is acceptable but could be written differently. And we can add examples. The important point is that examples should show both sides of the boundary, show what should be flagged.

**4:27 → 4:58**

show what should not be flagged. This helps Claude generalize to new patterns. We are not trying to list every possible future case. Instead, we are giving Claude representative examples that define the pattern. For Shoppersist, if Claude sees examples for duplicate charges, missing refunds, and bank disputes, it can usually generalize to a new message like, my refund says completed, but the money never came back to my card. This should be classified as billing dispute, even if this

**4:58 → 5:28**

exact sentence was not in the prompt. So the practical pattern is simple. Use explicit criteria to define judgment. Use few short examples to show ambiguous cases. Use examples to keep the output format consistent. And use backend validation for critical requirements. Prompting guides the model, but your application should still validate the result. If the category must be one of five values, validate that in code. If the response must be json.par.

**5:28 → 5:56**

and validate it. If a real refund or account action is involved, enforce the business rule in the backend. In this lesson, we improved ShopAssist classification by replacing vague instructions with explicit criteria. We used few short examples to reduce false positives, clarify ambiguous cases, and make the output format more consistent. In the next lesson, we will continue this reliability path by looking at structured outputs and
