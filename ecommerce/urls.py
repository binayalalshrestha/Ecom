from django.contrib import admin
from django.urls import path, include

# urls configuration for images
from django.conf.urls.static import static
from django.conf import settings

# for JWT 
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('api.urls')),

    path('', include('apiJWT.urls')),

    path('', include('NBA.urls')),
    
    path('', include('store.urls')),
    
    path('randomObject/', include('randomObject.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    # path('api/token/',TokenObtainPairView.as_view(),name='token_object_pair'),
    # path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]

# urls configuration for images
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
