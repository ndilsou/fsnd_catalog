import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from catalog.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), unique=True)

    def __repr__(self):
        return "<User{{username={}}}>".format(self.username)

    def to_dict(self):
        return {
            "username": self.username
        }


class Category(Base):
    _dict_keys = ["name", "description"]

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship(User)
    items = relationship("Item", backref="items")

    def __repr__(self):
        return "<Category{{name={name}, owner={owner}}}>".format(name=self.name, owner=self.owner.username)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description

        }


class Item(Base):
    _dict_keys = ["name", "description", "category_id"]
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category)

    def __repr__(self):
        return "<Item{{name={name}, category={category}}}>".format(name=self.name, category=self.category.name)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.name
        }
