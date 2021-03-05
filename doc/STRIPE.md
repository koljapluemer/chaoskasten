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

## Sign Up Flow

1. The User clicks Sign Up
2. This gets handled by `users.py/signup`, which just serves a basic Django Form
3. If the form is valid, a new *user* is created and he is redirect to the payment form
4. In the background, a `model.py` function adds a *profile* to the *user*.
5. Furthermore, the function creates a Stripe customer and saves the stripe ID in the *profile* object
6. The form redirection goes over URL and `views/stripe` into an basically empty template which loads a Stripe Checkout form with the relevant parameters
7. The Stripe form then redirects to either success or cancel template
8. No matter whether the payment was successful, the user now has an account in which he is logged in
9. We can check whether the subscription is active fairly easily (check the settings page). From this indicator, we can build nudges and locks later (who cares).

if we are converting an existing user, the process is essentially the same. We are still using the `signup.html` page, we are just using the redirect value stored
within the submit button.
