from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from db.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    outer_text = Column(String(400), nullable=True, index=True)
    questions_per_slide = Column(Integer, default=0)
    public = Column(Boolean, server_default="f")
    img_url = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    subquestions = relationship("Subquestion")
