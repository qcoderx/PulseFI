from rest_framework import serializers
from .models import User
from sme.models import BusinessProfile

class SmeRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    business_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'business_name')

    def create(self, validated_data):
        business_name = validated_data.pop('business_name')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=User.UserType.SME
        )
        # Create the initial business profile
        BusinessProfile.objects.create(user=user, business_name=business_name)
        return user

class LenderRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=User.UserType.LENDER
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=User.UserType.choices)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'user_type')