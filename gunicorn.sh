#!/bin/bash

source env/bin/activate

cd /var/lib/jenkins/workspace/django-cicd/

python3 manage.py makemigrations
python3 manage.py migrate

echo "migrations has been done"

cd /var/lib/jenkins/workspace/

sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/

echo "$USER"
echo "$PWD"

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

echo "Gunicorn has been started"

sudo systemctl status gunicorn
sudo systemctl restart gunicorn