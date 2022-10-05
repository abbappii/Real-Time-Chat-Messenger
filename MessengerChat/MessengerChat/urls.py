
from xml.dom.minidom import Document
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('chat.urls')),
    path('',include('account.urls')),
    path('', include('friend.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)