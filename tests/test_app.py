from fastapi.testclient import TestClient

from src.app import app


def test_signup_duplicate_email_is_rejected():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"

    # Cleanup
    activity = client.get("/activities").json()[activity_name]
    if email in activity["participants"]:
        activity["participants"].remove(email)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "remove-me@example.com"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    activity = client.get("/activities").json()[activity_name]

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activity["participants"]
