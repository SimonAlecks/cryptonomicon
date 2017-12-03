from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database import Base

engine = create_engine('sqlite:////home/simon/PycharmProjects/cryptonomicon/database/database.sqlite3', echo=True)
Base.metadata.create_all(engine)
session = Session(engine)
session.commit()


