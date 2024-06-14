import pytest
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, many_news, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, many_news, home_url, news):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, many_comments, detail_news_url, comment):
    response = client.get(detail_news_url)
    assert 'news' in response.context
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_news_url):
    response = client.get(detail_news_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, detail_news_url):
    response = admin_client.get(detail_news_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
