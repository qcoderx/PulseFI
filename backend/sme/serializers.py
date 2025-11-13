from rest_framework import serializers
from .models import BusinessProfile, CACDocument, BusinessVideo, Score
from users.models import User

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = [
            'business_name', 'business_category', 'industry', 
            'monthly_revenue', 'number_of_employees', 'business_description',
            'business_address'
        ]

class CACUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CACDocument
        fields = ['cac_file']

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessVideo
        fields = ['video_file']

class MonoConnectSerializer(serializers.Serializer):
    mono_token = serializers.CharField()

class SMEDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['business_name', 'verification_status', 'pulse_score', 'profit_score']