import os

from catalog.application import app
from config import Config
from catalog import database, views

if __name__ == '__main__':
    app.config.from_object(Config)
    database.init_db(app)
    app.run(host="0.0.0.0", port=5000)
