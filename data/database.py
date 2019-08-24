from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from data.models import Base


engine = create_engine('sqlite:///email_db.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_database():
    Base.metadata.create_all(bind=engine)
    db_session.commit()
