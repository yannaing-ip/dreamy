from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('dreams.urls')),
    path('api/', include('feeds.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]



