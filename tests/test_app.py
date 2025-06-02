from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}

#Exercício 01
def test_html_ola_mundo():
    client = TestClient(app)

    response = client.get('/olamundo')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá mundo! </h1>' in response.text
