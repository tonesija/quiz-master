import pytest

from db.quiz import Quiz
from db.question import Question


@pytest.fixture
def quiz_1_public():
    return {"name": "Quiz 1 public", "public": True}


@pytest.fixture
def quiz_2_public():
    return {"name": "Quiz 2 public", "public": True}


@pytest.fixture
def seed_public_quizes(
    fixture_db,
    seed_users,
    quiz_1_public,
    quiz_2_public,
    question_1_public,
    question_2_public,
):
    """Seeds the db with 2 users and 2 public quizes and 2 questions.

    Returns:
        (list[dict]): list of added quizes.
    """

    ids = seed_users
    quiz_1_db = Quiz(**quiz_1_public, user_id=ids[0])
    quiz_2_db = Quiz(**quiz_2_public, user_id=ids[1])
    question_1_db = Question(**question_1_public, user_id=ids[0])
    question_2_db = Question(**question_2_public, user_id=ids[1])

    quiz_1_db.questions.append(question_1_db)
    quiz_2_db.questions.append(question_2_db)

    fixture_db.add(quiz_1_db)
    fixture_db.add(quiz_2_db)
    fixture_db.commit()

    return [quiz_1_public, quiz_2_public]
