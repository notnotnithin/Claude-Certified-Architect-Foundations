---
hovernotes-transcript-of: doc_66ce8837-3238-41e4-b686-606eb80bad0d
hovernotes-transcript-version: 2
note: "[[Six Official Production Scenarios]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042113#overview"
updated: 2026-09-04T09:54:21.791Z
---

# Six Official Production Scenarios — Transcript

**0:00 → 0:30**

Look at the production scenarios. The official exam guide includes six production scenarios. These scenarios show how the exam topics appear in real cloud-based systems. The first scenario is customer support resolution agent. This scenario is about an AI support agent that handles customer issues such as refunds, billing disputes, account problems, and order questions. The system may use tools such as get customer, lookup order, process refund, and escalate to human.

**0:30 → 1:00**

This scenario connects to agentic architecture, tool use, MCP, business rules, customer verification, and human escalation. The second scenario is code generation with cloud code. This scenario focuses on using cloud code for software development tasks. For example, code generation, refactoring, debugging, documentation, and test creation. It also includes cloud.md file, project instructions, custom slash commands, plan mode, and direct execution.

**1:00 → 1:31**

The third scenario is multi-agent research system. This scenario is about a system where multiple agents work together. For example, one agent may search for information, another agent may analyze documents, another agent may synthesize findings, and another agent may generate the final report. This scenario connects to orchestration, context passing, citations, provenance, and handling incomplete or conflicting information. The fourth scenario is is developer productivity.

**1:31 → 2:01**

activity with Cloud. This scenario focuses on helping developers work more efficiently. Cloud may help explore a code base, understand legacy systems, generate boilerplate, automate routine tasks, or use built-in tools and MCP servers. This scenario connects to code base exploration, tool use, project context, and save developer workflows. The fifth scenario is Cloud Code for CI CD. This scenario focuses on using Cloud Code inside automated development

**1:59 → 2:28**

players should guarantee the behavior. Now let's talk about Cloud Code. Cloud Code is a developer workflow tool. It is used inside a code base to inspect files, understand architecture, make edits, write tests, refactor code, generate documentation, and review changes. So the distinction is simple. Cloud API belongs to the application runtime, but Cloud Code belongs to the development workflow.

**2:01 → 2:31**

pipelines. For example, Claude may review pull requests, generate tests, summarize code changes or provide structured feedback. This scenario connects to CI CD automation, structured output, actionable comments, false positive reduction and workflow integration. The sixth scenario is structured data extraction. This scenario is about extracting reliable structured data from unstructured content. For example, Claude may extract fields

**2:28 → 2:58**

Next move to the Agent SDK. A simple API integration can be one request and one response, but production workflows are often multi-step. A support agent may need to classify a request, verify a customer, look up an order, check policy, call a tool, inspect the result, and decide whether to continue or escalate. That is an agentic workflow. The Agent SDK helps structure this kind of orchestration. gives you a way to define agents, tools, hooks, handoffs,

**2:31 → 3:01**

from invoices, receipts, forms, emails, support tickets or documents. This scenario connects to JSON schemas, validation, retrieves, edge cases, confidence, human review, and downstream system integration. So these are the six official production scenarios. Customer support resolution agent, code generation with cloud code, multi-agent research system, developer productivity with cloud, cloud code for

**2:58 → 3:28**

execution flow. For exam purposes, the key point is control. What can the agent decide? What must the application enforce? When should the loop stop? When should the system escalate? Which actions require deterministic validation? Now let's talk about MCP. MCP stands for Model Context Protocol. In practical terms, MCP is a standard way to expose tools and context to cloud compatible clients. But MCP is not just

**3:01 → 3:31**

CI CD and structured data extraction. The important thing to understand is that these scenarios are not isolated from the exam domains. They combine multiple domains together. For example, customer support may involve agents, tools, MCP, context management and human escalation. CI CD may involve cloud code, structured output, prompt engineering and reliability. Structured extraction may involve prompts, schemas, validation, retention,

**3:28 → 3:50**

calling. It is an integration boundary. A good MCP tool needs a clear name, clear description, typed input schema, structured output, useful error handling, and appropriate permissions. The model-facing layer should make tools easy to understand and hard to misuse. This matters especially when Claude interacts with real business systems.

**3:31 → 3:51**

and human review. In this course, we will cover all six scenarios. We will also connect many of these ideas through a running project called Shop Assist AI. Shop Assist AI starts as a simple customer support chat. Then it gradually becomes a more complete cloud-based architecture with API calls, structured output,

**3:51 → 3:55**

tools, MCP integration, agentic workflows, close

**3:55 → 4:04**

code CICD document extraction and reliability patterns. In the next lesson, we will create a map of the cloud ecosystem. We will compare cloud app

**4:04 → 4:15**

Cloud API, Agent SDK, Cloud Code, and MCP. And we will clarify what each one is for before we go deeper into the technical lesson.
