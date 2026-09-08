---
hovernotes-transcript-of: doc_3eb827da-3560-483f-adc1-34c09d60f28d
hovernotes-transcript-version: 2
note: "[[12-Clear-And-Direct-Prompting-Specific-Guidelines-XML-Structure]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042215#overview"
updated: 2026-09-04T13:44:23.035Z
---

# 12-Clear-And-Direct-Prompting-Specific-Guidelines-XML-Structure — Transcript

**0:00 → 0:03**

In the previous lessons we learned how to send messages to Claude

**0:03 → 0:33**

Keep conversation history and use a system prompt. Now let's talk about one of the most important prompting skills. Writing instructions that are clear, direct and easy for Claude to follow. A good prompt is not about sounding clever. A good prompt tells Claude exactly what role it should play, what task it should complete, what rules it should follow and what format it should return. Let's start with a weak prompt. Help this customer. This is too vague. Claude does not know.

**0:33 → 1:03**

what kind of help we want. Should it write a polite response? Should it classify the issue? Should it ask for an order number? Should it approve a refund? The instruction is technically valid, but it leaves too many decisions open. For ShopAssist AI, we want something more specific. You are a customer support assistant for an online store. Read the customer message and write a short, helpful response. If the customer wants a refund, Ask for the order number.

**1:03 → 1:34**

Do not promise that the refund is approved. Keep the response under 80 words. This is much better. Now Claude has a role, a task, business rules and a length limit. That is the first principle. Be clear and direct. Do not make Claude guess what you want. Now let's make the instruction even more reliable by adding specific guidelines. This kind of list is useful because it turns vague expectations into explicit behavior. Instead of saying handle this well. explain

**1:34 → 2:04**

well means. That is the second principle. Give specific guidelines. Claude is very good at following instructions but the instructions need to describe the behavior you actually want. Now let's look at the anatomy of a good Claude prompt. In production a prompt is usually not just one sentence. A good prompt has several clear parts. First we define the task. What should Claude do? Then we provide context. What information does Claude need to answer correctly?

**2:04 → 2:34**

Next, we add rules. What should Claude always do? What should Claude never do? Then we provide the actual input, for example, the customer message. After that, we define the output format. Should Claude return plain text, JSON, a short answer, a classification, or something else? And finally, we can define success criteria. In other words, what does a good answer look like? For ShopAssist.ai, the structure can look like this. This structure makes the prompt much easier.

**2:34 → 3:04**

understand. It is easier for Claude to follow. And it is easier for developers to maintain. The important idea is simple. Do not mix everything into one messy paragraph. Separate the instruction, the context, the rules, the input, and the expected output. This is where XML tags become useful. XML tags are not magic, they are simply a clean way to separate different parts of your prompt. For example, we can separate the task, rules, customer message, and output

**3:04 → 3:34**

format. This helps Claude understand which text is instruction, which text is data, and which text describes the expected output. It also makes prompts easier for developers to read and update. In real applications this matters a lot. A prompt can grow quickly. You may have business rules, customer data, order data, tool results, examples, and formatting requirements without structure the prompt becomes messy with xml tags each

**3:34 → 4:04**

section has a clear purpose. Let's compare two versions. Here is a messy prompt. You are a support assistant. A customer wants a refund. Be nice. Ask for details if needed. Don't say too much and don't approve anything unless you know the order. Customer says I want my money back. This can work but it is harder to maintain. Now here is the same prompt with structure. The second version is easier to read. It is also easier to update later. For example, if the business rules

**4:04 → 4:34**

changes, we can update only the rules section. If the output format changes, we can update only the output format section. This is why XML is especially useful for production prompts. Now let's connect this to our Python code. Instead of putting everything into one short user message, we can create a clear prompt variable. Here, the customer message is dynamic. In a real app this value could come from the user interface, a support chat, or a backend

**4:34 → 5:04**

But the structure around it stays the same. That structure gives Claude consistent instructions every time. Then we send this prompt to Claude. This code is doing the same kind of API request we used before. The difference is the quality of the prompt. We are not just sending the customer message. We are sending the customer message together with clear instructions, specific rules and a structured format. A possible response could look like this. This is exactly the kind of response we want.

**5:04 → 5:34**

prompt. It is polite, it does not approve the refund, it asks for the missing order number and it stays short. That is the value of a good prompt. There is one important thing to remember. Prompting improves behavior, but it does not replace backend logic. For example, we can tell Claude, do not approve refunds directly. That is a good instruction. But if refund approval is a financial action, we should not rely only on the prompt. The backend should still enforce the real rule. Claude can drop

**5:34 → 6:05**

response. Claude can classify the request. Claude can decide that an order number is needed. But the actual refund approval should be controlled by application logic, permissions, and tools. So prompts guide behavior. Code enforces guarantees. This distinction is very important when building reliable AI systems. Let's summarize. Clear and direct instructions tell Claude exactly what to do. Specific guidelines explain what good behavior looks like. XML structure separation.

**6:05 → 6:21**

instructions, context, data, rules, and output format. Together, these techniques make prompts easier to follow, easier to debug, and easier to maintain. In the next lesson, we will continue improving our prompts by looking at examples in more controlled outputs.
