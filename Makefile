build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose stop

yapf:
	yapf -i app.py