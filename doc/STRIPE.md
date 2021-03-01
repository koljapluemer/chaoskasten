# Stripe

* Keys are everywhere: Settings, Views, Templates
* Test credit card is in Chaoskasten
* We're using this is a payment widget, I think: https://stripe.com/docs/billing/subscriptions/checkout

## Setup / Random shit

* In the second run, I did this tutorial <https://testdriven.io/blog/django-stripe-subscriptions/>
* First, we defined some weird js (`stripe.js`) to get the credit card from I think?
* We hooked that up with some even weirder AJAX (?) to pass the public key
* From there, we redirect to success or cancel
* Then we use webhooks to actually confirm payment
