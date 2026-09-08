---
hovernotes-transcript-of: doc_0003c0c3-ceda-445e-ab40-652da011457d
hovernotes-transcript-version: 2
note: "[[Multi-Turn-Conversations-And-Manual-History]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042161#overview"
updated: 2026-09-04T11:40:01.203Z
---

# Multi-Turn-Conversations-And-Manual-History — Transcript

**0:00 → 0:28**

In the previous lesson, we made our first real request to Claude. We sent one user message, received one assistant response, and looked at the response object. That was useful, but it was still not a real chat application. A real support assistant does not work with one isolated message. The customer says something and Shop Assist replies. Then the customer adds more details. Then Shop Assist continues from the previous context. Before we build that loop, it is important

**0:28 → 0:58**

to separate two things. Using Claude as a product is not the same as building with Claude as a developer. When you use Claude in the Claude app or in the web interface, a lot of application behavior is already built for you. You type a message Claude replies, then you type another message and the conversation continues naturally. But behind the scenes, the app is managing the conversation for you. It keeps the previous messages, it sends the relevant chat history back to the model and it may

**0:58 → 1:28**

also provide built-in tools and product features that make the experience feel seamless. When we work with the API, we are not using that ready-made chat application. We are building our own. And each API request is isolated. Cloud does not automatically see the previous request. It does not automatically remember what the customer said one minute ago. And it does not automatically know what happened in another API call. By default, the Cloud API returns a response due to the API.

**1:28 → 1:58**

from the request we send right now. That means all important context must be included manually. If we want Claude to know the previous messages, we must send those messages. If we want Claude to follow our assistant persona, we must provide a system prompt. If we want Claude to use business data, tools, order information or customer information, we must connect those pieces in our application. So when we say multi-turn conversation, We are not talking about hidden

**1:58 → 2:29**

We are talking about our backend collecting the conversation history and sending the right context to Claude on every request. This is one of the main differences between using Claude as a product and building a Claude-powered application. Now let's see this directly in a notebook. First I'll use the same basic setup from the previous lesson. This first code cell prepares our notebook to work with Claude. We import load.nv so Python can load environment.

**2:29 → 2:59**

variables from our .env file. That is where we keep the API key. Then we import Anthropic, which is the official SDK client. After that we call load.env. This makes the environment variables available to our Python code. Then we create the client with client Anthropic. Because the API key is already available in the environment, we do not need to pass it directly in the code. Finally, we store the model name in a variable called model. This makes the rest of the code cleaner.

**2:59 → 3:29**

because we can reuse the same model variable in every request. Now let's send a simple support message. Imagine a customer starts a return request. This code sends one message to Claude. We call client messages create just like in the previous lesson. We pass the model. We set max tokens to 300, which limits the maximum length of Claude's response. Then we pass the messages list. Right now that list has only one message. The role is user because the message comes from the

**3:29 → 3:59**

customer. The content is I want to return my order. After Claude responds, we print only the generated text with message content text. Claude will probably answer like a support assistant and ask for more information, such as the order number. Now let's pretend the customer replies with the order number. But here is the mistake. We send only the new message. This code sends another API request. But notice what is missing. We are not sending the

**3:59 → 4:29**

first message. We are not sending Claude's previous reply. We are only sending the new user message. My order number is 12345. From the API point of view, this is a completely new isolated request. Claude may still produce a reasonable answer. But it does not truly know the previous turn. It does not automatically know that the customer is trying to return an order. It only sees the message we sent right now. And this is exactly why we should not build applications that

**4:29 → 4:59**

depend on the model guessing the missing context. If the context matters, we need to send it explicitly. Now let's send the same follow-up correctly. This time we include the conversation history. This time we create a messages list with three messages. The first message is from the user. The customer says they want to return an order. The second message is from the assistant. This represents Claude's previous reply, where ShopAssist asked for the order number. The third message is

**4:59 → 5:29**

from the user again. Now the customer provides the order number. Then we send the full messages list to Claude. Now Claude has the context. It can understand that order number one, two, three, four, five is connected to the return request. This is the core idea behind multi-turn conversations. The conversation is not stored automatically inside Claude. The conversation is stored and managed by our application. In a production application, that could be a database, a session store,

**5:29 → 5:59**

or another backend storage mechanism. In this notebook, we can start with a simple Python list. And that is the main idea I want you to take from this lesson. Cloud does not automatically remember previous API requests. If the context is important, our application must send that context again. In the Cloud app, this is already handled for us. But when we build our own application with the API, conversation history becomes part of our architecture. For now, we manually created

**5:59 → 6:19**

messages list and sent it to Claude. In the next lesson, we will clean this up. Instead of manually writing message dictionaries every time, we will create small helper functions. Those functions will make it easier to add user messages, save assistant responses and build a simple reply loop for ShopAssist AI.
