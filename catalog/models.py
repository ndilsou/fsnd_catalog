from catalog.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(150), unique=True)

    def __repr__(self):
        return "<User{{username={}}}>".format(self.username)
