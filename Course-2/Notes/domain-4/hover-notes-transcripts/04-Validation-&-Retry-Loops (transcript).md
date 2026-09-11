---
hovernotes-transcript-of: doc_f80d64bb-a696-49ed-be39-99d36b287341
hovernotes-transcript-version: 2
note: "[[04-Validation-&-Retry-Loops]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57493853#overview"
updated: 2026-09-11T06:01:33.698Z
---

# 04-Validation-&-Retry-Loops — Transcript

**0:00 → 0:42**

Alright everyone, welcome back So in the last lecture, we got Claude to give us guaranteed valid JSON But we ended on a warning Valid does not mean correct The shape can be perfect and the numbers still wrong So this lecture is how you catch those wrong but valid answers And then fix them This is validation and retry loops So six things in this lecture Number one, syntax versus semantic errors Number two, the validation step Number three, retry with feedback Number four, retry limits

**0:42 → 1:28**

number five the self correction loop and number six a work loop all right so the first topic syntax versus semantic errors and the subtitle names the split there are two ways an answer can be wrong so look at the first kind a syntax error that is malformed json a broken shape and the good news is this one is already solved by tool use so notice we have met this before a syntax error is about the shape brackets that don't close fields that are broken and from the last lecture we know that tool use already guarantees the shape so this whole

**1:28 → 2:13**

kind of error is gone. Now look at the second kind, a semantic error. Here the shape is valid, but the content is wrong. Things like bad sums, a value in the wrong field, or a fabricated value. So notice why this one is trickier. The JSON looks perfectly fine, it passes every shape check. But the numbers inside are wrong and no amount of shape checking will ever catch that. And here is the distinction that the exam really leans on. Tool use kills syntax errors, but only validation catches the semantic ones. So please hold these two firmly apart because it is tested directly.

**2:13 → 2:58**

syntax is the shape and tool use handles it. Semantic is the meaning and for that you need a separate validation step which is exactly what we build next. Alright, so the second topic, the validation step and the subtitle tells you when it happens. After extraction, you verify the content with your own code. So look at what validation does. You check the values against your rules and against the source. So for example, do the line item sum to the total, is the date real and in range and does every value actually appear in the document? So notice these

**2:58 → 3:39**

meaning checks this is not clod checking its self this is your own code doing the arithmetic and the comparison adding up the line items checking the date makes sense and making sure that nothing was invented and here are the common semantic checks to remember do the totals add up are the dates and ranges same and does any value appear that isn't in the source because that would be fabrication so notice that last one especially checking that every extracted value actually exists in the In the original document is how you catch a made-up number if Claude reports a figure

**3:39 → 4:24**

nowhere in the source your validator flags it all right so the third topic retry with feedback and the subtitle gives you the golden rule don't just fail tell claude what was wrong so look at what you send back you send the document plus the bad extraction plus the specific error and you ask claude to correct it so for example you might say the line items sum to 4 800 rupees but the total says 5 000 rupees please fix so in that moment a failure becomes a guided correction so notice the shift you are not just rejecting the answer you are handing clod down

**4:24 → 5:10**

exact problem and asking it to fix that one thing. And here is the key. And it is everything. The feedback must be specific. So saying it's wrong barely helps. But saying the total doesn't match the line items fixes it fast. So please really take this in. A vague it's wrong gives Claude nothing to work with. It might change the wrong thing. But a precise error pointing at the exact mismatch tells it precisely what to fix. And so it fixes it on the very next try. All right. So the fourth topic, retry limits. And the subtitle is very sensible. You loop a few times.

**5:10 → 5:55**

and then you stop. So look at the rule. You cap your retries, commonly at two or three, and then you escalate. So each retry with feedback removes most of the remaining errors. But after the cap, you flag it for a human or you mark it as low confidence. Because you do not look forever on an input that Claude simply cannot fix. So notice the balance here. The first couple of retries fix nearly everything. But if it still fails after that, then something is genuinely hard and a human needs to look. And here is the warning. No cap means an infinite loop.

**5:55 → 6:39**

time and money on an input that Claude may simply be unable to fix. So please always set a cap, picture it, an input that Claude keeps getting wrong. Without a limit, it tries and fails and tries and fails forever quietly running up a bill. So the cap is what stops that. A few tries and then you hand it off. Alright, so the fifth topic, the self correction loop and the subtitle lays out the whole cycle. Extract, then validate, then feedback, then revalidate, then stop. So look at the five stages in order.

**6:39 → 7:19**

extract that is the tool use step then validate it that is where you check the meaning then feedback where if it fails you send the specific error then revalid it where you ask does it pass now and finally escalate where at the cap it goes to a human so notice how this all fits together everything we have covered so far becomes one connected loop extract check correct check again and if needed handoff and here is the beautiful idea This loop is self-directing.

**7:19 → 8:04**

Claude fixes its own mistakes when it is told precisely what they are. So please sit with that for a second. On its own, Claude made a mistake. But given a precise description of that mistake, it corrects itself. So you have built a system that catches its own errors and mends them with almost no human in the loop. Alright, so the sixth and final topic. A work example, the claim that didn't add up. And the subtitle tells you the ending. One bad total fixed in one retry. So here is the crucial thing to notice before we even start. the JSON was

**8:04 → 8:36**

it both times so only validation caught it so please hold that thought both attempts produced perfectly well for json so a shape check would have waved both straight through the only reason the error was caught at all is the validation step so look at attempt one it fails validation the line items are 2000 and 2800 but the total says 5000 so So the validator does the sum and says,

**8:36 → 9:22**

The sum is 4800. So notice exactly what happened. Claude added it up. Wrong. 2000 plus 2800 is 4800. But it wrote 5000. And your validator catches that mismatch. Now look at attempt 2. This is after the feedback. The line items are still 2000 and 2800. But now the total says 4800. So the validator passes. So notice how clean that was. You told Claude precisely that the sum was 4800 and not 5000. and on the very next try it fixed exactly

**9:22 → 10:07**

one specific correction and here is the whole lesson in one line the JSON was valid both times only the validation step got the wrong number so this is why this lecture exists structured output gave us a valid shape on both attempts but a valid shape is not correct content and it was the validation and retry loop that turned a wrong answer into a right one all right so let's hold this together the key takeaways from this lecture validation and retry in three lines number one validate the meaning tool use skills syntax errors but

**10:07 → 10:37**

the validation catches the semantic ones, the bad sums, the wrong fields and the fabrication. So remember, a valid shape still needs a meaning check. Number 2. Retry with feedback. On a failure, you send a specific error, so that Claude self-corrects. So remember, it's wrong, barely helps, but the exact mismatch fixes it fast. And number 3. Cap, then escalate. You cap your retries.

**10:37 → 11:07**

or retries at 2 or 3 and then you hand off to a human. You never loop forever. So remember the first couple of retries fix nearly everything and the cap protects you from the rest. Alright, so that is how you catch and fix the wrong but valid answers. In the next lecture, we will look at batch processing. So with this, I'm going to end this one and I will catch you in the next one.
