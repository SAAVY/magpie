.PHONY: clean build dev tests deploy

default:

install:
	./install.sh

build:
	./build.sh

dev:
	PYTHONPATH=. python client/api.py

prod:
	PYTHONPATH=. gunicorn -w 4 -b 127.0.0.1:8000 'client.api:start("logs",False)'

tests:
	PYTHONPATH=. nosetests test

clean:
	find client -name "*.pyc" -exec rm -rf {} \;

clean-logs:
	rm -r logs/*
