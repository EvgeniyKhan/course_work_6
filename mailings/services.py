import smtplib
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from mailings.models import Mailing, Reporting


def send_mailings():
    current_time = timezone.localtime(timezone.now())
    mailings = Mailing.objects.all().exclude(status=Mailing.STATUS_DONE)
    for mailing in mailings:
        try:
            if mailing.end_time < current_time:
                mailing.status = Mailing.STATUS_DONE
                mailing.save()
                continue
            if mailing.start_time <= current_time < mailing.end_time:
                email_list = [client.client_email for client in mailing.clients.all()]
                server_response = send_mail(
                    subject=mailing.message.letter_subject,
                    message=mailing.message.letter_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=email_list,
                    fail_silently=False
                )
                Reporting.objects.create(status=server_response, mailings=mailing)
                if mailing.period == 'daily':
                    next_mailing_time = current_time + timedelta(days=1)
                elif mailing.period == 'weekly':
                    next_mailing_time = current_time + timedelta(weeks=1)
                else:
                    next_mailing_time = current_time + relativedelta(months=1)
                mailing.status = Mailing.STATUS_CREATED
                mailing.start_time = next_mailing_time
                mailing.save()
        except smtplib.SMTPException:
            Reporting.objects.create(status=False, mailings=mailings)


def get_cache_for_mailings():
    if settings.CACHES_ENABLED:
        key = "mailings_count"
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_for_active_mailings():
    if settings.CACHES_ENABLED:
        key = "active_mailings_count"
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = (
                Mailing.objects.filter(is_active=True).count())
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_active=True).count()
    return active_mailings_count
