from django.core import mail

from accounts.tasks import send_welcome_email_task


def test_mail_is_sent():
    send_welcome_email_task(to='what@ev.er')
    assert len(mail.outbox) == 1
