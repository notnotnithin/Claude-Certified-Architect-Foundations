---
hovernotes-transcript-of: doc_bd3ace38-36d6-47fe-91aa-5b62203d0727
hovernotes-transcript-version: 2
note: "[[02-Few-Shot-Prompting]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57493847#overview"
updated: 2026-09-11T05:28:24.400Z
---

# 02-Few-Shot-Prompting — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So in the last lecture, we learned to tell Claude clearly what good looks like. But there is an even more powerful move than telling. And that is showing. This lecture is few-shot prompting and the subtitle captures it perfectly. Don't just tell Claude what you want, show it. And in fact, this is the very technique I promised you back in domain 3. So here it is in full. So 7 things in this lecture. Number 1, 0, 1 and few-shot. Number 2, why examples beat description. 3, pinning.

**0:42 → 1:28**

and format number four generalization number five reducing hallucination number six choosing good examples and number seven how many and in what order all right so the first topic zero one and few shot and the subtitle tells you why we are here the number of examples you show actually has a name so look at the three in order first zero shot that means no examples at all just instructions then one shot that means you give one example and then few shot that means several examples.

**1:28 → 2:11**

that is the clearest pattern of the tree. So notice how this simply count upward. Zero examples, then one example, then a few examples. And as you will see, showing a few is usually the strongest of the lot. Now here is the plain English key. The word short just means example. So few short really just means here are a few examples. Now do the same. So do not let that fancy name confuse you. It sounds technical, but it is the simplest idea. You show Claude a handful of examples and then you ask it to carry on in exactly that way.

**2:11 → 2:56**

Alright, so the second topic, why examples beat description? And the subtitle makes a bold claim. One good example can replace a whole paragraph of rules. So look at the first approach, description only. This is where you write a wall of rules for the tone and the format. And the trouble is, it is hard to write and it is easy to misread. So notice the problem. To describe in words exactly how you want something to look and to sound, you end up writing a long fiddly list of rules. And a long list of rules is easy to get wrong when you write it and easy for Claude to misread when it

**2:56 → 3:41**

That's it. Now look at the other approach, one example. A single good example shows the tone, the format and even the edge handling all at once. So the motto is show, don't tell. So notice how much one example carries. Instead of describing the tone in words, you just show a sentence in that tone. Instead of describing the format, you show the format. So one example does the work of a whole page of rules. And here is the deeper reason. An example carries details that you would struggle to write down as rules. So please sit with that because it is the heart of the slide. Some things are almost impossible.

**3:41 → 4:26**

to put into rules, the exact warmth of a tone, a subtle spacing in the format, but an example just shows all of it naturally. So the example captures things that words never quite good. All right, so the third topic, pinning, meaning and format. And the subtitle tells you the two jobs. Examples kill ambiguity and they lock the output shape. So look at the first job, reducing ambiguity. An example shows what you actually mean by a fuzzy label like urgent. So think about that word urgent for a second. It is vague. What counts as urgent to you

**4:26 → 5:11**

not to Claude. So instead of arguing about the definition, you just show an example of an urgent case. And now Claude knows exactly what you mean by that label. Now the second job, format consistency, you show the exact shape you want back. And then Claude copies it every single time. So notice how reliable that makes things. If you want the output in a particular shape, you do not describe the shape, you show one in that shape. And Claude simply matches it on every response. So your output stays consistent and tidy. And here is a very practical rule.

**5:11 → 5:57**

classifier that is inconsistent about a fuzzy label or messy about its format, then the fix is usually to add examples. So please remember this one because it is exactly how these problems get solved. When Claude keeps getting a fuzzy label wrong or keeps breaking the format, your first move is not more description. It is a few clear examples. Alright, so the fourth topic, generalization and the subtitle reveals something clever. Claude copies the pattern, not the literal examples. So look at what is really happening. examples teach the underlying rules

**5:57 → 6:42**

So Claude can then handle new inputs that it has never seen before. For example, show it three messy addresses turned clean. And then it will clean a fourth one on its own. So this is really training by demonstration. So notice the important word there, new. You are not just teaching Claude to repeat your three examples. You are teaching it, the rule behind them. So when a brand new fourth address arrives, it knows exactly what to do. And here is the key idea. The goal is the pattern behind the examples, not memorizing those exact cases. So please be clear about this because it is the whole part of the example.

**6:42 → 7:27**

of examples, you are not giving Claude a lookup table of specific answers, you are giving it a few cases so that it can work out the general rule and then it applies that rule to everything new. Alright, so the fifth topic and this one is important, reducing hallucination and the subtitle tells you the trick, example show the safe way to handle I don't know. So look at the technique, you include an example where the information is missing, so you show a case where the right answer is not found or a null value and that just means nothing there.

**7:27 → 8:12**

invent data because one honest example teaches honesty so notice what you are doing you are deliberately showing claude a case where the correct move is to admit there is nothing here and that one example teaches it that saying nothing is sometimes exactly the right answer and here is the warning and it is a subtle one if every single example is a full case with all the data present then claude assumes it must always produce a value so it fabricates one so you must show a missing data case. So please think about why this happens. If Claude only ever sees

**8:12 → 8:57**

complete examples, it quietly learns. The answer is always there somewhere. So when it hits a case with missing data, it feels it has to invent something and that is a hallucination. So one missing data example prevents it. Alright, so the sixth topic, choosing good examples and the subtitle lists the three qualities, diverse, correct and covering the edge cases. So look at the first quality, correct, because a wrong example teaches the wrong thing. So So notice how obvious and yet how important this really

**8:57 → 9:43**

Claude will faithfully copy whatever you show it. So if your example has a mistake in it, then you have just taught Claude to make that same mistake every time. So your examples must be exactly right. Now the second quality, diverse, which means not three near identical easy cases. So notice why that matters. If your three examples are all basically the same simple case, then Claude only learns that one narrow situation. So you want your examples to be different from each other, to spread out and cover a real range of what it might see. And the third quality, edge cases.

**9:43 → 10:28**

like an ambiguous input, a missing field, or an odd format. So, notice why you deliberately include the tricky ones. The easy cases Claude can often handle anyway. It is the awkward ones, the ambiguous, the incomplete, the strangely formatted that it really needs to be shown. So your examples should include those hard corners. And here is the key lesson tying those together. Three near identical easy examples teach almost nothing. It is the diversity plus the edge cases that actually makes few short work. So please remember this because it is a common mistake. because

**10:28 → 11:13**

safe, similar examples because they are the easiest to write. But those teach Claude almost nothing new. So the power comes from the variety and from the difficult cases. Alright. So the seventh and final topic. How many and in what order? And the subtitle sums up the recipe. Enough to show the range. And kept consistent and clean. So look at the three-part rule. A few examples uniform in style and placed before the input. So often that is two to five examples. And you stop when the accuracy stops improving. You keep every examples format

**11:13 → 11:58**

identical and you put the examples before the real input. So notice each piece, 2 to 5 is usually plenty, there is no need to pile on 20 and crucially the examples come first. So Claude has learned the pattern before it even sees the real question and here is one easy to miss warning, inconsistent formatting across your examples confuses the pattern. So you keep them uniform. So think about why this trips people up. If your first example is laid out one way and your second is laid out another, then Claude cannot tell which layout you actually want. The mixed signals just muddy the pattern.

**11:58 → 12:43**

So every example must follow the exact same format. Alright, so let's pull this together. The key takeaways from this lecture, few short prompting in three lines. Number one, show, don't tell. Examples pin down the meaning and the format and they generalize to new inputs. So remember, one good example often does more than a whole paragraph of rules. Number two, pick good examples. They should be correct, diverse and cover the edge cases, including a missing data or null case. So remember, three near identical easy examples teach almost nothing. Variety and hard cases are

**12:43 → 13:18**

count and number three few uniform and first you use just a few examples you keep their format identical and you place them before the input so remember two to five is usually enough and consistency in their format is what keeps the pattern clear all right so that is how you teach claude by showing and not just telling in the next lecture we will look at structured output with a tool use so with this i'm going to end this one and i will catch you in the next one
