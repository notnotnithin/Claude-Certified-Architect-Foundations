---
title: "Course: Claude Certified Architect Foundations: Complete Course | Udemy"
description: Pass the Claude Architect exam and build production-style AI apps with tools, agents, MCP, Claude Code, and evals.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview
created: "2026-09-04"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/Conversation-Helper-Function-And-Chat-Loop (transcript)|Transcript]]"
hovernotes-id: doc_d9ff5fd8-8281-4c2c-a92e-dc219790bb9b
---

[00:00:00](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:00:01](hover-notes-images/screenshot-01M1P3RJ85CX3KWKBM4S1NPH89.png)
[00:00:01](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### Statelessness in Cloud API Requests

- Cloud API requests are stateless
    - The Cloud does not automatically remember previous requests or context
- **[How to maintain conversation]** To enable multi-turn conversations (like in ShopAssist AI), the application must:
    - Keep track of previous messages
    - Send the entire conversation history back to the Cloud with each new request

#### Example Message History Structure

```python
{
    "role": "user",
    "content": "I want to return my order."
},
{
    "role": "assistant",
    "content": "Sure, I can help with that. Could you share your order number?"
},
{
    "role": "user",
    "content": "My order number is 12345."
}
```

[00:00:21](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:00:21](hover-notes-images/screenshot-01M1P3S5XC4HZMKV0CYQMP228S.png)
[00:00:21](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### Refactoring Message Management

- Manually writing message dictionaries for every turn is a poor pattern
- **[Plan for cleanup]** The code will be refactored using small helper functions to automate the process:
    - A function to add user messages
    - A function to add assistant messages
    - A function to send the current conversation to Claude
- **[Next step]** Adding a system prompt to define the behavior and persona of ShopAssist AI

[00:00:51](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:00:53](hover-notes-images/screenshot-01M1P3T3AVMAXJEASAF8MGTCEE.png)
[00:00:53](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### Refactoring with Helper Functions

- **[Purpose]** To ensure ShopAssist AI responds with the correct role, tone, and behavior without the need to manually write dictionaries for every turn
- `add_user_message` function
    - Performs the single job of adding the user's latest message to the conversation history
    - Takes `messages` (the list storing the conversation) as an input

[00:01:21](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:01:34](hover-notes-images/screenshot-01M1P3V09MZBEVRA2P2YHCVE5J.png)
[00:01:34](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

#### `add_user_message` Implementation

- **[Function Inputs]**
    - `messages`: The list representing the current conversation history
    - `text`: The new string message sent by the user
- **[Mechanism]**
    - Uses `.append()` to add a new dictionary to the end of the `messages` list
    - The dictionary contains two specific keys:
        - `"role"`: Set to `"user"` to identify the sender
        - `"content"`: Set to the value of the `text` parameter

```python
def add_user_message(messages, text):
    messages.append({
        "role": "user",
        "content": text
    })
```

[00:02:03](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:02:47](hover-notes-images/screenshot-01M1P3W7MQCC5A1E5C08X6VSZ5.png)
[00:02:47](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### `add_assistant_message` Implementation

- **[Purpose]** To add Claude's response to the conversation history with the correct identifier
- **[Function Inputs]**
    - `messages`: The current conversation history list
    - `text`: The response text received from Claude
- **[Mechanism]**
    - Uses `.append()` to add a dictionary to the `messages` list
    - The dictionary contains two keys:
        - `"role"`: Set to `"assistant"` to indicate the message was written by the AI
        - `"content"`: Set to the `text` parameter

**[Why the role matters]** Claude needs to know which messages came from the customer and which came from the assistant to maintain context in a multi-turn conversation.

```python
def add_assistant_message(messages, text):
    messages.append({
        "role": "assistant",
        "content": text
    })
```

### Sending Requests

- **[Next Step]** Creating a `chat` function, which will be responsible for the actual logic of sending the conversation history to Claude.

[00:02:48](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:03:04](hover-notes-images/screenshot-01M1P3X65G8EKSB85NKSQZWKS6.png)
[00:03:04](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### `chat` Implementation

- **[Purpose]** To handle the actual communication with the Claude API by sending the conversation history and retrieving the AI's response
- **[Function Inputs]**
    - `messages`: The complete list of conversation history (containing both user and assistant roles)
- **[Mechanism]**
    - Calls `client.messages.create` with the following parameters:
        - `model`: Specifies the AI model to use
        - `max_tokens`: Set to `300` to limit the length of the response
        - `messages`: The full conversation history list
    - **[Handling the Response]**
        - The API returns a complex response object containing metadata and other information
        - To simplify usage, the function extracts and returns only the specific text content of the response using `message.content[0].text`

```python
def chat(messages):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=messages
    )
    return message.content[0].text
```

### Integrating Helper Functions

- **[Workflow]** The helper functions (`add_user_message` and `add_assistant_message`) and the `chat` function work together to manage a multi-turn conversation:

    1. Initialize an empty list: `messages = []`
    2. Add user input via `add_user_message(messages, text)`
    3. Send history to Claude via `chat(messages)`
    4. Add Claude's response via `add_assistant_message(messages, text)`

[00:03:34](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:04:19](hover-notes-images/screenshot-01M1P3Y3J0MN53R2Z1HRYR9FEJ.png)
[00:04:19](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### Putting it All Together

- **[Workflow]** Using the helper functions and `chat` to drive a conversation:

    1. `messages = []`: Initialize an empty list to hold the history.
    2. `add_user_message(messages, "I want to return my order.")`: Add the initial user input.
    3. `answer = chat(messages)`: Send the current history to Claude and capture the response.
    4. `print("ShopAssist:", answer)`: Display the response to the user.
    5. `add_assistant_message(messages, answer)`: **[Critical Step]** Save Claude's response back into the `messages` list.

- **[Why the last step matters]** If you do not save the assistant's answer to the `messages` list, the next time you call `chat(messages)`, the history will only contain the user's message and will lack the context of what the assistant previously said.

```python
messages = []

add_user_message(messages, "I want to return my order.")
answer = chat(messages)
print("ShopAssist:", answer)
add_assistant_message(messages, answer)
```

### Inspecting the Conversation History

- **[Result]** After running the sequence above, the `messages` list contains both the user's prompt and the assistant's reply, allowing for a continuous dialogue.

```python

# The resulting messages list structure:
[
    {'role': 'user', 'content': 'I want to return my order.'},
    {'role': 'assistant', 'content': "I'd be happy to help you with your return! However, I should let you know that..."}
]
```

[00:04:19](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:04:45](hover-notes-images/screenshot-01M1P3YZNXP20WVPQ5QV6Z23HA.png)
[00:04:45](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### Maintaining Context in Multi-turn Conversations

- **[Workflow]** Adding a follow-up message to an existing conversation:

    1. Use the existing `messages` list (which already contains the previous user and assistant turns).
    2. Call `add_user_message(messages, "My order number is 12345")` to append the new input.
    3. Call `chat(messages)` to send the *entire* updated history to Claude.

```python

# Continuing the conversation
add_user_message(messages, "My order number is 12345")
answer = chat(messages)
print("ShopAssist:", answer)
add_assistant_message(messages, answer)
```

- **[Why this works]** Because the `messages` list is passed in its entirety, Claude receives the full context:
    - The original intent (wanting to return an order).
    - The assistant's previous request (asking for the order number).
    - The new information (the actual order number).
- **[Key Insight]** Claude does not remember previous requests on its own. The application is responsible for remembering the history and providing it back to the model in every new request.

[00:05:04](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

![00:05:05](hover-notes-images/screenshot-01M1P3Z70WEG3FVRZQTF8M4PQX.png)
[00:05:05](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview)

### Conversation History vs. System Prompts

- **Conversation History**
    - Provides the context of the interaction
    - Tells the model what has been said previously in the dialogue
- **System Prompt**
    - Defines the model's identity and persona
    - Tells the model how it should behave (e.g., acting as a specific support agent)