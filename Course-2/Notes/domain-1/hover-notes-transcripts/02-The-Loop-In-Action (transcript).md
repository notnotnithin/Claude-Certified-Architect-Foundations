---
hovernotes-transcript-of: doc_3b34ff37-4787-47e4-8513-b3cbd970608e
hovernotes-transcript-version: 2
note: "[[02-The-Loop-In-Action]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908963#overview"
updated: 2026-09-10T10:30:41.957Z
---

# 02-The-Loop-In-Action — Transcript

**0:00 → 0:14**

Alright everyone, welcome back. So in the last lecture we learned what the Argentic loop is, the 4 steps and the 1 signal that keeps it turning. But all of that was still a discussion.

**0:14 → 0:26**

So, this lecture is called the loop in action and the subtitle tells you exactly what we are going to do. Let us watch a real loop run. So two things in this lecture.

**0:26 → 1:11**

Number 1 feeding results back and Number 2 a full worked trace of a real customer question from start to finish. Alright, so the first topic is feeding the result back and the subtitle says it in one line. The tool's answer becomes Claude's next input. So look at the rule at the top. Now Claude reasons with real data and not a guess and then the three points underneath it. After the tool runs, you append its result to the conversation. You send it back so Claude sees what the tool found and it goes in as a tool result.

**1:11 → 1:57**

are three small words in there which are worth unpacking properly now the conversation simply means the running list of messages that get sent to cloud every single turn and appending means adding one more entry to the end of that list and the tool result is that new entry it is a message which says in effect you asked for this tool to run and here is what came back so that is the whole mechanism there is nothing cleverer hiding underneath it and now here is why this step exists at all because the tool did not run inside cloud it ran on your computer or on your server

**1:57 → 2:42**

or somewhere out on the internet. So Claude has no way of seeing that answer on its own. It genuinely cannot look. Think of it like a colleague who asks you to check a file. If you check it and then say nothing, they are still sitting there knowing nothing. But now look at the warning. Skip this step and Claude never learns what the tool found. So the loop falls apart. So please take that one seriously because it is easily the most common beginner mistake. You run the tool, you get the answer, but you never pass it back. So on the next turn Claude is sitting there with the original question. and

**2:42 → 3:27**

nothing new at all. So what does it do? It asks for the same tool again and you go round and round achieving absolutely nothing. Alright now the second topic a full work trace and the question we are answering is where is my refund for order 9931. So this is our customer from last lecture and now we watch the agent actually deal with her. So look at the whole trace on the screen. First Claude calls lookup order with the order number 9931. Then the result comes back delivered and no refund on file. Then Claude calls check refund policy then that result comes back.

**3:27 → 4:12**

eligible. And finally, end-turn where Claude explains the refund to the customer. So let us walk through that slowly because the interesting part is not what it did, it is why. Claude's very first move is to look up the order. Notice it did not guess, it did not say refunds usually take 5 working days. It went and fetched the real record for this one specific customer. And back comes two facts. The order did arrive. And no refund exists yet. Now look at what happens next. Claude calls check refund policy and I want you to see why it picked that.

**4:12 → 4:57**

that no refund was ever issued. So the obvious next question becomes, is this customer even entitled to one? And that question only makes sense because of what the first tool returned. Then eligible comes back. So she does qualify and then intern, which from last lecture means Claude is finished. And now here is the key insight of this whole lecture. Claude chose each tool based on the previous result and that is the loop reasoning, not a fixed script. So please sit with that for a moment. Nobody wrote instructions saying, first look up the order and then check the policy. That order is done.

**4:57 → 5:42**

And if the first result had been different, if the order had shown a refund already issued, then Claude would have gone somewhere else entirely and simply explained that refund instead. Alright, so let us pull this together. The key takeaways from this lecture, the loop in action in two lines. So number one, feed results back. That is how Claude learns within the loop. So remember that colleague who checked the file and said nothing. If the result never travels back, Claude learns nothing at all and the loop just stalls in place. And number two, live chaining. Claude chains tools live, each choice driven by the last result.

**5:42 → 6:22**

remember you are not writing the sequence in advance you are handing claude a set of tools and letting it build the sequence as it goes which means the same agent can handle situations that you never specifically planned for all right in the next video we finish off the argentic loop by asking who should be deciding these steps that means looking at model driven versus hard-coded and then the three anti-patterns which are the classic ways that people break a loop so with this i'm going to end this one and i will catch you in the next one
