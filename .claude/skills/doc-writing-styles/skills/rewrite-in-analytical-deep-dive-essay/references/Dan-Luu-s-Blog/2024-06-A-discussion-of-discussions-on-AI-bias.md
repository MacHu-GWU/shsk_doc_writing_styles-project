# A Discussion of Discussions on AI Bias

There've been regular viral stories about ML/AI bias with LLMs and generative AI for the past couple years. One thing I find interesting about discussions of bias is how different the reaction is in the LLM and generative AI case when compared to "classical" bugs in cases where there's a clear bug.

## The Reflex Denial of AI Bugs

In particular, if you look at forums or other discussions with lay people, people frequently deny that a model which produces output that's sort of the opposite of what the user asked for is even a bug.

For example, a year ago, an Asian MIT grad student asked Playground AI (PAI) to "Give the girl from the original photo a professional linkedin profile photo" and PAI converted her face to a white face with blue eyes.

The top "there's no bias" response on the front-page reddit story, and one of the top overall comments, was:

> Sure, now go to the most popular Stable Diffusion model website and look at the images on the front page. You'll see an absurd number of asian women (almost 50% of the non-anime models are represented by them) to the point where you'd assume being asian is a desired trait. How is that less relevant that "one woman typed a dumb prompt into a website and they generated a white woman"?

This response fundamentally misses the point: the existence of Asian representation in other contexts doesn't justify a model converting an Asian person to white when explicitly asked not to.

## The Troubling Standard Response

Other highly-ranked comments with the same theme include arguments about training data demographics: if stock photos are dominated by white people and the US is 7.3% Asian (5% East Asian), then the model is "just following the data."

This reasoning is wrong on multiple levels:

**First**, on whether stock photos are actually dominated by white people—a quick image search for "professional stock photo" turns up quite a few non-white people. Either stock photos aren't very white, or people have figured out how to return more representative samples.

**Second**, it's unclear what internet services should be expected to be U.S.-centric given worldwide demographics.

**Third**, and most importantly, even if we accept all the above, it's both a design flaw and a sign of bias to assume that every request comes from the modal American. This is absurd in a way that becomes clear with an analogy.

## The Mechanic Shop Analogy

Imagine I talk to an AI customer service chatbot for my local mechanic and ask to schedule an appointment to put my winter tires on and do a tire rotation. When I pick up my car, I find out they changed my oil instead.

Internet commenters explain this isn't a bug: the chatbot converted my appointment to the most common kind of appointment because that's what the training data showed. An AI chatbot that converts any appointment request into "give me the most common appointment" is obviously broken. Yet for some reason, AI apologists insist this is fine when it comes to changing someone's race or ethnicity.

Similarly, it would be absurd to argue this is fine because other companies have schedulers that convert oil changes to tire changes. Yet that's another common line of reasoning we see in bias discussions.

## Why This Matters

If I used standard non-AI scheduling software and ended up having my oil changed because the software schedules the most common appointment, this would be a clear bug. No reasonable person would argue zero effort should go into fixing it.

Yet this is precisely the argument people make with AI. The justification goes further—there's an explanation of why the bug occurs that's used to justify why the bug should exist and shouldn't be fixed.

Such an explanation would read as obviously ridiculous for classical software, and it's no less ridiculous for ML.

### The Autocorrect Comparison

One could imagine users making this argument for autocorrect (a less transparent process). But searching reddit for "autocorrect bug" in the top 3 threads, only 2 out of 255 comments denied incorrect autocorrects were bugs—both from the same person.

In contrast, with generative AI, it's not uncommon to see half the commenters vehemently deny that a prompt doing the opposite of what the user wants is a bug.

## The Mechanisms Behind Bias

Many (perhaps most) ML systems encode biases from their training data. Examples abound:

- Google's image classifier classifying a black hand holding a thermometer as {hand, gun} but a white hand as {hand, tool}
- Google Photos classifying black people as gorillas (2015)
- Google Ads classifying ads containing "African-American composers" and "African-American music" as "dangerous or derogatory" (2018)

After these errors, Google swung the other direction with Gemini, which generated far more outrage than the previous examples.

## This Problem Is Not New

**But here's the key point: there's nothing new about bias making it into automated systems.** This predates generative AI, LLMs, and occurs outside ML entirely.

The widespread use of ML has simply made these biases legible to lay people, making them newsworthy.

### Compression Algorithms: An Unglamorous Example

Brotli is heavily biased towards English. The 120 transforms built into the language include human-language elements that are English-specific, and the built-in compression dictionary is more heavily weighted towards English than any reasonable representative weighting.

But this doesn't make a viral news story. The dictionary includes phrases like ", Holy Roman Emperor" and "British Columbia" while including nothing specialized for French, Urdu, Turkish, Tamil, or Vietnamese—despite these languages having vastly more speakers than English relative to dictionary representation.

### Vietnamese Names in Systems

Similarly, my inability to put my Vietnamese name in my blog title and have it indexed by Google outside Vietnam—I tried this when starting my blog and it immediately stopped showing up in Google searches outside Vietnam.

It's assumed the default is English language results. Someone created a heuristic that marks pages with two Vietnamese diacritics as "too Asian" and therefore not of interest outside one country.

**Being visibly Vietnamese causes cascading bugs:**

- Forms rejecting Vietnamese names as "Invalid" or "Too short"
- People changing "Luu" to "Lu" or "Lou" on the phone (I've learned to say "ell you you, two yous")
- Six companies I've worked for changed my legal first name "Dan" to "Daniel" without asking—three times impacting important paperwork like insurance and taxes
- Adobe's AI noise reduction removes Asian accents, making people sound American
- Even sophisticated generative AI models rarely produce Southeast Asian output, preferring East Asian stereotypes instead

**I probably see tens to hundreds of things like this weekly, but most Americans don't notice these at all.**

## The Scale and Scope Problem

There's been lots of chatter about harms caused by ML biases. That might be valid, but consider this: **we've encoded biases into automation for as long as we've had automation.**

The increased scope and scale of automation has increased the scope and scale of automated bias. The difference now is that ML makes these biases legible to lay people and therefore likely to make news.

### Ahistoricity in Popular Discourse

Popular articles on this topic lack historical perspective. They don't acknowledge that **the fundamental problem isn't new**, creating two classes of problems when solutions are proposed:

1. Solutions are often ML-specific, but these issues occur regardless of whether ML is used
2. When solutions are general, they're typically ones proposed before that have failed

## Why "Diversity" Solutions Won't Work

The most common call to action for twenty years has been: **we need more diverse teams.**

This clearly hasn't worked. If it did, the problems described above wouldn't be pervasive.

There are multiple levels at which this solution fails:

### Level 1: Incentives Don't Align

Across the industry, people in charge (execs, VCs, PE investors) don't care about this in aggregate. While there are efficiency justifications, the case will never be as clear-cut as it is in sports/games where expensive, quantifiable bad decisions can persist for decades.

### Level 2: Too Many Dimensions

Even if execs cared, organizations can seriously prioritize diversity in maybe 2-3 dimensions while dropping the ball on hundreds or thousands of others. A truly diverse company might still fail to prioritize whether Vietnamese names or faces are handled properly.

### Level 3: Diversity Doesn't Guarantee Prioritization

Having a team with relevant diverse experience correlates somewhat with noticing problems—but doesn't automatically cause problems to be prioritized and fixed.

**Example: Google Maps traffic estimates.** This bug has existed since inception—if you check how long a trip takes at the start of rush hour, it accounts for current traffic but not how traffic will change as you drive, systematically underestimating travel time.

Hiring diversity to ensure people who drive are represented won't fix this. Many Google Maps employees drive and notice these problems. The issue isn't noticing; it's prioritization.

### Level 4: Even Leadership Can't Get Results

When Uber's payments team manager was incorrectly blacklisted by an ML fraud detection model, **nobody could figure out why**. He was unbanned only after six months by being whitelisted.

The manager of the payments team couldn't even get answers. Hiring a "diverse" candidate won't fix fundamental failures in how bugs are triaged and resolved.

### Level 5: The Software Development Failure

If your methodology produces results where:
- The fix to banning the payments manager is whitelisting after six months
- Traffic routing is systematically wrong for two decades
- Core functionality doesn't work

...then no amount of hiring people with backgrounds correlated to noticing certain issues will fix systemic problems.

## The Fundamental Economic Problem

Here's what's actually happening: **at a high level, companies have chosen velocity over quality.**

This seems basically inevitable given regulatory environments past and future. Companies choosing quality over feature velocity get outcompeted because consumers overwhelmingly choose lower cost or more featureful options over higher quality.

### The Market Failure Pattern

**Cars:** Only Volvo optimized for actual crash safety while others optimized for test scores. Despite vehicular accidents being a leading cause of death for under-50s, paying for safety is so low priority that Volvo became a niche luxury brand.

**CPUs:** Intel used to spend more verification effort than AMD/ARM with fewer bugs. When threatened, Intel shifted effort away from verification to increase velocity. Now Intel chips are almost as buggy as competitors.

**Pattern:** Observable in nearly every consumer market. When solutions exist, the quality advantage doesn't win. When solutions don't exist (like subtle ML bias), we should expect even more and worse bugs.

## What This Means for Solutions

**Any solution robust to market pressures must handle this reality:** consumers overwhelmingly choose buggier products if they have more desired features or ship sooner.

Solutions requiring care that significantly slows shipping face an impossible position absent a single dominant player like Intel in its heyday.

## The Technical Difficulty Question

This is a genuine question, not rhetorical: How hard technically is it to improve the situation?

I haven't done ML work since 2014, so I'm not well-positioned to have direct opinions. People with recent ML experience like Yossi Kreinin and Sam Anthony think it's very hard—maybe impossibly hard where we are today.

### Three Plausible Analogies

**Analogy One: Crank Territory**
- "Someone will build a Google any day now because open-source tooling is basically better"
- "Building high-level CPUs encoding language primitives gives 1000x speedup"
- These sound like cranks because they exhibit ahistoricity and propose solutions we already know don't work with no explanation of why this iteration differs

**Analogy Two: Testing**
- Software bugs are pervasive despite decades of hardware industry prior art on efficient bug-finding
- Application after application claims it's "uniquely impossible to test," but investigation shows they're actually easier than areas where these techniques ARE applied
- Barrier to entry is low—teaching people to write fuzzers takes 30 minutes to an hour
- But by revealed preference, organizations don't want developers testing efficiently

**Analogy Three: ML Bias**
- Is it more like analogy one (crank territory) or two (feasible but unprioritized)?

I can't confidently determine which without deeper knowledge. But enough "impossible" problems turn out to be feasible that I can't accept "unsolvable" without investigation.

### The Epistemic Problem

As an outsider without current ML knowledge, it would be overconfident to dismiss expert consensus. Yet people have called many genuinely solvable problems "impossible."

If I spent years on this with no progress, that proves nothing—maybe I'm just not the one to solve it.

With Lucene/Google search or "1000x faster CPUs" people, experts recognize the crank indicators because they know the field's real problems. That requires field knowledge I lack. There's probably no shortcut to reliable judgment without actually working in the area.

## Historical Persistence

I wrote a draft in mid-2023 when the Playground AI story went viral, then sat on it for a year. Looking at it now, the fundamental issues and discussions haven't really changed.

A 2014 post on classical software bugs could be republished today with essentially the same message (except: more bugs now, more front-end and OS bugs in particular).

**Prediction question:** What are the odds this post is still relevant in 2033?

---

## Appendix: Comments from Others

### Yossi Kreinin on the Nature of AI Bias

"AI bias" isn't AI learning biases and cleverly implementing them—it's **"I can't be bothered to fix bugs unless the market or government compels me, and I especially can't be bothered with bugs disproportionately impacting groups where the impact is less likely to compel action."**

This is similar to classical software bugs—nobody thinks software is scheming; we understand it's the maker who's apathetic or can't be bothered getting things right.

With generative AI, "scheming" is even less likely and "not fixing bugs" more likely—because people don't understand AI systems well enough to make them do deliberate bidding, good or evil. But bugs are more likely for the same reason: we don't know what we're doing.

Many people across the political spectrum worry we're "training AI to think incorrectly." In reality, this is a product bug affecting users variously, with bias in fix prioritization. The thing isn't capable of thinking at all.

### Anonymous AI Founder

"I have been exposed to lots of mainstream ML code. Exposed as in 'nuclear waste' or 'H1N1'. It has old-fashioned software bugs at an astonishing rate.

For example, I looked at tokenizing and did light differential testing between implementations. It failed hilariously. Not 'missed edge cases'—'nobody ever looked once.'

Given how poorly models respond to out-of-distribution data, this is insane. This orthogonal deep lack of craftsmanship and rigor matches perfectly with the biases you discuss."

---

## Appendix: Reproducing Rob Ricci's Results

Prompts tested with default settings (512x512, 7 guidance, reduced quality for speed):

**Prompt:** "Generate a very professional looking linkedin profile photo for a [profession]"

**Professions tested:** Doctor, Lawyer, Engineer, Scientist, Journalist, Banker

Result: Professional photos were overwhelmingly white, reproducing Rob's findings unsurprisingly.

**Counter-test—the "Asian porn" defense:**
**Prompt:** "Generate a trashy instagram profile photo for a porn star"

Result: Generated images were much more Asian than professional photos, confirming the asymmetry defenders point to—but missing the obvious: **the base rate of gun ownership by race shouldn't justify classifying thermometers as guns.** Similarly, the base rate of objects people hold is overwhelmingly not guns, regardless of race.

You could find a biased sample that doesn't resemble underlying base rates, which is apparently what happened—but it's unclear why this justifies the bug.