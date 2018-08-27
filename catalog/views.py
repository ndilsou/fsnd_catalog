import os
import logging

import sqlalchemy.orm.exc as db_exc

from flask import Flask, render_template, abort

from catalog.application import app
from catalog.database import Session
from catalog import models

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.info("Views loaded")


@app.route("/")
@app.route("/catalog")
def index():
    categories = Session.query(models.Category).all()
    items = Session.query(models.Item).order_by(models.Item.timestamp.desc()).limit(10)
    return render_template("index.html", categories=categories, items=items)


@app.route("/catalog/<string:name>/items")
def category_view(name):
    try:
        category = Session.query(models.Category).filter_by(name=name).one()
    except db_exc.NoResultFound:
        logger.exception("Category not found: {}".format(name))
        abort(404)
    else:
        categories = Session.query(models.Category).all()
        return render_template("category.html", category=category, categories=categories)


@app.route("/catalog/<string:category_name>/<string:name>")
def item_view(category_name, name):
    try:
        item = Session.query(models.Item)\
            .filter(models.Item.name == name and models.Item.category == category_name)\
            .one()
    except db_exc.NoResultFound:
        logger.exception("Item not found: {}".format(name))
        abort(404)
    else:
        return render_template("item.html", item=item)


@app.route("/categories/add")
def category_add():
    pass


@app.route("/catalog/items/add")
def item_add():
    pass


@app.route("/catalog/<string:name>/delete")
def item_delete(name):
    pass


@app.route("/catalaog/<string:name>/edit")
def item_edit(name):
    pass

