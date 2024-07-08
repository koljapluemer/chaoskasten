---
layout: post
title: Lessons Learned From Building My Own Note Taking System
tags: django lessons-learned web software
description: Chaoskasten — The story on how I wrote a system for note taking and organization, and what I learned.
---

 In 2017 I faced an ugly truth: My bookmark collection, several hundred items large, was a useless heap of data. It just sat there, slowly growing, never to be actually reviewed, referenced or reused. *Favorite & Forget* is the Reddit slang for doing this (with Reddit's "favorite" feature). This realization led me down a path of personal wiki's such as *vimwiki* or browser-based solutions, popular apps and tools like Notion and much more. Interestingly, most of them failed for a similar reason: They lacked an incentive to be used in the moment.

As it turns out, contributing to one's collection of information is not that interesting of an activity. Think about the moments where you *should* use your information system: Trying to find data on a view point you are currently arguing for or against, reading about an interesting book or movie or even something as abstract as wanting to fill a stretch of time with learning. Surely it does not matter if you just keep scrolling down the thread where someone name-dropped said book. Surely it does not matter if you just google the paper you are trying to cite, and surely it does not matter if you just go for the gamified experience of a DuoLingo session instead of reviewing your class notes.

It does not only matter, it is almost all that matters. In 2019, I probably would not have been able to put this key point into words, but I found the right track: The epitome of useless information in what ever personal information system are those artifacts entirely disconnected every other string of information inside and outside the system (read: your daily life, knowledge held in your head, and other information systems). Those are never reviewed and thus never used, and often so specific that they are not even found to stumble upon randomly on a deep dive.

So when I stumbled upon [Luhmann's Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten), I was elated. This guy had it all figured out. Others have written about Luhmann in detail - I recommend the book *How To Take Smart Notes: 10 Principles to Revolutionize Your Note-Taking and Writing* as well [Introduction to the Zettelkasten Method](https://zettelkasten.de/introduction/) which is the article I first stumbled upon. In any case, here is a short summary of his method: information is noted down on a (physical) paper note and then placed into a slip box, vaguely ordered by simple rules. The key: Each note also carries references to relevant other notes, and these connections are a first-class citizen of the system. Thus, a network of information is created, facilitating deep as well as novel thought. Unconnected notes fade into obscurity by design, since they obviously don't tie in to your externalized thought network. Simple and genius.  

Excited, I scoured the web for about five minutes, declared that no one had ever though about digitizing this concept ever before (of course, [the Obsidian app](https://obsidian.md/) and a bunch of others had done so, and very excellently, as well) and went about doing this myself.

## Chaoskasten

A mere two years later, I have [Chaoskasten](https://www.chaoskasten.com), a piece of software I am confident enough to show, say, close friends. On a technical level, it is Python/Django Webapp with a SQL database and Stripe to implement a SaaS Freemium model (don't worry, I am the only one who has ever paid for it).

Functionally, it digitizes most of the core features of Luhmann's slip box: You can create and edit notes, refer to other notes, open and close notes, delete notes, all that stuff. I've also integrated a *Learning* mode based on [Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition), but oh boy, that is a whole other topic.

Feel free to try out the app, just remember that the "Beta" in the title of the browser is an apt descriptor.

## Well, Does It Work?

On the plus side, at the point of writing, I have created 1095 notes and about a third of them refer to other notes, Luhmann style. So, success? Meh. The problem, that nothing actually incentives me to use the app in the key moments, remains. Chaoskasten is the least bad attempt of mine to fix that, so far. But I am not giving up. Instead, I am moving to bigger and better things (hopefully). So I think this post is neither a failed promotion nor dive into productivity systems cut short, but a kind of finalization. To label the hundreds of hours spent on this as "good investment", here are some lessons learned:

## Lesson Learned: Complicated Things Are Easy, Easy Things Are Complicated

Most likely due to the fact that Chaoskasten is my biggest personal project so far, it illustrated this relationship *a lot*, and starkly so: Setting up Stripe as a payment provider for a month-based subscription proved to be straight-forward, implementing a voucher system on top to allow friends (sorry, beta-testers) to test the app without forking over money took twice as long and was thrice as painful. Implementing the whole database scheme again was painless thanks to Django's comfy system of banishing SQL to a dark shadow world, undoing a de-sync of database migration due to bad git discipline almost made me redo the whole project from scratch.

What's the lesson here? I suppose being prepared for it - mentally, and maybe even technically (as in, having fail-safes) is a decent start.

## Ask What the Actual Problem Is. Then Ask Again.

I certainly do not regret the incredible of learning this project provided me in exchange for time invested. Yet, the fact remains: I mostly did not solve my own problem. The inconvenient truth here is that I was *very* prematurely convinced that I had found the right problem, when in fact I probably *still* haven't. Some of that might be quite human; you get handed a hammer - and it's so shiny! - surely you can use it on some nails. So, constantly question the hammer, the nail and the wielder and for the love of God, build some MVPs to validate assumptions.

## If You Build It, They Won't Come (why would they)

Not taking a line that made it's way from a movie ripe with ambiguous meaning into the world of startup speech seems like a good idea in general. I never geared this project toward income or even customers other than myself, but I am nonetheless happy to report that the only people that found their way to Chaoskasten on their own are weird bots promoting a Polish non-profit, presumably mistaking the website for social media. Maybe if you build, do some SEO, some word of mouth and a sassy Twitter account, they will come. Haven't tried it.

## Wrap Up

Well, this last paragraph reads like an end, albeit being a bit depressing and not really to the point of this post. Let me recommend you the excellent [Notation and thought](https://github.com/k-qy/notation) collection instead.
