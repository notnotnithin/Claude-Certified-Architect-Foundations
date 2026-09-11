---
hovernotes-transcript-of: doc_d0d4a5d2-63b9-4e30-9f21-458aac7641f0
hovernotes-transcript-version: 2
note: "[[22-ToolAccess-BuiltInTools-And-MCPConfiguration]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042305#overview"
updated: 2026-09-04T15:56:01.030Z
---

# 22-ToolAccess-BuiltInTools-And-MCPConfiguration — Transcript

**0:42 → 1:27**

returns customer data. Lookup order returns order data. But the descriptions are too minimal. They do not explain when each tool should be used. They do not explain the boundary between a customer lookup and an order lookup. And they do not explain what Claude should do when the user gives only partial information. For example, imagine the user says, can you check my order? My email is alex.example.com. The user mentioned an order, so Claude may try to call lookup order. But the user did not provide an order ID, they only provided an email address. So the better first step is to call the customer lookup tool, identify the customer and then continue from there. This is a tool design problem. Now let's

**1:27 → 2:13**

improve the same tools. This version is much better. First, the tool names are more specific. Instead of getCustomer, we use getCustomer by email. Instead of lookupOrder, we use lookupOrder by ID. The name already tells Claude what the tool does and what input it expects. Second, the descriptions explain the purpose, input, output examples and boundaries. GetCustomer by email says that it should be used when the user provides an email but no order ID. LookupOrder by ID says that it requires an order ID and should not be used with an email address. This is the key idea. A good tool description does not only describe the function. It guides Claude's routing decision.

**2:13 → 2:58**

Another important design choice is whether to split or consolidate tools. If one generic tool handles customers, orders, refunds, and policy checks, the interface becomes vague. In that case, it is usually better to split it into purpose-specific tools. For example, get customer by email, look up order by ID check, refund eligibility, create human escalation. But too many tiny tools can also create complexity. If three tools are always called together, use the same input, and return pieces of the same business operation, it may be better to combine them. The rule is simple. Split tools when it reduces ambiguity. Consolidate tools when it reduces complexity.

**2:58 → 3:43**

Now, let's look at two errors. In production, tools do not always return successful data. The order ID may be invalid, the customer may not have permission, the refund may violate policy, or the backend may time out. A weak error response would look like this. Something went wrong. This does not give Claude enough information to recover. Claude does not know whether it should retry, ask the user for better information, explain a policy issue, or escalate. So our tool should return structured errors. Here is a simple example for lookup order by ID. This function shows several important cases. If the order ID has the wrong format, we return a validation error. The request is not returned.

**3:43 → 4:28**

because calling the same tool again with the same invalid input will not help. Claude should ask the user to check the order number. If the order ID is valid, but no matching order is found, we return something like this. This is important. An empty result is not the same as an error. The tool worked. It just did not find matching data. Claude may ask the user for another email address or order ID. If the user does not have access to the order, we return a permission error. This should not be retried. Claude should not reveal private data, and the application may escalate if needed. If the backend times out, we return a transient error. This one is retriable because the same request may work

**4:28 → 5:13**

So, error category helps the system understand the type of failure. A useful set of categories is transient validation business permission. A transient error means a temporary system problem, like a timeout. A validation error means the input is malformed or incomplete. A business error means the request was understood, but business rules do not allow it. A permission error means the user is not allowed to access or perform the action. The isRetriable field tells the application whether another attempt makes sense. Now let's add one more shop assist example. Refund eligibility. This is a business error. The input is valid. The customer may have permission. backhand is

**5:13 → 5:58**

but the refund cannot be processed because the order is outside the return window. Retrying will not change that. Claude should explain the situation using the customer-friendly message or escalate if the workflow allows manual exceptions. One final production pattern is local recovery. Not every error should immediately go to a coordinator or a human. If the back-end times out once, the application can retry locally. If the order ID has extra spaces or lowercase letters, the application can normalize it. If required information is missing, Claude can ask the user for it. Escalation should happen after local recovery fails or when the error requires human judgment. So the main lesson

**5:58 → 6:26**

is tool design is not only about schemas. A good tool interface helps Claude choose the right tool, send the right input, understand the result, and recover safely from errors. For shop assist, this means better names, better descriptions, clear input boundaries, and structured MCP errors. That gives Claude less room to guess, gives the backend more control, and gives the customer a better experience

**6:26 → 0:42**

In the previous lesson, we looked at the agentic loop. Claude can decide that a tool is needed, request a tool call, wait for our application to execute it, and then use the tool result to continue the conversation. But now we need to solve a more practical problem. How does Claude know which tool to choose? The most important mechanism is the tool description. Claude can see the tool name, the input schema, and the conversation context, but the description explains when the tool should be used. So if our descriptions are too short, too generic, or too similar, Claude can select the wrong tool. Let's start with the weak version. In this version, we have two tools.
