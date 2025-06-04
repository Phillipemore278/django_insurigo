
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='frontend')),
    path('account/', include('account.urls', namespace='account')),
    path('account/user/', include('customer.urls', namespace='customer')),
    path('captcha/', include('captcha.urls')),
]
