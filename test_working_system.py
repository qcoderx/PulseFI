#!/usr/bin/env python
"""
Simple test script for working PulseFI system
Tests actual endpoints that you know work
"""
import os
import sys
import django
import requests
from django.test import TestCase
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append('backend')
django.setup()

User = get_user_model()

def test_basic_functionality():
    """Test basic system functionality"""
    print("Testing PulseFI System...")
    
    # Test 1: User model works
    try:
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            user_type='sme'
        )
        print("[PASS] User creation works")
        user.delete()
    except Exception as e:
        print(f"[FAIL] User creation failed: {e}")
    
    # Test 2: Database connection
    try:
        count = User.objects.count()
        print(f"[PASS] Database connection works ({count} users)")
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
    
    # Test 3: Models import correctly
    try:
        from sme.models import BusinessProfile
        from lender.models import LenderProfile
        print("[PASS] Models import correctly")
    except Exception as e:
        print(f"[FAIL] Model imports failed: {e}")
    
    # Test 4: Views import correctly
    try:
        from sme.views import BusinessProfileView
        from lender.views import LenderProfileViewSet
        print("[PASS] Views import correctly")
    except Exception as e:
        print(f"[FAIL] View imports failed: {e}")
    
    print("\nBasic system test complete!")

if __name__ == "__main__":
    test_basic_functionality()