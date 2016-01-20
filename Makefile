default:

install:
	./install.sh

build:
	./build.sh

dev:
	PYTHONPATH=. python client/api.py

prod:
	PYTHONPATH=. python client/api.py

tests:
	PYTHONPATH=. nosetests test

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

clean-logs:
	rm -r logs/*
