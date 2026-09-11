---
hovernotes-transcript-of: doc_f92e711b-2543-4637-a8fb-45e32ad088a9
hovernotes-transcript-version: 2
note: "[[18-Batch-Processing-And-MultiPass-Review-Architectures]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042269#overview"
updated: 2026-09-04T15:10:50.711Z
---

# 18-Batch-Processing-And-MultiPass-Review-Architectures — Transcript

**0:00 → 0:40**

In the previous lessons, we learned how to make structured extraction more reliable with validation, retry loops, confidence scores, and human review. Now we need to ask a bigger architecture question. What happens when we do not have one customer message or one document? What if we have 10,000 support tickets? What if we want to audit all return requests from last night? What if we want Claude to review many generated summaries, policies, or extracted records? For this type of work, we may not want to call the synchronous messages API one request at a time. Instead, we can use the message batches API. The message batches

**0:40 → 1:26**

for large latency tolerant workloads. You submit many requests together. Cloud processes them asynchronously. And later your application retrieves the results. This has two important benefits. First, batch processing can reduce calls by 50% compared with standard API calls. Second, it is useful when the work does not need an immediate answer. For example, ShopAssist should not use batch processing when a customer is actively chatting with support. If the customer asks, can I return this item, they are waiting for a response now. That should use a normal synchronous API call. But if ShopAssist wants to audit all support tickets from last night, batch processing is a much better

**1:26 → 2:11**

fit. The audit can run in the background. It can classify tickets, detect risky refunds, find policy exceptions, and identify cases that should be reviewed by a human. The important trade-off is latency. Batch requests may take up to 24 hours to complete, and there is no guaranteed latency SLA. So batch processing is great for offline workflows, but wrong for blocking workflows. For example, a pre-merge check in C, I should usually not wait on a batch job. If a developer opens a pull request and needs a pass or fail result before merging, that review should use a normal API call or a faster workflow. Another important batch concept is custom ID. When you submit

**2:11 → 2:56**

requests in one batch, you need a way to match each response back to the original input. That is what custom ID is for. For example, Shop Assist might submit ticket IDs like ticket 1001, ticket 1002, ticket 1003. When results come back, the system can use those IDs to update the correct audit record. This is critical because batch results may not be returned in the same order as the original requests. Now, let's talk about tools. Batch processing is not the same as a live agentic loop. In a normal tool use workflow, Claude can request a tool, your application executes it, and then you send the tool result back to Claude. But in a single

**2:56 → 3:41**

request, there is no mid request to execution loop. So if your task requires multiple live tool calls during reasoning, you need a different architecture. For batch jobs, you usually prepare the needed context before submitting the request. For example, before auditing a support ticket, ShopAssist might gather the ticket text, customer tier, order status, refund history, and policy version. Then it sends all of that information as part of the batch request. Another best practice is to refine your prompt before running a large batch. Do not start with 10,000 documents. Start with a small sample. Review the outputs, find common mistakes, improve the prompt, schema, and validation rules.

**3:41 → 4:26**

and run the larger batch. This avoids wasting costs on a flawed prompt. If some requests fail, you usually do not need to resubmit the entire batch. Instead, your application should identify the failed documents and resubmit only those. This is another reason why stable IDs are important. Now let's move from batch processing to review architecture. A common mistake is to ask Claude to generate something and then ask the same Claude response to review itself. Self-review can be useful, but it has limits. The model may miss the same assumptions or mistakes that appeared in the original answer. For higher reliability, use independent review instances. That means one Claude call generates the output.

**4:26 → 5:11**

separate cloud call reviews it with a different prompt, different role, or more focused criteria. For example, Shock Assist might use one request to draft a refund resolution policy. Then, a separate review request checks. Does this policy follow the refund rules? Does it create legal or compliance risk? Does it require human approval? Does it contradict any existing policy? This is called a multipulse review. The first pass produces or analyzes something. The second pass reviews it. A third pass may integrate the findings around the case to a human. This pattern is especially useful for code review, policy review, support summaries, and document analysis. There is also an important architecture pattern for large cloud

**5:11 → 5:57**

or large document sets. Per file local analysis followed by cross file integration analysis. In the first pass, Claude reviews each file or document separately. Each result is small, structured, and focused. Then a second pass looks across those per file findings and asks, are there conflicts? Are there repeated issues? Does one file change break assumptions in another file? What are the highest priority findings? This is better than trying to put an entire large project into one prompt. It also gives the system better traceability. You know which file produced which finding. You can filter low confidence results, and you can run integration analysis only after the local analysis is complete.

**5:57 → 6:42**

So the key idea of this lesson is simple. Use synchronous calls when the user is waiting. Use batch processing when the work is large and latency tolerant. Use custom ED to correlate results. Prepare tool context before the batch request. Test prompts on a sample before scaling. Resubmit only failed documents. And for important review workflows prefer independent multipass review over simple self-review. For ShopAssist, this means live customer conversations stay synchronous. Nightly support ticket audits use batch processing. Generated summaries and policies can go through independent review. And large analysis jobs can be split into local passes first, followed by cross-file or cross-ticket

**6:42 → 6:47**

That is the architecture pattern the exam wants you to recognize.
