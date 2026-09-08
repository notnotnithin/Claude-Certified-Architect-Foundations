---
hovernotes-transcript-of: doc_0dec1f66-45c4-4df6-a742-5390786d3546
hovernotes-transcript-version: 2
note: "[[13-RAG-Overview-Retrieval-Before-Generation]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042221#overview"
updated: 2026-09-04T13:52:43.784Z
---

# 13-RAG-Overview-Retrieval-Before-Generation — Transcript

**0:00 → 0:26**

In this lesson, we will briefly look at RUG or Retrieval Augmented Generation. RUG is a pattern that helps an AI model answer questions using information that is not fully included in the prompt. The basic problem is simple. Imagine ShopAssist has thousands of support articles, refund policies, shipping rules, product manuals, and previous incident reports. A user asks, can I return a damaged item

**0:26 → 0:57**

after 45 days. We could try to put all company documentation into the prompt, but this quickly becomes expensive, slow, and sometimes impossible because of context limits. Even if the model supports a large context window, sending everything is usually not ideal. The model has to search through too much information, the request costs more, and the answer may become less focused. RUG solves this by adding a retrieval step before generation.

**0:57 → 1:27**

Instead of giving Claude everything, we first search for the most relevant pieces of information. Then we send only those pieces to Claude together with the user's question. So the flow looks like this. First we prepare the knowledge base. We take documents, split them into chunks and store those chunks in a searchable system. Then when the user asks a question, we search for the most relevant chunks. Finally we put those chunks into the prompt and ask Claude to answer using that response.

**1:27 → 1:57**

context. For example, if the user asks about returning a damaged item after 45 days, the system may retrieve three pieces of context. The damaged item return policy, the exception policy, and the escalation instructions. Claude then uses that context to generate the final response. The important idea is this. Rack does not magically make the model know your documents. It gives the model the right pieces of your documents at the right time. Now let's talk about how

**1:57 → 2:27**

how the search part can work. The simplest option is keyword search. Keyword search looks for exact words or close matches. If the user asks about refund policy, it searches for documents containing words like refund and policy. This is useful, fast, and often very strong when users mention exact terms, EDS, product names, or error codes. For example, what happened with incident INC12345?

**2:27 → 2:57**

Keyword search is likely to work well here because the incident ID is exact. But keyword search has a limitation. If the user says, can I get my money back? And the document says, customers may request a refund. A pure keyword search may miss the best result because the wording is different. This is where semantic search helps. Semantic search uses embeddings. An embedding is a numerical representation of text meaning. The system converts both.

**2:57 → 3:27**

user's question and each document chunk into vectors, which are lists of numbers. Then it compares those vectors to find chunks with similar meaning. So can I get my money back? Can match a document about refund eligibility, even if the exact words are different. These embeddings are usually stored in a vector database. A vector database is optimized for storing and searching embeddings. It helps find the chunks that are closest in meaning to the user's question.

**3:27 → 3:57**

This is the part people often associate with RUG. Chunk documents generate embeddings, store them in a vector database, retrieve similar chunks and pass them to the model. But vector search is not the only option. In many real systems, the best approach is hybrid search. Hybrid search combines semantic search and keyword search. Semantic search is good for meaning. Keyword search is good for exact terms. Together they cover more cases. For example, if a user

**3:57 → 4:27**

asks, why was order 1, 2, 3, 4, 5 escalated? Semantic search may understand the general meaning, but keyword search is better at finding the exact order ED. A hybrid retriever can search both ways, merge the results and return the strongest final set of chunks. This matters because rug quality depends heavily on retrieval quality. If the retrieval step finds the wrong context, Claude may produce a confident but wrong answer. If the retrieval step finds incomplete

**4:27 → 4:58**

context, Claude may miss an important policy exception. So when designing RUG, the main question is not just can the model answer. The better question is did we retrieve the right evidence for the model to answer? There are several practical decisions in any RUG system. How should we split documents into chunks? Should chunks be based on size, paragraphs, headings, or semantic meaning? How many chunks should we retrieve? Should we use vector?

**4:58 → 5:28**

search, keyword search, or hybrid search? Should we re-rank results before sending them to the model? And should Claude cite the retrieved sources in the final answer? For this course, you do not need to implement a full production RUG system right now. What matters is understanding the pattern. RUG is useful when your application needs to answer using large or changing knowledge sources, documentation, policies, support history, contracts, product catalogs, or internal rip

**5:28 → 5:58**

supports. It improves scalability because you do not send everything to the model. It improves freshness because documents can be updated outside the model. And it improves control because the answer can be grounded in retrieved sources. In ShopAssist, RUG could be used to answer support questions based on the latest return policies, shipping rules, warranty terms, and escalation procedures. The model does not need to memorize those policies. It only needs the right policy excerpts

**5:58 → 6:06**

prompt. That is the core idea of RAC. Retrieve relevant information first, then generate the answer using that information.
