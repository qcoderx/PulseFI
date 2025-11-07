from rest_framework import serializers
from .models import BusinessProfile, CACDocument, BusinessVideo, Score

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ('business_name', 'industry', 'location', 'description', 'founded_date')

class CACDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CACDocument
        fields = ('cac_file',)

class BusinessVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessVideo
        fields = ('video_file',)

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('pulse_score', 'profit_score', 'status', 'pulse_fail_reason')