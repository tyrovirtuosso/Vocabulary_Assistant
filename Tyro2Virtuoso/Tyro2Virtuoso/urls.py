from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Include allauth URLs for social authentication
    path("accounts/", include("allauth.urls")),
    path('accounts/', include('allauth.socialaccount.urls')),
    
    # Third Party app Urls
    path("__debug__/", include("debug_toolbar.urls")),
    
    # Custom App Urls
    path("", include("usersApp.urls")),
    path("polls/", include("polls.urls")),
    
]
