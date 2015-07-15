default:

install:
	./install.sh

build:
	./build.sh

dev:
	PYTHONPATH=. python client/api.py

prod:
	PYTHONPATH=. python client/api.py

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
