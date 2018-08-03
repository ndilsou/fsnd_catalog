from flask import Flask, render_template
import os
import logging

from catalog.application import app
from catalog.database import Session
from catalog.models import User

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.info("Views loaded")


@app.route("/")
def index():
    logger.info("Getting Index")
    sess = Session()
    users = sess.query(User).all()
    logging.info(users)
    return render_template("index.html")
