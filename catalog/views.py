import os
import logging
from contextlib import contextmanager

import sqlalchemy.orm.exc as db_exc

from flask import Flask, render_template, abort, request, redirect, url_for

from catalog.application import app
from catalog.database import Session
from catalog import models

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.info("Views loaded")


@contextmanager
def abort_if_raised(error_code, exc=Exception, msg="Request failed."):
    try:
        yield
    except exc:
        logger.exception(msg)
        abort(error_code)


@app.route("/")
@app.route("/catalog")
def index():
    categories = Session.query(models.Category).all()
    items = Session.query(models.Item).order_by(models.Item.timestamp.desc()).limit(10)
    return render_template("index.html", categories=categories, items=items)


@app.route("/catalog/<string:name>/items")
def category_view(name):
    with abort_if_raised(404, exc=db_exc.NoResultFound, msg="Category not found: {}".format(name)):
        category = Session.query(models.Category).filter_by(name=name).one()

    categories = Session.query(models.Category).all()
    return render_template("category.html", category=category, categories=categories)


@app.route("/catalog/<string:category_name>/<string:name>")
def item_view(category_name, name):
    with abort_if_raised(404, exc=db_exc.NoResultFound, msg="Item not found: {}".format(name)):
        item = Session.query(models.Item)\
            .filter(models.Item.name == name and models.Item.category == category_name)\
            .one()

    return render_template("item.html", item=item)


@app.route("/categories/add", methods=["GET", "POST"])
def category_add():
    pass


@app.route("/catalog/items/add", methods=["GET", "POST"])
def item_add():
    if request.method == "GET":
        categories = Session.query(models.Category).all()
        return render_template("item_add.html", categories=categories)

    elif request.method == "POST":
        logger.debug(request.form)
        return redirect(url_for("index"), 303)


@app.route("/catalog/<string:name>/delete", methods=["GET", "POST"])
def item_delete(name):
    with abort_if_raised(404, db_exc.NoResultFound):
        item = Session.query(models.Item).filter_by(name=name).one()

    if request.method == "GET":
        return render_template("item_delete.html", item=item)

    elif request.method == "POST":
        raise NotImplementedError("Method not supported")


@app.route("/catalog/<string:name>/edit", methods=["GET", "POST"])
def item_edit(name):
    with abort_if_raised(404, db_exc.NoResultFound):
        item = Session.query(models.Item).filter_by(name=name).one()

    if request.method == "GET":
        categories = Session.query(models.Category).all()
        return render_template("item_edit.html", item=item, categories=categories)

    elif request.method == "POST":
        raise NotImplementedError("Method not supported")

