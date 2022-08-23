def test_add_employee(test_client, employees):
    for emp in employees:
        response = test_client.post("/cake/add_employee", json=emp)
        assert response.status_code == 200


def test_submit_preference(test_client, cake_preferences):
    for pref in cake_preferences:
        response = test_client.post("/cake/submit_preferences", json=pref)
        assert response.status_code == 200
