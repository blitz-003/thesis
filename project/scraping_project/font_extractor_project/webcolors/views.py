from django.shortcuts import render
from .models import Country, WebsiteColor

def index(request):
    countries = Country.objects.all()
    selected_country = request.GET.get('country')
    colors = []
    if selected_country:
        colors = WebsiteColor.objects.filter(country__name=selected_country)
    return render(request, 'webcolors/index.html', {'countries': countries, 'colors': colors})
