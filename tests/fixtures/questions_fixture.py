import pytest
from db.question import Question


@pytest.fixture
def question_1_public():
    return {
        "outer_text": "Question 1 public outer text",
        "questions_per_slide": 1,
        "public": True,
    }


@pytest.fixture
def question_2_public():
    return {
        "outer_text": "Question 2 public outer text",
        "questions_per_slide": 1,
        "public": True,
    }


@pytest.fixture
def question_1():
    return {
        "outer_text": "Question 1 outer text",
        "questions_per_slide": 1,
    }


@pytest.fixture
def question_2():
    return {
        "outer_text": "Question 2 outer text",
        "questions_per_slide": 1,
    }


@pytest.fixture
def question_3():
    return {
        "outer_text": "Question 3 outer text",
        "questions_per_slide": 1,
    }


@pytest.fixture
def seed_public_questions(fixture_db, seed_users, question_1_public, question_2_public):
    """Seeds the db with 2 users and 2 public questions.

    Returns:
        (list[dict]): list of added questions.
    """

    ids = seed_users
    question_1_db = Question(**question_1_public, user_id=ids[0])
    question_2_db = Question(**question_2_public, user_id=ids[1])

    fixture_db.add(question_1_db)
    fixture_db.add(question_2_db)
    fixture_db.commit()

    return [question_1_public, question_2_public]
