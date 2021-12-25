from fastapi import status
from starlette.status import HTTP_200_OK


class TestTmp:
    """Temporary class for testing."""

    def test_root(self, client):
        """Temporary test for the time being."""

        res = client.get("/")

        assert res.status_code == status.HTTP_200_OK
