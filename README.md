### next up

* Put all those things like redirect if not logged in etc etc in a function I guess?
* The Webhook does not really create/activate an account (obviously, if you go through the stripe process, you never sign up, lol)
* Also includes: Stripe subscription data

Just get a fucking Django Stripe tutorial and work through it, it smells like uncatched edge cases around here.

After putting in signup data, we are getting:
`Request req_Hnmrx8Ke6uGAHZ: No such customer: 'cus_J1DmwfT668tExA'; a similar object exists in test mode, but a live mode key was used to make this request.`

I thought it was environments problems, but putting everything into .env did not help...
...There is a key hardcoded into html...

### Sprint 26.2 - 2.3

* Get the normal signup process going!
* allow free access codes

### backlog:

* beim Bearbeiten von Notes: Zwischenspeichern ohne Edit-Modus zu verlassen
* Sendgrid
* Stripe
* First note does not show up in recent
* spellcheck für Texte
* der tag zum Drawer bei offener Note sieht sehr ähnlich aus, wie die Kästen der dazu connecteten notes
* Links immer in neuem Tab öffnen lassen
* einbauen von Latexformeln (pandoc?)
* neuen Drawer auch beim Erstelle/ Edititeren einer Note
* die Größe beim Editieren einer Note sollte die selbe Größe behalten wie die Original Note
* color gradient over scrollable text
* optimize SQL
* disallow SSH by password

### wontfix

* zwei Notes sind nicht gleichzeitig bearbeitbar; jedwede andere Aktion schließt unwiderruflich den aktuellen Edit einer Note -> Warnhinweis öffnen
* Erlaube Markdown Formatierung von Code (zB Python)
* Notes in Kästen in der Sidebar: öffnen auch dann, wenn nur in den Kasten geklickt wird


### bugs:

* recent notes (check all cases)
* active users only counts logins, and includes temp users
* password forgot connection problem

### ideas:

* Hypercard
* needs attention button

### future:

* write HN dude

### notes:

* Docker Stuff

`docker-compose -f docker-compose.prod.yml up -d --build`

`docker-compose -f docker-compose.prod.yml logs -f`

* locally, use *testaccount4* for lots of generated notes.
* env is called `.virtualenv`

* The static files sometimes not loading has something to do with the static directory
* For some reason, the server tries to serve the files from an url dependent on the current url we are on

### deploy:

./chaoskasten3/deploy.sh
