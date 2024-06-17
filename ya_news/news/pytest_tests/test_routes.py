from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('pk_news')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None)
    )
)
def test_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'client, status',
    (
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_changing_comments_different_users(client, status, pk_comment, name):
    url = reverse(name, args=pk_comment)
    response = client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_redirect_for_anonymous_users(client, pk_comment, name):
    login_url = reverse('users:login')
    url = reverse(name, args=pk_comment)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
