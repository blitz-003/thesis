import os
import io
import base64
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from django.shortcuts import render
from .forms import URLForm
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            screenshot_path = capture_screenshot(url)
            colors = analyze_colors(screenshot_path)
            pie_chart = create_pie_chart(colors)
            pie_chart_base64 = base64.b64encode(pie_chart.getvalue()).decode()
            return render(request, 'main/result.html', {'chart': pie_chart_base64})
    else:
        form = URLForm()
    return render(request, 'main/index.html', {'form': form})

def capture_screenshot(url):
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        os.makedirs(media_root)

    screenshot_path = os.path.join(media_root, 'screenshot.png')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1280, 1024)
    driver.get(url)
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path

def analyze_colors(image_path):
    image = Image.open(image_path)
    image = image.resize((100, 100))
    image = image.convert('RGB')
    colors = image.getcolors(10000)
    color_count = Counter({color: count for count, color in colors})
    return color_count.most_common(10)

def create_pie_chart(colors):
    fig, ax = plt.subplots()
    labels = [f'#{r:02x}{g:02x}{b:02x}' for ((r, g, b), count) in colors]
    sizes = [count for ((r, g, b), count) in colors]
    color_hex = [f'#{r:02x}{g:02x}{b:02x}' for ((r, g, b), count) in colors]
    ax.pie(sizes, labels=labels, colors=color_hex, autopct='%1.1f%%')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf
