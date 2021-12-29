from sqlalchemy import Column, ForeignKey, Integer, String, Table
from db.db import Base
from sqlalchemy.orm import relationship

# Association table between users and groups (many-to-many)
users_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("group_id", ForeignKey("groups.id")),
)

# Association table between questions and groups (many-to-many)
questions_groups = Table(
    "questions_groups",
    Base.metadata,
    Column("question_id", ForeignKey("questions.id")),
    Column("group_id", ForeignKey("groups.id")),
)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("Users", secondary=users_groups)
    questions = relationship("Questions", secondary=questions_groups)
