from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client, detail_news_url, form_data
):
    client.post(detail_news_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, author, detail_news_url, news,
                                 form_data, comment):
    response = author_client.post(detail_news_url, data=form_data)
    assertRedirects(response, f'{detail_news_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 2
    comment = Comment.objects.last()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_news_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_news_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, delete_comment_url, detail_news_url
):
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, f'{detail_news_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, delete_comment_url
):
    response = not_author_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
    author_client, form_data, comment, edit_comment_url, detail_news_url
):
    response = author_client.post(edit_comment_url, data=form_data)
    assertRedirects(response, f'{detail_news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == 'Новый текст'


def test_user_cant_edit_comment_of_another_user(
    not_author_client, form_data, comment, edit_comment_url
):
    response = not_author_client.post(edit_comment_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст'
