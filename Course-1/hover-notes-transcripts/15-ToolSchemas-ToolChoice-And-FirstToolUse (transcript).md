---
hovernotes-transcript-of: doc_b9475026-81cd-4632-a5d3-5b6bb1176b42
hovernotes-transcript-version: 2
note: "[[15-ToolSchemas-ToolChoice-And-FirstToolUse]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042243#overview"
updated: 2026-09-04T14:14:39.332Z
---

# 15-ToolSchemas-ToolChoice-And-FirstToolUse — Transcript

**0:00 → 0:19**

In the previous lessons, ShopAssist could read a customer message, follow instructions, and return structured information. But in a real support application, that is not enough. If a customer asks, I want to return order 12345, is it still eligible? Claude should not invent the answer.

**0:19 → 0:49**

Claude needs access to real backend systems. For example, it may need to look up the order, check the purchase date, check the return policy and maybe create a return request. This is where tool use comes in. A tool is a function that your application exposes to Claude. Claude does not execute the function directly. Instead Claude decides that a tool should be called and returns a structured tool use request. Then your backend executes the real function and sends the result back to Claude.

**0:49 → 1:20**

So, the responsibility is split. Claude decides what information it needs. Your code executes the tool safely. And your application controls what Claude is allowed to access. Let's start with a simple example. ShopAssist needs a tool called Lookup Order. This tool accepts an order ID. Then it returns information about the order. For example, whether the order exists, what item was purchased, when it was delivered, and whether it may be eligible for return.

**1:20 → 1:50**

The important part is that we describe this tool to Claude using a schema. The schema tells Claude what the tool is called, what the tool does, what input fields it accepts, which fields are required, and what data types those fields should have. The tools list defines the tools that Claude can use in this request. Here we define one tool. Lookup order. The name is the exact tool name Claude will use. The description helps Claude understand when this tool is useful.

**1:50 → 2:20**

An input schema defines the arguments Claude must provide when it requests the tool. In this case, the tool accepts one required field, order ID. This schema is very important. We are not just telling Claude call some function. We are giving Claude a contract. If Claude wants to use this tool, it must provide arguments that match this shape. Now we can send a customer message to Claude and include the tool definition. Here we pass the tools list into the API.

**2:20 → 2:50**

a request. This means Claude is allowed to use the lookup order tool if it thinks the tool is needed. Since the customer asks about a real order, Claude should not guess. A good response is not a final answer yet. A good response is a request to call the tool. After the request, we can inspect the response. In a normal text response, stop reason is often end turn. But when Claude wants to use a tool, the stop reason is usually tool use. And the The content contains

**2:50 → 3:20**

tool use block. Conceptually it looks like this. This is Claude saying I need you to call lookup order with this input. But again Claude did not actually call your database. Claude only produced a structured request. Your back-end is responsible for taking this request, calling the real function and returning the result. That is one of the most important ideas in tool use. Claude suggests the tool call. Your application performs the tool call. Tool use helps us

**3:20 → 3:50**

avoid a very common AI application problem. Without tools, Claude might answer based only on the conversation. For example, yes, your order is probably eligible for return. But that answer may be completely wrong. Claude does not know the real order status unless we provide it. With tools, Claude can say, I need to look up the order first. Then the backend can retrieve real data. This makes the application much more reliable. It also keeps

**3:50 → 4:20**

operations under application control. Claude can request a tool, but your code decides whether the tool is actually executed. Good tool schemas are specific. A weak tool might look like this. This is too vague. Claude has to guess what kind of information the tool can return. A better tool is more specific. This version is clearer. The tool has a specific purpose. The input field has a clear name. And the description explains exactly what Claude should provide.

**4:20 → 4:50**

Exam preparation remembers this pattern. Good tools are narrow, well-named, and clearly described. Vague tools make tool use less reliable. Sometimes a tool needs more than one field. For example, we may want a tool that creates a return request. This schema tells Claude that all three fields are required. If the customer does not provide the item or reason, Claude should not fabricate them. Instead, the assistant should ask a follow-up question. This is one reason schema.

**4:50 → 5:20**

are so useful. They make missing information visible. They also make the boundary between Claude and your backend much cleaner. By default Claude can decide whether to use a tool. This is called automatic tool choice. Conceptually, the request uses tool choice type auto. With auto Claude can either answer normally or request a tool. For example, if the user asks what is your return policy. Claude might answer from the system instructions, but if the user Ah,

**5:20 → 5:51**

asks, is order 12345 eligible for return? Claude should use lookup order. Sometimes however, you want to force Claude to use a tool. For example, if this request is specifically an extraction step and your application needs structured arguments every time, in that case you can use a forced tool choice. This tells Claude, you must use this specific tool. There is also a middle option, tool choice type any.

**5:51 → 6:21**

Claude must use one of the available tools, but it can choose which one. So we have three common patterns. Use auto when Claude may or may not need a tool. Use any when Claude must use a tool. But the choice is flexible. Use a forced tool when your application requires one specific tool. Let's connect this back to ShopAssist. The customer says, hi, I want to return order 1, 2, 3, 4, 5. It arrived yesterday, but the box was damaged.

**6:21 → 6:51**

App Assist may need to do several things. First it needs to look up the order. Then it may need to check the return policy. Later it may create a return request. But in this lesson we only focus on the first step. Claude receives the message. Claude sees that order specific information is required. Claude returns a tool use request for lookup order. Our backend receives that request. Then our backend calls the real order system. This is the foundation of two

**6:51 → 7:21**

A tool is not Claude directly accessing your database. It is a structured interface exposed by your application. Claude can request a tool call, but your backend executes it. Your backend still validates permissions, applies business rules, handles errors, and controls what data is returned. So prompts can guide Claude and schemas can structure Claude's requests. But deterministic business logic should stay in code.

**7:21 → 7:34**

lesson we learned that tools are defined with schemas. Claude returns a tool use block when it wants to call one, and tool choice controls whether tool use is optional, required, or forced to
