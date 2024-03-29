import uuid
import mock

from django.db import models
from django.urls import reverse

from assets.models import Contact
from assets.models.contact import ContactManager
from authentication.middleware.current_user import get_current_collection
from authentication.models import Collection
from tests.test_case import AppTestCase


class TestManager(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def test_default_manager(self):
        self.assertTrue(isinstance(Contact._default_manager, ContactManager))

    def test_queryset_filters_by_collection(self):
        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection1):
            qs = Contact.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection1)

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection2):
            qs = Contact.for_collection.get_queryset()
            self.assertEqual(qs.count(), 1)
            self.assertEqual(qs.get().collection, self.collection2)

    def test_search(self):
        search_terms = ['Contact', 'One']

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection1):
            # blank returns all results
            self.assertEqual(Contact.for_collection.search('').count(), 1)

            # found for collection one when active
            for term in search_terms:
                self.assertEqual(Contact.for_collection.search(term).count(), 1)

        Contact.objects.filter(collection=self.collection2).delete()

        with mock.patch('assets.models.mixins.get_current_collection', return_value=self.collection2):
            # not found for collection two as not their asset
            for term in search_terms:
                self.assertEqual(Contact.for_collection.search(term).count(), 0)


class TestModel(AppTestCase):

    # fields

    def test_id(self):
        field = Contact._meta.get_field('id')
        self.assertModelField(field, models.UUIDField, default=uuid.uuid4)
        self.assertFalse(field.editable)
        self.assertTrue(field.primary_key)

    def test_name(self):
        field = Contact._meta.get_field('name')
        self.assertModelField(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_email(self):
        field = Contact._meta.get_field('email')
        self.assertModelField(field, models.EmailField, blank=True)

    def test_phone_number(self):
        field = Contact._meta.get_field('phone_number')
        self.assertModelField(field, models.CharField, blank=True)
        self.assertEqual(field.max_length, 20)

    def test_mobile_number(self):
        field = Contact._meta.get_field('mobile_number')
        self.assertModelField(field, models.CharField, blank=True)
        self.assertEqual(field.max_length, 20)

    def test_address(self):
        field = Contact._meta.get_field('address')
        self.assertModelField(field, models.TextField, blank=True)

    def test_url(self):
        field = Contact._meta.get_field('url')
        self.assertModelField(field, models.URLField, blank=True)

    def test_notes(self):
        field = Contact._meta.get_field('notes')
        self.assertModelField(field, models.TextField, blank=True)

    def test_collection(self):
        field = Contact._meta.get_field('collection')
        self.assertModelPKField(field, Collection, on_delete=models.CASCADE)
        self.assertEqual(field.default, get_current_collection)

    # properties

    def test_str(self):
        self.assertEqual(Contact(name='Contact One').__str__(), 'Contact One')

    def test_absolute_url(self):
        pk = 'fe8aa6e1-93b9-480e-bc82-fcce14b707f6'
        self.assertEqual(
            Contact(pk=pk).get_absolute_url(),
            reverse('assets:contact-update', kwargs={'pk': pk})
        )

    def test_google_maps_link(self):
        contact = Contact(address='Norwich\nNR8 5FZ')
        expected_html = """
            <a href="https://www.google.co.uk/maps/search/Norwich+NR8+5FZ" target="_blank">Google Maps</a>
        """
        self.assertEqual(contact.google_maps_link, expected_html.strip())
