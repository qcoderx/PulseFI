from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import requests
from django.conf import settings
from datetime import datetime
# --- UPDATED IMPORTS ---
from .models import BusinessProfile, CACDocument, BusinessVideo
from .serializers import (
    BusinessProfileSerializer,
    CACUploadSerializer,
    VideoUploadSerializer,
    MonoConnectSerializer,
    SMEDashboardSerializer,
    VerifyCACSerializer,      # Added
    BusinessTypeSerializer,   # Added
    SMEOfferResponseSerializer # Added
)
from rest_framework import serializers # Added

class BusinessProfileView(APIView):
    """POST /sme/profile - Submit business information"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = BusinessProfileSerializer

    def post(self, request):
        try:
            profile, created = BusinessProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'business_name': request.data.get('businessName', ''),
                    'business_category': request.data.get('businessType', ''),
                    'industry': request.data.get('industry', ''),
                    'monthly_revenue': request.data.get('monthlyRevenue', 0),
                    'number_of_employees': request.data.get('employeeCount', 0),
                    'business_description': request.data.get('businessDescription', ''),
                    'business_address': request.data.get('businessAddress', ''),
                }
            )
            
            if not created:
                for field_map in [
                    ('businessName', 'business_name'),
                    ('businessType', 'business_category'), 
                    ('industry', 'industry'),
                    ('monthlyRevenue', 'monthly_revenue'),
                    ('employeeCount', 'number_of_employees'),
                    ('businessDescription', 'business_description'),
                    ('businessAddress', 'business_address')
                ]:
                    if field_map[0] in request.data:
                        setattr(profile, field_map[1], request.data[field_map[0]])
                profile.save()
            
            return Response({
                "success": True,
                "message": "Business profile saved successfully",
                "data": {
                    "profileId": str(profile.id),
                    "status": "profile_completed",
                    "nextStep": "cac_upload"
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Profile creation failed: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """GET /sme/profile - Get complete SME profile"""
        try:
            profile = BusinessProfile.objects.get(user=request.user)
            has_cac = CACDocument.objects.filter(user=request.user).exists()
            has_video = BusinessVideo.objects.filter(user=request.user).exists()
            
            return Response({
                "success": True,
                "data": {
                    "businessInfo": {
                        "businessName": profile.business_name,
                        "businessType": profile.business_category,
                        "industry": profile.industry,
                        "monthlyRevenue": profile.monthly_revenue,
                        "employeeCount": profile.number_of_employees,
                        "businessDescription": profile.business_description,
                        "businessAddress": profile.business_address,
                    },
                    "verification": {
                        "pulseScore": profile.pulse_score,
                        "profitScore": profile.profit_score,
                        "verificationStatus": profile.verification_status,
                        "cacVerified": has_cac,
                        "videoVerified": has_video,
                        "bankConnected": profile.mono_connected
                    },
                    "financialData": {
                        "monthlyRevenue": profile.monthly_revenue,
                        "monthlyExpenses": int(profile.monthly_revenue * 0.7) if profile.monthly_revenue else 0,
                        "profitMargin": 30,
                        "cashFlow": "positive",
                        "growthRate": 15
                    },
                    "documents": {
                        "cacCertificate": {
                            "fileName": "cac_certificate.pdf" if has_cac else None,
                            "verified": has_cac
                        },
                        "businessVideo": {
                            "fileName": "business_video.mp4" if has_video else None,
                            "verified": has_video
                        }
                    }
                }
            })
        except BusinessProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "Profile not found"
            }, status=status.HTTP_404_NOT_FOUND)

class CACUploadView(APIView):
    """POST /sme/upload/cac - Upload CAC certificate"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    # --- ADDED THIS LINE ---
    serializer_class = CACUploadSerializer

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({
                "success": False,
                "message": "No CAC file provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cac_file = request.FILES['file']
        
        try:
            cac_doc, created = CACDocument.objects.get_or_create(
                user=request.user,
                defaults={'cac_file': cac_file}
            )
            
            if not created:
                cac_doc.cac_file = cac_file
                cac_doc.save()
            
            return Response({
                "success": True,
                "message": "CAC certificate uploaded successfully",
                "data": {
                    "fileId": str(cac_doc.id),
                    "fileName": cac_file.name,
                    "fileSize": cac_file.size,
                    "uploadedAt": datetime.now().isoformat(),
                    "status": "uploaded",
                    "nextStep": "business_type_check"
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": f"CAC upload failed: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

class VerifyCACView(APIView):
    """POST /sme/verify-cac - Verify RC number with CAC database"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = VerifyCACSerializer

    def post(self, request):
        rc_number = request.data.get('rcNumber')
        if not rc_number:
            return Response({
                "success": False,
                "message": "RC number is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # !!! WARNING: THIS IS MOCKED DATA !!!
        # You must replace this with a real call to a CAC verification service
        if rc_number.startswith('RC'):
            return Response({
                "success": True,
                "message": "CAC verification successful",
                "data": {
                    "rcNumber": rc_number,
                    "name": "TEST BUSINESS LIMITED",
                    "address": "15 BUSINESS STREET, LAGOS ISLAND, LAGOS",
                    "dateOfRegistration": "2020-03-15",
                    "isRegistrationComplete": True,
                    "status": "active"
                }
            })
        else:
            return Response({
                "success": False,
                "message": "Company not found in CAC database",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

class BusinessTypeView(APIView):
    """POST /sme/business-type - Submit business type verification"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = BusinessTypeSerializer

    def post(self, request):
        # !!! WARNING: THIS IS MOCKED DATA !!!
        # This endpoint doesn't save anything
        return Response({
            "success": True,
            "message": "Business type information saved",
            "data": {
                "status": "business_type_completed",
                "nextStep": "video_recording"
            }
        }, status=status.HTTP_201_CREATED)

class VideoUploadView(APIView):
    """POST /sme/upload/video - Upload business video"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    # --- ADDED THIS LINE ---
    serializer_class = VideoUploadSerializer

    def post(self, request):
        if 'video' not in request.FILES:
            return Response({
                "success": False,
                "message": "No video file provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        video_file = request.FILES['video']
        
        try:
            video_doc, created = BusinessVideo.objects.get_or_create(
                user=request.user,
                defaults={'video_file': video_file}
            )
            
            if not created:
                video_doc.video_file = video_file
                video_doc.save()
            
            return Response({
                "success": True,
                "message": "Video uploaded successfully",
                "data": {
                    "videoId": str(video_doc.id),
                    "fileName": video_file.name,
                    "fileSize": video_file.size,
                    "duration": request.data.get('duration', 45),
                    "uploadedAt": datetime.now().isoformat(),
                    "status": "uploaded",
                    "nextStep": "bank_connection"
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Video upload failed: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

class MonoConnectView(APIView):
    """POST /sme/mono/connect - Connect bank account via Mono"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = MonoConnectSerializer

    def post(self, request):
        mono_code = request.data.get('monoCode')
        if not mono_code:
            return Response({
                "success": False,
                "message": "Mono code is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # !!! WARNING: THIS IS PARTIALLY MOCKED !!!
            # It uses the accountName from the request, not from a real Mono API call.
            # A real implementation would exchange mono_code for an account_id,
            # then fetch account details (including name) from Mono.
            account_name = request.data.get('accountName', 'TEST BUSINESS LIMITED')
            
            # Update user profile with bank connection
            profile = BusinessProfile.objects.get(user=request.user)
            profile.mono_connected = True
            
            # Trigger AI verification (This part is real)
            from core.services import PulseEngine
            engine = PulseEngine(request.user, account_name)
            pulse_score, fail_reason = engine.run_verification()
            
            profile.pulse_score = pulse_score
            profile.profit_score = 74  # Sample profit score
            if fail_reason:
                profile.verification_status = 'failed'
            else:
                profile.verification_status = 'verified'
            profile.save()
            
            return Response({
                "success": True,
                "message": "Bank account connected successfully",
                "data": {
                    "connectionId": f"mono_conn_{request.user.id}",
                    "accountId": request.data.get('accountId', 'acc_123'),
                    "bankName": request.data.get('bankName', 'Test Bank'),
                    "accountName": account_name,
                    "connectedAt": datetime.now().isoformat(),
                    "status": "connected",
                    "nextStep": "processing"
                }
            }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Mono connection failed: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

class SMEDashboardView(APIView):
    """GET /sme/dashboard - Get SME dashboard data"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = SMEDashboardSerializer # Used for output inference

    def get(self, request):
        try:
            profile = BusinessProfile.objects.get(user=request.user)
            has_cac = CACDocument.objects.filter(user=request.user).exists()
            has_video = BusinessVideo.objects.filter(user=request.user).exists()
            
            # This data is real, pulled from the profile
            return Response({
                "success": True,
                "data": {
                    "user": {
                        "firstName": request.user.email.split('@')[0],
                        "lastName": "User",
                        "businessName": profile.business_name,
                        "email": request.user.email
                    },
                    "verificationStatus": profile.verification_status,
                    "pulseScore": profile.pulse_score,
                    "profitScore": profile.profit_score,
                    "verificationSteps": {
                        "profile": {"completed": bool(profile.business_name)},
                        "cac": {"completed": has_cac},
                        "businessType": {"completed": True},
                        "video": {"completed": has_video},
                        "bankConnection": {"completed": profile.mono_connected}
                    },
                    "scoreBreakdown": {
                        "pulseScore": {
                            "total": profile.pulse_score,
                            "components": {
                                "cacVerification": 25 if has_cac else 0,
                                "videoAuthenticity": 22 if has_video else 0,
                                "bankAccountMatch": 20 if profile.mono_connected else 0,
                                "profileConsistency": 20 if profile.business_name else 0
                            }
                        },
                        "profitScore": {
                            "total": profile.profit_score,
                            "components": {
                                "profitability": 18,
                                "cashFlow": 20,
                                "growthTrend": 16,
                                "customerRetention": 20
                            }
                        }
                    },
                    "recommendations": [
                        "Your CAC verification boosted your Pulse Score significantly",
                        "Consider improving cash flow consistency for better Profit Score"
                    ],
                    "marketplaceStats": {
                        "profileViews": 23,
                        "lenderInterest": 5,
                        "activeOffers": 2
                    }
                }
            })
            
        except BusinessProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "Profile not found"
            }, status=status.HTTP_404_NOT_FOUND)

class SMEOffersView(APIView):
    """GET /sme/offers - Get investment offers for SME"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = serializers.Serializer # Dummy

    def get(self, request):
        # !!! WARNING: THIS IS MOCKED DATA !!!
        # This should query the LoanNegotiation model from the 'escrow' app
        return Response({
            "success": True,
            "data": {
                "offers": [
                    {
                        "offerId": "offer_12345",
                        "lender": {
                            "id": "lender_67890",
                            "organizationName": "Lagos Investment Partners",
                            "rating": 4.8,
                            "totalInvestments": 15,
                            "averageROI": 22.5
                        },
                        "offerDetails": {
                            "amount": 4500000,
                            "interestRate": 18,
                            "termMonths": 24,
                            "offerType": "loan",
                            "conditions": [
                                "Monthly financial reporting required",
                                "Quarterly business reviews"
                            ]
                        },
                        "status": "pending",
                        "submittedAt": datetime.now().isoformat(),
                        "expiresAt": datetime.now().isoformat(),
                        "message": "We're impressed with your business model and growth potential."
                    }
                ],
                "summary": {
                    "totalOffers": 3,
                    "pendingOffers": 2,
                    "averageAmount": 4200000,
                    "bestRate": 16.5
                }
            }
        })

class SMEOfferResponseView(APIView):
    """POST /sme/offers/:offerId/respond - Respond to investment offer"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = SMEOfferResponseSerializer

    def post(self, request, offerId):
        action = request.data.get('action', 'negotiate')
        
        # !!! WARNING: THIS IS MOCKED DATA !!!
        # This should use the logic from 'escrow.views.LoanNegotiationViewSet'
        return Response({
            "success": True,
            "message": "Response submitted successfully",
            "data": {
                "offerId": offerId,
                "status": "negotiating",
                "updatedAt": datetime.now().isoformat(),
                "negotiationRound": 1
            }
        })