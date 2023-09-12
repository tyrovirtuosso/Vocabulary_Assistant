from django.contrib import admin
from django.urls import path, include

import allauth.account.urls
urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Include allauth URLs for social authentication
    path("accounts/", include("allauth.urls")),
    path('accounts/', include('allauth.socialaccount.urls')),
    
    path("", include("authenticationApp.urls")),
    
    
]
