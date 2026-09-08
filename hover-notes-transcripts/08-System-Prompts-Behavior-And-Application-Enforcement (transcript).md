---
hovernotes-transcript-of: doc_b4f76133-fec7-41ee-9945-7a993589912b
hovernotes-transcript-version: 2
note: "[[08-System-Prompts-Behavior-And-Application-Enforcement]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042185#overview"
updated: 2026-09-04T12:01:07.436Z
---

# 08-System-Prompts-Behavior-And-Application-Enforcement — Transcript

**0:00 → 0:28**

In the previous lesson, we built a basic multi-turn conversation. Our application stored the conversation history and sent it back to Claude with each new request. That gave ShopAssist context. Now we need to give it behavior. We do not want a generic chatbot. We want ShopAssist AI, a concise, polite customer support assistant that follows our support rules. This is where the system prompt comes in. The messages list tells Claude what has been said.

**0:28 → 0:58**

so far. The system prompt tells Claude how the assistant should behave. For ShopAssist AI, we do not want Claude to sound like a generic chatbot. We want it to behave like a helpful customer support assistant for an online store. So let's define a system prompt. This code defines a variable called system prompt. The value is a multi-line string. The first line tells Claude who it is. It is ShopAssist AI, a helpful customer support assistant for

**0:58 → 1:28**

store. The next line describes the kind of tasks it should handle. Order questions, returns, refunds, shipping issues, and product support. Then we define the tone. Be concise, polite, and practical. After that, we add an important behavior rule. Do not promise a refund until the order is checked. And finally, we tell Claude how to ask for missing information. If more information is needed ask one clear question at a time this is a good example of a system prompt

**1:28 → 1:58**

It does not contain the user's current message. It contains the assistant's role, tone, and behavior guidelines. Now we can update our chat function to include the system prompt. This updated chat function is almost the same as before. The important difference is this line. System was set as a system prompt. That means every request will now include the ShopAssist AI instructions. So Claude will not only see the conversation history, it will also know how it should behave inside

**1:58 → 2:36**

that conversation. The system prompt is not just another user message. It has its own place in the API request. That matters because the system prompt is where we usually put durable instructions for the assistant's behavior. The messages list answers the question, what has been said so far? The system prompt answers the question, how should the assistant behave? Now let's test this again from the beginning. Here we start a new conversation. So we reset messages to an empty list. Then we add a user message. The customer says they bought headphones last week, the headphones do not work.

**2:36 → 3:22**

want their money back. Then we call chat messages. This sends the customer message to Claude, together with the system prompt. Because the system prompt says not to promise a refund before the order is checked, ShopAssist should be helpful but careful. It can acknowledge the issue. It can ask for the order number. It can explain the next step, but it should not immediately say, your refund is approved. That is the behavior we want. Now let's continue the conversation. Now we add the customer's next message to the same conversation. The customer gives the order number. Then we call chat messages again. Because we are using the same messages list, Claude sees the

**3:22 → 4:07**

customer has broken headphones and wants a refund, it knows that ShopAssist already replied. And now it sees the order number. This is what creates the feeling of a real conversation. But technically it is not hidden memory. It is the conversation history that our code sends to Claude. Now let's inspect the final messages list. When we display the messages list now, we should see the full conversation. A user message, an assistant response, another user message, another assistant response. This list is the conversation state. In a real application, we would usually store this somewhere outside of the Python process. For example, in a database or session storage. But the basic structure is the same.

**4:07 → 4:52**

the application owns the conversation history. Claude generates the next response based on the context the application sends. Before we finish, there is one more important architectural point. A system prompt can guide behavior, but it is not the same as a guaranteed business rule. For example, we can tell Claude, do not issue refunds before customer verification. That is a good instruction, but if this rule is financially important, the backend should still enforce it programmatically. The prompt is guidance. The application code is enforcement. This distinction will become more important later when we add tools like lookup order, process refund, and escalate to human. For now, our goal is simpler.

**4:52 → 5:37**

is to keep the conversation going and maintain a consistent persona. So the basic structure of our application is first, define the system prompt. Second, keep messages list for the conversation history. Third, when the user sends a message, append it with the user role. Fourth, send the system prompt and messages to Claude. Fifth, take Claude's response and append it back with the assistant role. Then repeat. There are also practical limits. If the conversation becomes very long, the context becomes larger. That can increase cost, latency, and complexity. So in production, we usually do not keep unlimited role history forever. We may summarize older terms. We we may store important facts separately.

**5:37 → 6:01**

structured state like customer ID, order ID, and refund intent. But the foundation is still the same. Cloud can only respond based on the context we provide. In this lesson, we added two key building blocks. Multi-turn conversation history, which lets ShopAssist continue the chat, and the system prompt, which gives ShopAssist its role
