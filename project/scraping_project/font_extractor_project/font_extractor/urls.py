from django.urls import path
from . import views

app_name = 'font_extractor'

urlpatterns = [
    path('', views.home, name='home'),
    path('font-sizes/', views.font_sizes, name='font_sizes'),
]
