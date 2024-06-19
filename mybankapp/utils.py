import random
from . models import User, UserAccountNumber, UserAccount
from django.conf import settings
from django.core.mail import EmailMessage


def generate_accNo():
    acc_no = ""
    for i in range(10):
        acc_no += str(random.randint(0,9))
    return acc_no

def send_user_accno(email):
    Subject = "Bank Account Number"
    accno = generate_accNo()
    print(accno)
    user = User.objects.get(email=email)
    message = f"Hello {user.first_name} thank you for choosing to bank with us \nWe welcome you so much!!\nYour Account number is {accno}(Do not share with anyone)"
    email_sender = settings.DEFAULT_FROM_EMAIL

    UserAccountNumber.objects.create(user=user, accno=accno)

    send_email = EmailMessage(subject=Subject, body=message, from_email=email_sender, to=[email])
    send_email.send(fail_silently=True)






