from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Table
from sqlalchemy import ForeignKey


Base = declarative_base()

class TokenHolders(Base):

    __tablename__ = 'tokenholders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime)
    Rank = Column(Integer)
    Address = Column(String)
    Quantity = Column(Float)
    Percentage = Column(Float)
    Currency = Column(String)

