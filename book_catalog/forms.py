from django import forms
from .models import UserBookRelation

class ChangeBookStatusForm(forms.ModelForm):
    class Meta:
        model = UserBookRelation
        fields = ['status', 'read_date', 'reading_date']
        labels = {
            'status': 'Status',
            'read_date': 'Read date',
            'reading_date': 'Reading date'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = True
        self.fields['read_date'].required = False
        self.fields['reading_date'].required = False

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
