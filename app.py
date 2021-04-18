import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from flask_cors import CORS

def create_app(test_config=None):
    
    app = Flask(__name__)
    setup_db(app)
    CORS(app) 
    
    @app.route('/')
    def home():
        
        return 'Welcome to Capstone!'

    return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)