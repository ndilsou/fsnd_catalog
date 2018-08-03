from sqlalchemy.orm import relationship

from catalog.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), unique=True)

    def __repr__(self):
        return "<User{{username={}}}>".format(self.username)


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(500))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship(User)

    def __repr__(self):
        return "<User{{name={name}}, owner={owner}})>".format(name=self.name, owner=self.owner.username)
