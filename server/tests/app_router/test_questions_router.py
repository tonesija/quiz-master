from fastapi import status
from db.question import Question
from tests.conftest import test_db_session


class TestQuestionsRouter:
    def test_list_owned_questions_pagination(self, client, seed_20_questions_to_you):
        """Test the "/api/my/questions" endpoint with pagination."""

        offset = 5
        limit = 5
        res = client.get(f"api/my/questions?limit={limit}&offset={offset}")
        res_json_pagination = res.json()
        res = client.get("api/my/questions")
        res_json_all = res.json()

        assert limit == len(res_json_pagination)
        for question_paginated in res_json_pagination:
            assert question_paginated in res_json_all

    def test_delete_all_your_questions(self, client, seed_20_questions_to_you):
        """Test the "/api/my/questions" DELETE endpoint."""

        with test_db_session() as db:
            questions = db.query(Question).all()
            for question in questions:
                question_id = question.id
                res = client.delete(f"api/my/questions/{question_id}")

                assert res.status_code == status.HTTP_200_OK

            assert db.query(Question).count() == 0
