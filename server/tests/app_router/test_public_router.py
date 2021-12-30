from fastapi import status
from db.quiz import Quiz
from tests.conftest import test_db_session


class TestPublicRouter:
    def test_get_public_questions(self, client, seed_public_questions):
        """Test the /questions public endpoint."""

        res = client.get("/questions")
        res_json = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert len(res_json) == len(seed_public_questions)

    def test_get_public_quizes(self, client, seed_public_quizes):
        """Test the /quizes public endpoint."""

        res = client.get("/quizes")
        res_json = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert len(res_json) == len(seed_public_quizes)

    def test_get_specific_public_quiz(self, client, seed_public_quizes):
        """Test the /quizes/{quiz_id} endpoint."""

        with test_db_session() as db:
            quiz = db.query(Quiz).first()

        res = client.get(f"/quizes/{quiz.id}")
        res_json = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert res_json["name"] == quiz.name

        res = client.get(f"/quizes/{10000}")
        res_json = res.json()

        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in res_json["detail"]

    def test_get_specific_public_quiz_questions(self, client, seed_public_quizes):
        """Test the /quizes/{quiz_id}/questions endpoint."""

        with test_db_session() as db:
            quiz = db.query(Quiz).first()
            questions = quiz.questions

        res = client.get(f"/quizes/{quiz.id}/questions")
        res_json = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert len(res_json) == len(questions)
        assert res_json[0]["outer_text"] == questions[0].outer_text

        res = client.get(f"/quizes/{10000}")
        res_json = res.json()

        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in res_json["detail"]
