from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('pages.urls')),
    path('tickersymbols/', include('tickersymbols.urls')),
    path('tickersymbols/backtests/', include('backtests.urls')),
    path('admin/', admin.site.urls),
]
