from fastapi import status
from db.question import Question
from db.subquestion import Subquestion
from tests.conftest import test_db_session


class TestSubquestionsRouter:
    def test_add_subquestion(self, client, seed_questions_to_you, subquestion_1):
        """Test the "/api/my/questions/{question_id}/subquestions" POST endpoint."""

        N = 3

        with test_db_session() as db:
            question = db.query(Question).first()

        for i in range(N):
            res = client.post(
                f"/api/my/questions/{question.id}/subquestions", json=subquestion_1
            )

        assert res.status_code == status.HTTP_200_OK

        with test_db_session() as db:
            question_after = db.query(Question).filter(Question.id == question.id).one()
            assert question_after.subquestions[0].text == subquestion_1["text"]
            assert question_after.subquestions[0].answer == subquestion_1["answer"]
            assert question_after.subquestions[0].img_url == subquestion_1["img_url"]
            assert len(question_after.subquestions) == N

    def test_add_subquestion_unowned_question(
        self, client, seed_you, subquestion_1, seed_questions, question_1
    ):
        """Test the "/api/my/questions/{question_id}/subquestions" POST endpoint with an unowned question."""

        id = seed_you

        with test_db_session() as db:
            question_owned = Question(**question_1, user_id=id)
            db.add(question_owned)
            db.commit()
            question_unowned = db.query(Question).filter(Question.user_id != id).first()
            question_owned = db.query(Question).filter(Question.user_id == id).first()
            num_subquestions_before = db.query(Subquestion).count()

        res = client.post(
            f"/api/my/questions/{question_unowned.id}/subquestions", json=subquestion_1
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

        res = client.post(
            f"/api/my/questions/{question_owned.id}/subquestions", json=subquestion_1
        )
        assert res.status_code == status.HTTP_200_OK
        with test_db_session() as db:
            assert db.query(Subquestion).count() == num_subquestions_before + 1
