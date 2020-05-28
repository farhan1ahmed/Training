from app.utils import status_codes
import json
import re


def test_reporting(test_client):
    test_user_1_details = json.dumps(dict(email="farhan1ahmed@hotmail.com", password="test123"))
    response = test_client.post('/login', data=test_user_1_details, content_type='application/json')
    cookie = re.findall(r'cookie=(.*);', response.headers.get("Set-cookie"))
    if cookie: access_cookie = cookie[0]

    header = {'Authorization': f'Bearer {access_cookie}'}
    response = test_client.get('/reports/tasks_opened_week', headers=header)
    days = [b"Monday", b"Tuesday", b"Wednesday", b"Thursday", b"Friday", b"Saturday", b"Sunday"]
    assert response.status_code == status_codes.OK
    for day in days:
        assert day in response.data

    response = test_client.get('/reports/max_tasks_day', headers=header)
    assert response.status_code == status_codes.OK
    assert b'date' in response.data
    assert b'max_count' in response.data

    response = test_client.get('/reports/late_tasks', headers=header)
    assert response.status_code == status_codes.OK
    assert b'count' in response.data

    response = test_client.get('/reports/avg_tasks_per_day', headers=header)
    assert response.status_code == status_codes.OK
    assert b'avg_tasks' in response.data

    response = test_client.get('/reports/tasks_count_breakdown', headers=header)
    assert response.status_code == status_codes.OK
    assert b'completed_tasks' in response.data
    assert b'remaining_tasks' in response.data
    assert b'total_tasks' in response.data

    response = test_client.get('/logout', headers=header)
    assert response.status_code == status_codes.OK
    assert b'{"message":"Logged Out successfully"}' in response.data