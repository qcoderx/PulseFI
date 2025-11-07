from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import BusinessProfile, CACDocument, BusinessVideo, Score
from .serializers import BusinessProfileSerializer, CACDocumentSerializer, BusinessVideoSerializer, ScoreSerializer
from core.services import PulseEngine
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class BusinessProfileView(generics.RetrieveUpdateAPIView):
    """
    Handles GET/PUT/PATCH /sme/profile
    Allows SME to update their "Stated Truth"
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessProfileSerializer

    def get_object(self):
        profile, created = BusinessProfile.objects.get_or_create(user=self.request.user)
        return profile

class CACUploadView(generics.CreateAPIView):
    """
    Handles POST /sme/upload/cac
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CACDocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Use update_or_create to replace the file if it already exists
        CACDocument.objects.update_or_create(
            user=self.request.user,
            defaults={'cac_file': serializer.validated_data['cac_file']}
        )

class VideoUploadView(generics.CreateAPIView):
    """
    Handles POST /sme/upload/video
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessVideoSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Use update_or_create to replace the file if it already exists
        BusinessVideo.objects.update_or_create(
            user=self.request.user,
            defaults={'video_file': serializer.validated_data['video_file']}
        )

class MonoConnectView(views.APIView):
    """
    Handles POST /sme/mono/connect
    This is the final step that triggers the Pulse Engine
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mono_token = request.data.get('mono_token')
        if not mono_token:
            return Response({'detail': 'Mono token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Exchange token for account ID (Financial Truth)
            auth_response = requests.post(
                f"{settings.MONO_BASE_URL}/account/auth",
                headers={'mono-sec-key': settings.MONO_SECRET_KEY, 'Content-Type': 'application/json'},
                json={'code': mono_token}
            )
            auth_response.raise_for_status() # Raise error for bad responses
            account_id = auth_response.json().get('id')

            if not account_id:
                logger.warning(f"Mono auth succeeded but no account ID for user {request.user.email}")
                return Response({'detail': 'Failed to retrieve account ID from Mono.'}, status=status.HTTP_400_BAD_REQUEST)

            # 2. Get account details (holder name)
            details_response = requests.get(
                f"{settings.MONO_BASE_URL}/accounts/{account_id}",
                headers={'mono-sec-key': settings.MONO_SECRET_KEY}
            )
            details_response.raise_for_status()
            account_data = details_response.json().get('account', {})
            bank_account_name = account_data.get('name')

            if not bank_account_name:
                logger.warning(f"Mono details succeeded but no account name for user {request.user.email}")
                return Response({'detail': 'Failed to retrieve account holder name from Mono.'}, status=status.HTTP_400_BAD_REQUEST)

            # 3. This is the "magic" trigger
            # We pass the REAL (sandbox) bank name to the engine
            pulse_engine = PulseEngine(request.user, bank_account_name)
            pulse_score, fail_reason = pulse_engine.run_verification()
            
            # 4. Update the user's score
            score_obj, created = Score.objects.get_or_create(user=request.user)
            score_obj.pulse_score = pulse_score
            
            if pulse_score >= 75:
                score_obj.status = Score.Status.VERIFIED
                score_obj.pulse_fail_reason = None
                
                # TODO: Call Abdulrahman's ProfitEngine here
                # We can now pass him the account_id
                # profit_score = ProfitEngine.analyze_profit(request.user.id, account_id)
                # score_obj.profit_score = profit_score
                
                # For now, simulate a high profit score on success
                score_obj.profit_score = 85 # Placeholder for Profit Engine
            
            else:
                score_obj.status = Score.Status.FAILED
                score_obj.pulse_fail_reason = fail_reason
            
            score_obj.save()

            return Response(ScoreSerializer(score_obj).data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            logger.error(f"Mono API request failed for {request.user.email}: {e}")
            return Response({'detail': f'Mono API error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Verification failed for {request.user.email}: {e}")
            return Response({'detail': f'Verification failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SMEBashboardView(generics.RetrieveAPIView):
    """
    Handles GET /sme/dashboard
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def get_object(self):
        score, created = Score.objects.get_or_create(user=self.request.user)
        return score