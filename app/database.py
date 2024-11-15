from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from datetime import datetime

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True)
    preferences = Column(String)  # Comma-separated list of tokens (e.g., "BTC,ETH")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    tx_hash = Column(String, unique=True)
    symbol = Column(String)
    amount = Column(Float)
    amount_usd = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database Initialization
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
