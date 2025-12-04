from django.urls import path
from . import views

urlpatterns = [
    path('locations/', views.AddressListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', views.AddressDetailView.as_view(), name='location-detail'),
]