import factory.fuzzy
from factory import Factory, Faker # type: ignore
from fastapi_zero.models import Todo, TodoState


class TodoFactory(Factory):
    class Meta:
        model = Todo

    title = Faker('text')
    description = Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
    }
