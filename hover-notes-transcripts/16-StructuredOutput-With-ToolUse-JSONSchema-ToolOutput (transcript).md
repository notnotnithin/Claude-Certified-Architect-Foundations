---
hovernotes-transcript-of: doc_abc80e61-dd8d-4539-b004-0d11099dca73
hovernotes-transcript-version: 2
note: "[[16-StructuredOutput-With-ToolUse-JSONSchema-ToolOutput]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042253#overview"
updated: 2026-09-04T14:34:04.786Z
---

# 16-StructuredOutput-With-ToolUse-JSONSchema-ToolOutput — Transcript

**0:00 → 0:22**

In the previous lesson we introduced the basics of tool use. Now we will apply that idea to one of the most common production use cases – reliable structured output. For example, in ShopAssist a customer might write something messy, like, I got my shoes yesterday and they're scratched. I don't know if I can return them, but I want a replacement.

**0:22 → 0:52**

send a photo if needed. As humans, we understand this message. But for an application, we need something more structured. We may need fields like order ID, item, reason, desired action, evidence, urgency, and missing information. A common beginner approach is to ask the model, return only valid JSON. This can work sometimes, but it is not the most reliable approach. The model might add extra text, it might forget the

**0:52 → 1:22**

It might return a value in the wrong format. Or it might invent a field because the prompt was not strict enough. For production applications, a better pattern is to use tool use. With tool use, we define a tool that has an input schema. Claude does not just write JSON as plain text. Instead Claude produces a structured tool call that follows the schema we defined. This is one of the most reliable ways to get schema-compliant structured output. Let's first look at the lesson.

**1:22 → 1:52**

reliable version. This prompt asks for JSON, but the structure exists only in the instruction. Claude has to infer the fields. It may return good JSON. But our application is still depending on text formatting. And if the response is not valid JSON, our parser may fail. This is the problem we want to avoid. Now let's define the structure as a tool. The tool name is ExtractReturnRequest. The The description tells Claude what this tool is for, and the input schema defines

**1:52 → 2:22**

exactly which fields we want. Notice a few important schema design choices. First, some fields are required even when the customer does not provide the information. For example, Order ID is required, but it can be null. This is important. Required means the field must exist. Nullable means the value may be missing. So instead of Claude inventing an Order ID, we allow it to say Order ID. None. This is much safer.

**2:22 → 2:57**

we use the num fields. For reason, Claude must choose one of the allowed values. This prevents random labels like product issue or return problem when our system expects damaged item or normal return. Third, we include an unclear value. This is useful when the customer message is ambiguous. Instead of forcing a bad classification, Claude can explicitly say the intent is unclear. Fourth, we include the other plus detail pattern. If the customer says something that does not fit our categories, Claude can choose other and explicitly

**2:57 → 3:43**

the case in reason detail. This gives us controlled structure without losing flexibility. Now let's send the customer message with this tool available. Here we use tool choice to force Claude to use our extraction tool. This means Claude should return a tool used block instead of a normal text answer. The response content can contain different block types. For this example, we look for the tool used block and extract its input. The result is now a Python dictionary. It may look like this. This is much easier to use in real application code. We can save it to a database. We can route the request to the right workflow. We can ask the customer for missing information. Or we can trigger an escalation if the reason or urge

**3:43 → 4:28**

requires it. The tool choice setting controls how Claude decides whether to use a tool. With forced tool selection Claude must use one specific tool. That is what we used here. For structured extraction, forced tool selection is often the best choice because we do not want a conversational answer. We want the structured object every time. There is one important limitation. A strict schema can prevent many syntax and formatting problems. For example, it can make sure the output has the expected fields, it can make sure an enum value comes from the allowed list, and it can make sure missing information is an array. But a schema does not guarantee that the meaning is correct. Claude could still choose normal return. When the better answer is the same.

**4:28 → 5:13**

damaged item. It could still mark urgency as high when the message does not justify that. So tool use solves the structure problem. But we still need good prompt instructions, explicit criteria, examples and evaluation tests to solve the judgment problem. That is why this lesson connects directly to the previous lessons. Structure and judgment are different problems. A schema controls the shape of the answer. Criteria control the quality of the decision. Even with a good schema, we should still add format normalization rules in the prompt. For example, use these normalization rules. If the order ID is missing, use null. Do not invent one. If the customer offers to send a photo later,

**5:13 → 5:58**

Evidence provided is false. Use urgency high only when the customer mentions a deadline, repeated failed attempts, or business critical impact. Use unclear when the message does not contain enough information. Use other only when none of the listed num values fit. These rules make the structured output more consistent. They also reduce false positives. For ShopAssist, this matters because the extracted data may drive real workflow decisions. A damaged item may go to a replacement workflow. A billing dispute may go to a billing team. A policy exception may require escalation. And a missing order ID may trigger a follow-up question instead of a return authorization. In the demo we compared.

**5:58 → 6:43**

two approaches. First, we asked Claude to return freeform JSON. That approach is simple, but it depends on text formatting and can break parsing. Then we used ToolUse with a JSON schema. This gave us a structured tool input that our application can extract directly. We also saw why nullable fields are important. When the customer does not provide an order ID, Claude should return null, not invent a fake value. And finally, we saw that schemas improve reliability, but they do not replace good instructions. For the exam, remember the key idea. Use ToolUse and JSON schemas when your application needs reliable structured output. Use required fields, nullable value,

**6:43 → 6:58**

and norms unclear and other plus detail fields to make the schema both strict and practical and use tool choice when you need to control whether Claude may use a tool must use a tool or must use one
