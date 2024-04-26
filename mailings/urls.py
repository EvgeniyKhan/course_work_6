from django.urls import path

from mailings.views import (MailingCreateView, MailingDeleteView,
                            MailingDetailView, MailingListView,
                            MailingUpdateView, ReportingListView,
                            toggle_activity)

urlpatterns = [
    path('create/', MailingCreateView.as_view(), name='create_mailings'),
    path('list/', MailingListView.as_view(), name='mailings_list'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='update_mailings'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailings'),
    path('view/<int:pk>/', MailingDetailView.as_view(), name='view_mailings'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
    path('list_report/', ReportingListView.as_view(), name='report_list'),


]
