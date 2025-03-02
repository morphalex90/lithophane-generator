from app import app

@app.route('/')
@app.route('/test')
def test():
    return "Hello, World!"