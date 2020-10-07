from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Mailer:
    def matched_mail(self, payer, receiver, email):
        message = render_to_string('mails/matched.html', {'payer':payer, 'receiver':receiver})
        subject = "You've been matched on Leverage Capital"
        to_mail = email
        raw_message = strip_tags(message)
        from_mail = 'Leverage capital <noreply@leveragecapital.com.ng>'
        try:
            mail.send_mail(subject, raw_message, from_mail, [to_mail], html_message=message)
        except Exception:
            pass