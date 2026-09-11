---
hovernotes-transcript-of: doc_56d1795b-9c02-433d-882c-52fc9f03567e
hovernotes-transcript-version: 2
note: "[[02-Structured-Error-Responses]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460123#overview"
updated: 2026-09-10T13:04:15.515Z
---

# 02-Structured-Error-Responses — Transcript

**0:00 → 0:43**

Alright everyone, welcome back. So in the last lecture we designed the tool so that Claude picks it and calls it correctly. But here is the thing, even a perfectly described tool will sometimes fail. The payment bounces, the database is down, the order simply isn't there. So this lecture is about that exact moment, this is structured error responses. Because when a tool fails, your error message is Claude's only clue. So six things in this lecture. Number one, errors are Claude's window into failure. to the ease a reflection

**0:43 → 1:28**

Number 3, Error Categories Number 4, Is Retriable Number 5, An Empty Result Versus A Real Failure And Number 6, Writing A Useful Error Alright, so the first topic Errors are Claude's window into failure And the subtitle makes the problem clear Something went wrong, tells Claude absolutely nothing So, look at the useless error first It just says, Booking failed And that leaves Claude completely stuck With nothing to act on So, notice why this is a dead end Booking failed does not say why it failed Was the card

**1:28 → 2:13**

declined, was the flight full, was the whole service down. So Claude has no idea what to do next because you told it nothing about what actually went wrong. Now look at the actionable error. Something like payment failed insufficient balance or refund in 3 days, try another method. So notice the difference immediately. These errors do not just say that something broke. They say exactly what broke and they even hint at the next move. So Claude can now do something sensible. It can tell the customer their balance is low or it can suggest a different payment method. And here is the principle underneath it.

**2:13 → 2:58**

and only act on what the error actually says. So, vague errors force it to guess, and specific errors let it recover. So, please hold on to that. Claude is not sitting inside your system, watching what happened. All it ever sees is the text of the error you handed back. So, that one little message is the entire window it has into what went wrong. All right. So, the second topic, the isError flag, and the subtitle tells you exactly what it is. One true or false value that says, I ran, but I failed.

**2:58 → 3:44**

how you use it, you return is error, sad to true, inside an otherwise successful response. So that Claude actually sees the failure and can react to it. So you don't throw a raw exception because Claude handles that very poorly. It should be a readable failure and not a crash. So please notice the clever bit here. The call itself succeeds at the technical level. But inside it, you have raised a little flag that says, careful, the real work failed. And because it all came back cleanly, Claude can read it and respond. Now here is why you must not just throw. A thrown exception becomes a low level.

**3:44 → 4:29**

protocol error. So you return isError set to true with details instead. So think about the difference. If your tool crashes with an exception, that failure happens below the conversation, down at the plumbing level where Claude cannot see it or reason about it, but any error response arrives as a normal message that Claude can read and act on. So always hand the failure back gently as data. Alright, so the third topic, error categories, and the subtitle points out something important. Not all failures are the same kind of failure. So look at the four kinds. validation

**4:29 → 5:14**

that is bad input so fix it and retry second, auth or permission that is not allowed so escalate it third, not found there is simply nothing there to return and fourth, rate limit or transient the service is busy so wait and then retry so notice that each category points to a completely different next move bad input you fix, not allowed you escalate nothing there you accept busy you wait so four failures and four different responses now here is the instruction you tag every error with an error category because each kind implies

**5:14 → 5:59**

different next move for Claude. So notice why this tag is so powerful. Without it, every failure looks the same and Claude has to guess how to react. But with the category attached, Claude instantly knows which of those four paths to take. So that one small label turns a vague failure into a clear decision. Alright, so the fourth topic is retryable. Should Claude try again? And the subtitle makes a big claim. It is the single most useful field in your error. So look at what it does. It is one true or false value, text stops, blind return,

**5:59 → 6:44**

loops so is retriable true means the failure was transient or a rate limit so wait a moment and retry and is retriable false means it was validation or a business rule so retrying it is pointless and a business error like a refund over the limit is never retriable so notice how this directly guides claude one flag tells it whether trying again could ever help or whether it would just be banging on a locked door and here is the warning retrying a validation or business error just burns calls and time because the answer will be no it's not a business error and it's

**6:44 → 7:30**

every single time. So think about why that matters. If the input was invalid, it is still invalid on the second try. And if a refund breaks a policy, it still breaks it on the tenth try. So without this flag, an agent can sit there retrying a thing that can never possibly succeed, wasting money and time on every single loop. Alright, so the fifth topic and this one is a classic trap. An empty result versus a real failure. And the subtitle states the key idea, found nothing is a success and not an error. So look at the first case, success but empty. it.

**7:30 → 8:15**

Error is false and the result count is zero. And that is a real genuine answer. No orders found. So notice that this is not a failure at all. The tool worked perfectly. It looked and it correctly reported that there was nothing there. So an empty answer is still a complete and successful answer. Now look at the second case. Access failed. Here is error is true and it is retryable. Something like couldn't reach the database. So notice how different this one is. This time the tool never got to look at all. It could not even reach the data. So, it does not know whether they were orders

**8:15 → 9:00**

not so that is a genuine failure and it is worth retrying and here is the trap and it is the classic one for this whole domain an agent retrying a successful empty query so remember this empty is an answer a failure is not so please be very careful with this distinction because it is heavily tested if your empty result looks like an error the agent will retry it again and again hunting for orders that simply are not there so an empty result must clearly say i succeeded and the answer is nothing. Alright, so the sixth and final topic, writing a useful error may

**9:00 → 9:45**

And the subtitle gives you the recipe. What was attempted, what failed, and what to do next. So here is the balance you are aiming for. You say enough to recover, but nothing that leaks. So a good one reads like, couldn't fetch order number 4471. The database timed out after 5 seconds. This is transient, safe to retry. A bad one is just a bare error. And you never return a raw stack trace because it leaks your internals. So you sanitize, you wrap a raw message like no search table, users v2 into something safe. Like the requested resource could not be accessed. be accessed.

**9:45 → 10:30**

So notice the two goals sitting together, say plenty about what to do next, but say nothing that exposes how your system is built inside. And here is why that masking matters so much. A raw stack trace confuses Claude and it reveals your database and your internal structure. So you mask it. So think about both harms at once. To Claude, a ball of stack trace text is just noise. That makes it harder to see the real problem. And to an outsider, that very same text is a free map of your table names and your file paths. So one clean, sanitized message fixes both. it helps clot and

**10:30 → 11:15**

nothing away. Alright, so the key takeaways from this lecture, structured errors in three lines. Number one, return, don't throw. And his error response with details is Claude's only clue. A thrown exception is not. Number two, category plus retryable. You tag the error category and is retryable. So Claude knows whether to fix, wait, escalate or stop. And number three, empty is not failure. And his error of false with a count of zero is a success. So you never retry it as a failure. So notice the single idea running through this whole lecture. When a tool fails, Claude is not in the room.

**11:15 → 12:01**

It cannot see your logs or your exceptions or your database. All it has is the error message you chose to hand back. So a good error is not an afterthought. It is a small structured note that tells Claude what happened and what to do about it. So write it well and the agent recovers gracefully. Write it badly and it guesses or it loops. Alright. In the next video, we step back and ask a different question. Not how to describe one tool, but how many tools to hand Claude in the first place and how to steer each choice. This is tool distribution and tool choice. That means the too many tools problem

**12:01 → 12:13**

Scoping Tools to the Job, the Tool Choice Level, its 4 modes, when to use each, and a Work example. So with this, I am going to end this one, and I will catch you in the next one.
