import json
import subprocess
from django.shortcuts import render
from django.http import JsonResponse
from .forms import URLForm

def get_font_sizes(request):
    form = URLForm()
    font_sizes = {}
    font_sizes_data={}
    
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                # Run the Puppeteer script
                result = subprocess.run(
                    ['node', 'puppeteer_scripts/get_font_sizes.js', url],
                    capture_output=True,
                    text=True,
                    check=True
                )
                font_sizes_data = json.loads(result.stdout)
                
                # Extract font sizes for specific elements
                font_sizes['h1'] = font_sizes_data.get('h1', [])
                font_sizes['p'] = font_sizes_data.get('p', [])
                font_sizes['span'] = font_sizes_data.get('span', [])
            except subprocess.CalledProcessError as e:
                font_sizes = {'error': str(e)}
            except json.JSONDecodeError:
                font_sizes = {'error': 'Failed to parse JSON output from Puppeteer script'}
    
    return render(request, 'fontsize/get_font_sizes.html', {'form': form, 'font_sizes': font_sizes,'font_sizes_data': font_sizes_data})
