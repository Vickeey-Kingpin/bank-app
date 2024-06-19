from rest_framework import serializers
from . models import User, UserAccount


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','password','password2']

    def validate(self, attrs):
        # getting the incoming data passed to the serializer
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError("Password do not match")
        else:
          if len(password) < 8:
              raise serializers.ValidationError("Password should contain atleast 8 characters")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password = validated_data.get('password')
        )
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length= 100)
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = [ 'email','password']

class UserFirstDepositSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length= 100)
    amount = serializers.CharField(max_length=10)
    accno = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email','accno','amount','password']

    def validate(self, attrs):
        amount = attrs.get('amount')
        amount = int(amount)  
        if amount < 500:
            raise serializers.ValidationError("Minimum amount you can deposit for the first deposit is 500")
        else:
            amount = str(amount)
            return attrs
    
    def create(self, validated_data):
        user= UserAccount.objects.create_user(
            email = validated_data['email'],
            accno = validated_data.get('accno'),           
            amount = validated_data.get('amount'),
            password = validated_data.get('password')
        )
        return user
    
class UserDepositSerializer(serializers.ModelSerializer):
    amount = serializers.CharField(max_length=10)
    class Meta:
        model = UserAccount
        fields = ['accno','amount','password']

    def validate(self, attrs):
        accno = attrs.get('accno')
        amount = attrs.get('amount')

        # retrive user from the DB
        user = UserAccount.objects.get(accno=accno)

        # getting the balance(amount) from the DB
        db_amount = user.amount

        # convert the inputed amount and the db_amount that are strings to integers for calculation
        amount = int(amount)
        if amount < 100:
            raise serializers.ValidationError("Deposit minimum amount is $100")
        elif amount > 100000:
            raise serializers.ValidationError("You can deposit only upto $100,0000")
                    
        db_amount = int(db_amount)
       
       # calculate the above integer values
        total = amount + db_amount

        # convert them back to string
        total = str(total)

        # update the balance in the database
        updated_user = UserAccount.objects.filter(accno=accno).update(amount=total)
        return updated_user
    
class UserWithdawalSerializer(serializers.ModelSerializer):
    amount = serializers.CharField(max_length=10)
    class Meta:
        model = UserAccount
        fields = ['accno','amount','password']

    def validate(self, attrs):
        accno = attrs.get('accno')
        amount = attrs.get('amount')

        # retrive user from the DB
        user = UserAccount.objects.get(accno=accno)

        # getting the balance(amount) from the DB
        db_amount = user.amount

        # convert the inputed amount and the db_amount that are strings to integers for calculation
        amount = int(amount)
        db_amount = int(db_amount)
        if amount > db_amount:
            raise serializers.ValidationError("Your balance is insufficient")
       
       # calculate the above integer values
        total = db_amount - amount

        # convert them back to string
        total = str(total)

        # update the balance in the database
        updated_user = UserAccount.objects.filter(accno=accno).update(amount=total)
        return updated_user    

class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['accno','password']

class UserTransferFundSerializer(serializers.ModelSerializer):
    accno = serializers.CharField(max_length=10)
    # send_to = serializers.ManyRelatedField(accno=accno)
    amount = serializers.CharField(max_length=10)
    class Meta:
        model = UserAccount
        fields = ['accno','amount','password']

    def validate(self, attrs):
        accno = attrs.get('accno')
        amount = attrs.get('amount')
        # send_to = attrs.get('send_to')

        # retrive user from the DB
        sender = UserAccount.objects.get(accno=accno)
        # receiver = UserAccount.objects.get(accno=accno)

        # getting the balance(amount) from the DB
        sender_amount = sender.amount
        # receiver_amount = receiver.amount

        # convert the inputed amount and the db_amount that are strings to integers for calculation
        amount = int(amount)
        sender_amount = int(sender_amount)
        # receiver_amount = int(receiver_amount)
        if amount > sender_amount:
            raise serializers.ValidationError("Your balance is insufficient")
       
       # calculate the above integer values
        total = sender_amount - amount
        # receiver_total = receiver_amount + amount

        # convert them back to string
        total = str(total)
        # receiver_total = str(receiver_total)

        # update the balance in the database
        updated_user = UserAccount.objects.filter(accno=accno).update(amount=total)
        # updated_user2 = UserAccount.objects.filter(send_to=send_to).update(amount=receiver_total)
        return updated_user




