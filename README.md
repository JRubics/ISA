# ISA

run tests:
$python manage.py test

run app:
$python manage.py runserver

# DOCKER
latest image builds: https://hub.docker.com/r/jrubics/isa/

build image:

$docker build -t isa .

$docker run -p 8000:8000 -itd isa

