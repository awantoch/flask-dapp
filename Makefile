SHELL=/bin/bash
include .env
export

install:
	@npm i
	@pip install -r requirements.txt
run:
	@FLASK_APP=src/main.py FLASK_ENV=development python -m flask run

migrate: deploy

compile: contracts

contracts:
	@npm run compile

deploy:
	@npm run deploy
