from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_font_sizes, name='get_font_sizes'),
]
