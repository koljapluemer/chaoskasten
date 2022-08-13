## About 

Notetaking Tool. Deployed at <https://www.chaoskasten.com>

## Organisation

### user feedback - seems fixed

* Password Requirements are shown badly
* Redirect von Password Reset broken
* Delete fails for help note and first note
* Settings broken (fuck)
* Settings -> Signup does not convert (because its not a dynamic covnert/signup thing)
* Adapt home page when signed in
* Does Password reset *work*?
* "You have notes"
* Login does not properly auto-redirect

### backlog:

* Pricing not too clear
* Formatting not too discoverable
* Initial user question: what's a good note to test?
* Basic Documentation editorialize
* Email validation?
* Feedback
* Connection Visualization
* when learning queue is exhausted, we are currently just jumping back to root w/o explaination
* beim Bearbeiten von Notes: Zwischenspeichern ohne Edit-Modus zu verlassen
* Wenn in den Settings, dann kommt man nicht wieder zurück über Bedienfeld
* Redirect zur Homepage (Login-Seite), wenn auf einer anderen aber nicht eingeloggt
* Sendgrid
* Stripe
* First note does not show up in recent
* Temporary user does not get redirect to his notes
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

### deploy:

./chaoskasten3/deploy.sh



### check for real users:

```
heroku run python manage.py shell -a chaoskasten
from main.models import *
from django.db.models import Count
Profile.objects.annotate(notes_num=Count('note')).filter(notes_num__gt=2).count()
```

### run local


do this to have it running but broken on localhost (missing .env). `.env` stuff can probably be pulled from Heroku or so. 
Not motivated to find that out before I actively developing this again...

```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```