from django.test import TestCase
from book_catalog.forms import ChangeBookStatusForm

class ChangeBookStatusFormTest(TestCase):
    def test_form(self):
        """
        Test if form is correctly created
        """
        form = ChangeBookStatusForm()
        assert form.fields['status'].label == 'Status'
        assert form.fields['status'].required is True
        assert form.fields['status'].choices == [('r', 'Read'), ('i', 'Reading'), ('t', 'To read')]

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
        assert form.is_valid() is False
