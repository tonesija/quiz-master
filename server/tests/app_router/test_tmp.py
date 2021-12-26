from fastapi import status
import pytest


class TestTmp:
    """Temporary class for testing."""

    @pytest.skip
    def test_tmp(self, client):
        """Temporary test for the time being."""

        res = client.get("/posts")

        assert res.status_code == status.HTTP_200_OK
