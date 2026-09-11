---
hovernotes-transcript-of: doc_af0b54d8-f5a3-4073-b0fd-2a43fe68ba91
hovernotes-transcript-version: 2
note: "[[09-Temperature-ModelSelection-Prefill-And-StopSequences]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042193#overview"
updated: 2026-09-04T12:40:12.847Z
---

# 09-Temperature-ModelSelection-Prefill-And-StopSequences — Transcript

**0:00 → 0:13**

In the previous lessons, we made requests to Claude, added conversation history, and use the system prompt to control the behavior of ShopAssist AI. Now let's look at a few important parameters that help us

**0:13 → 0:43**

control how Claude responds. In this lesson we will cover three things. Model selection, temperature and stop sequences. These settings are small, but they matter a lot when you move from a demo to a real application. Let's start with model selection. When you build with Claude you should not think only in terms of model names. Model names can change and new models can appear. The architectural question is simpler. What kind of task are we solving? For many production applications,

**0:43 → 1:13**

general purpose model as a default. In ShopAssist, this is useful for normal customer support conversations, where the model needs to understand context, follow policy, and produce a helpful answer. For simple high-volume tasks, you may use a smaller or faster model. For example, detecting whether a message is a refund request, classifying intent, extracting a short field, or routing a case to the right workflow. complex or high-risk tasks you should test a more capable reasoning

**1:13 → 1:43**

model. For example, resolving a multi-step customer issue, handling policy exceptions, analyzing conflicting information, or coordinating an advanced agentic workflow. So the important idea is this. Do not choose the most powerful model automatically. Choose the model based on the task. A simple task does not always need the most expensive model, but a risky or complex task should not be optimized only for cost. In a real architecture, you may even use multiple

**1:43 → 2:15**

models together, a faster model for classification and routing, and a stronger model for the final customer-facing response. Now let's look at temperature. When Claude generates text, it does not write a full sentence all at once. It predicts the next token. For example, after a phrase like, what do you think, Claude may consider many possible next tokens. Maybe the next token could be about would of is when makes OE. Each option has some probability, one token is

**2:15 → 3:00**

likely, other tokens are less likely. Temperature changes how strongly Claude follows those probabilities. At low temperature Claude becomes more deterministic. It usually chooses the most likely token. At higher temperature Claude allows more variety. When the temperature is close to zero the model strongly prefers the highest probability token. So one token gets almost all the probability. This makes the output more stable and predictable. When we move the slider closer to one the probability becomes more spread out. Now lower probability tokens have a better chance to be selected. This does not mean Claude becomes random in a bad way. It means Claude has more freedom to choose less obvious options. For shoppers

**3:00 → 3:45**

AI. This is important. If we are writing refund policy answers, we probably want a low temperature. We want the answer to be consistent. But if we ask Claude to brainstorm five creative product campaign ideas, then a higher temperature can be useful. So temperature is not about good or bad, it is about matching the setting to the task. For support automation, we usually want predictable behavior. So we can use a low temperature. Here, temperature equals zero tells Claude to be more consistent. It does not mean the output will be perfectly identical every time, but it reduces randomness. For ShopAssist AI, this is useful because we do not want customer support replies to change too much from one request.

**3:45 → 4:31**

other. If we were writing creative product descriptions, marketing copy or brainstorming ideas, we might use a higher value. But for support extraction, classification and policy driven decisions, lower temperature is usually better. Now let's look at stop sequences. A stop sequence is a custom text marker that tells Claude when to stop generating. For example, imagine we want Claude to generate only the customer face in reply and then stop before an internal notes section. We can use a marker like this. The stop sequences parameter accepts a list of strings. If Claude generates one of those strings, the API stops the response, stop reason will tell us why the response stopped. If it stopped because of our customer

**4:31 → 5:16**

marker, the stop reason will be stop sequence, and stop sequence will show which exact sequence was used. This is useful when your application needs to separate sections, prevent extra text, or stop generation at a non-boundary. But stop sequences are not the same as validation. They can help control where the model stops, but they do not guarantee that the full output is correct. So for production systems, especially when we expect JSON or tool calls, we still need validation in code. Let's summarize. Use model selection to balance reasoning quality, speed, latency, and cost. For ShopAssist AI, choose a strong general purpose model as the default for customer support conversations. Use smaller

**5:16 → 5:50**

or faster models for simple classification, routing, summaries, and other low-risk background tasks. Use the most capable reasoning model for complex cases, policy exceptions, multi-step analysis, or high-impact decisions. As new models appear, do not memorize only the names. Focus on the role each model plays in your system – default assistant, fast utility model, or highest reasoning model. Use low temperature when you need predictable support behavior. Use stop sequences when your application needs claw to stop at a specific time.
