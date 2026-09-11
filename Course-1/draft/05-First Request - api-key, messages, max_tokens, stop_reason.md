---
title: "Course: Claude Certified Architect Foundations: Complete Course | Udemy"
description: Pass the Claude Architect exam and build production-style AI apps with tools, agents, MCP, Claude Code, and evals.
author: Udemy
source: https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042131#overview
created: "2026-09-04"
tags:
  - hover-notes
  - udemy
transcript: "[[hover-notes-transcripts/First Request - api-key, messages, max_tokens, stop_reason (transcript)|Transcript]]"
hovernotes-id: doc_2f64480a-9f4d-442b-8291-b4589928b0db
---

![Captured video screenshot](hover-notes-images/screenshot-01M1P292P48P63F5G7E62RJ449.png)

[00:00:00](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:00:02](hover-notes-images/screenshot-01M1P2APXCTTAM5SVRZ6KHBZB8.png)
[00:00:02](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Language and SDK Support

- Python is used for the course demonstrations
    - It is a popular choice for API demos, backend prototypes, automation, and AI workflows
- Cloud API concepts are language-agnostic
    - The principles apply regardless of the language used
- Anthropic provides official SDKs for several languages:
    - Python
    - TypeScript
    - Java
    - Go
    - Ruby

[00:00:29](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:00:29](hover-notes-images/screenshot-01M1P2BKWXEDKVV18R8CF0V29V.png)
[00:00:29](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### API Interaction Pattern

- The core structure of an API call remains the same regardless of the language used
    - Create a client
    - Send messages
    - Set parameters (e.g., `model`, `max tokens`)
    - Read the response

### Development Environment

- Visual Studio Code with the Jupyter Notebook extension

[00:00:59](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:00:59](hover-notes-images/screenshot-01M1P2CGWY88943DC4248HQ8FZ.png)
[00:00:59](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Jupyter Notebooks

- Provides a convenient way to run Python code step by step
    - Allows for immediate feedback on code execution

[00:01:05](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:01:05](hover-notes-images/screenshot-01M1P2DEAQ8CSWKS3AMYF7WY90.png)
[00:01:05](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

[00:01:07](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:01:15](hover-notes-images/screenshot-01M1P2ECB0WC1H9F66TTDP2FW0.png)
[00:01:15](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Notebooks vs. Backend Frameworks

- While production backend projects typically use frameworks like FastAPI, Django, or Flask, notebooks are preferred for learning and debugging
    - They allow for running small, isolated pieces of code at a time
    - They make it easy to inspect the exact contents of a response from Claude

### Lesson Roadmap

- The upcoming workflow for this lesson includes:

    1. Setting up the development environment
    2. Storing the API key safely
    3. Creating the Anthropic client
    4. Sending the first message
    5. Inspecting the API response

[00:01:37](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:01:38](hover-notes-images/screenshot-01M1P2FM3EJ5YX1D7J3251V9TZ.png)
[00:01:38](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:01:51](hover-notes-images/screenshot-01M1P2FM3EAK3JXXDY9P3EAH2K.png)
[00:01:51](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Getting an API Key

- Before building the full Shop Assist AI, the first step is verifying that Python can communicate with Claude
- To do this, an API key must be generated through the Anthropic Console
- **Process for creating a key:**

    1. **Open the Console**: Navigate to `console.anthropic.com` and log in
    2. **Name it**: Go to the API Keys section and create a new key with a clear, identifiable name (e.g., `my-api-key`)
    3. **Copy it once**: Copy the key immediately, as you will not be able to view it again after closing the dialog

- **Security Warning**:
    - Treat the API key like a password
    - Never hard-code it or commit it to a code repository
    - Store it as an environment variable so the SDK can read it automatically
    - If a key is ever leaked, rotate it immediately

[00:02:07](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:02:08](hover-notes-images/screenshot-01M1P2G73RQ3N8C0MZED5C48XG.png)
[00:02:08](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:02:25](hover-notes-images/screenshot-01M1P2G73RJZKVCDHVN5RD57X5.png)
[00:02:25](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:02:32](hover-notes-images/screenshot-01M1P2G73RW3914RNTBE58DDP3.png)
[00:02:32](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### API Key Security Best Practices

- **[Crucial]** Never expose your API key by:
    - Pasting it directly into Python code
    - Including it in frontend JavaScript
    - Committing it to GitHub
- **Storage Strategies**:
    - **Local Development**: Store the key in a `.env` file
    - **Production**: Use environment variables or a dedicated secrets manager

### Project Setup

- Initial project structure created in VS Code:
    - A root project folder
    - A `.env` file for secure key storage
    - A Jupyter Notebook (`.ipynb`) for the lesson

```text

# Contents of .env
ANTHROPIC_API_KEY="your-api-key-here"
```

[00:02:37](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:02:53](hover-notes-images/screenshot-01M1P2H41Q2DM4JY62TS2EFSWP.png)
[00:02:53](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:03:01](hover-notes-images/screenshot-01M1P2H41Q5N38ACPCYW0CM5M5.png)
[00:03:01](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:03:02](hover-notes-images/screenshot-01M1P2H41QFA771H6Y83PEER4Q.png)
[00:03:02](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Environment and Package Installation

- **Protecting Sensitive Files**
    - Add the `.env` file to `.gitignore` if using Git
    - **[Why?]** This prevents the API key from being accidentally committed to a version control system
- **Required Python Packages**
    - Install the necessary libraries using `pip`:

```bash
pip install anthropic python-dotenv
```

    - `anthropic`: The official Python SDK for interacting with Claude
    - `python-dotenv`: Allows the application to load variables from a `.env` file into the Python environment
- **Loading Environment Variables**
    - To use the stored key in a notebook, import the library:

```python
from dotenv import load_dotenv
```

[00:03:08](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:03:17](hover-notes-images/screenshot-01M1P2JBD2GTP0BMVAXA0B5TKQ.png)
[00:03:17](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Initializing the Anthropic Client

- **[Automatic Key Loading]** When initializing the client, you do not need to pass the API key directly into the code
    - The SDK automatically searches for an environment variable named `ANTHROPIC_API_KEY`
    - This follows the best practice of keeping secrets outside of the source code

```python
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
```

### Defining the Model

- **Model Selection**: The project will use `claude-3-5-sonnet-20240620` (noted as Claude Sonnet 3.5 in discussion)
    - **[Pro-tip]** Model names can change over time; always verify the specific string in the official Anthropic documentation for production projects

```python
model = "claude-3-5-sonnet-20240620"
```

[00:03:38](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:03:47](hover-notes-images/screenshot-01M1P2JYHHBK9FH21NAY2RY6TY.png)
[00:03:47](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Making the First Request

- **[Design Choice]** The model name is stored in a variable to allow for easy updates or changes later in the development process
- **The&#32;`client.messages.create`&#32;function**: This is the primary method used to send a message to Claude
- **Core Parameters for a Basic Request**:
    - `model`: Specifies which Claude model to use for the interaction
    - `max_tokens`: Defines the maximum number of tokens Claude is permitted to generate in its response
        - **[Important Distinction]** This is a ceiling (limit) on generation, not a target amount of text

[00:04:08](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:04:14](hover-notes-images/screenshot-01M1P2M5XZ4G7K6B2HGMG0D2BK.png)
[00:04:14](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Making the First Request (continued)

- **`max_tokens`&#32;parameter**: Acts as a ceiling for generation
    - It is a limit, not a target; the model will simply stop once it reaches this number
    - For short tasks like customer support, a value like 300 is sufficient
- **The&#32;`messages`&#32;parameter**: Contains the structured conversation sent to Claude
    - The conversation is represented as a list of message objects
    - Each message requires a `role` and `content`
        - `role`: Defines who is speaking (e.g., `"user"`)
        - `content`: The actual text of the message

```python
message = client.messages.create(
    model=model,
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "A customer wants to return an order. Write a short helpful response."
        }
    ]
)
```

[00:04:38](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:04:39](hover-notes-images/screenshot-01M1P2N3XC2FACVQ9RN77WHZVP.png)
[00:04:39](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:04:46](hover-notes-images/screenshot-01M1P2N3XC3D3AMBB9012M9QAC.png)
[00:04:46](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Inspecting the API Response

- **Accessing the response text**: To see only the text generated by Claude, you access the `content` attribute of the message object.
    - The content is a list of content blocks, so you access the first element's text using `[0].text`.

```python
print(message.content[0].text)
```

- **Example Output**:
    - For a customer support prompt, the output might look like:

    > Hi there, I'm sorry to hear you'd like to return your order! I'm happy to help make this process as easy as possible. Here's what to do next:

    > 1. Have your order number ready...

- **The&#32;`stop_reason`&#32;attribute**: The response object contains metadata explaining why the model stopped generating.
    - **[Why check this?]** It is important to know if Claude finished its thought naturally or if it was cut off because it hit the `max_tokens` limit.
    - **`end_turn`**: This indicates a normal, completed response where the model finished its intended task.
    - **`length`**: This indicates the model stopped because it reached the `max_tokens` ceiling.

```python
print(message.stop_reason)
```

[00:05:08](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:05:15](hover-notes-images/screenshot-01M1P2P0NNSDMVDY5TZJKBG5V6.png)
[00:05:15](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Understanding `stop_reason` values

- **`end_turn`**: Indicates Claude finished its response naturally.
    - **[Application Logic]** Since the response is complete, it is safe to display the text to the user.
- **`max_tokens`**: Indicates the model stopped because it reached the `max_tokens` limit.
    - **[Application Logic]** The response may be incomplete or cut off mid-sentence.
- **`tool_use`**: Indicates Claude is requesting the application to run a specific tool before it can proceed.
    - This is a key signal used when building more advanced agentic workflows.

| stop_reason | Meaning | Application Action |
| --- | --- | --- |
| end_turn | Completed naturally | Show response to user |
| max_tokens | Hit token limit | Handle incomplete text |
| tool_use | Requesting a tool | Execute tool and continue |

[00:05:38](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:06:06](hover-notes-images/screenshot-01M1P2PY8G8BPBST7CXV7DSQQF.png)
[00:06:06](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Inspecting the Full API Response

- **[Why print the full object?]** While users only need the generated text, developers need to see the complete structure during development to inspect metadata.
- **Key fields in the response object include**:
    - `id`: The unique response ID
    - `model`: The specific model used (e.g., `claude-sonnet-4-6`)
    - `role`: The role of the message (e.g., `assistant`)
    - `content`: The actual content blocks
    - `stop_reason`: Why the model stopped generating
    - `usage`: Information regarding token usage (e.g., `cache_creation`)

```python
print(message)
```

- **Example of a full response structure**:

```json
{
    "id": "msg_012TwBrtb78cukwg4QWKST",
    "type": "message",
    "model": "claude-sonnet-4-6",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "\nHi there,\nThanks for reaching out! We're sorry to hear you'd like to return your order, but we're happy to help make the process as easy as possible.\n\nHere's what to do next:\n\n1. Confirm eligibility..."
        }
    ],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {
        "cache_creation": "CacheCreation"
    }
}
```

[00:06:08](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:06:15](hover-notes-images/screenshot-01M1P2QHK5GDCGZGDRBGEK9099.png)
[00:06:15](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:06:16](hover-notes-images/screenshot-01M1P2QHK5T8QYNC4JESX1ZWDA.png)
[00:06:16](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Summary of Initial Setup

- **Development Environment**
    - Used Visual Studio Code with Jupyter Notebooks for step-by-step Python execution
- **Security and Configuration**
    - Stored the Anthropic API key in a `.env` file (avoiding hard-coding)
    - Loaded the key into the environment using `python-dotenv`
- **API Interaction**
    - Initialized the Anthropic client
    - Selected a specific Claude model
    - Sent the first message using the `client.messages.create` function
    - Capped response length with `max_tokens`
    - Passed the prompt through the `messages` parameter
    - Printed the generated text
    - Checked the `stop_reason` to understand the model's exit state
    - Inspected the full API response object for debugging

[00:06:38](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:06:39](hover-notes-images/screenshot-01M1P2RSTFP62FB60JKTVPFW7K.png)
[00:06:39](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Initial Setup Recap

- **Development Environment**
    - Ran Python step-by-step using VS Code + Jupyter
- **Security and Configuration**
    - Stored the API key in a `.env` file (never hardcoded)
    - Loaded the key using `python-dotenv`
- **API Interaction**
    - Created the Anthropic client
    - Selected a Claude model
    - Sent the first message via `client.messages.create`
    - Passed the user prompt through `messages`
    - Capped the response length with `max_tokens`
    - Printed the generated text
    - Checked `stop_reason`
    - Inspected the full `response` object

> The foundation for everything else. Next: ShopAssist AI's first backend flow.

[00:06:42](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:06:42](hover-notes-images/screenshot-01M1P2SE3287ZK6T143FX6X3NJ.png)
[00:06:42](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

[00:06:42](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

![00:06:43](hover-notes-images/screenshot-01M1P2SYZAJX58P8XKFEGJY8SG.png)
[00:06:43](https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview)

### Transition to Backend Development

- **Foundation Established**
    - Successfully configured the environment and security
    - Verified API connectivity with a basic request
- **Next Step: ShopAssist AI Backend Flow**
    - Moving from simple, isolated API requests to building the actual backend logic for the application