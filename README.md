### evi sprint:

* make a proper CI/CD


### sprint:

* beim Bearbeiten von Notes: Zwischenspeichern ohne Edit-Modus zu verlassen
* Wenn in den Settings, dann kommt man nicht wieder zurück über Bedienfeld
* Redirect zur Homepage (Login-Seite), wenn auf einer anderen aber nicht eingeloggt
* Sendgrid
* Stripe
* First note does not show up in recent
* Temporary user does not get redirect to his notes

### backlog:

* split views and model file
* unfuck static files
* code formatting in adjacent lines touches
* blockquote formatting
* spellcheck für Texte
* Notes in Kästen in der Sidebar: öffnen auch dann, wenn nur in den Kasten geklickt wird
* der tag zum Drawer bei offener Note sieht sehr ähnlich aus, wie die Kästen der dazu connecteten notes
* Links immer in neuem Tab öffnen lassen
* einbauen von Latexformeln (pandoc?)
* neuen Drawer auch beim Erstelle/ Edititeren einer Note
* Erlaube Markdown Formatierung von Code (zB Python)
* zwei Notes sind nicht gleichzeitig bearbeitbar; jedwede andere Aktion schließt unwiderruflich den aktuellen Edit einer Note -> Warnhinweis öffnen
* die Größe beim Editieren einer Note sollte die selbe Größe behalten wie die Original Note
* color gradient over scrollable text


### bugs:

* recent notes (check all cases)
* weird bugging out of button icons
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

### deploy:

* `collectstatic`
* `nginx`
* `gunicorn`
* install requirements
* migrate/make migrations
* settings `DEBUG=FALSE`
* check `~/.env`
