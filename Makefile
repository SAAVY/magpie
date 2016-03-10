.PHONY: clean build dev tests deploy

default:

install:
	./install.sh

build:
	./build.sh

dev:
	PYTHONPATH=. python client/api.py

prod:
	PYTHONPATH=. gunicorn -w 4 -b 127.0.0.1:8002 'client.api:start()'

tests:
	PYTHONPATH=. nosetests test

clean:
	find client -name "*.pyc" -exec rm -rf {} \;

clean-logs:
	rm -r logs/*

db:
	redis-server