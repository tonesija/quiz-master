from sqlalchemy import Column, ForeignKey, Integer, String
from db.db import Base


class Quiz(Base):
    __tablename__ = "quizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
