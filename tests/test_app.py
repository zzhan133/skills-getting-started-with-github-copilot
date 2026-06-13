import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import activities, app


@pytest.fixture(autouse=True)
def restore_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_unregister_participant_from_activity():
    with TestClient(app) as client:
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 200
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert "removed" in response.json()["message"].lower()
