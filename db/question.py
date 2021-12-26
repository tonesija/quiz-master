from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    outer_text = Column(String(400), nullable=True, index=True)
    questions_per_slide = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey("users.id"))

    subquestions = relationship("Subquestion")
