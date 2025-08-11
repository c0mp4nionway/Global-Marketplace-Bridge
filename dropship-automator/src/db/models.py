from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ali_product_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    ebay_item_id = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    qty = Column(Integer, nullable=False)
    last_sync = Column(DateTime, default=datetime.utcnow)
    raw = Column(JSON, nullable=True)

class Price(Base):
    __tablename__ = 'prices'

    sku = Column(String, primary_key=True)
    price = Column(Float, nullable=False)

def init_db(db_url='sqlite:///dropship.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()