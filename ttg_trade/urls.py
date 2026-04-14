from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('trade/', include('ecommerce.urls')),
    path('forex/', include('forex.urls')),
    path('insurance/', include('insurance.urls')),
    path('coffee/', include('coffee.urls')),
    path('training/', include('training.urls')),
    path('notifications/', include('notifications.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
