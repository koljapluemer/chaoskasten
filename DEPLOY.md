We are following this guide: <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04>

## how it was set up

The structure was in place for ages, I put the new cleaned up version recently and documenting my process here.

* clone the git repo
* install venv and make and env called .env; activate, install
* make the settings file `production.py` and copypaste from the local repo (this could be better, lol)
* This pulls in OS environ stuff that already exists, probably just harcoded into the ubuntu distro or wherever they live
* Django server does start
* ~~ Copypaste database from old repo in attempt to easily keep data (lord have mercy) ~~
* Nevermind, i don't see a db. It is probably already accessing the existing one (lord have even more mercy please)
* Adapt the paths in `/etc/systemd/system/gunicorn.service`
* Mind the `wsgi`, bitch
* Adapt the paths in `sudo vim /etc/nginx/sites-available/chaosnotes`
* Run `collectstatic`
* Check the fucking system Environment
* Some settings was set to a settings module from the old project
* The file holding all the values is `.env`, but I am not sure how it's sourced
* I think venv sucks for this, because you have to hack env values real hard
* I just did: `export DJANGO_SETTINGS_MODULE=main.settings.production`
* At this point, gunicorn was able to start in a test run (`gunicorn --bind 0.0.0.0:8000 main.wsgi`)
* Gunicorn journal told me that the secret key must not be empty...I think those env values are thoroughly fucked
* If I don't source control the settings file, I don't see a problem putting the values in there to be honest
* Put everything into settings/deployment, still empty secret key. What?
* I gave up and just made up a secret key, putting it into the base file. Oof.
* The error is different now, but I am still getting this shit. Why??
* Ok I had to put the run option into the gunicorn file, making it really shitty
* Putting the gunicorn file into this repo, but I really need decent secret management
* Now nginx throws 502
* The specifics (111 connection refused) imply that the db is wrongly configured
* 30 minutes later: I think this absolute salad of secrets is fucking this up :/
### new day
* I am now trying to manage stuff with `django-environ`
* For that, you have to put an `.env` file in the same directory as the settings

## Debugging
* `sudo journalctl -u gunicorn`
* `sudo tail -F /var/log/nginx/error.log`

## every time

* Restart nginx

```
sudo nginx -t && sudo systemctl restart nginx
```

* Restart gunicorn

```
sudo systemctl daemon-reload && sudo systemctl restart gunicorn
```
