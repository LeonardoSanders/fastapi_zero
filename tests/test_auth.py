from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_invalid_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'invalid', 'password': 'invalid'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect Email or Password!'}


def test_get_token_invalid_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'invalid'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect Email or Password!'}
