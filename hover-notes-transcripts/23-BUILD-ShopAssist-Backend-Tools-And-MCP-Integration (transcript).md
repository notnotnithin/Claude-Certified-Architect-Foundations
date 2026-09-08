---
hovernotes-transcript-of: doc_dc5a1528-76a0-44af-bfe1-2c0777492bf3
hovernotes-transcript-version: 2
note: "[[23-BUILD-ShopAssist-Backend-Tools-And-MCP-Integration]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042315#overview"
updated: 2026-09-04T16:25:22.159Z
---

# 23-BUILD-ShopAssist-Backend-Tools-And-MCP-Integration — Transcript

**0:00 → 0:42**

In the previous lessons we designed better tools, structured errors, scope access, and MCP configuration. Now, we will apply those ideas in the ShopAssist project. This lesson is not about introducing tool design again. Here we are building the backend tool layer that our agents can actually use. For ShopAssist we will start with five backend functions. GetCustomerByEmail, LookupOrderByID, CheckRefundEligibility, ProcessRefund, and CreateHumanEscalation. Each tool has a clear job. GetCustomerByEmail finds the customer. LookupOrderByID retrieves order data. CheckRefundEligibility applies the refund process.

**0:42 → 1:27**

process refund performs the actual refund action. Create human escalation sends the case to a human support team. The important design choice is that these are not all exposed to the same agent. The main support agent can use safe lookup and decision support tools. The refund execution tool is more sensitive, so we can keep it for a narrower refund workflow. This keeps the main support agent helpful but not overpowered. Now let's implement mocked backend functions. In a real application, these functions would call databases, order systems, payment providers, or internal APEs. For the course demo, we will use test data, so we can focus on the interface. interface. We have one customer and two owners.

**1:27 → 2:13**

One order was delivered 12 days ago. The other was delivered 45 days ago. That gives us one eligible refund case and one policy exception case. Now let's build the customer lookup tool. This function returns a structured success response. If no customer is found, we do not treat that as a system error. The tool worked. It simply found no matching customer. That distinction matters because Claude should not retry the same lookup as if the backend failed. Next, let's implement order lookup. This tool shows three important backend cases. If the order ID format is wrong, that is a validation error. If the order does not exist, that is an empty result, not a system error. If the

**2:13 → 2:58**

belongs to a different customer that is a permission error. Claude should handle each case differently. Now we can check refund eligibility. This function does not process the refund. It only answers the policy question. That separation is useful. The main support agent can check eligibility without having permission to move money. Now let's implement the actual refund action. In a real backend this function might call Stripe, Adyen, Shopify, Magento, or an internal payment service. In this mocked version we return a structured refund object. The important point is that this tool should be more restricted than simple lookup tools. Finally, let's create the escalation tool. Escalation is important when automation

**2:58 → 3:43**

stop. For example, we may escalate if there is a permission issue, a policy exception, a high value refund, or conflicting customer information. Now let's walk through a successful refund path. This is a happy path. First, we identify the customer, then we look up the order, then we check eligibility. Only after that do we process the refund. The model should not jump directly from user message to refund execution. The workflow should move through back-end checks. Now let's look at a policy exception path. This order is outside the 30-day return window, so we do not process the refund automatically. Instead, we create a human escalation. This is a good production pattern. Automation handles the standard path. Human

**3:43 → 4:28**

handle exceptions. Now let's connect this to MCP. The business logic stays almost the same. The difference is where the tool layer lives and how Claude gets access to it. In the editor, I would replace the previous plain Python functions with this MCP version. Let's focus only on what changed. First we create an MCP server. This server becomes the layer that exposes ShopAssist capabilities to an MCP compatible client. Next, each function has MCP tool. The function is still normal Python, but now the MCPSDK can expose it as a tool. The type hints define the inputs. For example, email. str means this tool expects a string email.

**4:28 → 5:13**

lookup we require both order ID and customer ID. That boundary matters. The caller should first verify the customer, then use the verified customer ID to look up the order. The docstrings also matter. In this MCP version, docstrings become part of the tool description. So we use them to explain when the tool should be used, what it returns and what it should not do. The structured responses stay the same. MCP changes how Claude discovers and calls the tool. It does not remove the need for backend validation. The backend still returns structured success results, validation errors, permission errors and business errors. For For this lesson, the important point is the pattern.

**5:13 → 5:58**

mcp-mcp2, typed parameters, doc strings with boundaries, structured responses, backend validation. Now, let's test this mcp server with the mcp inspector. The Python mcp SDK includes a browser-based inspector that lets us debug and test the server without wiring it into a full-clothed application first. Here we have shopassist mcp server Python script. This file contains the same shopassist tools we already discussed. The difference is that now they are exposed through fastmcp using the mcp tool decorator. To start the inspector, we can run mcpdev command. The command prints a local browser URL with a session token. I'll open that URL in the

**5:58 → 6:44**

In the inspector, we click connect. Now the inspector connects to our MCP server. Then we go to the tools section and click list tools. And here we can see the tools exposed by the server. This is the important architectural difference. Before MCP, our application had to define tool schemas, keep the tool implementations, execute tool calls, and send results back to Cloud. With MCP, the tool implementation leaves behind an MCP server. A Cloud compatible client can connect to the server, discover the available tools, read the descriptions and input schemas, and call them through the MCP protocol. So our main agent application does not need to manually hard code every backend tool

**6:44 → 7:29**

its own tool loop. It can connect with the server through MCP configuration, such as a project level MCP JSON file, and the server provides the available tools. Let's test one tool. I'll select get customer by email. For the email, I'll enter alex.example.com. Now I run the tool. The inspector shows the structured result from our MCP server. We get the customer ID, email, name, and account status. This confirms two things. First, the Python business logic works. Second, the MCP server exposes that logic correctly as tools. In production, the dictionaries in this demo would be replaced

**7:29 → 8:06**

or ticketing system. But the MCP interface stays the same. The client sees clear tool names, typed inputs, useful descriptions, and structured results. So the exam takeaway is MCP is not just a way to give Cloud more tools. It is a standard way to expose controlled backend capabilities through a reusable server layer. Use local tools when the tools belong only to one application. Use MCP when you want those tools to be discoverable, reusable, and configurable across Cloud Code, Cloud Desktop, Internal Agents, or other MCP compatible workloads.
