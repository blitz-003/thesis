# palette_analyzer/views.py
from django.shortcuts import render
from .models import Website

def index(request):
    countries = ['America', 'China', 'India', 'Japan', 'South Korea']
    selected_country = request.GET.get('country', countries[0])
    websites = Website.objects.filter(country=selected_country)

    all_colors = []
    for website in websites:
        all_colors.extend(website.palette)

    return render(request, 'palette_analyzer/index.html', {
        'countries': countries,
        'selected_country': selected_country,
        'all_colors': all_colors,
    })
