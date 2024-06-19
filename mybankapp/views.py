from rest_framework.generics import GenericAPIView
from .serializer import UserRegistrationSerializer,UserLoginSerializer,UserFirstDepositSerializer,UserDepositSerializer,UserWithdawalSerializer,UserBalanceSerializer, UserTransferFundSerializer
from rest_framework.response import Response
from rest_framework import status
from . utils import send_user_accno
from . models import User, UserAccount, UserAccountNumber
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password


# Create your views here.
class RegisterUserView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_user_accno(user['email'])
            return Response({
                'data':user,
                'message': f"Thank you {user['first_name']},for signing up,An email with your account number has been sent to {user['email']}"
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def  post(self, request):
        # getting the user inputs
        email = request.data.get('email')
        password = request.data.get('password')

        # retrive user from the DB
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(_("The user does not exist"))
        
        if check_password(password, user.password):
            return Response({f"{user.email}, your account is created successifully. Please pay $500 in order to unlock your transactions and transact with us. Thank you!!"})
        else:
            return Response(_("Wrong Password"))

class UserFistDepositView(GenericAPIView):
    serializer_class = UserFirstDepositSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        accno = request.data.get('accno')

        # retrive user from the DB
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({f"You are not registered on our bank, Register first in order to access our transactions"})
        
        try:
            UserAccountNumber.objects.get(accno=accno)
        except UserAccountNumber.DoesNotExist:
            return Response(f"Account Number Do not match")
        
        if check_password(password, user.password):
            user_data = request.data
            serializer = self.serializer_class(data=user_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data':serializer.data,
                    'message': f'Thank you for your first deposit,you can now transact with us'
                },status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(_("Wrong Password"))
        
class UserDepositView(GenericAPIView):
    serializer_class = UserDepositSerializer

    def put(self, request):
        accno = request.data.get('accno')
        password = request.data.get('password')

        # retrive user from the DB
        try:
            user = UserAccount.objects.get(accno=accno)
        except UserAccount.DoesNotExist:
            return Response({f"Account Number does not exist. You cannot transact with us at the moment. Pay $500 to unlock your transactions"})
        
        if password == user.password:
            serializer = self.serializer_class(user,data=request.data)
            if serializer.is_valid():
                serializer.save
                return Response({f"Thank you {user.email}. Deposit was successiful. You can check your balance."})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(_("Wrong Password"))
        
class UserWithdawView(GenericAPIView):
    serializer_class = UserWithdawalSerializer

    def put(self, request):
        accno = request.data.get('accno')
        password = request.data.get('password')

        # retrive user from the DB
        try:
            user = UserAccount.objects.get(accno=accno)
        except UserAccount.DoesNotExist:
            return Response({f"Account Number does not exist. You cannot transact with us at the moment. Pay $500 to unlock your transactions."})
        
        if password == user.password:
            serializer = self.serializer_class(user,data=request.data)
            if serializer.is_valid():
                serializer.save
                return Response({f"Thank you {user.email}. Withdrawal was successiful. Check your balance."})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(_("Wrong Password"))
        
class UserBalanceView(GenericAPIView):
    serializer_class = UserBalanceSerializer

    def post(self, request):
        accno = request.data.get('accno')
        password = request.data.get('password')

        # retrive user from the DB
        try:
            user = UserAccount.objects.get(accno=accno)
        except UserAccount.DoesNotExist:
            return Response({f"Balance not found. Email don't exist"})
        
        if password == user.password:
            return Response({f"Thank you {user.email}. Your balance is {user.amount}."})

        else:
            return Response(_("Wrong Password"))

class UserTransferFundView(GenericAPIView):
    serializer_class = UserTransferFundSerializer

    def put(self, request):
        accno = request.data.get('accno')
        password = request.data.get('password')
        amount = request.data.get('amount')
        # receiver_accno = request.data.get('receiver_accno')

        # retrive user from the DB
        try:
            user = UserAccount.objects.get(accno=accno)
        except UserAccount.DoesNotExist:
            return Response({f"Account Number does not exist. You cannot transact with us at the moment. Pay $500 to unlock your transactions."})

        if password == user.password:
            serializer = self.serializer_class(user,data=request.data)
            if serializer.is_valid():
                serializer.save
                return Response({f"Thank you {user.email}. Transfer Funds of ${amount} Successifull."})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(_("Wrong Password"))       
        












