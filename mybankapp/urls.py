from django.urls import path
from . import views
from . views import RegisterUserView, UserLoginView, UserFistDepositView, UserDepositView, UserWithdawView, UserBalanceView, UserTransferFundView

urlpatterns = [
    path('register_user/',RegisterUserView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('register_transaction/',UserFistDepositView.as_view()),
    path('deposit/',UserDepositView.as_view()),
    path('withdraw/',UserWithdawView.as_view()),
    path('transfer/funds',UserTransferFundView.as_view()),
    path('balance/',UserBalanceView.as_view()),
]