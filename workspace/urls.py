from django.urls import path
from . import views
from .views import SaveWorkspaceAPIView, TranslateTextAPIView, TransliterateAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('workspace/', views.workspace_page, name='workspace_page'),
    path('api/workspace/save/', SaveWorkspaceAPIView.as_view(), name='workspace-save'),
    path('api/workspace/translate/', TranslateTextAPIView.as_view(), name='workspace-translate'),
    path('api/workspace/transliterate/', TransliterateAPIView.as_view(), name='workspace-transliterate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)