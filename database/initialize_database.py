from database import Base, TokenHolders
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine('sqlite:////home/simon/PycharmProjects/cryptonomicon/database/database.sqlite3', echo=True)
Base.metadata.create_all(engine)
session = Session(engine)
session.commit()


