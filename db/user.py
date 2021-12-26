from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    quizes = relationship("Quiz")
    questions = relationship("Question")
