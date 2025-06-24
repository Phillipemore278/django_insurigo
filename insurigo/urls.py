
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),
    path('account/', include('account.urls', namespace='account')),
    path('account/user/', include('customer.urls', namespace='customer')),
    path('account/car-insurance/', include('car_insurance.urls', namespace='car_insurance')),
    path('account/payments/', include('payments.urls', namespace='payments')),
    path('account/health_insurance/', include('health_insurance.urls', namespace='health_insurance')),
    path('account/claims/', include('claims.urls', namespace='claims')),
    path('api/', include('quote.urls', namespace='quote')),
    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
