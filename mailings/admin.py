from django.contrib import admin

from mailings.models import Mailing, Reporting


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'period', 'status')
    search_filter = ('name', 'status',)


@admin.register(Reporting)
class ReportingAdmin(admin.ModelAdmin):
    list_display = ('time_log', 'status', 'mailings')
    search_filter = ('status', 'mailings')
