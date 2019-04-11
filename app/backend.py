from flask import Flask, render_template, send_from_directory
from backend import backend, callFetchData

app = Flask(__name__)

@app.route("/")
def index(path):
    '''Serves the welcome page'''
    return send_from_directory('faculty', path)

@app.route("/")
def facultyIndex(path):
    '''Serves the faculty portal '''
    return send_from_directory('faculty', path)

@app.after_request
def add_header(r):
    """
    Add headers to force the browser to not cache static files. 
    To make it easier for development, can be safely removed 
    in production. 
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    callFetchData()
    app.run(debug=True, threaded=True)