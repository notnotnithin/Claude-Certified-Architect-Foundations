---
hovernotes-transcript-of: doc_328e110f-ed79-4d8a-94bd-6cb85ddbbfc4
hovernotes-transcript-version: 2
note: "[[05-Human-Review-&-Confidence-Calibration]]"
source: "https://www.udemy.com/course/claude-ai-certification/learn/lecture/57569867#overview"
updated: 2026-09-11T08:40:05.218Z
---

# 05-Human-Review-&-Confidence-Calibration — Transcript

**0:14 → 0:56**

takes that routing idea and builds a whole review workflow around it. This lecture is human review and confidence calibration. And the subtitle sums up the goal. Trust the sure answers. And check the shaky ones. So five things in this lecture. Number one, why human review? Number two, field level confidence. Number three, routing by confidence. Number four, stratified sampling. And number five, accuracy by document type and field. Alright. So the first topic, why human review? And the subtitle.

**0:56 → 1:19**

gives you the tension. You can't check everything and you shouldn't have to. So look at the goal. You review the right ones, not all and not none. So reviewing every output at scale is impossible, but reviewing none is risky. So you target the ones most likely to be wrong. So notice the balance

**1:18 → 2:00**

So, notice the balance here. At scale, with thousands of outputs, a human simply cannot check everyone. But checking nothing leaves real errors slipping through. So the smart part is in between. You aim your review at exactly the outputs most likely to have a problem. Now here is the key idea. Smart review is not check everything. And it is not trust everything. It is check the ones most likely to be wrong. So please hold on to that phrase. Those two extremes are both wrong. Checking all of it is impossible.

**1:35 → 1:37**

exactly the outputs

**2:00 → 2:45**

trusting all of it is reckless so the whole art of this lecture is finding that middle path spending your limited human attention only where it is most needed all right so the second topic field level confidence and the subtitle sharpens the question not is this right but which parts are shaky so look at the shift you score confidence per field not per document so imagine the typed policy number may be completely certain while the handwritten total is not so you localize the doubt instead of doubting the whole document

**2:45 → 3:30**

So notice how much sharper this is. A document is not simply right or wrong. Some fields are crystal clear, others are genuinely uncertain. So instead of one score for the whole page, you score each field on its own. And here is the key point, field level beats document level, you trust the clear fields and you route only the shaky one for review. So please see why this saves so much effort. If one field on a document is uncertain, you do not need a human to recheck the whole page. You send them just that one shaky field. else.

**3:30 → 4:15**

clear confident fields sail straight through. Alright, so the third topic, routing by confidence, and the subtitle tells you what it does. Confidence decides the path automatically. So look at the rule, high confidence goes to auto accept, and low confidence goes to a human, so the score becomes a routing rule. And so the obvious cases never bother anyone. The human's time goes only to the uncertain cases. So notice how automatic this is, the confidence score is not just information, it is the switch. a high score

**4:15 → 5:00**

The output is accepted on its own. A low score and it goes to a person. No one has to decide case by case. And here is the connection. This is the routing idea from lecture 4.6. But now it is the backbone of the whole review workflow. So please notice we have seen this before. Back in 4.6, a review findings confidence decided whether to auto apply it or send it to a human. So it is the exact same idea. And here it grows up into the central engine of your entire review system. Alright. So the fourth topic, stratified sampling and the subtitle, ad sampling.

**5:00 → 5:45**

twist, you also spot check the confident ones with a smart sample. So look at the idea, you sample across every confidence band. So you do not only review the low confidence items, you sample high, medium and low because that catches the tesis where Claude was confidently wrong. So notice what problem this solves. If you only ever check the low confidence outputs, you are trusting that a high score always means correct. But what if Claude is sometimes confidently wrong? You would never catch it. So you sample a few from every band. Here is the warning.

**5:45 → 6:31**

Reviewing only the low confidence items misses the confident mistakes. So sampling every band keeps confidence itself honest. So please take this in because it is subtle but important. The whole system rests on the confidence scores being trustworthy. So you have to check that they actually are. And the only way to catch a confident mistake is to occasionally look at the high confidence ones too. Alright, so the fifth and final topic, Accuracy by Document Type and Field. And the subtitle gives you the aim.

**6:31 → 7:16**

where Claude is weak and you watch those spots. So look at the practice. You track accuracy by document type and by field. So at the handwritten forms, error prone is the total field weak. Then you route those for review more aggressively and you relax on the fields that are consistently correct. So notice what you are building here. A clear picture of exactly where the errors tend to happen and then you point your review right at those weak spots. And here is the lovely idea. Your review data is a map of weaknesses. So you feed it back to tighten the

**7:16 → 8:01**

where the errors actually cluster. So please see the loop here. Every time a human reviews something, you learn a little more about where Claude struggles. And you use that knowledge to aim the next round of review even more precisely. So the system gets smarter about itself over time. Alright, so let's pull this together. The key takeaways from this lecture. Human review and confidence in three lines. Number one, review the right ones, not all and not none. You target the outputs most likely to be wrong. So remember checking everything is impossible. And checking nothing is risky.

**8:01 → 8:46**

Number two, field level plus routing. You score confidence per field. And high goes to auto, low goes to a human. So remember, you localize the doubt and you send only the shaky field for review. And number three, sample and track. You stratified sample every band and you track accuracy by type and field to aim your review. So remember, sampling every band keeps confidence honest. And your review data shows you where to look. Alright, so that is how you trust the sure answers and check the shaky ones. In the next lecture, we will look at provenance.

**8:46 → 8:55**

and multi-source synthesis. So with this, I'm going to end this one, and I will catch you in the next one.
