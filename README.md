# ISA

run tests:
$python manage.py test

run app:
$python manage.py runserver

# DOCKER

$docker build -t isa .

$docker run -p 8000:8000 -itd isa
