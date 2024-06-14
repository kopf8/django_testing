import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from django.test.client import Client

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def pk_news(news):
    return (news.pk,)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст',
    )
    return comment


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
