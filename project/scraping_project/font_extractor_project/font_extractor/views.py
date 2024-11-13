from django.shortcuts import render, redirect
from .forms import WebsiteForm
from .models import Website, FontSize
from bs4 import BeautifulSoup
import requests

def extract_font_sizes(url):
    font_sizes = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup.find_all(style=True):
            styles = element['style'].split(';')
            for prop in styles:
                if 'font-size' in prop:
                    value = prop.split(':')[1].strip()
                    font_sizes.add(value)
    except Exception as e:
        print("Error:", e)
    return font_sizes

def home(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            website, created = Website.objects.get_or_create(url=url)
            font_sizes = extract_font_sizes(url)
            print(font_sizes)
            
            for font_size in font_sizes:
                FontSize.objects.create(website=website, font_size=font_size)
            return redirect('font_extractor:font_sizes')
    else:
        form = WebsiteForm()
    return render(request, 'font_extractor/home.html', {'form': form})

def font_sizes(request):
    font_sizes = FontSize.objects.all()
    return render(request, 'font_extractor/font_sizes.html', {'font_sizes': font_sizes})
