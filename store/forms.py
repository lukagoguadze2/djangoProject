from django import forms
from urllib3 import request


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control p-3',
                'placeholder': 'Keywords'
            }
        ),
        required=False
    )

    rangeInput = forms.IntegerField(required=False, min_value=-1)
    tag = forms.IntegerField(required=False, min_value=0)
    sort = forms.IntegerField(required=False, min_value=0)
