# Why It's Impossible to Agree on What's Allowed

On large platforms, it's impossible to have policies on things like moderation, spam, fraud, and sexual content that people agree on.

David Turner made a simple game to illustrate how difficult this is even in a trivial case: **No Vehicles in the Park**. I recommend playing it before reading further.

## The Fundamental Problem: Agreement is Impossible

The game demonstrates that it's very difficult to get people to agree on moderation rules—even in a much simpler context than real-world platform moderation. The rule is straightforward: "No Vehicles in the Park." Yet when asked a small set of questions about edge cases, people couldn't reach consensus.

My initial reaction to the survey was that the questions weren't chosen to be particularly challenging. Dave could've asked much more nettlesome edge cases if he wanted. **Yet despite not making it particularly challenging, there's no broad agreement.**

### The Overconfidence Problem

Comments reveal another insight: **people dramatically underestimate how hard agreement actually is.**

If you read rule interpretation discussions on Lobsters, Hacker News, Reddit, etc., when people suggest solutions, the vast majority propose something that anyone experienced in moderation knows cannot work. It's the moderation equivalent of "I could build that in a weekend."

The top Hacker News comment perfectly illustrates this overconfidence:

> I'm fascinated by the fact that my takeaway is the precise opposite of what the author intended.
>
> To me, the answer to all of the questions was crystal-clear. Yes, you can academically wonder whether an orbiting space station is a vehicle and whether it's in the park, but the obvious intent of the sign couldn't be clearer. Cars/trucks/motorcycles aren't allowed, and obviously police and ambulances (and fire trucks) doing their jobs don't have to follow the sign.
>
> So if this is supposed to be an example of how content moderation rules are unclear to follow, it's achieving precisely the opposite.

Someone agreed: "Exactly. There is a clear majority in the answers."

This interpretation is based on looking at the survey graph showing majority responses per question. But this reasoning is flawed.

## The Math of Disagreement

There's a critical difference between:
1. Having a majority on each individual question
2. Having consensus on a consistent set of answers

**Even if there's a majority position on each question, this doesn't mean most people agree with you.** Given how the per-question majorities vary, it would be extraordinary if being in the majority for each question meant most people agreed overall—or if any consistent position had majority support.

### The Data Reveals the Truth

When I examined the actual data (which Dave generously shared), the results were stark:

**There was no set of answers which the majority of users agreed on. It wasn't even close.**

The survey collected 36,902 responses, which produced **9,432 distinct opinions**—an average of ~3.9 people per unique position. The average user agreement is ~0.01%.

The "obvious" position that the top commenter described was selected by only **11.7% of people**. This means 88.3% of people disagreed with the "crystal-clear" answer.

### Distribution of Disagreement

- **1st most popular position:** 11.7%
- **2nd most popular position:** 8.5% (disagrees on whether a non-functioning WWII tank memorial violates the rule)
- **3rd most popular position:** 6.5%
- **4th-7th most popular positions:** ~1% each
- **Everything else:** Less than 1%

**Only 27% of people find themselves in agreement with significantly more than 1% of other users.** The median user agrees with just 0.16% of other users.

When plotted, the distribution of agreement looks like a few points above zero followed by a long tail of zeros when graphed on a linear scale. A logarithmic scale is necessary because there's so little agreement.

### What This Actually Means

Michael Chermside had a more insightful comment on Hacker News:

> That's not particularly surprising. But you may be asking the wrong question.
>
> If you want to know whether the rules are clear then I think that the right question to ask is not "Are the answers crystal-clear to you?" but "Will different people produce the same answers?".
>
> If we had a sharp drop in the graph at one point then it would suggest that most everyone has the same cutoff; instead we see a very smooth curve as if different people read this VERY SIMPLE AND CLEAR rule and still didn't agree on when it applied.

## Why People Misunderstand Disagreement

Many people are overconfident when predicting what others find obvious. They incorrectly assume other people will think the same thoughts and find the same things obvious.

This is true even for simple examples like "No Vehicles in the Park." It's far more true for charged issues where moderation fights become bitter.

### The Draymond Green Analogy

Consider a more emotionally-charged example: In basketball, ask any serious non-Warriors fan who's the dirtiest player in the NBA. You'll find general agreement it's **Draymond Green** (some might say Dillon Brooks for near-uniform agreement).

Yet ask Warriors fans about Draymond? Most explain away every dirty play of his.

So even on a question more straightforward than "no vehicles in the park"—"is it okay to stomp on another player's chest?"—you'll find sizable groups with extremely strong disagreement with the "obvious" answer.

### From Abstract to Real-World

When you move from a contrived abstract example to a real-world issue people have emotional attachments to, it generally becomes **impossible to get agreement even in cases where disinterested third parties would all agree.**

And we've already shown that agreement is already impossible even without emotional attachment.

When you move further into issues people care about—like politics—the disagreements become even more intense.

## The Fractally Contentious Nature of Charged Issues

People often struggle to "agree to disagree" over what would seem like small differences of opinion.

Charged issues are **fractally contentious**: they cause disagreement among people holding nearly identical opinions, making them far harder to reach consensus on than "no vehicles in the park."

### Jo Freeman's "Trashing"

In 1976, feminist Jo Freeman wrote about being canceled for minute differences in opinion—a common experience in activist movements. Freeman used the term "trashing" (later popularized as "cancellation").

Nearly fifty years later, this pattern persists unchanged. 

A recent parallel: Natalie Wynn's similar experience. For people far from both in the political spectrum, the differences between Natalie and those calling for her deplatforming seem fairly small.

Yet "small" differences resulted in calls not just for deplatforming, but for:
- Physical assault
- Doxing
- Same treatment for friends and associates
- Treatment for people who publicly discussed similar topics without canceling her

**Years later, she still receives calls for deplatforming.** A Twitter search years after the incident found lengthy rants about how horrible she is for the alleged transgression—from posts just 10 days old.

The actual positions are close enough that describing them would require 5,000-10,000 words (compared to a left-wing vs. right-wing politician, where differences are blatant enough to describe in a sentence).

The point: **Almost any person with public opinions on charged issues operates in fractally contentious opinion space.**

## Why Large Platforms Can't Satisfy Everyone

**No large platform can satisfy user preferences because users fundamentally disagree over what content should be moderated off and what should be allowed.**

This problem scales up as platforms grow larger.

## The "No Moderation" Fantasy

### Naive Solution One: Eliminate Moderation Entirely

Some suggest removing all moderation will solve everything. If you want a small forum like 4chan, no moderation can work fine. But even if you want a big platform resembling 4chan, no moderation doesn't actually work.

Consider Twitter's numbers: 300M users and 1M bots removed per day.

If you stop "censoring" bots, the platform will quickly fill with bots until:
- Everything visible is spam/scams/phishing
- Accounts copy content from elsewhere
- LLM-generated content posts scams
- Most accounts are bots
- Bots form massive engagement/voting rings that drown out human content

### Naive Solution Two: Allow Memes and Jokes

Another suggestion: stop downranking memes and dumb jokes. Forums with upvoting/ranking ban memes after becoming totally dominated by them because people upvote memes at much higher rates than nuanced content.

Not everyone wants forums full of lowest-common-denominator meme content.

When cheap humor isn't banned, top comments get dominated by it. For months, one top comment on Reddit (where cheap humor wasn't restricted) was variants of "I'm surprised he can walk with balls that weigh 900 lbs." on any story about men doing vaguely heroic things—repeated 150 times a day across the forum.

Some people actually want this. But most who complain "no one has a sense of humor here" when flagged probably don't actually want to read forums dominated by other people's cheap humor.

## Federation Doesn't Solve This

Nowadays, "federation" is trendy as a cure-all (like "blockchain" five years ago). But federation doesn't solve this problem for typical users.

I had a conversation with someone who's an ActivityPub spec creator. They claimed federation solves this problem—that Threads adding ActivityPub would create a federating panacea.

I noted that:
- Fragmentation is already a problem on Mastodon
- Whether to block Threads is contentious
- This would only increase fragmentation

Their response: "Most people won't block Threads, and it's their problem if they do."

I replied with a real-world problem: Many non-technical friends who tried Mastodon picked a server, only to find they couldn't follow someone they wanted due to server blocking. They'd try another server to follow that person, then find another person they wanted is blocked by that server.

**The fundamental problem:** Users on different servers want different things allowed, resulting in no server giving access to everything they want to see.

The ActivityPub creator had no response and deleted their comment.

### The Simpler Problem Federation Can't Even Solve

There's an easier problem than moderation/spam/fraud policy that the fediverse can't solve: **how to present content across platforms.**

When using Mastodon with someone using "honk," messages get mangled. For example, a quote mark `"` in the subject/content warning field gets converted to `&quot;`. When the Mastodon user sees replies from the honk user, the discussion forks into a different subject.

This is a problem that can be fully specified without ambiguity, where people are far less emotionally attached than to moderation issues—**and the fediverse can't even solve it across two platforms.**

If federation can't solve basic technical interoperability problems, it certainly can't solve the value-disagreement problems that moderation represents.

## The Core Insight

The difficulty of reaching agreement on moderation isn't a solvable problem waiting for the right policy framework. **It's a fundamental reflection of human disagreement on values.**

On issues where people care deeply, where values are at stake, and where different groups prioritize different outcomes, consensus is not just hard to achieve—it's mathematically and practically impossible at scale.

Any system claiming to have solved "the moderation problem" has either:
1. Solved it for a small, homogeneous group
2. Not actually solved it (and eventually people realize this)
3. Made choices that satisfy one group while dissatisfying another

The third option is what actually happens on large platforms. The question isn't whether to make choices—it's who makes them and what values they reflect.