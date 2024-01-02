from flask import Flask
from app.config import Config

# class Config(object):
#     SECRET_KEY = 'secret-key'

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
