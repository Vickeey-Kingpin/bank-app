from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . managers import UserManager, UserTransactionManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=20, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=20, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name","last_name"]

    def __str__(self):
        return self.email
    
    objects = UserManager()
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class UserAccountNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    accno = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.user.first_name}-Account Number"
    
class UserAccount(models.Model):
    email = models.EmailField(null=True,max_length=100, unique=True)
    accno = models.CharField(unique=True,max_length=10,null=True)
    amount = models.FloatField(verbose_name=_("Balance($)"),null=True)
    password = models.CharField(max_length=20)

    objects = UserTransactionManager()

    def __str__(self):
        return f"Thank you {self.email} for choosing us"


