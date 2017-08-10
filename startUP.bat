call myvenv\Scripts\activate
cd WebMateriel/
python manage.py makemigrations main
python manage.py sqlmigrate main 0001 &
python manage.py migrate
python manage.py runserver localhost:8888 &
