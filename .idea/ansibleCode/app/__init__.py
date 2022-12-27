from flask import Flask

wa_app = Flask(__name__)

# import the endpoint definitions from routes.py
from app import routes