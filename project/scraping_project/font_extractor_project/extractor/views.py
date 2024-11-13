import time
from django.shortcuts import render
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from .forms import WebsiteForm

def extract_font_sizes(request):
    form = WebsiteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            url = form.cleaned_data['url']
            font_sizes = get_computed_font_sizes(url)
            if font_sizes:
                return render(request, 'extractor/font_sizes.html', {'font_sizes': font_sizes})
    return render(request, 'extractor/extract_font_sizes.html', {'form': form})

from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def get_computed_font_sizes(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    font_sizes = {}
    for element in driver.find_elements(By.TAG_NAME, "*"):  # Use By.TAG_NAME for finding elements
        font_size = element.value_of_css_property('font-size')
        if font_size:
            font_sizes[font_size] = font_sizes.get(font_size, 0) + 1

    driver.quit()
    return font_sizes