# How you migrate is everything

Production systems are always mid-migration. Managing this mess is the job.

## Your code becomes legacy software when it works

You build something to solve a problem, then the problem changes. Or best practices evolve. Or you hire team members with more experience. Or the world changes. Or you have more people touching the same code and your beautiful architectural vision didn't translate.

You look at your system and feel a tinge of disgust. What were we thinking? It barely works!

But it does work ;)

Despite what you hear online and read about in books, **big ball of mud is the world's most popular architecture in practice**. Unavoidable really. Things change too fast.

---

## Good software barely works

The goal of software development is to get you to the next stage. Like kicking a can. You build something that barely works. Anything more would be wasting resources.

Like Colin Chapman, legendary F1 car designer, used to say:

> "Any car which holds together for a whole race is too heavy"

Your ideal race car wins the race then promptly falls apart at the finish line. That's why we have safety standards now 😅

**Realistically, the quality you put in depends on the buxton index of the project.** You put more effort and resources into the new billing system than the marketing page. Because marketing iterates fast and billing should be steady and reliable.

Both will change.

---

## You're always mid-migration

Production software is like a living thing. You're always fixing bits that are broken, building new systems where you need them, and replacing entire areas as they become decrepit and no longer fit for purpose.

**Software engineering is the art of programming over time.** Adapting systems to changing requirements.

### The data problem

With infinite resources, you'd fix everything all at once. Throw away the old code, write the perfect new code, and switch over. But that doesn't work.

There's a lot of accumulated knowledge in that old code. Little quirks and edge cases you forgot the company even supports. Someone out there depends on that behavior :)

And even if you could account for every little detail, **data lives forever**. Unless you can migrate the data, your code will have to support the old way in perpetuity.

That's where most migration efforts fall down. Your code has to keep working for that user with an old document from 5 years ago.

And if you get lucky, the leading edge of your migration will be starting a new migration while the trailing edge hasn't even caught up yet. Half-completed refactors are surprisingly common in production software. You put the work down one day and didn't even realize you'll never have time to come back 🫠

---

## How you migrate is everything

The winning software team, then, is not the team with the best coding or system design chops, **it's the team most comfortable with smoothly migrating between different versions of their software.**

I can't give you a generic solution. This is the dependiest "it depends" area of our field. Every situation really is different.

### Key principles

**Never undertake a rewrite or refactor that keeps your software in a broken state for long periods of time.** If you can't merge to main every few hours, something is wrong.

**You may have to stop refactoring at any moment.** You won't come back for months. Act accordingly.

**Visible wins matter.** What new capability will this unlock? What hard problems will become trivially easy? Who will feel happy when your migration, rewrite, or refactor are done?

**Get sponsorship.** You need buy-in.

**Include others in your design.** Ask for advice not just feedback. Advice gives you champions fighting for the cause, feedback gives you critics.

**Populate the new data first, support old and new data in parallel, migrate the old data, then kill support for the old way.**

**First consolidate your control flows.** Every part of your code should call the same function or service to make a decision. You cannot migrate when business logic is smeared around.

**The hardest part is building new abstractions.** Moving code around without building abstractions is just window dressing. Yes, this can take months even if the coding takes weeks.

---

Cheers,
~Swizec