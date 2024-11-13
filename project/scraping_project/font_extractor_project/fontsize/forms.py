# forms.py
from django import forms

class URLForm(forms.Form):
    url = forms.URLField(
        label='Enter URL',
        required=True,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.example.com'})
    )
