from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='Website URL', widget=forms.URLInput(attrs={'class': 'form-control'}))
