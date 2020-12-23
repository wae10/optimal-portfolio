import os
from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
    
