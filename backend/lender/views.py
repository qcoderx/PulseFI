from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import LenderProfile, SMEInterest, SearchFilter
# --- UPDATED IMPORTS ---
from .serializers import (
    LenderProfileSerializer, LenderProfileCreateSerializer,
    VerifiedSMESerializer, SMEDetailSerializer,
    SMEInterestSerializer, SMEInterestCreateSerializer,
    SearchFilterSerializer, SearchFilterCreateSerializer,
    MarketplaceFilterSerializer
)
from sme.models import BusinessProfile
from rest_framework import serializers # Added

class LenderProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LenderProfile.objects.filter(user=self.request.user).order_by('created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LenderProfileCreateSerializer
        return LenderProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MarketplaceViewSet(viewsets.GenericViewSet):
    """GET /lender/marketplace - Get list of verified SMEs for lenders"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = VerifiedSMESerializer

    def get_queryset(self):
        # --- MODIFIED THIS ---
        # Return a base queryset, even if empty, to help spectacular
        return BusinessProfile.objects.filter(verification_status='verified')
    
    def list(self, request):
        try:
            lender_profile = LenderProfile.objects.get(user=request.user)
        except LenderProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "Lender profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get verified SMEs
        queryset = self.get_queryset().filter(pulse_score__gte=75).order_by('-pulse_score')
        
        # Apply filters from query params
        industry = request.query_params.get('industry')
        if industry:
            queryset = queryset.filter(business_category=industry)
        
        min_pulse_score = request.query_params.get('minPulseScore')
        if min_pulse_score:
            queryset = queryset.filter(pulse_score__gte=int(min_pulse_score))
        
        min_profit_score = request.query_params.get('minProfitScore')
        if min_profit_score:
            queryset = queryset.filter(profit_score__gte=int(min_profit_score))
        
        # Track views
        for sme in queryset:
            SMEInterest.objects.get_or_create(
                lender=lender_profile,
                sme_business=sme,
                defaults={'status': 'viewed'}
            )
        
        # Format response
        smes_data = []
        for sme in queryset[:10]:  # Limit to 10 for demo
            smes_data.append({
                "id": str(sme.id),
                "businessName": sme.business_name,
                "industry": sme.industry,
                "location": sme.business_address or "Lagos, Nigeria",
                "pulseScore": sme.pulse_score,
                "profitScore": sme.profit_score,
                "fundingAmount": 5000000,  # Sample
                "fundingPurpose": "Business expansion",
                "yearEstablished": 2020,
                "employeeCount": sme.number_of_employees or 10,
                "monthlyRevenue": sme.monthly_revenue or 2500000,
                "growthRate": 15,
                "riskLevel": "low" if sme.pulse_score > 80 else "medium",
                "lastActive": datetime.now().isoformat()
            })
        
        return Response({
            "success": True,
            "data": {
                "smes": smes_data,
                "pagination": {
                    "currentPage": 1,
                    "totalPages": 5,
                    "totalItems": len(smes_data),
                    "itemsPerPage": 10,
                    "hasNext": False,
                    "hasPrev": False
                },
                "filters": {
                    "industries": ["fashion", "fintech", "agriculture", "retail"],
                    "states": ["Lagos", "Abuja", "Kano", "Rivers"],
                    "pulseScoreRange": {"min": 0, "max": 100},
                    "profitScoreRange": {"min": 0, "max": 100}
                }
            }
        })
    
    def retrieve(self, request, pk=None):
        """GET /lender/marketplace/:smeId - Get detailed SME profile"""
        try:
            lender_profile = LenderProfile.objects.get(user=request.user)
        except LenderProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "Lender profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            sme_business = BusinessProfile.objects.get(
                id=pk, 
                verification_status='verified', 
                pulse_score__gte=75
            )
        except BusinessProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "SME not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Track interest
        SMEInterest.objects.get_or_create(
            lender=lender_profile,
            sme_business=sme_business,
            defaults={'status': 'viewed'}
        )
        
        # !!! WARNING: This response contains MOCKED/SAMPLE data !!!
        return Response({
            "success": True,
            "data": {
                "basicInfo": {
                    "id": str(sme_business.id),
                    "businessName": sme_business.business_name,
                    "industry": sme_business.industry,
                    "businessType": sme_business.business_category,
                    "yearEstablished": 2020,
                    "employeeCount": sme_business.number_of_employees or 8,
                    "location": sme_business.business_address or "Lagos Island, Lagos",
                    "businessDescription": sme_business.business_description,
                    "targetMarket": "Young professionals aged 25-40", # Sample
                    "competitiveAdvantage": "Unique blend of traditional and modern designs" # Sample
                },
                "scores": {
                    "pulseScore": sme_business.pulse_score,
                    "profitScore": sme_business.profit_score,
                    "riskLevel": "low" if sme_business.pulse_score > 80 else "medium",
                    "verificationStatus": sme_business.verification_status
                },
                "financialHighlights": { # Sample
                    "monthlyRevenue": sme_business.monthly_revenue or 2500000,
                    "profitMargin": 28,
                    "growthRate": 15,
                    "cashFlowStatus": "positive",
                    "debtToIncomeRatio": 0.3
                },
                "fundingRequest": { # Sample
                    "amount": 5000000,
                    "purpose": "Expand inventory and open new location",
                    "expectedROI": 25,
                    "paybackPeriod": 24,
                    "collateral": "Business inventory and equipment"
                },
                "verification": {
                    "cacVerified": True,
                    "videoVerified": True,
                    "bankConnected": sme_business.mono_connected,
                    "documentsComplete": True,
                    "lastVerified": datetime.now().isoformat()
                },
                "marketMetrics": { # Sample
                    "profileViews": 23,
                    "lenderInterest": 5,
                    "activeOffers": 2,
                    "averageOfferAmount": 4200000
                }
            }
        })

class SMEInterestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        lender_profile = get_object_or_404(LenderProfile, user=self.request.user)
        return SMEInterest.objects.filter(lender=lender_profile)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SMEInterestCreateSerializer
        return SMEInterestSerializer
    
    def perform_create(self, serializer):
        lender_profile = get_object_or_404(LenderProfile, user=self.request.user)
        serializer.save(lender=lender_profile)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        interest = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(SMEInterest.INTEREST_STATUS):
            return Response({
                "error": "Invalid status"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        interest.status = new_status
        interest.save()
        
        serializer = SMEInterestSerializer(interest)
        return Response(serializer.data)

class SearchFilterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        lender_profile = get_object_or_404(LenderProfile, user=self.request.user)
        return SearchFilter.objects.filter(lender=lender_profile)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SearchFilterCreateSerializer
        return SearchFilterSerializer
    
    def perform_create(self, serializer):
        lender_profile = get_object_or_404(LenderProfile, user=self.request.user)
        serializer.save(lender=lender_profile)

class LenderDashboardView(APIView):
    """GET /lender/dashboard - Get lender dashboard data"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = serializers.Serializer # Dummy

    def get(self, request):
        try:
            lender_profile = LenderProfile.objects.get(user=request.user)
        except LenderProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "Lender profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Count verified SMEs
        total_verified_smes = BusinessProfile.objects.filter(
            verification_status='verified',
            pulse_score__gte=75
        ).count()
        
        # Count SME interests by status
        interests = SMEInterest.objects.filter(lender=lender_profile)
        funded_count = interests.filter(status='funded').count()
        
        # !!! WARNING: This response contains MOCKED/SAMPLE data !!!
        return Response({
            "success": True,
            "data": {
                "user": {
                    "firstName": request.user.email.split('@')[0],
                    "lastName": "User",
                    "organizationName": lender_profile.company_name,
                    "email": request.user.email
                },
                "portfolio": { # Partially Mocked
                    "totalInvestments": funded_count,
                    "totalAmount": funded_count * 5000000,
                    "activeInvestments": funded_count,
                    "averageROI": 22.5, # Mocked
                    "defaultRate": 2.1 # Mocked
                },
                "marketplaceStats": { # Partially Mocked
                    "totalVerifiedSMEs": total_verified_smes,
                    "newSMEsThisWeek": 8, # Mocked
                    "averagePulseScore": 78, # Mocked
                    "averageProfitScore": 71 # Mocked
                },
                "recentActivity": [ # Mocked
                    {
                        "type": "new_sme",
                        "smeId": "sme_12345",
                        "businessName": "Sample Business",
                        "pulseScore": 87,
                        "timestamp": datetime.now().isoformat()
                    }
                ],
                "recommendations": [ # Mocked
                    {
                        "smeId": "sme_12345",
                        "businessName": "Sample Business",
                        "reason": "High Pulse Score and growing industry",
                        "matchScore": 92
                    }
                ]
            }
        })

class LenderOffersView(APIView):
    """POST /lender/offers - Make investment offer to SME"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = serializers.Serializer # Dummy

    def post(self, request):
        try:
            lender_profile = LenderProfile.objects.get(user=request.user)
        except LenderProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "Lender profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        sme_id = request.data.get('smeId')
        offer_amount = request.data.get('offerAmount')
        
        if not sme_id or not offer_amount:
            return Response({
                "success": False,
                "message": "Missing required fields"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            sme_business = BusinessProfile.objects.get(id=sme_id, verification_status='verified')
        except BusinessProfile.DoesNotExist:
            return Response({
                "success": False,
                "message": "SME not found or not verified"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # !!! WARNING: This is a SIMPLIFIED implementation !!!
        # It just creates an 'SMEInterest' record, not a real 'LoanNegotiation' offer.
        # You should replace this with logic that creates a 'LoanNegotiation' object from the 'escrow' app.
        interest, created = SMEInterest.objects.get_or_create(
            lender=lender_profile,
            sme_business=sme_business,
            defaults={'status': 'interested'}
        )
        
        return Response({
            "success": True,
            "message": "Investment offer submitted successfully",
            "data": {
                "offerId": f"offer_{interest.id}",
                "smeId": sme_id,
                "lenderId": str(lender_profile.id),
                "offerAmount": offer_amount,
                "status": "pending",
                "submittedAt": datetime.now().isoformat(),
                "expiresAt": datetime.now().isoformat()
            }
        }, status=status.HTTP_201_CREATED)

class AdminAnalyticsView(APIView):
    """GET /admin/analytics/overview - Get platform analytics (Admin only)"""
    permission_classes = [IsAuthenticated]
    # --- ADDED THIS LINE ---
    serializer_class = serializers.Serializer # Dummy
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({
                "success": False,
                "message": "Admin access required"
            }, status=status.HTTP_403_FORBIDDEN)
        
        total_smes = BusinessProfile.objects.count()
        verified_smes = BusinessProfile.objects.filter(verification_status='verified').count()
        total_lenders = LenderProfile.objects.count()
        
        # !!! WARNING: This response contains MOCKED/SAMPLE data !!!
        return Response({
            "success": True,
            "data": {
                "userStats": { # Real
                    "totalSMEs": total_smes,
                    "totalLenders": total_lenders,
                    "verifiedSMEs": verified_smes,
                    "activeLenders": total_lenders
                },
                "verificationStats": { # Mocked
                    "averagePulseScore": 78.5,
                    "averageProfitScore": 71.2,
                    "verificationSuccessRate": 76.5,
                    "processingTime": "2.3 hours"
                },
                "marketplaceStats": { # Mocked
                    "totalOffers": 156,
                    "successfulMatches": 89,
                    "totalFundingAmount": 450000000,
                    "averageOfferAmount": 4200000
                },
                "monthlyGrowth": { # Mocked
                    "newSMEs": 23,
                    "newLenders": 4,
                    "completedDeals": 12,
                    "platformRevenue": 2500000
                }
            }
        })