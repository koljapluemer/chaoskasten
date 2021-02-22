cd chaoskasten3/
source .virtualenv/bin/activate
unset DJANGO_SETTINGS_MODULE
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl daemon-reload && sudo systemctl restart gunicorn
sudo nginx -t && sudo systemctl restart nginx
