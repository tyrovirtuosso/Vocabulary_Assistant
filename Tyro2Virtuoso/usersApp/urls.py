from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home_view, name='home_view'),
]

if settings.DEBUG:
    # Don't do this in production!    
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

