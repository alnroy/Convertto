from django.urls import path
from . import views
from .views import ConvertHandwritingAPIView, home, upload_and_convert

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_and_convert, name='upload'),
    path('api/convert/', ConvertHandwritingAPIView.as_view(), name='api-convert'),
    path('save_document/', views.save_document, name='save_document'),
    path('translate/', views.translate_text, name='translate_text'),
    path('transliterate/', views.transliterate_text, name='transliterate_text'),
]
