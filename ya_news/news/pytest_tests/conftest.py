from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def pk_news(news):
    return (news.pk,)


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст',
    )


@pytest.fixture
def pk_comment(comment):
    return (comment.pk,)


@pytest.fixture
def many_news():
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def many_comments(author, news):
    all_comments = [
        Comment(
            text='Tекст',
            news=news,
            author=author,
            created=timezone.now() + timedelta(days=index)
        )
        for index in range(2)
    ]
    Comment.objects.bulk_create(all_comments)


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def delete_comment_url(pk_comment):
    return reverse('news:delete', args=pk_comment)


@pytest.fixture
def edit_comment_url(pk_comment):
    return reverse('news:edit', args=pk_comment)


@pytest.fixture
def detail_news_url(pk_news):
    return reverse('news:detail', args=pk_news)
