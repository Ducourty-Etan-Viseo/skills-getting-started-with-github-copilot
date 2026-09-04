from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_duplicate_email_is_rejected():
    activity_name = "Chess Club"
    email = "student@example.com"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"

    # cleanup for subsequent tests
    activity = client.get("/activities").json()[activity_name]
    if email in activity["participants"]:
        activity["participants"].remove(email)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "remove-me@example.com"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]
