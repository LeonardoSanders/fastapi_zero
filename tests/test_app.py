from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


# def test_update_user_error(client, user):
#     response = client.put(
#         '/users/666',
#         json={
#             'username': 'bla',
#             'email': 'bla@example.com',
#             'password': 'bla123',
#         },
#     )

#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'User Not Found!'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'user deleted'}


# def test_delete_user_error(client, user):
#     response = client.delete('/users/-1')

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User Not Found!'}


def test_upgrade_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_get_user_id(client):
    client.post(
        '/users',
        json={
            'username': 'example',
            'email': 'example@example.com',
            'password': 'secret',
        },
    )

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'example',
        'email': 'example@example.com',
        'id': 1,
    }


def test_get_user_id_error(client):
    response = client.get('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'USER not found!'}


# Exercício 01
# def test_html_ola_mundo(client):
#     response = client.get('/olamundo')

#     assert response.status_code == HTTPStatus.OK
#     assert '<h1> Olá mundo! </h1>' in response.text
