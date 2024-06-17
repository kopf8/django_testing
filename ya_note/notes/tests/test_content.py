from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()

NOTES_COUNT = 10
NOTES_LIST = reverse('notes:list')


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор1')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.other_user = User.objects.create(username='Автор2')
        cls.other_user_client = Client()
        cls.other_user_client.force_login(cls.other_user)
        cls.notes = [
            Note(
                author=cls.author,
                title=f'Заметка {index}',
                text='Текст',
                slug=f'mynote-{index}'
            )
            for index in range(NOTES_COUNT)
        ]
        Note.objects.bulk_create(cls.notes)
        cls.notes = list(Note.objects.filter(author=cls.author))
        cls.other_note = Note.objects.create(
            author=cls.other_user,
            title='Чужая заметка',
            text='Текст чужой заметки',
            slug='someones_note'
        )

    def test_note_in_object_list(self):
        response = self.author_client.get(NOTES_LIST)
        object_list = response.context['object_list']
        self.assertIn(self.notes[0], object_list)

    def test_other_user_notes_not_in_list(self):
        response = self.author_client.get(NOTES_LIST)
        object_list = response.context['object_list']
        self.assertNotIn(self.other_note, object_list)

    def test_note_add_page_contains_form(self):
        add_url = reverse('notes:add')
        response = self.author_client.get(add_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_edit_page_contains_form(self):
        edit_url = reverse('notes:edit', args=(self.notes[0].slug,))
        response = self.author_client.get(edit_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_notes_count(self):
        response = self.author_client.get(NOTES_LIST)
        notes_count = response.context['object_list'].count()
        self.assertEqual(notes_count, NOTES_COUNT)

    def test_notes_order(self):
        response = self.author_client.get(NOTES_LIST)
        object_list = response.context['object_list']
        all_notes = [note.id for note in object_list]
        sorted_dates = sorted(all_notes)
        self.assertEqual(all_notes, sorted_dates)
