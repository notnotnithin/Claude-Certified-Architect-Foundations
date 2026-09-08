---
hovernotes-transcript-of: doc_08b29c69-0847-4983-80ce-d162c19df75a
hovernotes-transcript-version: 2
note: "[[10-Prompt-Evaluation-Workflow 1]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042201#overview"
updated: 2026-09-04T13:19:40.993Z
---

# 10-Prompt-Evaluation-Workflow 1 — Transcript

**0:00 → 0:20**

So far we have focused mostly on prompt engineering. Prompt engineering is about writing better prompts. For example, we can make instructions clearer. We can add examples. We can ask Claude to return structured output. We can use XML tags to separate different parts of the prompt. All of these techniques help Claude

**0:20 → 0:50**

understand what we want. But writing a good prompt is only the first part. The second part is prompt evaluation. Prompt evaluation is about measuring how well the prompt actually works. And this is where many AI projects become risky. A prompt may look good. It may work in one demo. It may work for three examples you tested manually. But real users will send inputs you did not expect. They will write unclear messages. They will forget important details.

**0:50 → 1:21**

They will ask about edge cases. They may combine several problems in one message. So if we want to build reliable cloud applications, we cannot only rely on manual testing. For ShopAssist AI, this is especially important. Our assistant may need to handle refund requests, missing packages, damaged items, billing problems, angry customers, and cases that require human escalation. A prompt that works for one refund request may fail on another.

**1:21 → 1:51**

So, instead of asking, does this prompt look good, we ask a better question. How does this prompt perform across many realistic examples? That is the goal of Evolve. After writing a prompt, engineers usually follow one of three paths. The first path is testing the prompt once and deciding it is good enough. This is risky. It may work in a notebook but fail in production. The second path is testing the prompt a few times and fixing one or two obvious problems. This is better

**1:51 → 2:21**

but still limited, you are only testing the cases you happen to think about. The third path is building an evaluation pipeline. You create a dataset of test cases. You run your prompt against all of them, you grade the results, then you change the prompt and run the same eval again. This gives you a more objective way to decide whether the prompt actually improved. The basic eval workflow looks like this. Draft a prompt. Create an evil data set. Run each test case through cloud.

**2:21 → 2:51**

grade the output, change the prompt and repeat. Let's make this concrete with ShopAssist AI. First, we create a small evaluation data set. Here I have a list called test cases. Each test case has two parts, the customer message and the expected intent. So we are not just asking Claude a random question. We already know what the correct answer should be. This is what makes it an eval. Now let's run these examples through our prompt.

**2:51 → 3:21**

I'll create a simple loop. For each test case, we take the input message, pass it into classifyIntent function and print Claude's response. Before running it, let's quickly look at classifyIntent. This function sends the customer message to Claude and asks for one of our supported intent categories. We also set temperature to zero because this is a classification task, not a creative task. And we ask Claude to return JSON. So our Python code can read the result. now,

**3:21 → 3:51**

let's go back and run the loop. At this point we can see that Claude returns an intent for each customer message, but we are only printing the output. We are not checking whether it is correct yet. So let's add the comparison. We take the actual intent from Claude's response. Then we take the expected intent from our test case and we compare them. If they match the test passes, if they do not match the test fails. Now we can run the eval again and see true or false for each test case.

**3:51 → 4:21**

This is already the core idea of prompt evaluation. We create examples. We run the prompt. We compare actual results with expected results. Then when we change the prompt, we can run the same eval again and see whether the prompt actually improved. That is the important mindset shift. Prompt engineering should not be only based on feeling. It should become an engineering workflow. Make a change. Run evals, compare results, then decide whether the change is better.

**4:21 → 4:36**

A good prompt is not just a prompt that sounds good. A good prompt is a prompt that performs well across realistic examples. In the next lesson, we will make this more systematic by looking at code-based grading and model-based grading.
