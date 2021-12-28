from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.sql.sqltypes import Boolean
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
    public = Column(Boolean, server_default="f")

    user_id = Column(Integer, ForeignKey("users.id"))

    children = relationship("Question", secondary=questions_quizes)
