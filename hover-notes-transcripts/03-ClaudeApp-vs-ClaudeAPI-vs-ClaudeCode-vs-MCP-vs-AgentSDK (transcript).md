---
hovernotes-transcript-of: doc_bf3f982c-23f1-4b6f-aca8-a254968cf939
hovernotes-transcript-version: 2
note: "[[ClaudeApp-vs-ClaudeAPI-vs-ClaudeCode-vs-MCP-vs-AgentSDK]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview"
updated: 2026-09-04T10:50:18.154Z
---

# ClaudeApp-vs-ClaudeAPI-vs-ClaudeCode-vs-MCP-vs-AgentSDK — Transcript

**0:00 → 0:22**

In this lesson, we will separate five concepts. Claude app, Claude API, Claude code, Agent SDK, and MCP. Let's start with Claude app. Claude app is the hosted product experience. You use it directly through the browser, desktop app, or mobile app. It is useful for interactive work.

**0:22 → 0:52**

writing, coding help, document review, and research. But from an architecture perspective, Cloud App is not your production runtime. You do not own the full application state, backend orchestration, tool execution, validation, or deployment model. For this course, Cloud App is mostly a reference point. Most architecture decisions happen outside the app. Now let's move to the Cloud API. For developers, the Cloud API is the model interface

**0:52 → 1:22**

inside your own application. Your backend sends messages, system instructions, model parameters, tool definitions, and sometimes structured output requirements. Cloud returns a response, structured data, or a tool use request. But the API does not remove your responsibility as an architect. Your backend still owns conversation state, authentication, permission checks, tool execution, output validation, retries, observability, and business rule enforcement.

**1:22 → 1:52**

That boundary is critical. For example, a customer may ask for a refund. Claude may decide that it needs to look up an order or call a refund tool, but the backhand must decide whether that action is allowed. If customer verification is required before order lookup, that rule should not depend only on the system prompt. The safer architecture is a programmatic prerequisite gate. If the customer is not verified, the tool call is blocked. This is the kind

**1:52 → 2:22**

distinction the exam often cares about. Not just how do we prompt Claude, but which layer should guarantee the behavior. Now let's talk about Claude Code. Claude Code is a developer workflow tool. It is used inside a code base to inspect files, understand architecture, make edits, write tests, refactor code, generate documentation and review changes. So the distinction is simple. Claude API belongs to the application

**2:22 → 2:52**

runtime, but cloud code belongs to the development workflow. Now let's move to the agent SDK. A simple API integration can be one request and one response, but production workflows are often multi-step. A support agent may need to classify a request, verify a customer, look up an order, check policy, call a tool, inspect the result, and decide whether to continue or escalate. That is an agentic workflow. The agent SDK helps structure.

**2:52 → 3:23**

this kind of orchestration. It gives you a way to define agents, tools, hooks, handoffs, and execution flow. For exam purposes, the key point is control. What can the agent decide? What must the application enforce? When should the loop stop? When should the system escalate? Which actions require deterministic validation? Now let's talk about MCP. MCP stands for Model context protocol. In practical terms, MCP is a standard way to expose tools and

**3:23 → 3:55**

context to cloud compatible clients. But MCP is not just tool calling. It is an integration boundary. A good MCP tool needs a clear name, clear description, typed input schema, structured output, useful error handling, and appropriate permissions. The model facing layer should make tools easy to understand and hard to misuse. This matters especially when cloud interacts with real business systems. Now let's put the map together. Cloud app is the hosted

**3:55 → 4:23**

facing product. Cloud API is the model interface for your application runtime. Agent SDK is for orchestrating multi-step agentic workflows. MCP is for exposing tools and context through a standard integration layer. Cloud Code is for developer workflows inside a code base. These pieces can work together, but they solve different problems. In ShopAssist AI, the customer interacts with our front end, our backend code.

**4:23 → 4:48**

of the Cloud API. Cloud may request tools. Those tools may be exposed through MCP. A complex workflow may be orchestrated with the agent SDK. And the engineering team may use Cloud code to build, test, document, and review the system. This is the mental model we will use throughout the course. In the next lesson, we will introduce ShopAssist AI in more detail.
