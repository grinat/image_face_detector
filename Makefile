.PHONY: help dev run build-docker-image run-docker-image

CONT_NAME ?= "image_face_detector"
PORT ?= 5001

help: Makefile
	@echo

prod:
	uwsgi --plugins http,python --http :$(PORT) --wsgi-file app.py --callable app

dev:
	python app.py

dev-docker-compose:
	echo "TODO: mount ./venv:/app/venv for code higlliht"
	python app.py

build-docker-image:
	docker build . -t $(CONT_NAME)

run-docker-image:
	docker rm --force $(CONT_NAME) || echo ""
	docker run -d -p $(PORT):5001 --name $(CONT_NAME) --restart always $(CONT_NAME)
