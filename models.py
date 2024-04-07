from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True)
    user_input = Column(String(10))
    execution_time = Column(Integer)
    is_valid_input = Column(Boolean)
    result = Column(Text)
    timestamp = Column(DateTime)

engine = create_engine(getenv('DATABASE_URL', 'postgresql://chatbot:chatbot@localhost:5432/chatbot'))
Session = sessionmaker(bind=engine)