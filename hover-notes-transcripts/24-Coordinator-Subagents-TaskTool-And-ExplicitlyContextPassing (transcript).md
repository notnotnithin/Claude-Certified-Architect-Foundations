---
hovernotes-transcript-of: doc_1a1d05ac-8361-4e0a-ae01-e7587249129f
hovernotes-transcript-version: 2
note: "[[24-Coordinator-Subagents-TaskTool-And-ExplicitlyContextPassing]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042349#overview"
updated: 2026-09-04T16:37:28.803Z
---

# 24-Coordinator-Subagents-TaskTool-And-ExplicitlyContextPassing — Transcript

**0:00 → 0:42**

In the previous lesson, ShopAssist already had backend tools and MCP integration. Now we move one level higher. Instead of one agent trying to solve every part of a complex customer request by itself, we can use a coordinator sub-agent architecture. The pattern is simple. The coordinator stays in the center. It receives the user request, decides how to split the work, sends tasks to specialized sub-agents, receives their findings, and produces one final answer. This is a hub-and-spoke architecture. The coordinator is the hub. The sub-agents are the spokes. For ShopAssist, this becomes useful when one customer message contains several different problems.

**0:42 → 1:27**

Hi, I think I was charged twice for order A1042. Also, the headphones arrived damaged, and I want to know if I can still return the charger from my previous order. This is not one issue. It is a billing issue, an order investigation issue, and a policy review issue. A weak design would ask one agent to handle everything in one long context. A better design is to let the coordinator delegate. On screen, we define our agents. The important detail here is allowed tools. If the coordinator is expected to spawn sub-agents, it must be allowed to use the the task goal. Without task, the coordinator may still reason about delegation, but it cannot

**1:27 → 2:12**

invokes sub-agents. Now let's define the sub-agents. Notice the tool restrictions. The billing agent can inspect payment events, but it cannot process a refund. The order agent can inspect shipment data, but it cannot make policy decisions. The policy agent can read policy, but it cannot change an order. This is one of the main practical benefits of sub-agents. Each agent receives only the tools it needs. Now we send the customer message to the coordinator. The coordinator should not assume sub-agents automatically know the full conversation. Sub-agents have isolated context. They do not automatically inherit the parent conversation history. So the coordinator must pass context explicitly.

**2:12 → 2:57**

agent task would look like this. This is too vague. The subagent does not know the customer, the order ID, the original message or what has already been verified. A better task passes complete context. This is explicit context passing. We are not relying on hidden memory. We are giving the subagent the exact facts it needs. For larger workflows, it is useful to separate content from metadata. This structure helps prevent the subagent from mixing source text, system facts and prior findings. It also makes the final synthesis easier. Now, if the issues are independent, the coordinator can run subagents in parallel by emitting multiple task tool calls in one response.

**2:57 → 3:43**

Conceptually, the coordinator emits this. The key idea is that the coordinator is not waiting for billing before it starts order investigation because these tasks do not depend on each other. But parallel execution should not mean chaotic communication. All communication still routes through the coordinator. Subagents return findings to the coordinator. The coordinator decides what to tell the customer. For example, the results may look like this. Then the coordinator synthesizes one unified response. This is what the coordinator owns, routing, aggregation, and final response quality. One important design warning, do not decompose too narrowly. You do not need a spread subagent for every tiny field, every sentence,

**3:43 → 4:28**

every database lookup that creates overhead and can make the system harder to reason about. Good decomposition follows meaningful business boundaries. In ShopAssist, billing, order investigation, policy review, and escalation are meaningful boundaries. Check customer name and check order date are probably too narrow unless they are part of a larger specialized workflow. For the exam, remember the core mechanics. The coordinator is the central routing and aggregation point. Subagents have isolated context. They do not automatically inherit the parent conversation. The task tool is the mechanism for spawning subagents. The coordinator must have tasks in allowed tools. Each sub-agent is configured with an

**4:28 → 5:05**

definition style setup, name, description, system prompt, and allowed tools. Context must be passed explicitly, including relevant prior findings from other agents. And when tasks are independent, the coordinator can request multiple task calls in one response for parallel execution. In production, this architecture keeps complex support workflows more modular, safer, and easier to debug. Instead of one large agent with every tool and every responsibility, ShopAssist becomes a coordinated system of smaller specialists, with one coordinator responsible for the final customer
