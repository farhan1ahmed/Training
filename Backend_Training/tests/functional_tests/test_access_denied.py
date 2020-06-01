from app.utils import status_codes
import json


def test_access_denied(test_client):
    task_details = json.dumps(dict(Title="Sample Task", Description="Sample", DueDate="2020-07-01"))
    response = test_client.post('/create', data=task_details, content_type='application/json')
    assert response.status_code == status_codes.UNAUTHORIZED