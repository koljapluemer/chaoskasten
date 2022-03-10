to clear out stale data:

```
heroku login
heroku ps:exec -a chaoskasten
python manage.py remove_expired_users
```