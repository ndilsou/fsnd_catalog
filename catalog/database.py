from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from .application import app
# from .config import Config

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base = declarative_base()
Base.query = Session.query_property()


def init_db(app):
    global Session
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    engine = create_engine(app.config["DATABASE"], convert_unicode=True)
    import catalog.models
    Session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        global Session
        Session.remove()

