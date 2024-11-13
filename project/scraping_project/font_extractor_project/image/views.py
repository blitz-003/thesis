from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
import numpy as np

def capture_screenshot(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    image = Image.open(io.BytesIO(screenshot))
    return image

def reduce_colors(image, num_colors=10):
    quantized_image = image.quantize(colors=num_colors)
    return quantized_image

def calculate_color_percentages(image):
    image = image.convert('RGB')
    np_image = np.array(image)
    
    pixels = np_image.reshape(-1, 3)
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    total_pixels = np_image.shape[0] * np_image.shape[1]
    percentages = (counts / total_pixels) * 100
    
    color_percentages = dict(zip(map(tuple, unique_colors), percentages))
    return color_percentages

def analyze_image(request):
    url = request.GET.get('url', '')
    if not url:
        return JsonResponse({'error': 'URL parameter is required'}, status=400)

    image = capture_screenshot(url)
    num_colors = 10
    quantized_image = reduce_colors(image, num_colors)
    color_percentages = calculate_color_percentages(quantized_image)

    # Prepare data for Chart.js
    labels = [f'RGB{color}' for color in color_percentages.keys()]
    data = list(color_percentages.values())
    colors = [f'rgb{color}' for color in color_percentages.keys()]

    context = {
        'labels': labels,
        'data': data,
        'colors': colors,
        'url': url
    }

    return render(request, 'image/chart.html', context)

def analyze_image_form(request):
    return render(request, 'image/form.html')
