from django.contrib import admin

from letters.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('letter_subject', 'letter_body')
    search_fields = ('letter_subject',)
