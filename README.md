# ISA
install requirements:
pip install -r requirements.txt

run tests:
$python manage.py test --settings=ISA.settings.local

run app:
$python manage.py runserver --settings=ISA.settings.local

travis:
https://travis-ci.com/JRubics/ISA

# DOCKER
latest image builds: https://hub.docker.com/r/jrubics/isa/

build image:

$docker build -t isa .

$docker run -p 8000:8000 -itd isa
