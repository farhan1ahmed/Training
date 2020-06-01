from app.utils import status_codes
import json


def test_login_user(test_client):
    test_user_1_details = json.dumps(dict(email="farhan1ahmed@hotmail.com", password="test123"))
    response = test_client.post('/login', data=test_user_1_details, content_type='application/json')
    assert b'{"message": "Success"}' in response.data
    assert response.status_code == status_codes.OK
    assert 'access_token_cookie' in response.headers.get("Set-Cookie")

    


