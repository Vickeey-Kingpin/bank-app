from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))
        
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator
        else:
            raise ValueError(_("An email is required"))
        if not first_name:
            raise(_("First Name is required"))
        if not last_name:
            raise(_("Last Name is required"))
        
        # create the above object in the model
        user=self.model(email=email,first_name=first_name,last_name=last_name,**extra_fields)
        user.set_password(password)
        # save the created object in the model
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        user= self.create_user(
            email, first_name, last_name, password, **extra_fields
        )
        user.save(using=self._db)
        return user

class UserTransactionManager(BaseUserManager):
    def create_user(self, email, amount,password, **extra_fields):
        user=self.model(email=email,amount=amount,password=password,**extra_fields)
        user.save(using=self._db)
        return user

