from sqlalchemy import Column, ForeignKey, Integer, String, Table
from db.db import Base
from sqlalchemy.orm import relationship

# Association table between questions and quizes (many-to-many)
questions_quizes = Table(
    "questions_quizes",
    Base.metadata,
    Column("questions_id", ForeignKey("questions.id")),
    Column("quizes_id", ForeignKey("quizes.id")),
)


class Quiz(Base):
    __tablename__ = "quizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    children = relationship("Child", secondary=questions_quizes)
