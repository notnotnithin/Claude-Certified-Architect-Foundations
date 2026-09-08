---
title: "Course: Claude Certified Architect Foundations: Complete Course | Udemy"
description: Pass the Claude Architect exam and build production-style AI apps with tools, agents, MCP, Claude Code, and evals.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview
created: "2026-09-04"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/08-System-Prompts-Behavior-And-Application-Enforcement (transcript)|Transcript]]"
hovernotes-id: doc_b4f76133-fec7-41ee-9945-7a993589912b
---

[00:00:00](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![Captured video screenshot](hover-notes-images/screenshot-01M1P4EKVP4PST256V16BNQ060.png)

### Giving the Assistant Behavior

- **[Context vs. Behavior]**
    - **messages**: Represents what has been said so far
        - This is the running conversation history
        - It includes every user and assistant turn, appended and resent on each request
    - **system**: Represents how the assistant should behave
        - These are durable instructions that set the assistant's role, tone, and behavior rules
        - These instructions are independent of any single message
- **[API Structure]**
    - The system prompt is not just another user message
    - It has its own dedicated slot in the API request

[00:00:28](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:00:29](hover-notes-images/screenshot-01M1P4FV6V5JVXEANPM4MEKPR6.png)
[00:00:29](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:00:33](hover-notes-images/screenshot-01M1P4FV6WYWXAKKJ2FWEVP7Z8.png)
[00:00:33](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Defining ShopAssist AI Behavior

- **[The Goal]** To transform the assistant from a generic chatbot into a specialized customer support agent for an online store
    - This is achieved by defining a `system_prompt` variable containing specific instructions
- **[Implementation]** Using a multi-line string to establish persona and rules

```python
system_prompt = """
  You are ShopAssist AI, a helpful customer support assistant for an online store.

  Your job is to help customers with order questions, returns, refunds, shipping issues,
  Be concise, polite, and practical.

  Do not promise a refund until the order is checked.

  If you need more information, ask one clear question at a time.
  """
```

    - **Persona**: Defines who the assistant is (ShopAssist AI)
    - **Scope**: Defines what tasks it handles (order questions, returns, refunds, shipping)
    - **Tone**: Sets the style (concise, polite, and practical)
    - **Constraints**: Establishes hard rules (don't promise refunds prematurely; ask only one question at a time)

[00:00:58](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:00:58](hover-notes-images/screenshot-01M1P4GRZCJNXV6R30X9NZ6F2N.png)
[00:00:58](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Breakdown of System Prompt Logic

- **[Task Specialization]** Beyond basic support, the prompt explicitly includes **product support** to expand the assistant's utility.
- **[Strategic Communication]** The instructions are designed to prevent common chatbot errors:
    - **Preventing premature commitments**: The refund constraint ensures the assistant follows a logical verification workflow.
    - **Optimizing user experience**: The single-question rule prevents overwhelming the customer, ensuring a smoother information-gathering process.

[00:01:28](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:01:38](hover-notes-images/screenshot-01M1P4HBJET17Z65YY8D5MCC9N.png)
[00:01:38](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Integrating the System Prompt into the Chat Function

- **[Implementation]** The `chat` function is updated to include the `system_prompt` variable in the request payload.
- **[Mechanism]** By setting `system=system_prompt` within the message creation, the instructions are sent to the model alongside the conversation history.

```python
def chat(messages):
    message = model.messages.create(
        model=model,
        max_tokens=300,
        system=system_prompt,
        messages=messages
    )
    return message.content[0].text
```

- **[Impact]** This ensures that Claude doesn't just see the message history, but also understands its specific identity and operational constraints for every single turn in the conversation.

[00:01:58](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:02:11](hover-notes-images/screenshot-01M1P4J8ZDMQ7GSJAWF292EKZ8.png)
[00:02:11](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:02:31](hover-notes-images/screenshot-01M1P4J8ZEE9G43CCRRHKX5PRY.png)
[00:02:31](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### The Role of the System Prompt vs. Messages

- The system prompt is not merely another user message; it occupies a distinct place in the API request
    - **System Prompt**: Provides durable instructions for the assistant's behavior (answers "how should the assistant behave?")
    - **Messages List**: Maintains the conversation history (answers "what has been said so far?")

### Testing the Implementation

- To test the updated logic, a new conversation is initialized:

    1. Reset `messages` to an empty list `[]`
    2. Add a user message to simulate a customer interaction

```python
messages = []

# Example user message:

# "I bought headphones last week, the headphones do not work."
```

[00:02:36](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:02:46](hover-notes-images/screenshot-01M1P4KH6AGF5XV5KRDNVNVZ6R.png)
[00:02:46](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:03:06](hover-notes-images/screenshot-01M1P4KH6BJVF1ZVC3DSNB5HJ5.png)
[00:03:06](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Evaluating the System Prompt in Action

- **[Test Scenario]** Simulating a customer interaction to see if the assistant adheres to its constraints:
    - **User Input**: "Hi, I bought headphones last week and they do not work. I want my money back."
    - **Process**: Calling `chat(messages)` sends this user message to Claude alongside the `system_prompt`.
- **[Observed Behavior]** Because the system prompt forbids promising refunds before verifying an order, the assistant's response is shaped as follows:
    - **What ShopAssist DOES**:
        - Acknowledges the issue
        - Asks for the order number
        - Explains the next steps
    - **What ShopAssist DOES NOT do**:
        - It does **not** say "Your refund is approved."
- **[Key Insight]** The assistant's cautious and helpful tone is driven entirely by the system prompt, even though no explicit business logic code has been written yet.

```python
messages = []

add_user_message(messages, "Hi, I bought headphones last week and they do not work. I want my money back.")

answer = chat(messages)
print("ShopAssist:", answer)
```

- **[Maintaining Context]** To continue the conversation, the next user message (e.g., providing the order number) is added to the same `messages` list, allowing Claude to maintain the history of the interaction.

[00:03:22](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:03:56](hover-notes-images/screenshot-01M1P4ME5B4QZSCWR2JFTA03GH.png)
[00:03:56](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Conversation State and History

- The feeling of a continuous conversation is created by sending the entire history of interactions back to the model with every new request
    - This is not "hidden memory" within the model itself
    - It is the `messages` list being sent to the API
- **[The Conversation Flow]** A typical multi-turn interaction involves alternating roles:

    1. `user`: Initial problem/question
    2. `assistant`: Response based on system prompt
    3. `user`: Follow-up (e.g., providing an order number)
    4. `assistant`: Response acknowledging the new context

```python

# The messages list represents the current conversation state
messages = [
    {'role': 'user', 'content': 'Hi, I bought headphones last week and they do not work. I want my money back.'},
    {'role': 'assistant', 'content': "I'm sorry to hear your headphones aren't working! I'd be happy to help you get this resolved. Could you please share your **order number** so I can look into this for you?"},
    {'role': 'user', 'content': 'The order number is 12345.'},
    {'role': 'assistant', 'content': "Thank you! Let me look up order #12345 for you..."}
]
```

- **[Storage in Production]** In a real-world application, this `messages` list (the conversation state) cannot just live in a local Python variable
    - It must be persisted externally so it survives between different user requests
    - Common storage methods include:
        - Databases
        - Session storage

[00:04:07](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:04:08](hover-notes-images/screenshot-01M1P4N2S00A8MQQJFZHD4A4YB.png)
[00:04:08](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:04:15](hover-notes-images/screenshot-01M1P4N2S011DYR3CTCTWCYAGX.png)
[00:04:15](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Guidance Is Not Enforcement

- A prompt steers behavior, but it does not guarantee it
- **[The Distinction]**

| Feature | Prompt (Guidance) | Code (Enforcement) |
| --- | --- | --- |
| Nature | Soft | Hard |
| Function | Shapes tone, persona, and intent; sets sensible defaults | Backend verifies before it acts; financially critical rules live here |
| Reliability | Can be nudged, ignored, or slip | Cannot be talked out of by a user |

- **[Why this matters]** If a rule is financially or operationally important (e.g., "do not issue refunds before verification"), the application code must enforce it programmatically rather than relying solely on the LLM to follow instructions in the prompt.

[00:04:52](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:04:52](hover-notes-images/screenshot-01M1P4P9HMFABBXBJ2B3A5AMCA.png)
[00:04:52](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Putting It Together

- **[The Application Loop]** To maintain a consistent persona and keep a conversation flowing, the application follows a specific cycle:

    1. Define the system prompt
    2. Maintain a `messages` list for conversation history
    3. Append each new user message with the `user` role
    4. Send both the system prompt and the `messages` list to the LLM (e.g., Claude)
    5. Append the LLM's response back to the list with the `assistant` role
    6. Repeat the cycle

- **[Scaling Conversation History]** In production, keeping an unlimited history of every message is impractical due to technical constraints
    - **[The Problem]** As conversations grow longer, the context window increases, leading to:
        - Higher costs (more tokens processed)
        - Increased latency (slower response times)
        - Greater complexity
    - **[Production Strategies]** To manage this, developers use several techniques:
        - Summarizing older turns to condense context
        - Storing key facts separately from the raw chat log
        - Keeping a structured state (e.g., tracking `customer`, `order`, and `intent` as distinct data points)

[00:05:37](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:05:39](hover-notes-images/screenshot-01M1P4PER7G9PC4DBVSJMKT59A.png)
[00:05:39](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

![00:06:01](hover-notes-images/screenshot-01M1P4PER7HHVVMGRSH3A2KBGX.png)
[00:06:01](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview)

### Summary of Building Blocks

- **[Core Components]** Two key elements were added to enable a functional assistant:
    - **Multi-turn conversation history**: Allows the assistant to maintain continuity throughout a chat
    - **System prompt**: Provides the assistant with its specific role and persona
- **[Context Responsibility]** The application owns the conversation; Claude simply responds based on the context provided by the application

### Managing History at Scale

- **[The Challenge]** Long conversation histories increase token usage, cost, and latency
- **[Production Strategies]** To avoid keeping raw history forever, production apps use several techniques:
    - Summarize older turns
    - Store key facts separately
    - Keep structured state (e.g., customer ID, order ID, or refund intent)