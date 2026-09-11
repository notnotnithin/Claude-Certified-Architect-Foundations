---
hovernotes-transcript-of: doc_9d30c152-326d-46b1-b2bc-2938a725deb9
hovernotes-transcript-version: 2
note: "[[03-Path-Specific-Rules]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57479749#overview"
updated: 2026-09-10T15:31:53.267Z
---

# 03-Path-Specific-Rules — Transcript

**0:00 → 0:43**

Alright everyone, welcome back. So back in lecture 3.1, we met cloud.md and even nested folder memory. But there is a sharper tool for that very same idea. Rules that switch on only for the exact files they apply to. This is path specific rules. The right rules only where they apply. So 6 things in this lecture. Number 1. Why 1. Cloud.md is too broad. Number 2. The .cloud rules folder. Number 3. Scoping with paths. Number 4. Conditional loading. versus a subdirectory.

**0:43 → 1:28**

Claude.md and number 6, precedence. Alright, so the first topic, why one? Claude.md is too broad and the subtitle puts it plainly. Backend rules shouldn't clutter your frontend work. So look at the problem, a single file applies to everything. So in a large repo, most of it is irrelevant to any one task. Your API security rules do not help you when you are editing CSS. So you really want rules that appear only in their own area. So please notice the waste here. If everything lives in one file, then every session, Claude is carrying rules for parts of the project.

**1:28 → 2:13**

are not even touching. So your front end work gets cluttered with back end rules that simply do not apply. Now here is the picture for it. You want zone specific signage, pool rules at the pool, gym rules at the gym, not one giant sign for the whole building. So think about how sensible that is in a real building. You do not put the pools, no diving rule up on the gym wall. It would just be noise in the wrong place. So path specific rules do exactly the same thing. The right rules posted exactly where they belong and nowhere else. Alright, so the second topic.

**2:13 → 2:58**

.cloud rules folder and the subtitle tells you the shape one folder holding many focused rule files so look at how it works each MD file in that folder loads as project memory by default so you drop in focused files like api.md, test.md, and style.md and it is the same behavior as cloud.md, just split up so it is simply a tidier way to organize your project rules so notice that nothing magic is happening yet these files behave exactly like your cloud.md you have just broken one big file into several small focused ones

**2:58 → 3:43**

Now here is an important point about priority. The MD files in the .cloud rules folder and your .cloud.claud.md sit at the same priority. So the rules folder is just a tidier way to split them up. So please be clear about this. Splitting into a rules folder does not change how important the rules are. A rule in api.md carries exactly the same weight as that same rule in cloud.md. It is purely about organization and not about priority. Alright, so the third topic. And this is where it gets powerful.

**3:43 → 4:28**

And the subtitle tells you the trick. Add a glob and the rule wakes up. Only for matching files. So look at how you scope it. You add a parts field in the front matter. And that scopes the rule. So parts is a list of glob patterns. And the rule then loads only when Claude touches a matching file. So for example, a parts pattern like SRC, then API, then a wildcard. So notice what has changed here. Up to now, a rule file loaded every single time. But the moment you add this parts field, it goes quiet and it only wakes up. When you touch a file that matches the pattern.

**4:28 → 5:14**

Now here is the key idea stated simply. The path's glob is the trigger. So that pattern, src, api and a wildcard means apply this rule only inside the api folder. So think of the glob as a little switch. When Claude opens the file inside the api folder, the pattern matches and the rule switches on. When it is anywhere else, the pattern does not match and the rule stays asleep. So the glob decides exactly when the rule appears. Alright, so the fourth topic, conditional loading and the subtitle sums the whole thing up. With paths, it is on demand.

**5:14 → 5:59**

always. So look at the first case. With a parts field, the rule loads only for matching files. So it is conditional and area specific. So notice what that gives you. This rule is polite, it stays out of the way and it only shows up in the one area it belongs to. So it is on demand, triggered by the files you actually touch. Now look at the second case. With no parts field, the rule loads every session. So it is unconditional and project wide. So notice the difference. Without a parts field, the rule behaves like ordinary project memory. It is always on everywhere. So no

**5:59 → 6:44**

means always and a paths field means only sometimes and here is the best part you mix both you keep always on rules for your project-wide conventions and you use path scoped rules for the area specific ones so think about how natural that is some rules truly apply everywhere like your general coding style so those stay always on but others only matter in one corner like your api security rules so those get a paths field so you get the best of both all right so the fifth topic rules versus a subdirectory cloud

**6:44 → 7:29**

and the subtitle warns you. There are two ways to scope by location, so you pick the right one. So look at the two options. On one side, the glob rule using a parts field. It is flexible and it is good for cross-cutting patterns. For example, every star.test.js file anywhere in the repo. On the other side, a subdirectory, glob.md, that covers everything under one folder. A whole subtree of the repo. So notice the real difference. The glob follows a pattern wherever it appears, and the subdirectory file covers one location, top to bottom. Now here is the exam distinction,

**7:29 → 8:14**

a sharp one a pattern that spans the repo goes to a glob rule but everything in one directory goes to a cloud.md in that directory so please hold this one carefully think about test files they are scattered all over the repo sitting next to the code they test there is no single folder that holds them all so that is a glob job star.test.js wherever it lives but if all of your api code sits neatly in one folder then a cloud.md right in that folder is the simpler fit all right So, the sixth and final topic, Presidents,

**8:14 → 8:59**

and the subtitle tells you the outcome. Part rules land last, and last usually wins. So look at the order. User then project, then part specific, which is appended last. So part rules append when you touch matching files. And on a conflict, the later more specific rule wins. So this is consistent with the Claude.md hierarchy. So notice how it all fits together. The broad rules come first, then the part specific rule arrives last, exactly when it becomes relevant, and because it is last and most specific, it is the one that wins any disagreement. Now here is the reassuring part. is the very

**8:59 → 9:45**

same principle as lecture 3.1 broader rules first the most specific rule last and the closest rule wins so you already know this pattern back in 3.1 the more specific level won a conflict and here it is exactly the same the path specific rule is the most specific and it lands last so it takes priority so one consistent idea running right through the whole domain all right so the key takeaways from this lecture path rules in three lines number one the rules folder the md files in the .cloud rules folder.

**9:45 → 10:30**

load as project memory. And a parts glob scopes a rule to matching files. Number 2, conditional vs always. With a parts field, a rule is conditional and it loads on demand. Without one, it is always on. And number 3, glob vs folder. You use a glob rule for crosscutting patterns and a subdirectory clod.md for a whole folder. So notice the single idea running through this whole lecture. You are aiming the right rules at exactly the right files. So a plain rule file behaves like project memory. Always on, add a parts field and it becomes a targeted rule that

**10:30 → 10:55**

only where it belongs and you mix the two always on for the whole project and part scope for each area so claude sees the rules that matter right where they matter and nothing more all right in the next video we look at plan mode versus direct execution so with this i'm going to end this one and i will catch you in the next one
