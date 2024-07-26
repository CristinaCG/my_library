from django import forms
# from .models import UserBookRelation
from .models import Author, Book, BookSaga, UserBookRelation, Language


# class ChangeBookStatusForm(forms.Form):
#     STATUS_CHOICES = (
#         ('r', 'Read'),
#         ('i', 'Reading'),
#         ('t', 'To read'),
#     )
#     status = forms.ChoiceField(choices=STATUS_CHOICES, label="Status", required=True)

class ChangeBookStatusForm(forms.ModelForm):
    class Meta:
        model=UserBookRelation
        fields = ['status',  'read_date', 'reading_date']
    

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

# class UserBookRelationForm(forms.ModelForm):
#     class Meta:
#         model = UserBookRelation
#         fields = ['status', 'read_date', 'reading_date', 'rate', 'review']
#         widgets = {
#             'status': forms.Select(attrs={'class': 'form-select'}, 0),
#             'read_date': forms.DateInput(attrs={'class': 'form-control'}),
#             'reading_date': forms.DateInput(attrs={'class': 'form-control'}),
#             'rate': forms.NumberInput(attrs={'class': 'form-control'}),
#             'review': forms.Textarea(attrs={'class': 'form-control'}),
#         }