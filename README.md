# Generate STL lithophane from image

## Install
- `pip3 install -r requirements.txt`

## Run
`python3 generate.py`

## Run web server (https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `export FLASK_APP=app/routes.py`
- `export FLASK_DEBUG=1`
- `flask run`