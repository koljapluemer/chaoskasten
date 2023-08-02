## About 

Notetaking Tool. Deployed at <https://www.chaoskasten.com>

## Organisation

### deploy:

./deploy.sh

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