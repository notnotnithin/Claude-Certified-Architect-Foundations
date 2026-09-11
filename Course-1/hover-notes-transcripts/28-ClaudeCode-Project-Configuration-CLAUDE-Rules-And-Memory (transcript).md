---
hovernotes-transcript-of: doc_eb909751-c7c0-4eb2-bcbe-b3ae0b21232b
hovernotes-transcript-version: 2
note: "[[28-ClaudeCode-Project-Configuration-CLAUDE.md-Rules-And-Memory]]"
source: "https://www.udemy.com/course/claude-certified-architect-foundations-complete-course/learn/lecture/57042383#overview"
updated: 2026-09-06T11:26:33.159Z
---

# 28-ClaudeCode-Project-Configuration-CLAUDE.md-Rules-And-Memory — Transcript

**0:00 → 0:32**

In this lesson, we'll configure Cloud Code for a real project. Cloud Code is an agentic coding assistant that runs in your terminal. It can read files, edit code, run commands, inspect tests, and help with multi-step development tasks. It is important to distinguish Cloud Code from using Cloud through the SDK. When we use the SDK, we build the application layer ourselves. We define the tools. We decide how to store and resend conversation history. We decide how to read files, fetch external content,

**0:32 → 1:17**

validate tool inputs, and connect Cloud to backend systems. Cloud Code already includes many of these agent capabilities as part of the product. It can work across a project, inspect files, run terminal commands, keep session context, and use built-in or connected tools. So in the SDK lessons, we were building the agent workflow ourselves. In Cloud Code, we are configuring and guiding an existing agent coding environment. But Cloud Code does not automatically know your team conventions, your architecture, your testing style, or your domain rules. That is why project configuration matters. Before we configure project memory, let's quickly make sure Cloud Code is installed. Cloud Code runs

**1:17 → 2:02**

the terminal and the setup is simple. First, install node.js if you do not already have it. You can check whether npm is available by running npm help. Then install CloudCode. After installation, go to your project folder and run cloud command. The first time you run this command, CloudCode will ask you to log in. Once authentication is complete, Cloud is available directly inside your terminal. Now we can move into the project setup. For CloudCode, the most important project memory file is CloudMD file. This file tells CloudCode how to work inside your repository. For ShopAssist, we want CloudCode to understand four things, coding standards, testing conventions,

**2:02 → 2:48**

Cloud API patterns, support domain rules. The easiest way to start is with the init command. Inside the shop assist repository, we can run init command. CloudCode scans the project and creates an initial CloudMD file. That generated file usually includes project structure, common commands, dependencies, and development patterns. But init is only the starting point. After that, we should edit CloudMD file manually and make it useful for the team. For example, our shop assist CloudMD file could look like this. Now CloudCode has much better context. If we ask it to add a validation rule, it knows we use Pedantic. If we ask it to update extraction logic, it knows

**2:48 → 3:33**

output still needs validation. If we ask it to add tests, it knows we use PyTest. This is the main value of project memory. We do not have to repeat the same instructions in every prompt. Cloud code supports different memory levels. First, there is user level memory. This is personal. It can contain your own preferences across projects. This file is not shared with the team. That distinction matters. User level memory is for personal workflow preferences. Project level memory is for shared instructions that belong in version control. For the project we usually use cloud MD file or depending on the repository layout, cloud MD file in cloud folder. This is where we put instructions that every

**3:33 → 4:18**

should share. CloudCode can also use more specific memory files in subdirectories. For example, if ShopAssist has API code in this folder, ShopAssist API, we can add ShopAssist API CloudMD file with instructions like this. This is useful because not every rule belongs everywhere. API files need API rules. Test files need test rules. Prompt files may need different rules again. For larger projects, one large CloudMD file can become hard to maintain. In that case, we can organize memory with imports. For example, like this. This keeps the main CloudMD file short while still giving CloudCode detailed project context. Now,

**4:18 → 5:03**

Let's look at path specific rules. Sometimes a directory level cloud.md file is enough. For example, if all tests live under tests, then tests cloud.md file is clean and simple. But sometimes files are spread across the repository. For example, API related files might live in shop assist routes, shop assist controllers, shop assist handlers. In that case, path.zart rules are easier to maintain. A team may organize these under rules directory, cloud rules API.md files and cloud rules tests md files. An API rule file can use YAMU front matter to describe which files it applies to. And a test rule can target test files.

**5:03 → 5:48**

is simple. Use a subdirectory clodemd file when all files in that folder share the same rules. Use path-specific rules when matching files are spread across multiple folders. CloudCode also gives us two useful commands for memory work. First, we can use hash to quickly add a memory node. For example, hash always run pytest before committing changes. CloudCode will ask where to save that memory. This is useful when you discover a new convention during development and want CloudCode to remember it. Second, we can use memory command. This helps us inspect and manage the memory files CloudCode is using. That is very useful for debugging. If CloudCode keeps Yeah.

**5:48 → 6:34**

using the wrong test command, check memory. If it follows an old architecture pattern, check memory. If it ignores a domain rule, check whether that rule is actually loaded. So for ShopAssist, our setup workflow is install CloudCode and run the init command. Then we edit the generated CloudMD file. We add project specific instructions for coding standards, testing, Cloud API usage and support rules. Then we add more specific memory for API files and test files. Then we use memory command to inspect what CloudCode actually loaded. And we use hash when we want to quickly save a new instruction during a session. The key idea is this. CloudCode works best

**6:34 → 7:09**

when it has durable project context. A good CloudMD file turns CloudCode from a generic coding assistant into a project-aware teammate. It knows how the repository is structured. It knows which commands to run. It knows which patterns to follow. And for ShopAssist, it knows that AI output must be validated, retried carefully, and routed to humans when confidence is low, or the customer message is contradictory. That is why project configuration is not just setup. It is part of making CloudCode reliable in a real engineering world.
