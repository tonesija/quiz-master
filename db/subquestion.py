from sqlalchemy import Column, Integer, String, ForeignKey
from db.db import Base


class Subquestion(Base):
    __tablename__ = "subquestions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)
    answer = Column(String(255), index=True)
    img_url = Column(String(255), nullable=True)

    question_id = Column(Integer, ForeignKey("questions.id"))
