from fastapi import status
from db.quiz import Quiz
from db.question import Question
from db.user import User
from tests.conftest import test_db_session


class TestQuizesRouter:
    def test_get_quizes(self, client, seed_quizes_to_you):
        """Test the "api//my/quizzes" endpoint."""

        res = client.get("api//my/quizzes")

        assert res.status_code == status.HTTP_200_OK

        res_json = res.json()

        assert len(seed_quizes_to_you) == len(res_json)
        assert seed_quizes_to_you[0]["name"] == res_json[0]["name"]

    def test_create_quiz(self, client, seed_quizes_to_you, quiz_2):
        """Test the "api//my/quizzes" POST endpoint."""

        with test_db_session() as db:
            num_quizes_before = db.query(Quiz).count()

        res = client.post("api//my/quizzes", json=quiz_2)

        assert res.status_code == status.HTTP_201_CREATED
        with test_db_session() as db:
            assert db.query(Quiz).count() == num_quizes_before + 1

    def test_get_one_quiz(self, client, quiz_1, seed_you):
        """Test the "api//my/quizzes/{quiz_id}" endpoint."""

        id = seed_you

        with test_db_session() as db:
            quiz_db = Quiz(**quiz_1, user_id=id)
            db.add(quiz_db)
            db.commit()
            quiz_id = quiz_db.id

        res = client.get(f"api//my/quizzes/{quiz_id}")
        res_json = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert quiz_1["name"] == res_json["name"]

        res = client.get("api//my/quizzes/10000")

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_update_quiz(self, client, seed_quizes_to_you, quiz_2):
        """Test the "api//my/quizzes/{quiz_id}" PUT endpoint."""

        with test_db_session() as db:
            quiz_before = db.query(Quiz).first()

        res = client.put(f"api//my/quizzes/{quiz_before.id}", json=quiz_2)

        assert res.status_code == status.HTTP_200_OK
        with test_db_session() as db:
            quiz_after = db.query(Quiz).first()
            assert quiz_after.name == quiz_2["name"]

        res = client.put(f"api//my/quizzes/10000", json=quiz_2)

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_quiz(self, client, seed_quizes_to_you):
        """Test the "api//my/quizzes/{quiz_id}" DELETE endpoint."""

        with test_db_session() as db:
            quiz_before = db.query(Quiz).first()
            num_quiz_before = db.query(Quiz).count()

        res = client.delete(f"api//my/quizzes/{quiz_before.id}")

        assert res.status_code == status.HTTP_200_OK
        with test_db_session() as db:
            assert db.query(Quiz).count() == num_quiz_before - 1

        res = client.delete(f"api//my/quizzes/10000")

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_get_one_quizes_questions(self, client, seed_quizes_to_you):
        """Test the "api//my/quizzes/{quiz_id}/questions" endpoint."""

        with test_db_session() as db:
            quiz_db = db.query(Quiz).first()
            questions = quiz_db.questions

        res = client.get(f"api//my/quizzes/{quiz_db.id}/questions")
        res_json = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert len(questions) == len(res_json)
        assert questions[0].outer_text in [
            question_dict["outer_text"] for question_dict in res_json
        ]

        res = client.get("api//my/quizzes/10000/questions")

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_add_question_to_quiz(self, client, seed_quizes_to_you, question_3):
        """Test the "api/my/quizzes/{quiz_id}/add-question" POST endpoint."""

        with test_db_session() as db:
            quiz_db = db.query(Quiz).first()

            user = db.query(User).first()

            question = Question(**question_3, user_id=user.id)
            db.add(question)
            db.commit()

            question_id = question.id
            num_questions_before = len(quiz_db.questions)

        res = client.post(
            f"api//my/quizzes/{quiz_db.id}/add-question",
            json={"question_id": question_id},
        )

        assert res.status_code == status.HTTP_200_OK
        with test_db_session() as db:
            quiz_db = db.query(Quiz).first()

            assert len(quiz_db.questions) == num_questions_before + 1

        res = client.post(
            "api/my/quizzes/10000/add-question", json={"question_id": question_id}
        )

        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_count_quizes(self, client, seed_quizes_to_you):
        """Test the "api/my/quizzes/{quiz_id}/questions/count" endpoint."""
        
        with test_db_session()as db:
            quiz_id = db.query(Quiz).one().id

        res = client.get(f"api/my/quizzes/{quiz_id}/questions/count")

        assert res.status_code == status.HTTP_200_OK
        with test_db_session() as db:
            assert res.json() == db.query(Question).count()
