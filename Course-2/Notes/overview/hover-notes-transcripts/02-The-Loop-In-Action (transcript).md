---
hovernotes-transcript-of: doc_f5834c5e-dbb2-4f1e-b521-fca072a6b50f
hovernotes-transcript-version: 2
note: "[[02-The-Loop-In-Action]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57908963#overview"
updated: 2026-09-10T09:23:08.269Z
---

# 02-The-Loop-In-Action — Transcript

**0:00 → 0:43**

Alright everyone, welcome back. So in the last lecture, we learned what the Argentic loop is. The four steps and the one signal that keeps it turning. But all of that was still a description. So this lecture is called the loop in action. And the subtitle tells you exactly what we are going to do. Let us watch a real loop run. So two things in this lecture. Number one, feeding results back. And number two, a full worked trace of a real customer question from start to finish. Alright, so the first topic is feeding the result back.

**0:43 → 1:28**

and the subtitle says it in one line. The tool's answer becomes Claude's next input. So look at the rule at the top. Now Claude reasons with real data and not a guess. And then the three points underneath it. After the tool runs, you append its result to the conversation. You send it back, so Claude sees what the tool found. And it goes in as a tool result. So there are three small words in there, which are worth unpacking properly. Now the conversation simply means the running list of messages that get sent to Claude every single turn. and appending means adding one

**1:28 → 2:13**

entry to the end of that list and the tool result is that new entry it is a message which says in effect you asked for this tool to run and here is what came back so that is the whole mechanism there is nothing cleverer hiding underneath it and now here is why this step exists at all because the tool did not run inside cloud it ran on your computer or on your server or somewhere out on the internet so cloud has no way of seeing that answer on its own it genuinely cannot look think Think of it like a colleague who asks you to check a file. If you check it and then say nothing,

**2:13 → 2:58**

still sitting there knowing nothing but now look at the warning skip this step and Claude never learns what the tool found so the loop falls apart so please take that one seriously because it is easily the most common beginner mistake you run the tool you get the answer but you never pass it back so on the next turn Claude is sitting there with the original question and nothing new at all so what does it do it asks for the same tool again and you go round and round achieving absolutely nothing all right now the second topic a full work trace And the question we are answering

**2:58 → 3:43**

is where is my refund for order 9931 so this is our customer from last lecture and now we watch the agent actually deal with her so look at the whole trace on the screen first claude calls look up order with the order number 9931 then the result comes back delivered and no refund on file then claude calls check refund policy then that result comes back eligible and finally and turn where claude explains the refund to the customer so let us walk through that slowly because the interesting part is not what it did. It is why. Claude's very first move is to look up the

**3:43 → 4:28**

notice it did not guess it did not say refunds usually take five working days it went and fetched the real record for this one specific customer and back comes two facts the order did arrive and no refund exists yet now look at what happens next Claude calls check refund policy and I want you to see why it picked that it has just learned that no refund was ever issued so the obvious next question becomes is this customer even entitled to one and that question only makes sense because of what the first tool returned then eligible comes back so she does

**4:28 → 5:14**

and then enter which from last lecture means Claude is finished and now here is the key insight of this whole lecture Claude chose each tool based on the previous result and that is the loop reasoning not a fixed script so please sit with that for a moment nobody wrote instructions saying first look up the order and then check the policy that order emerged and if the first result had been different if the order had shown a refund already issued then Claude would have gone somewhere else entirely and simply explained that refund instead alright so let us pull this together the key

**5:14 → 5:21**

from this lecture the loop in action in two lines so number one feed results back that is how cloud
