from django import forms
from .models import UserBookRelation

class ChangeBookStatusForm(forms.Form):
    STATUS_CHOICES = (
        ('r', 'Read'),
        ('i', 'Reading'),
        ('t', 'To read'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Status", required=True)
