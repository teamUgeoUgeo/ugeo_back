from fastapi import status
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("test logger")


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


def test_search_user(client, email, nickname, username, password):
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

    search_url = f'/api/user/search'
    resp = client.request('GET', search_url + f'/{username}')

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == 1
    assert set(resp.json()[0].keys()) == {'username', 'nickname'}
