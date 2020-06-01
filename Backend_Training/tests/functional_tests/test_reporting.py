from app.utils import status_codes
from datetime import datetime
import json
import re


def test_reporting(test_client):
    test_user_1_details = json.dumps(dict(email="farhan1ahmed@hotmail.com", password="test123"))
    response = test_client.post('/login', data=test_user_1_details, content_type='application/json')
    cookie = re.findall(r'cookie=(.*);', response.headers.get("Set-cookie"))
    if cookie: access_cookie = cookie[0]

    header = {'Authorization': f'Bearer {access_cookie}'}
    response = test_client.get('/reports/tasks_opened_week', headers=header)
    today = datetime.today().strftime('%A')
    json_response = json.loads(response.data)
    assert response.status_code == status_codes.OK
    for day in json_response:
        assert json_response.get(day) == (3 if day == today else 0)

    response = test_client.get('/reports/max_tasks_day', headers=header)
    assert response.status_code == status_codes.OK
    json_response = json.loads(response.data)
    today = datetime.today().date().strftime("%a, %d %b %Y %H:%M:%S GMT")
    assert json_response.get("date")[0] == today
    assert json_response.get("max_count") == 1

    response = test_client.get('/reports/late_tasks', headers=header)
    assert response.status_code == status_codes.OK
    assert json.loads(response.data).get("count") == 1

    response = test_client.get('/reports/avg_tasks_per_day', headers=header)
    assert response.status_code == status_codes.OK
    assert json.loads(response.data).get("avg_tasks") == 1.0

    response = test_client.get('/reports/tasks_count_breakdown', headers=header)
    assert response.status_code == status_codes.OK
    assert json.loads(response.data).get("completed_tasks") == 1
    assert json.loads(response.data).get("remaining_tasks") == 2
    assert json.loads(response.data).get("total_tasks") == 3

    response = test_client.get('/logout', headers=header)
    assert response.status_code == status_codes.OK
    assert b'{"message":"Logged Out successfully"}' in response.data