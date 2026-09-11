---
hovernotes-transcript-of: doc_a883ef92-1228-49d3-a1f3-9ae2013e09ba
hovernotes-transcript-version: 2
note: "[[19-BUILD-ShopAssist-Extracts-Structured-Return]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042287#overview"
updated: 2026-09-04T15:26:45.033Z
---

# 19-BUILD-ShopAssist-Extracts-Structured-Return — Transcript

**0:00 → 0:40**

In the previous lessons, we learned three important patterns. First we learned how explicit criteria and examples make Claude's judgment more consistent. Then we learned how to use tool use, JSON schema, and tool choice to get reliable structured output. And finally, we learned how to validate model output, retry when the error is fixable, and route on certain cases to human review. In this lesson, we will combine those ideas into one practical shop assist module. The goal is simple. Take a messy customer message and convert it into a validated structured return request. This is a common real-world pattern.

**0:40 → 1:25**

can check an order, apply a policy, or create a refund, it needs to understand what the customer is asking for. So this extraction step becomes the bridge between natural language and backend logic. A customer might write something like, hi, I got my headphones yesterday, but the box was crushed and one side does not work. Can I send it back? I think the order was 12345. This message contains useful information, but it is not structured. For our application, we want something closer to this. This structure is much easier for code to validate and process. But we need to be careful. If the customer does not provide an order ID, Claude should not invent one. If the reason is ambiguous, Claude should

**1:25 → 2:11**

mark it as unclear. If the message suggests a policy exception or contradiction, we may need human review. That is the point of this build lesson. We are not just extracting fields. We are designing a reliable extraction workflow. Step one, define the extraction schema. First, we define the schema for the structured return request. This schema tells Claude exactly what fields we expect. For example, we might include notice a few important choices, order ID and item are nullable. That means Claude can return null when the customer did not provide the information. This is better than forcing Claude to guess. The reason field uses unannown. This keeps the output consistent. Instead of getting 10 different

**2:11 → 2:56**

of damaged, we normalize the reason into damaged item. We also include other and reason details. This gives us structure without losing flexibility, and we include human review required. This lets the extraction step tell the rest of the system. This case may need a person. Step two, use forced tool choice. For this task, we do not want Claude to decide whether to return text or structured output. This step is an extraction module. So we want structured output every time. That is why we use a forced tool choice. This tells Claude, use this specific schema. Do not answer conversationally. Return the structured extraction. This is an important exam pattern. When your application needs rely

**2:56 → 3:41**

structured output. Forced tool use is usually better than asking the model to return JSON. Step 3. Extract the tool input. After Claude responds, we read the tool used block. In a demo, I would print it in a readable format. This shows the actual structured block returned by Claude. At this point, we have a Python dictionary that our code can validate. But remember, a schema helps with structure. It does not guarantee that every value is semantically correct. So the next step is validation. Step 4. Validates the result. Now we check the extracted values. For example, this is a simple validation function. In production, we would likely use stronger validation with a formal schema validator.

**3:41 → 4:26**

But for the course demo, this is enough to show the architecture pattern. The key idea is Claude extracts, code validates. The model should not be the only line of defense. Step 5. Retry only when it helps. If validation fails, we need to decide what to do. Some errors are fixable. For example, if Claude placed information in the wrong field or forgot to fill reason details, we can retry with specific feedback. But some errors are not fixable. If the customer never provided an order ID, retrying will not magically produce a real order ID. In that case, the correct behavior is to return null, add order ID to missing information, and possibly ask the customer for

**4:26 → 5:11**

This is a very important reliability point. Retries are useful for fixing extraction mistakes. Retries are not a license to fabricate missing information. Step 6. Human review routing. Finally, we decide whether this request can continue automatically. ShopAssist should route the case to human review when the confidence is low. The reason is unclear. The customer message contains contradictory information. The request looks like a policy exception, or the customer is asking for something sensitive, such as a refund outside the normal policy. For the demo, we can run a few realistic messages. First, a complete return request. I want to return order 12344.

**5:11 → 5:56**

The headphones arrived broken. This should extract cleanly. Second, a missing order ID. I bought a jacket last week and want to return it. I do not have the order number. Here, order ID should be null and missing information should include order ID. Third, an ambiguous reason. This product is not what I expected. Can I get my money back? This may produce reason, unclear or changed mind, depending on the criteria. Fourth, a policy exception. I bought this six months ago, but I still want a refund because I never used it. This should likely be routed to human review or policy handling. And fifth, a contradiction. The item works perfectly,

**5:56 → 6:42**

it arrived broken and I need a replacement today. This should be flagged as contradictory or low confidence. These examples show why structured extraction is not just about formatting, it is about creating reliable inputs for the rest of the system. The exam will often test the difference between model output, schema enforcement and application reliability. A strong architecture does not rely on prompting alone. Use tool use and schemas to get structured output. Use nullable fields to avoid fabricated data. Use enoms to normalize categories. Use validation to catch structural and semantic problems. Use retrieves only when the problem is fixable. And use human review routing when confidence

**6:42 → 7:10**

So information is contradictory or the request falls outside normal policy. In this lesson, we turned messy customer messages into validated structured return requests. In the next section, we will move from structured extraction to real tool workflows. Shop Assist will not only understand what the customer wants. It will begin using backend tools to look up customers, inspect orders, process refunds, and escalate cases when needed.
