from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.models import Base
from app.config import Config

engine = create_engine(url=Config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def init_db():
    Base.metadata.create_all(bind=engine)

