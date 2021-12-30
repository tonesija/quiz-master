from fastapi import status
from starlette.status import HTTP_200_OK


class TestPublicRouter:
    def test_get_public_questions(self, client, seed_public_questions):
        """Test the /questions public endpoint."""

        res = client.get("/questions")
        res_json = res.json()

        assert res.status_code == status.HTTP_200_OK
        assert len(res_json) == len(seed_public_questions)
