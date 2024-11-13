from django.urls import path
from .views import analyze_image, analyze_image_form

urlpatterns = [
    path('', analyze_image_form, name='analyze_image_form'),
    path('analyze/', analyze_image, name='analyze_image'),
]
