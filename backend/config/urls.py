"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.common.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/locations/', include('apps.locations.urls')),

    #TODO: Uncomment when ready
    path('api/v1/restaurants/', include('apps.restaurants.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/cart/', include('apps.cart.urls')),
    path('api/v1/delivery/', include('apps.delivery.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/ratings/', include('apps.ratings.urls')),
]
