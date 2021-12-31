from fastapi import status

class TestQuizesRouter:

  def test_quizes(self, client, seed_quizes_to_you):
    """Test the "/my/quizes/" endpoint."""
    
    res = client.get("/my/quizes/")

    assert res.status_code == status.HTTP_200_OK

    res_json = res.json()

    assert len(seed_quizes_to_you) == len(res_json)
    assert seed_quizes_to_you[0]["name"] == res_json[0]["name"]