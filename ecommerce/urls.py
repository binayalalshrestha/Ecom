from django.contrib import admin
from django.urls import path, include

# urls configuration for images
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('api.urls')),
    path('', include('store.urls')),
    path('randomObject', include('randomObject.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# urls configuration for images
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
