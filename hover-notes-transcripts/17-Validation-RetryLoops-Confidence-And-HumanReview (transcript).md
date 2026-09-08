---
hovernotes-transcript-of: doc_738c4d41-27e2-4548-a5a2-d1e0f578a33a
hovernotes-transcript-version: 2
note: "[[17-Validation-RetryLoops-Confidence-And-HumanReview]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042263#overview"
updated: 2026-09-04T14:45:39.046Z
---

# 17-Validation-RetryLoops-Confidence-And-HumanReview — Transcript

**0:00 → 0:42**

In the previous lesson, we used to use and JSON schema to make Claude return structured data. That solves one big problem. The output is much easier for our application to parse. But structured output does not automatically mean correct output. Claude may return a valid structure but still extracts the wrong value, choose the wrong enum, miss a contradiction or infer information that was not actually present. This is why production systems need validation after the model returns output. There are two important types of validation. The first is schema validation. Schema validation checks the shape of the output. Are all required fields present? Are the

**0:42 → 1:27**

types correct are enum values valid. For example, if desired action must be refund, replacement, store credit or unclear and Claude returns exchange schema validation should catch that. The second type is semantic validation. Semantic validation checks whether the extracted values make sense. For example, the structure may be valid, but the customer message says I want a replacement while Claude extracted desired action as refund. That is not a JSON problem. That is a meaning problem. In ShopAssist Claude might extract a return request with fields like order ID, ID, item, reason, desired action, evidence provided, urgency, missing information, confidentiality,

**1:27 → 2:12**

Conflict detected, human review required. After extraction, our backend should validate the result. If the problem is structural and fixable, we can retry. But the retry should include specific feedback. A weak retry says, try again. A better retry includes the original customer message, the failed extraction, the validation error, and a clear instruction not to invent missing information. For example, the field desired action must be one of refund, replacement, store credit or unclear, your returned exchange, which is not allowed. Re-extract the return request from the original message. Use unclear if the desired action is ambiguous. Do not invent missing information.

**2:12 → 2:57**

The kind of retry works well when the source contains the right information, but Claude placed it incorrectly or used the wrong format. Retries help with wrong and null values, missing required fields, wrong field placement, and structural mismatches. But retries do not help when the information is absent from the source. If the customer never gave an order ID, the correct behavior is not to retry until Claude guesses one. The correct behavior is to return null for order ID and add order ID to missing information. This distinction is very important. Retry when the model made a fixable extraction mistake. Do not retry when the source does not contain the answer. Now let's talk about contradiction.

**2:57 → 3:42**

Sometimes a customer message contains conflicting information. For example, I want a refund, but if possible, just send me another one. This mentions both refund and replacement. Instead of forcing one answer, ShopAssist should return something like desired action, unclear, conflict detected, true, conflict reason. The customer mentions both refund and replacement. This is safer than pretending the request is clear. A similar pattern is useful for numeric extraction. For example, when extracting totals from a receipt, we can separate stated total from calculated total. Stated total is what the document says. Calculated total is what our code calculates from the line items. If they do not match, we can set

**3:42 → 4:28**

click detected to true and route the case for review. This pattern is useful because the model extracts information, but deterministic code verifies it. Another useful field is detected pattern. For example, detected pattern, damaged item. Pattern evidence. The customer says the left side does not work. This helps us analyze false positives. If ShopAssist keeps classifying normal returns as damaged items, detected pattern can help us understand which words or phrases cause the mistake. Now let's add confidence. Confidence should usually be field level, not just one global score. For example, order ID confidence high, item confidence high, reason confidence medium,

**4:28 → 5:13**

action confidence low. This is useful because some fields may be clear while others are uncertain. The order ID may be obvious, but the desired action may be ambiguous. However, confidence is only useful if we test it. A model can be confidently wrong. So in production, confidence should be calibrated with labeled validation sets. That means we collect examples where we already know the correct extraction, run our system, and measure how often high confidence fields are actually correct. We should also measure accuracy by document type and by field. For example, ShopAssist may perform well on plain customer messages, but worse on receipts or screenshots.

**5:13 → 5:58**

We may extract order IDs accurately, but struggle with return reasons. A single accuracy number is not enough. We need to know where the system is reliable and where it needs review. This brings us to human review routing. Not every case should go to a human. The goal is to automate clear cases and escalate risky cases. In Shop Assist, we might route to human review when confidence is low. Conflict detected is true. Required information is missing. The customer asks for a policy exception. The refund amount is high or the extracted request contradicts business rules. We should also sample some high confidence outputs. This is called stratified sampling. It means we review examples from high.

**5:58 → 6:43**

medium and low confidence groups. Why? Because high confidence does not guarantee correctness. Sampling across confidence levels helps catch hidden systematic errors. Now let's look at a simple validation function. This function checks the extraction after Claude returns it. First it checks whether desired action is one of the allowed values. If not, it adds a validation error. That kind of error can usually be fixed with a retry. Next, if order ID is missing, we add it to missing information. We do not ask Claude to invent it. Then if a conflict is detected, we require human review. And if the desired action has low confidence, we also require human review. In a real application,

**6:43 → 7:28**

validation layer can include schema libraries, business rules, database checks, policy checks, and review queues. But the architecture stays the same. Cloud extracts. Your application validates. Retry only when the problem is fixable. Return null when information is missing. Use confidence and conflict fields to decide when human review is needed. Lesson summary. In this lesson, we looked at how to make structured extraction more reliable after the model returns output. Schema validation checks whether the output has the right structure. Semantic validation checks whether the extracted values make sense. Retry loops are useful for fixable issues like wrong genome values, missing fields or wrong

**7:28 → 8:13**

field placement. A good retry includes the original message, the failed extraction, and the specific validation error. But retreats should not be used to force missing information. If the source does not contain the answer, the system should return null, mark the field as missing, ask for clarification, or route to human review. We also covered conflict detected fields, calculated total versus stated total, detected pattern fields, field level confidence, confidence calibration, stratified sampling, and human review routing. For shop assist, this means we can extract return requests, validate them, retry when appropriate, and escalate low confidence or contradictory cases instead of blindly automating them.
