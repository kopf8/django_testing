from http import HTTPStatus

import pytest
from django.conf import settings
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, many_news, home_url):
    response = client.get(home_url)
    news_list = response.context['object_list']
    news_count = news_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, many_news, home_url, news):
    response = client.get(home_url)
    assert response.status_code == HTTPStatus.OK
    news_list = list(response.context['object_list'])
    sorted_list = sorted(news_list, key=lambda x: x.date, reverse=True)
    assert news_list == sorted_list


@pytest.mark.django_db
def test_comments_order(client, news, many_comments, detail_news_url, comment):
    response = client.get(detail_news_url)
    assert 'news' in response.context
    all_comments = [news.comment_set.all()]
    sorted_comments = sorted(
        all_comments,
        key=lambda x: comment.created,
        reverse=True
    )
    assert all_comments == sorted_comments


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_news_url):
    response = client.get(detail_news_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, detail_news_url):
    response = admin_client.get(detail_news_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
