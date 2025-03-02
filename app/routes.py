from app import app

@app.route('/')
def homepage():
    return "Homepage"
@app.route('/test')
def test():
    return "Test url"