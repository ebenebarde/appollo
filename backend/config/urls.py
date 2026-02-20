from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Version 1
    # Wir kapseln die catalogue-URLs unter 'api/v1/'.
    # Das macht die API zukunftssicher.
    path('api/v1/', include('catalogue.urls')),
    path('api/v1/', include('reviews.urls')),
    path('api/v1/auth/', include('accounts.urls')),

    # Authentifizierungs-URLs (Login/Logout für die Browsable API)
    # Nützlich für Entwickler, um sich im Browser einzuloggen.
    path('api-auth/', include('rest_framework.urls')),
]
