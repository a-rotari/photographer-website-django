from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import redirect, render



def send_email(request, subject, message, from_email, recipient_list):
    user = request.user

    # Render the HTML email template using a context
    context = {
        'user': user,
        'subject': subject,
        'message': message,
    }
    html_message = render_to_string('email_template.html', context)

    # Create a plain text version of the email content
    plain_message = strip_tags(html_message)

    # Send the email using EmailMultiAlternatives
    from_email = None  # Set your sender email address
    to_email = recipient_list
    msg = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
    # msg.attach_alternative(html_message, "text/html")
    msg.send()

    return