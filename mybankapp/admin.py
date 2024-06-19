from django.contrib import admin
from . models import User, UserAccountNumber, UserAccount

# Register your models here.
admin.site.register(User)
admin.site.register(UserAccountNumber)

class useraccounts(admin.ModelAdmin):
    list_display = ['id','email','accno','amount']
    ordering = ['id']
admin.site.register(UserAccount,useraccounts)


