
def test_new_user(make_new_user):
    username = "test_user"
    email = "test_user@gmail.com"
    password = "test123"
    assert make_new_user.username == username
    assert make_new_user.password != password
    assert make_new_user.email == email
