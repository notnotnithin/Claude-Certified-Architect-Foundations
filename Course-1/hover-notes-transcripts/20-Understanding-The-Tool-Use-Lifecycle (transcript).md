---
hovernotes-transcript-of: doc_2caabb5d-3c19-4843-ac76-a3ea1a6ddfb3
hovernotes-transcript-version: 2
note: "[[20-Understanding-The-Tool-Use-Lifecycle]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042299#overview"
updated: 2026-09-04T15:34:26.266Z
---

# 20-Understanding-The-Tool-Use-Lifecycle — Transcript

**0:00 → 0:42**

In the previous lessons, we introduced tools, schemas, and structured output. Now let's connect those pieces into the full tool use loop. This is the mechanism that allows Claude to act as part of an autonomous workflow. But the most important thing to remember is this. Claude does not execute tools by itself. Claude decides that a tool should be used. Your application executes the tool, then your application sends the result back to Claude. And Claude decides what to do next. Let's look at how this works. When Claude wants to use a tool, the assistant response does not contain only normal text. It can contain a tool use block. That block tells your application three things.

**0:42 → 1:28**

the tool Claude wants to call, the input arguments for that tool, and the tool use ID. The tool use ID is important because it connects the tool request with the tool result. For example, in ShopAssist, Claude might receive a customer message like, I want a refund for my last order, it arrived damaged. Claude should not guess the customer record, it may request a tool call like get customer, with the customer email or account identifier as input. At this point, the API response usually has stop reason tool use. This means Claude is not finished yet. It is asking your application to run a tool before it can continue. Now your back end executes the requested tool, maybe it looks up

**1:28 → 2:13**

customer in your database. Maybe it calls an order service. Maybe it checks whether the refunds is allowed. The model is not doing any of that directly. Your application is responsible for permissions, business rules, authentication, validation, rate limits, and safety checks. After your application runs the tool, it sends the tool result back to Claude. This result is added to the conversation history as a user message containing a tool result block. That result must include the same tool use ID. This is how Claude knows which tool request the result belongs to. Then we call Claude again with the updated conversation history. Now Claude can the tool result and decide the next step. Maybe it needs to call

**2:13 → 2:58**

up order. Maybe it has enough information to call process refund. Maybe the order is outside the refund window, so it should call escalate to human. Or maybe it has enough information to answer the customer directly. This is the agent pick loop. The loop is simple. Send the current conversation to Claude. If Claude returns, stop reason, tool use, execute the requested tool. Append the tool result to the conversation history. Call Claude again. Continue until Claude returns, stop reason, and turn. When Claude returns, and turn, that means it has produced the final assistant message for this turn. That is the response we can show to the customer. This is also why we should not parse natural language to decide whether the task

**2:58 → 3:43**

complete. For example, we should not look for phrases like I'm done. Here is the final answer. No more tools needed. That is fragile. The reliable signal is the API response itself. If the stop reason is tool use, continue the tool loop. If the stop reason is nturn, return the final response. In real systems, we may still add a maximum iteration limit as a safety guard, but that should not be the primary stopping mechanism. The primary stopping mechanism is model-driven completion through nturn. The iteration cap is only protection against bugs, unexpected tool behavior, or poorly designed loops. This is different from a hard-coded decision tree. In a hard-coded flow, we might

**3:43 → 4:28**

First call GetCustomer, then call LookupOrder, then call ProcessRefund, then Respond. That can work for simple cases. But customer support conversations are often messy. The customer may ask about a refund, a damaged item, a duplicate charge, and a policy exception in one message. A tool-enabled assistant can choose the next action based on the current conversation and previous tool results. For ShopAssist, we can expose tools like GetCustomer, LookupOrder, ProcessRefund, Escalate to Human. Claude decides which tool is appropriate. Your backend decides whether the requested tool call is allowed. This distinction is very important. Claude can make model-driven decisions.

**4:28 → 5:14**

application still enforces deterministic rules. For example, even if Claude requests process refund, your backend should reject that call if the customer has not been verified, if the refund amount exceeds a limit, or if the order is not eligible. So the agentic loop does not mean let the model do anything. It means let Claude decide the next reasonable step. Let your application execute tools safely, then return the result to Claude so it can continue. In this example, ShopAssist has access to four tools and get customer returns a customer object based on the customer email. Lookup order returns order details based on the order ID process refund processes refund when the

**5:14 → 5:59**

is eligible. And EscalateToHuman creates an escalation when the case should not be handled automatically. These two definitions describe what Claude is allowed to request. Each tool has a name, a description and an input schema. But the tool definition itself does not run anything. It only tells Claude what structured tool calls are available. Now let's look at the actual implementation of these functions. In this demo, GetCustomer simply returns test customer data. In a real application, this could be a database query or an API call to a customer service. LookupOrder returns a fake order object with the order status, item name and refund eligibility. In production,

**5:59 → 6:44**

This could call an order management system. Process refund returns a fake approved refund result. In a real system, this would usually call a payment provider or internal refund service and escalate to human returns a simple escalation object. In production, this could create a ticket in Zendesk, Salesforce, Jira, or any other support platform. Next, we have the tool functions dictionary. This is the bridge between Claude's tool request and our Python code. Claude may request a tool by name, like lookup order. Our application uses this dictionary to find the matching Python function and execute it. After that, we define the starting customer message. The customer provides an email, an order ID, and

**6:44 → 7:29**

item arrived damaged. So Claude has enough context to decide which tool to use first. Now we get to the main loop. On each iteration we send the current message history to Claude together with the tool definitions. Claude can either return a final answer or request a tool. If Claude returns stop reason, end turn, the task is finished. We print the final customer facing response and exit the loop. If Claude returns stop reason, tool use, then Claude is asking our application to run a tool. The code looks through Claude's response blocks and finds each tool use block. From that block we read the tool name, the tool input, and the tool use ID.

**7:29 → 8:14**

the matching Python function from two functions. Once the function returns data, we send that data back to Claude as a tool result. The tool result includes the same tool use ID, so Claude can connect the result to the original tool request. Then we append the tool result to the conversation history and continue the loop. Claude now sees the new tool result and decides what to do next. It may request another tool, or it may return the final answer. That is the core mechanic behind tool use. Assistant messages can contain tool use blocks. Each tool call has a tool use ID. Your backend executes the tool. Tool results are returned to Claude. Tool results are appended to the conversation

**8:14 → 8:33**

The loop continues while Claude returns tool use. The loop ends when Claude returns and turns. Once you understand this pattern, tool use becomes much easier to reason about. You're not building magic. You're building a controlled loop between Claude, your application, and your backend
