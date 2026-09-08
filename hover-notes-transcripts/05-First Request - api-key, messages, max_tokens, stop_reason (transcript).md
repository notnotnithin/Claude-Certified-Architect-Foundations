---
hovernotes-transcript-of: doc_2f64480a-9f4d-442b-8291-b4589928b0db
hovernotes-transcript-version: 2
note: "[[First Request - API Key, Messages, max_tokens, stop_reason]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042147#overview"
updated: 2026-09-04T11:28:32.328Z
---

# First Request - API Key, Messages, max_tokens, stop_reason — Transcript

**0:00 → 0:29**

are ready to move from the request flow to a real API call. For this course I will use Python. Python is one of the most popular choices for API demos, backend prototypes, automation and AI workflows. But this is not a Python only course. The same cloud API concepts apply if you use another supported language. Anthropic provides official SDKs for multiple languages including Python, TypeScript, Java, Go Ruby.

**0:29 → 0:59**

PHP and the command line. So the exact syntax may change from language to language, but the course structure stays the same. You create a client, send messages, set parameters like model and max tokens, and read the response. If your production stack uses Node.js, Java, Go, or another supported language, you can port the same ideas to that SDK. For this course, I will use Visual Studio Code with the Jupyter Notebook extension.

**0:59 → 1:05**

This gives us a convenient way to run Python code step by step and immediately

**1:05 → 1:07**

See the output below each code section. the output below each code section.

**1:07 → 1:37**

In a real backend project, you may use regular Python files, FastAPI, Django, Flask, or another framework. But for learning and debugging, notebooks are very useful because we can run one small piece at a time and inspect exactly what Claude returns. In this lesson, we will set up our environment, store the API key safely, create the Anthropic client, send our first message, and inspect the response. We are still building toward our course project.

**1:37 → 2:07**

Shop Assist AI. Eventually, Shop Assist AI will help customers with orders, returns, refunds and product questions. But before we build a full assistant, we need to verify one basic thing. Can our Python code talk to Claude? First we need an API key. Open the Anthropic console. In your browser, navigate to console.anthropic.com and log in to your Anthropic account. Go to the API keys section and create a new key. it a clear name.

**2:07 → 2:37**

For example, shopassist.ai key. Now very important, do not paste your API key directly into your Python code. Do not put it into frontend JavaScript. Do not commit it to GitHub. For local development, we will store it in a .env file. In production, you would usually store it as an environment variable or in a secrets manager. Now let's create the project structure. In VS Code, I have a folder for this project. Inside it, I will create a notebook for this lesson and a .env.

**2:37 → 3:08**

file. The .env file will contain the API key. If you are using git, also add .env file to gitignore. This helps prevent accidentally committing your API key. Now let's install the packages we need. In the first notebook cell, I will run pip install anthropic python.env. The anthropic package is the official python SDK. The python.env package lets us load variables from the .env file into our python environment. Now let's load the environment

**3:08 → 3:38**

variables and create the client. Notice that we are not passing the API key directly into the code. The SDK will automatically look for an environment variable named Anthropic underscore API underscore key. That is the pattern you should remember. Keep secrets outside the code. Now let's define the model in one place. Model is Claude Sonnet 4.6. Model names can change over time, so in real projects you should always check the current Anthropic documentation.

**3:38 → 4:08**

but the important architecture idea is the same. We keep the model name in a variable so it is easy to change later. Now let's make the first request. The main function we use is client messages create. For a basic request we need three important parameters. The first one is model. This tells Claude which model we want to use. The second one is max tokens. This is the maximum number of tokens Claude is allowed to generate in the response. It is not a target.

**4:08 → 4:38**

try to use all available tokens. It simply stops if it reaches that limit. For a short customer support answer, 300 tokens is more than enough. The messages parameter contains the conversation we sent to Claude. Here we send one message with the role user. The content is, a customer wants to return an order. Write a short helpful response. This is similar to a user typing into a chat. But in the API, we represent that chat message as structured

**4:38 → 5:08**

Now let's print the response text. Claude should return a short customer support answer. We should see something like this. Hi there, I am sorry to hear you'd like to return your order, and then the details we expect from the client. But the response object contains more than just the text. Now let's inspect why Claude stopped generating. Print message stop reason. For a normal completed response we will often see, and turn. This means Claude finished its item.

**5:08 → 5:38**

naturally. Another possible value is max tokens. That means Claude stopped because it reached the limit we set in max tokens. This is important for application logic. If stop reason is n-turn, we can usually show the response to the user. If stop reason is max tokens, the response may be incomplete. Later in the course when we use tools, we will see another important stop reason. Tool use. That That means Claude is asking our application to run a tool before it can continue.

**5:38 → 6:08**

For example, ShopAssist AI may need to look up an order in the database before answering a refund question. Finally, let's print the full response object. Print message. This is useful because we can see the complete structure returned by the API. We can inspect fields like the response ID, model, content, role, stop reason, and token usage. In real applications we usually do not print the full object to the user. during development

**6:08 → 6:38**

It is very helpful. It lets us understand what the API returns and which fields our backend can use. So let's summarize what we did. We used Visual Studio Code with Jupyter notebooks to run Python code step by step. We stored the API key in a .env file instead of hard coding it. We loaded the key with Python.env. We created the Anthropic client. We selected a cloud model. We sent our first message using client messages create function. we

**6:38 → 6:42**

We used messages to send the user prompt. We used max token.

**6:42 → 6:42**

Thank you.

**6:42 → 7:01**

To limit the response length, we printed the generated text, we checked stop reason, and finally we inspected the full response object. This is the foundation for everything else we will build in this course. In the next lesson, we will start turning this simple request into the first backend flow for ShopAssist AI.
