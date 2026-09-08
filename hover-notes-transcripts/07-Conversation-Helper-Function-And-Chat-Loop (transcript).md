---
hovernotes-transcript-of: doc_d9ff5fd8-8281-4c2c-a92e-dc219790bb9b
hovernotes-transcript-version: 2
note: "[[Conversation-Helper-Function-And-Chat-Loop]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042171#overview"
updated: 2026-09-04T11:48:24.185Z
---

# Conversation-Helper-Function-And-Chat-Loop — Transcript

**0:00 → 0:21**

We saw why conversation history matters. Cloud API requests are stateless. That means Cloud does not automatically remember what happened in a previous request. If we want ShopAssist AI to continue a conversation, our application must keep the previous messages and send them back to Cloud. We already tested this manual.

**0:21 → 0:51**

by creating a messages list. That worked, but writing message dictionaries by hand every time is not a good pattern. So in this lesson, we will clean up the code. We will create a few small helper functions. One function will add user messages. Another function will add assistant messages. And another function will send the current conversation to Claude. After that, we will add a system prompt. So ShopAssist AI does not just continue the conversation,

**0:51 → 1:21**

but also responds with the right role, tone, and behavior. Now let's make this easier to work with. Instead of manually writing dictionaries every time, we can create a few helper functions. First we need a function that adds a user message to the conversation history. The addUserMessage function does one simple job. It adds the user's latest message to the conversation history. It takes two inputs. The first input is messages. This is the list that stores the conversation

**1:21 → 2:03**

so far. The second input is text. This is the new message that the user wants to send. Inside the function, we call append on the messages list. This adds a new item to the end of the conversation. That new item is a dictionary with two keys. The first key is role. We set it to user because this message came from the user. The second key is content. We set it to the text that was passed into the function. So in plain English, every time we call add user message function, we take the user's latest message and add it to the conversation history, clearly labeled as a user message. Now let's create the same kind of helper function for Claude's replies. The added

**2:03 → 2:48**

message function does almost the same thing, but for Claude's response, it takes the same two inputs. Messages is the current conversation history. Text is the assistant response that we received from Claude. Inside the function we again call append, but this time the role is assistant. That tells Claude that this message was not written by the user, it was written by the assistant in an earlier turn. This distinction is important. When we send the conversation history back to Claude, Claude needs to know which messages came from the customer and which messages came from the assistant. Now let's create a simple function that actually sends the request to Claude. The chat function is responsible for Claude.

**2:48 → 3:34**

the Claude API. It takes one input messages. This is the full conversation history that we want to send to Claude. Inside the function we call client messages create, we pass the model, we set max tokens to 300. And we pass the full messages list. Claude then generates a response based on the context we provided. The response object contains more than just text. But for now, we only need the generated answer. So we return message content text. In plain terms, this function takes the current conversation, sends it to Claude and gives us back the assistance text response. Now let's use these helper functions together. Here we start with an empty list called messages. This list

**3:34 → 4:19**

all the conversation history. Then we call addUserMessage function. This adds the customer's first message to the list. After that, we call chatMessages. This sends the current conversation to Claude. Claude returns an answer, and we store that answer in the answer variable. Then we print the response using the label shopassist. Finally, we call addAssistantMessage. This saves Claude's response back into the conversation history. That last step is important. If we do not save Claude's answer, the next request will not include what the assistant said before. Now let's inspect the messages list. When we run this cell, we should see two messages. The first message has a role user. The second message has a role user. The

**4:19 → 5:04**

assistant. This is exactly what we want. Our Python list is now acting as a simple conversation history. Now let's add the customer's follow up message. This time we are not starting from an empty list. We are using the same messages list that already contains the previous conversation. So when we add the order number, Claude receives the full context. It sees that the customer first wanted to return an order. It sees that shop assist asked for the order number. And now it sees that the customer provided the order number. That is why Claude can continue the conversation naturally. But again, the important point is this. Claude did not remember the previous request by itself. We remembered it in our application. Then we

**5:04 → 5:29**

history back to Claude in the next API call, so now ShopAssist can continue a basic conversation, but it still does not have a clear role or behavior. It can use the previous messages, but we have not told it how a ShopAssist support agent should act. That is what we will fix next. Conversation history tells Claude what has been said. A system prompt tells Claude how to behave.
