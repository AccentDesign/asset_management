import uuid
import mock

from django.db import models
from django.urls import reverse
from simplemde.fields import SimpleMDEField

from assets.models import Note
from assets.models.note import NoteManager
from authentication.middleware.current_user import get_current_team
from authentication.models import Team, User
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(Note._default_manager, NoteManager))

    def test_queryset_filters_by_team(self):
        with mock.patch('assets.models.note.get_current_team', return_value=self.team1):
            qs = Note.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team1)

        with mock.patch('assets.models.note.get_current_team', return_value=self.team2):
            qs = Note.for_team.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().team, self.team2)

    def test_search(self):
        search_terms = ['Note', 'One']

        with mock.patch('assets.models.note.get_current_team', return_value=self.team1):
            # blank returns all results
            self.assertEqual(Note.for_team.search('').count(), 1)

            # found for team one when active
            for term in search_terms:
                self.assertEqual(Note.for_team.search(term).count(), 1)

        Note.objects.filter(team=self.team2).delete()

        with mock.patch('assets.models.note.get_current_team', return_value=self.team2):
            # not found for team two as not their note
            for term in search_terms:
                self.assertEqual(Note.for_team.search(term).count(), 0)


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = Note._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_title(self):
        field = Note._meta.get_field('title')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_content(self):
        field = Note._meta.get_field('content')
        self.assertModelField(field, SimpleMDEField, blank=True)

    def test_user(self):
        field = Note._meta.get_field('user')
        self.assertModelPKField(field, User, on_delete=models.CASCADE)
        self.assertFalse(field.editable)

    def test_created_on(self):
        field = Note._meta.get_field('created_on')
        self.assertModelField(field, models.DateTimeField, blank=True)
        self.assertFalse(field.editable)
        self.assertTrue(field.auto_now_add)

    def test_updated_on(self):
        field = Note._meta.get_field('updated_on')
        self.assertModelField(field, models.DateTimeField, blank=True)
        self.assertFalse(field.editable)
        self.assertTrue(field.auto_now)

    def test_team(self):
        field = Note._meta.get_field('team')
        self.assertModelPKField(field, Team, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_team)

    # properties

    def test_str(self):
        self.assertEqual(Note(title='Some Note').__str__(), 'Some Note')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            Note(pk=pk).get_absolute_url(),
            reverse('assets:note-update', kwargs={'pk': pk})
        )
