from fastapi import status


def test_register_user(client, email, nickname, username, password):
    url = f'/api/user/create'
    resp = client.request('POST',
                          url,
                          json={
                              'email': email,
                              'nickname': nickname,
                              'username': username,
                              'password': password
                          })
    assert resp.status_code == status.HTTP_204_NO_CONTENT


def test_login(client, email, nickname, username, password):
    register_url = f'/api/user/create'
    resp = client.request('POST',
                          register_url,
                          json={
                              'email': email,
                              'nickname': nickname,
                              'username': username,
                              'password': password
                          })
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    login_url = f'/api/user/login'

    resp = client.request('POST',
                          login_url,
                          json={
                              'email': email,
                              'password': password
                          })

    assert resp.status_code == status.HTTP_200_OK
    response_json = resp.json()
    assert type(response_json['access_token']) == str
