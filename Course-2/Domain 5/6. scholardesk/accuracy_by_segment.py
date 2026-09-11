"""
accuracy_by_segment.py
==================================================================
Part 5 demo - Task 5.5: one big number can hide a weak spot

Before you trust ScholarDesk to answer without review, you measure how accurate it
is. The trap is looking only at ONE overall number. This script shows why that hides
problems, and how breaking accuracy down by SEGMENT (here: question topic) reveals
them.

It also shows STRATIFIED SAMPLING: instead of spot-checking random answers, you
sample some from EACH topic, so every topic actually gets looked at.

This does NOT call the API - it works from a small set of labelled results (answers
already marked correct/incorrect) to make the statistics visible.

HOW TO RUN (from the project root, in cmd):

    python accuracy_by_segment.py
"""

import os
import sys
import random

# A labelled evaluation set: each item is (topic, was_the_answer_correct).
# Overall this looks great - but one topic is quietly weak.
RESULTS = (
    [("cost", True)] * 149 + [("cost", False)] * 1 +          # 149/150 = 99.3%
    [("adoption", True)] * 98 + [("adoption", False)] * 2 +   # 98/100 = 98.0%
    [("charging", True)] * 6 + [("charging", False)] * 4      # 6/10 = 60% !
)


def overall_accuracy(results):
    return sum(1 for _, ok in results if ok) / len(results)


def accuracy_by_topic(results):
    topics = {}
    for topic, ok in results:
        topics.setdefault(topic, [0, 0])
        topics[topic][0] += 1 if ok else 0
        topics[topic][1] += 1
    return topics


def stratified_sample(results, per_topic=3):
    """Take a few samples from EACH topic, so none is overlooked."""
    by_topic = {}
    for item in results:
        by_topic.setdefault(item[0], []).append(item)
    sample = []
    for topic, items in by_topic.items():
        sample.extend(random.sample(items, min(per_topic, len(items))))
    return sample


def main():
    print("\n" + "=" * 64)
    print("  ACCURACY BY SEGMENT")
    print("=" * 64)

    overall = overall_accuracy(RESULTS)
    print(f"\n[1] The headline number:  {overall*100:.1f}% accurate overall")
    print("    Looks great! You might trust it without review on this basis.")

    print("\n[2] But break it down BY TOPIC:\n")
    topics = accuracy_by_topic(RESULTS)
    for topic, (right, total) in sorted(topics.items()):
        pct = right / total * 100
        flag = "   <-- WEAK SPOT" if pct < 80 else ""
        print(f"    {topic:12} {right}/{total}  = {pct:5.1f}%{flag}")

    print("""
    The overall ~97% HID a topic sitting at 60%. 'charging' is where the
    assistant is unreliable - and a single aggregate number would have
    sent you live without ever noticing.""")

    print("\n[3] STRATIFIED SAMPLING - check some from every topic:\n")
    sample = stratified_sample(RESULTS, per_topic=3)
    counts = {}
    for topic, _ in sample:
        counts[topic] = counts.get(topic, 0) + 1
    for topic, n in sorted(counts.items()):
        print(f"    sampled {n} from {topic}")
    print("""
    Plain random sampling might draw mostly 'cost' (the biggest group)
    and barely touch 'charging'. Stratified sampling guarantees every
    topic gets checked - so the weak one can't hide.""")

    print("-" * 64)
    print("""  The lesson of Task 5.5: never trust one aggregate accuracy number.
  Measure accuracy PER segment (topic/field) before automating, and
  sample in a way that looks at every segment. Route the weak segment's
  answers to human review until it improves.""")


if __name__ == "__main__":
    main()
