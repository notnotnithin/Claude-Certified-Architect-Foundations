---
hovernotes-transcript-of: doc_2a926a9c-41aa-4d41-9972-21e5aae0d074
hovernotes-transcript-version: 2
note: "[[04-MCP-Server-Integration]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57460129#overview"
updated: 2026-09-10T13:45:41.189Z
---

# 04-MCP-Server-Integration — Transcript

**0:00 → 0:42**

Alright everyone, welcome back. So up to now, every tool we have talked about, you wrote yourself. You designed it, you described it, and you handled its errors. But here is the good news. You do not always have to build from scratch. There is a standard way to plug in tools that already exist. So this lecture is MCP server integration. Think of MCP as one standard plug that connects Claude to almost anything. So 7 things in this lecture. Number 1. What MCP is? tools versus results.

**0:42 → 1:27**

this number three connecting a server number four keeping secrets safe number five the three scopes number six residence and number seven running multiple servers all right so the first topic what is mcp and the subtitle gives you the perfect one-liner it is usbc for ai tools so look at what it is mcp is a universal standard for connecting cloud to external systems so before mcp you needed a custom connector for every single tool but with mcp there is just one standard plug and any mcp You said it was?

**1:27 → 2:12**

works so you build a server once and cloud plugs straight in so please notice why this is such a big deal without a standard every new tool meant a new bespoke piece of wiring with MCP that wiring is the same every time build it once to the standard and it just connects now here is the picture that makes it obvious it is like USB see replacing every proprietary charger one plug for github for databases for slack and for much more so think back to the bad old days of chargers every device had its own odd cable

**2:12 → 2:57**

and none of them fit each other. Then USB-C came along and one cable did everything. So MCP is exactly that but for connecting Claude to your tools. One shape that fits them all. Alright, so the second topic, tools versus resources. And the subtitle draws the line. Verbs you can call and data you can pull in. So look at the first kind. Tools are verbs. They are actions that Claude calls. Things like create issue or run query. So notice the keyword verbs. A tool does something. It changes the world or it changes the world.

**2:57 → 3:42**

That is an answer when Claude decides to call it. So these are the active parts. Claude reaches for a tool when it wants to make something happen. Now look at the second kind. Resources are nouns. They are read-only data or context. Things like a file, a document or a schema. And you pull one in by typing an at sign. So notice the difference. A resource does not do anything. It is just information sitting there that Claude can pull into the conversation to inform its work. And here is the clean summary. Tools do things. Resources inform Claude.

**3:42 → 4:28**

And in Cloud code, you reference a resource by typing an at sign. So hold on to that split because it is a favorite distinction. If it takes an action, it is a tool. If it just gives Cloud something to read, it is a resource. So verbs and nouns, doing and knowing. All right, so the third topic, connecting a server. And the subtitle tells you how small it is. Just a little JSON entry with a command or a URL. So look at what a connection actually is. Each server is one entry under a section called MCP servers. So there are two ways it can talk.

**4:28 → 5:13**

The first is STDIO, which is a local program that Claude launches, with a command and its arguments. And the second is HTTP, which is a remote server reached by a URL. And that word transport just means how Claude talks to it, local or remote, and a config entry looks like. A server named docs with type HTTP and a URL pointing at its MCP endpoint. So notice how little there really is to it, a name, a type, and either a command or an address. Now here is one thing to keep clear in your head. The transport, that is STDIO.

**5:13 → 5:58**

versus HTTP is a completely separate question from where the config actually lives. And that where is what the next few slides are all about. So notice that we are splitting two ideas apart. One is how does Cloud reach the server, local or remote? And the other is who can see this configuration? Just you or your whole team. So do not mix those two up. They are genuinely different questions. All right. So the fourth topic, and this one really matters. Keep your secrets out of the config. And the subtitle states the rule, reference secrets by name.

**5:58 → 6:43**

never paste them in. So look at the technique, you use variable extension, that $ with braces syntax, so your keys live in your environment and not in the file. So the actual API key stays out of the committed file. And there is a handy variant with a colon and a dash that gives you a fallback default if the variable is missing. And it works everywhere. In the command, the arguments, the env block, the URL, and the headers. So a safe entry reads like an env block where your API token is set to a reference, the GitHub token variable, rather than the real key itself.

**6:43 → 7:23**

You write the name of the secret and not the secret itself. And here is the warning and it is a serious one. A key hardcoded in a shared mcp.json gets committed to git. And that is a real leak. The variable syntax keeps it off disk entirely. So please take this one to heart because it is a genuine and common security accident. The moment you paste a real key into a shared config and commit it, that key is now in your git history for anyone with the repo to find.

**7:23 → 8:08**

So you reference it by name and the secret never touches the file at all. Alright, so the fifth topic, the three scopes and the subtitle lays them out. Just you, your team or all of your projects. So look at the first scope, local. This lives in your personal cloud.json and it is only for you on this one project and it is the default. So notice what local really means. It is the most private setting of the tree. Just you and just here. Nobody else on the team sees it and it does not follow you to your other projects. Now the second scope, project.

**8:08 → 8:53**

In the mcp.json file, it gets committed, and it is shared with the whole team. So, notice the jump. This one is deliberately shared. When you put a server in project scope and commit it, everyone who pulls the repo gets it too. So, this is for the tools that the whole team should have. And the third scope, user. This also lives in your cloud.json, but now it applies to you across all of your projects. So, notice how this differs from local. Local was you on one project. User is you on every project. So, this is for your own personal tools, the ones you want with you.

**8:53 → 9:38**

everywhere you work. And here is the big warning, and it is the classic MCP mistake. Peeking the wrong scope is the number one MCP error. Because a personal token drop into project scope leaks straight to the whole team. So please be very careful here. Imagine you put your own private key into project scope and you commit it. Now every single teammate has your personal token. So this is exactly why the scopes matter. Your private things belong in local or in user and only genuinely shared things belong in project. All right. So the sixth topic, precedence and inheritance.

**9:38 → 10:23**

the subtitle asks the obvious question. When the same server exists twice, who wins? So, look at the order. Local beats project, which beats user. So, if the same name server appears in two places, the higher scope wins. Which means your local override beats the team's shared one. And if you're running in a subfolder, any parent mcp.json files merge in two. So, notice what this gives you. You can quietly override a shared team server. Just for yourself, with a local one of the same name. And your local version simply takes priority. Now, here is why this is worth memorizing. Knowing this order saves you a

**10:23 → 11:09**

of why on earth is it using the wrong server confusion. So think about that moment something behaves oddly and you're sure you configured it differently. 9 times out of 10 the same server exists in 2 scopes and a higher one is quietly winning. So once you know local beats project beats user that little mystery just disappears. Alright. So the 7th and final topic multiple servers and the subtitle sets the tone. Many servers in one session so keep them tidy. So look at what is possible. You can run several servers all at once. GitHub plus a database

**11:09 → 11:54**

plus browser automation all together in a single session and you check their connection status with a slash dash MCP command and you name them clearly Github or Stripe Dash Broad not server 1 so notice both halves of that you are not limited to a single connection but once you have several clear names become essential so you can tell them apart at a glance now here is the little piece of wisdom to end on you name your servers the way you name your variables because you will be reading these names months later so you treat them that way so think about your future self in six months

**11:54 → 12:39**

and server 2 will mean nothing to you. But GitHub and Stripe prod will be instantly clear. So spend the 2 seconds now and give them names that will still make sense later. Alright, so the key takeaways from this lecture, MCP integration in 3 lines. Number 1, one standard plug. MCP servers offer tools, which are actions and resources, which are data you pull in with an add sign. Number 2, scopes plus secrets. Local bits, project, bits, user. And you use the variable syntax to keep your keys out of git. And number 3, many servers kept tidy.

**12:39 → 12:49**

You can run several at once, you check them with the slash mcp command, and you name them clearly. So notice the shift, this whole lecture really...

**12:40 → 13:23**

Then run several at once, you check them with the slash mcp command and you name them clearly. So notice the shift this whole lecture really represents. Up to now, you were building every tool by hand. mcp is how you stop reinventing the wheel and plug into tools that already exist through one common standard. So the design work does not go away. You still choose which servers to connect, which scope they belong in and how to protect your secrets. But the wiring itself becomes standard. One plug for almost anything. Alright, in the next video, we'll look at the tools that Cloud Code already

**13:23 → 13:47**

tips with, right out of the box, and how to pick the right one. This is the built-in tools, that means the six built-in tools, grab versus glob, read, edit and write, the read before edit rule, referring built-ins over bash, and exploring a code base incrementally. So with this, I'm going to end this one and I will catch you in the next one.
