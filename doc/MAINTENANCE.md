to clear out stale data:

```
heroku login
heroku ps:exec -a chaoskasten
python manage.py remove_expired_users
```

do it the hard way:

```
heroku pg:psql postgresql-cubic-94388 --app chaoskasten


SELECT schemaname, relname, n_live_tup 
FROM pg_stat_user_tables 
ORDER BY n_live_tup DESC;


DELETE FROM django_session;
```