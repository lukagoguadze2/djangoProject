from django import forms


class SearchCategory(forms.Form):
    q = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control p-3',
                'placeholder': 'Keywords'
            }
        )
    )