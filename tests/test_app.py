from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


# Exercício 01
# def test_html_ola_mundo(client):
#     response = client.get('/olamundo')

#     assert response.status_code == HTTPStatus.OK
#     assert '<h1> Olá mundo! </h1>' in response.text
