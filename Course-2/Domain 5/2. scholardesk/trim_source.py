"""
trim_source.py
==================================================================
Part 1 demo - Task 5.1: trim verbose source content before it piles up

When a research assistant pulls in a source - a fetched web page, a long report -
it often arrives wrapped in a LOT of noise: navigation text, boilerplate, unrelated
sections, metadata. If you drop the whole thing into the conversation, it eats
tokens and buries the few sentences that actually answer the question. Over a long
session, many such dumps crowd out everything that matters.

The fix is simple: trim each source to only the RELEVANT part before it goes into
context.

This script shows a realistic "raw" fetched result, then the trimmed version. It
does NOT call the API - it's about what you feed into context.

HOW TO RUN (from the project root, in cmd):

    python trim_source.py
"""

import os
import sys

# A realistic "raw" fetched result - what pulling a page might actually return.
# Only a couple of sentences are relevant to an EV cost question.
RAW_FETCH = """\
[NAV] Home | About | News | Contact | Login | Subscribe
[COOKIE BANNER] We use cookies to improve your experience. Accept | Reject
[ADVERT] Buy the new PhonePro 12 - now with 200MP camera!
---
Electric Vehicle Cost Corner - our weekly column

Welcome back to Cost Corner! Before we begin, a big thank you to our sponsors and to
the 4,200 readers who wrote in last week. Don't forget to subscribe to our newsletter
and follow us on social media for daily updates and giveaways.

>>> KEY FACT: For a Pune city commuter, an electric two-wheeler runs at about
Rs 0.25 per km, versus roughly Rs 2.50 per km for a petrol two-wheeler. <<<

Related articles you might like: '10 EV myths busted', 'Best helmets of 2026',
'Why petrol prices keep rising', 'Our editor's scooter diary'.
[FOOTER] Terms | Privacy | Careers | (c) 2026 Cost Corner Media. All rights reserved.
Sign up | Unsubscribe | Manage preferences | Advertise with us
"""

# The one sentence that actually answers a cost question.
RELEVANT_EXCERPT = ("For a Pune city commuter, an electric two-wheeler runs at about "
                    "Rs 0.25 per km, versus roughly Rs 2.50 per km for a petrol "
                    "two-wheeler.")


def main():
    print("\n" + "=" * 64)
    print("  TRIMMING A VERBOSE SOURCE")
    print("=" * 64)

    print(f"\n[RAW fetched source] {len(RAW_FETCH)} characters of mostly noise:")
    print(RAW_FETCH)

    print(f"[TRIMMED to the relevant excerpt] {len(RELEVANT_EXCERPT)} characters:")
    print("  " + RELEVANT_EXCERPT)

    saved = len(RAW_FETCH) - len(RELEVANT_EXCERPT)
    print("\n" + "-" * 64)
    print(f"""  Same answer, far less context: we dropped from {len(RAW_FETCH)} characters of
  nav bars, ads, and footers to the {len(RELEVANT_EXCERPT)} that actually matter -
  saving {saved} characters on this ONE source. In a long research
  session pulling many sources, trimming like this is the difference
  between a focused context and one clogged with boilerplate.

  Rule of thumb: extract the relevant excerpt; drop the noise BEFORE it
  enters the session.""")


if __name__ == "__main__":
    main()
