from django import forms

class WebsiteForm(forms.Form):
    url = forms.URLField(label='Website URL')
