from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_security.models import sqla

engine = create_engine('sqlite:///test.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# class Base(DeclarativeBase):
    # pass

# db = SQLAlchemy(model_class=Base)
db = declarative_base()
sqla.FsModels.set_db_info(base_model=db)

def init_db():
    import app.models
    db.metadata.create_all(bind=engine)