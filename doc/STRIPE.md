# Stripe

* Keys are everywhere: Settings, Views, Templates
* Test credit card is in Chaoskasten
* We're using this is a payment widget, I think: https://stripe.com/docs/billing/subscriptions/checkout

## Setup / Random shit

* In the second run, I did this tutorial <https://testdriven.io/blog/django-stripe-subscriptions/>
* First, we defined some weird js (`stripe.js`) to get the credit card from I think?
* We hooked that up with some even weirder AJAX (?) to pass the public key
* From there, we redirect to success or cancel

> There are two types of events in Stripe and programming in general. Synchronous events, which have an immediate effect and results (e.g., creating a customer), and asynchronous events, which don't have an immediate result (e.g., confirming payments). Because payment confirmation is done asynchronously, the user might get redirected to the success page before their payment is confirmed and before we receive their funds.

* Then we use webhooks to actually confirm payment

## Todos

* When locally testing via Stripe CLI, why is there 404 galore when creating a new user?
* We are 80% through the guide, CTRL F "Fetch Subscription Data"
