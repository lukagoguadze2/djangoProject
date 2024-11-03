from django import forms


class EmailForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'w-100 form-control border-0 py-3 mb-4',
                'placeholder': 'Your Name',
            }
        )

    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'w-100 form-control border-0 py-3 mb-4',
                'placeholder': 'Enter Your Email',
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'w-100 form-control border-0 mb-4',
                'rows': 5,
                'cols': 10,
                'placeholder': 'Your Message',
            }
        )
    )
