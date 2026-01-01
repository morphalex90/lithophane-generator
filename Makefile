install:
	pip3 install -r requirements.txt

start:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	export FLASK_APP=app/routes.py
	flask run