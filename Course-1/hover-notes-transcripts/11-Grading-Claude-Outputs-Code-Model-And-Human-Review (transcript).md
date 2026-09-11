---
hovernotes-transcript-of: doc_b95de859-9c19-47e4-a4b7-d453a05d88f8
hovernotes-transcript-version: 2
note: "[[11-Grading-Claude-Outputs-Code-Model-And-Human-Review]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042211#overview"
updated: 2026-09-04T13:32:27.861Z
---

# 11-Grading-Claude-Outputs-Code-Model-And-Human-Review — Transcript

**0:00 → 0:19**

In the previous lesson, we looked at the basic prompt evaluation workflow. We create test cases. We run them through Claude, we compare the outputs, then we improve the prompt and run the eval again. But one important question remains. How do we grade the output? There are three common ways to grade the output.

**0:19 → 0:49**

model outputs code based grading model based grading and human grading human grading means a person reviews the output manually it can be very accurate but it is slow and expensive so in this lesson we will focus mainly on the two approaches that are easier to automate code based grading and model based grading let's start with code based grading code based grading means that normal program logic checks whether the answer is correct this works very well well

**0:49 → 1:19**

and the output has a clear structure. For example, if Claude returns JSON, we can check whether the JSON is valid. This function does one simple job. It checks whether the model output can be parsed as JSON. This type of grading is deterministic. The JSON is either valid or invalid. We can also check required fields. This function checks that Claude returned all fields our application expects. For ShopAssist AI, this matters because our

**1:19 → 1:49**

The token may depend on these fields. If intent is missing, we cannot route the request. If order id is missing, we may need to ask a follow-up question. If needs human review is missing, we may fail to escalate a sensitive case. We can also check whether a value is inside an allowed list. This checks that Claude returned one of the intent values our system supports. These are good examples of code-based grading. It is fast. It is reliable. It is easy to automate.

**1:49 → 2:19**

But, code-based grading has a limitation. It works best when the answer can be checked with strict rules. For example, is the JSON valid? Is the field present? Is the value allowed? Does the output match a schema? But sometimes we need to evaluate quality. For example, was the answer polite? Did Claude explain the return policy clearly? Did it avoid promising a refund too early? Did it ask for the order number when it was missing? Did it escalate?

**2:19 → 2:49**

customer mentioned fraud or legal action, these are harder to check with simple code. This is where model-based grading is useful. Model-based grading means we use another cloud code to evaluate the first cloud response. The first cloud code produces the customer support answer. The second cloud code acts as the grader. For example, we can write a grading prompt like this. You are evaluating a customer support assistant response. Check whether the response follows these rules.

**2:49 → 3:19**

1. The assistant must be polite. 2. The assistant must not promise a refund before checking the order. 3. The assistant must ask for the order number if it is missing. 4. The assistant must escalate if the customer mentions fraud or legal action. Return JSON with score a number from 1 to 10. Past, true or false, reason. Short explanation. This grading prompt defines the evaluation criteria. And we send both the original

**3:19 → 3:50**

customer message and the assistant response to the grader. The grader is not answering the customer. It is evaluating the answer. A possible grading result could look like this. This is useful because it gives us feedback that would be hard to capture with code alone. Model based grading is especially helpful for evaluating helpfulness, politeness, completeness, instruction, following business policy compliance, safety and escalation behavior. But we should also be careful.

**3:50 → 4:20**

A model-based grader is still a model. It can make mistakes. It can be inconsistent. And if the grading criteria are vague, the scores may not be very useful. That is why the grading prompt should be specific. Instead of saying grade whether the response is good, it is better to say grade whether the response follows the refund policy, avoids unsupported promises, asks for missing information and uses a polite tone. The clearer the evaluation criteria, the more

**4:20 → 4:50**

useful the greater becomes. In production systems we often combine both approaches. Use code-based grading for deterministic checks. Use model-based grading for semantic judgment. For example, in ShopAssist AI, code-based grading can check. Is the output valid JSON? Does it match the expected schema? Is the intent one of the allowed values? Is the order ID in the correct format? Is needs human review a boolean? Model-based grading can check

**4:50 → 5:20**

Was the response helpful? Was it polite? Did it follow the refund policy? Did it avoid unsupported promises? Did it escalate when needed? We can also combine the scores. For example, final score equals code score plus model score divided by two. This gives us one overall score for each test case. Then we can calculate the average score across the entire eval dataset. The exact number is not magic. The important part is comparison. If prompt version 1.

**5:20 → 5:50**

gets an average score of 6.8 and prompt version 2 gets 8.4 on the same dataset, we have evidence that version 2 is probably better. But we should also inspect failures. A higher average score is useful but it does not tell the whole story. Maybe the new prompt improved refund requests but broke billing issues. Maybe it became more polite but less direct. Maybe it reduced hallucinations but started asking too many follow-up questions. That is why

**5:50 → 6:13**

files are not just about numbers. They are also about reviewing failed cases and understanding what changed. Code-based grading helps us check structure, schema, syntax, and exact rules. Model-based grading helps us check quality, judgment, tone, and policy following. Together they give us a practical way to build more reliable cloud applications.
