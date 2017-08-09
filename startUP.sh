#!/bin/bash
source last-minute-env/bin/activate
cd WebMateriel/
#fuser 8888/tcp -k
#pip install -r requirements.txt
python manage.py makemigrations main
#python manage.py check --deploy
python manage.py sqlmigrate main 0001 &
python manage.py migrate
#python manage.py test
BUILD_ID=dontKillMe nohup python manage.py runserver localhost:8888 &
