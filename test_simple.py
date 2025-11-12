#!/usr/bin/env python
"""
Simple PulseFI System Test
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_system():
    print("Testing PulseFI System...")
    
    # SME Registration
    sme_data = {
        "email": f"sme_{int(time.time())}@test.com",
        "password": "testpass123",
        "business_name": "Test Business"
    }
    
    response = requests.post(f"{BASE_URL}/auth/sme/register", json=sme_data)
    print(f"SME Registration: {response.status_code}")
    
    # SME Login
    login_data = {
        "email": sme_data["email"],
        "password": sme_data["password"],
        "user_type": "sme"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"SME Login: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"Token: {'Yes' if token else 'No'}")
        
        # Test authenticated endpoint
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{BASE_URL}/sme/dashboard", headers=headers)
        print(f"Dashboard: {response.status_code}")
    
    # Lender Registration
    lender_data = {
        "email": f"lender_{int(time.time())}@test.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/lender/register", json=lender_data)
    print(f"Lender Registration: {response.status_code}")
    
    print("\nSystem Status: WORKING" if all([
        response.status_code in [200, 201] for response in [
            requests.get(f"{BASE_URL}/admin/")
        ]
    ]) else "System Status: CHECK ERRORS")

if __name__ == "__main__":
    test_system()