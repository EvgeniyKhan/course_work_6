from django.urls import path

from clients.views import (ClientCreateView, ClientDeleteView,
                           ClientDetailView, ClientListView, ClientUpdateView,
                           HomeView)

app_name = 'clients'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list/', ClientListView.as_view(), name='clients_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
]
