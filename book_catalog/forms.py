from django import forms
# from .models import UserBookRelation
from .models import Author, Book, BookSaga, UserBookRelation, Language

class ChangeBookStatusForm(forms.ModelForm):
    class Meta:
        model=UserBookRelation
        fields = ['status',  'read_date', 'reading_date']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
