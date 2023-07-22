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


def test_article_crud(client, email, nickname, username, password, price,
                      article, article2):
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

    url = f'/api/article'
    resp = client.request(
        'POST',
        url,
        headers={'Authorization': f"Bearer {response_json['access_token']}"},
        json={
            'detail': article,
            'amount': price
        })

    assert resp.status_code == status.HTTP_201_CREATED
    print('create successful')

    assert {'article_id', 'created_at'} == set(resp.json())

    article_id = resp.json()['article_id']

    url = f'/api/article'
    resp = client.request(
        'PUT',
        url,
        headers={'Authorization': f"Bearer {response_json['access_token']}"},
        json={
            'detail': article,
            'amount': price,
            'article_id': article_id
        })

    assert resp.status_code == status.HTTP_204_NO_CONTENT
    print('edit successful')

    resp = client.request(
        'DELETE',
        url + f'/{article_id}',
        headers={'Authorization': f"Bearer {response_json['access_token']}"})

    assert resp.status_code == status.HTTP_204_NO_CONTENT
    print('delete successful')
