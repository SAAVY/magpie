default:

install:
	./install.sh

build:
	./build.sh

dev:
	python client/api.py

prod:
	python client/api.py

clean:
	rm -r *.pyc
