from django import forms

class ChangeBookStatusForm(forms.Form):
    STATUS_CHOICES = (
        ('r', 'Read'),
        ('i', 'Reading'),
        ('t', 'To read'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Status", required=True)