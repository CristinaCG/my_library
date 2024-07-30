from django.test import TestCase
from book_catalog.forms import ChangeBookStatusForm, SearchForm


class ChangeBookStatusFormTest(TestCase):
    """
    Test for ChangeBookStatusForm
    """
    def test_form(self):
        """
        Test if form is correctly created
        """
        form = ChangeBookStatusForm()
        assert form.fields['status'].label == 'Status'
        assert form.fields['status'].required is True
        assert form.fields['status'].choices == [('', '---------'),
                                                 ('r', 'Read'),
                                                 ('t', 'To read'),
                                                 ('i', 'Reading')]
        assert form.fields['read_date'].label == 'Read date'
        assert form.fields['read_date'].required is False
        assert form.fields['reading_date'].label == 'Reading date'
        assert form.fields['reading_date'].required is False

    def test_form_valid(self):
        """
        Test if form is valid
        """
        form = ChangeBookStatusForm(data={'status': 'r'})
        assert form.is_valid() is True

    def test_form_not_valid(self):
        """
        Test if form is valid
        """
        form = ChangeBookStatusForm(data={'status': 'w'})
        self.assertFalse(form.is_valid())
        msg = 'Select a valid choice. w is not one of the available choices.'
        self.assertEqual(form.errors, {'status': [msg]})

    def test_form_not_valid_empty(self):
        """
        Test if form is not valid
        """
        form = ChangeBookStatusForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'status': ['This field is required.']})

    def test_form_not_valid_empty_status(self):
        """
        Test if form is not valid
        """
        form = ChangeBookStatusForm(data={'status': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'status': ['This field is required.']})

class SearchTest(TestCase):
    """
    Test for SearchForm
    """
    def test_form(self):
        """
        Test if form is correctly created
        """
        form = SearchForm()
        assert form.fields['query'].label == 'Search'
        assert form.fields['query'].max_length == 100
        assert form.fields['query'].required is True

    def test_form_valid(self):
        """
        Test if form is valid
        """
        form = SearchForm(data={'query': 'test'})
        assert form.is_valid() is True

    def test_form_not_valid(self):
        """
        Test if form is not valid
        """
        form = SearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'query': ['This field is required.']})
