from django.urls import path
from .views import extract_font_sizes

urlpatterns = [
    path('', extract_font_sizes, name='extract_font_sizes')

]
