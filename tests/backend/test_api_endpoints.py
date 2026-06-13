import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from app import activities, app


@pytest.fixture(autouse=True)
def restore_activities():
    # Arrange
    original = copy.deepcopy(activities)
    yield
    # Cleanup
    activities.clear()
    activities.update(original)


def test_get_activities_returns_activity_catalog():
    # Arrange
    with TestClient(app) as client:
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        payload = response.json()
        assert "Chess Club" in payload
        assert payload["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_participant():
    # Arrange
    with TestClient(app) as client:
        email = "newstudent@mergington.edu"

        # Act
        response = client.post("/activities/Chess Club/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert email in activities["Chess Club"]["participants"]
        assert "signed up" in response.json()["message"].lower()


def test_unregister_from_activity_removes_participant():
    # Arrange
    with TestClient(app) as client:
        email = "michael@mergington.edu"

        # Act
        response = client.delete("/activities/Chess Club/unregister", params={"email": email})

        # Assert
        assert response.status_code == 200
        assert email not in activities["Chess Club"]["participants"]
        assert "removed" in response.json()["message"].lower()
