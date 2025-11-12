# PulseFI Manual Testing Guide

## Complete Feature Testing Checklist

### 🔐 Authentication System
- [ ] SME user registration
- [ ] Lender user registration  
- [ ] SME login/logout
- [ ] Lender login/logout
- [ ] JWT token validation
- [ ] Password validation
- [ ] Email uniqueness validation

### 🏢 SME Features
- [ ] Business profile creation/update
- [ ] CAC document upload (PDF)
- [ ] Business video upload (MP4)
- [ ] Mono bank account connection
- [ ] AI verification process
- [ ] Pulse score calculation
- [ ] Profit score calculation
- [ ] Dashboard view with scores

### 🏦 Lender Features
- [ ] Lender profile creation
- [ ] Marketplace browsing
- [ ] SME filtering by:
  - [ ] Industry
  - [ ] Pulse score range
  - [ ] Profit score range
  - [ ] Employee count
  - [ ] Revenue range
  - [ ] Location
- [ ] SME detail view
- [ ] Interest tracking (viewed/interested/contacted/funded)
- [ ] Search filter saving
- [ ] Dashboard statistics

### 🤖 AI Integration
- [ ] CAC document OCR extraction
- [ ] Business name verification
- [ ] Video analysis for industry matching
- [ ] Score calculation based on verification
- [ ] Error handling for AI failures

### 💳 Mono Integration
- [ ] Bank account connection
- [ ] Account name retrieval
- [ ] Balance information
- [ ] Name matching with business profile
- [ ] Error handling for invalid tokens

### 🎨 Frontend Integration
- [ ] API authentication headers
- [ ] File upload functionality
- [ ] Error message display
- [ ] Loading states
- [ ] Responsive design
- [ ] Navigation between pages

## Manual Test Scenarios

### Scenario 1: Complete SME Onboarding
1. Register as SME user
2. Create business profile
3. Upload CAC document
4. Record business video
5. Connect Mono account
6. Wait for AI verification
7. Check pulse/profit scores
8. View dashboard

### Scenario 2: Lender Discovery Flow
1. Register as lender
2. Create lender profile
3. Browse marketplace
4. Apply filters
5. View SME details
6. Mark interest
7. Save search filters
8. Check dashboard stats

### Scenario 3: Error Handling
1. Test invalid login credentials
2. Test file upload errors
3. Test network failures
4. Test AI service failures
5. Test Mono API errors
6. Test unauthorized access

### Scenario 4: Data Validation
1. Test required field validation
2. Test email format validation
3. Test file type validation
4. Test score range validation
5. Test business category validation

## Performance Testing
- [ ] File upload speed (large PDFs/videos)
- [ ] AI processing time
- [ ] Marketplace loading with many SMEs
- [ ] Database query performance
- [ ] API response times

## Security Testing
- [ ] JWT token expiration
- [ ] Unauthorized endpoint access
- [ ] File upload security
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CORS configuration

## Browser Compatibility
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile browsers

## API Endpoint Testing

### Authentication Endpoints
```bash
# SME Registration
POST /auth/sme/register
{
  "email": "sme@test.com",
  "password": "testpass123"
}

# Lender Registration  
POST /auth/lender/register
{
  "email": "lender@test.com", 
  "password": "testpass123"
}

# Login
POST /auth/login
{
  "email": "user@test.com",
  "password": "testpass123",
  "user_type": "sme"
}
```

### SME Endpoints
```bash
# Profile
POST /sme/profile
GET /sme/profile

# File Uploads
POST /sme/upload/cac (multipart/form-data)
POST /sme/upload/video (multipart/form-data)

# Mono Connection
POST /sme/mono/connect
{
  "mono_token": "token_from_mono_widget"
}

# Dashboard
GET /sme/dashboard
```

### Lender Endpoints
```bash
# Profile
POST /lender/profile/
GET /lender/profile/

# Marketplace
GET /lender/marketplace/
GET /lender/marketplace/{sme_id}/

# Interests
GET /lender/interests/
POST /lender/interests/{id}/update_status/

# Dashboard
GET /lender/dashboard/stats/
```

## Test Data Setup

### Sample SME Profile
```json
{
  "business_name": "Tech Solutions Ltd",
  "business_category": "software",
  "industry": "Technology",
  "monthly_revenue": 500000,
  "number_of_employees": 25,
  "business_description": "Software development company"
}
```

### Sample Lender Profile
```json
{
  "lender_type": "bank",
  "company_name": "Test Bank Ltd",
  "years_in_operation": 15,
  "risk_appetite": 7,
  "contact_person": "John Doe",
  "contact_email": "john@testbank.com",
  "contact_phone": "+1234567890",
  "office_address": "123 Bank Street"
}
```

## Expected Results

### Successful SME Verification
- Pulse Score: 80-100 (all verifications pass)
- Profit Score: Based on financial data
- Verification Status: "verified"
- Visible in lender marketplace

### Successful Lender Experience
- Can browse verified SMEs
- Filtering works correctly
- Interest tracking functions
- Dashboard shows accurate stats

## Troubleshooting Common Issues

### AI Verification Fails
- Check Google AI API key
- Verify file formats (PDF for CAC, MP4 for video)
- Check file size limits
- Review AI prompt responses

### Mono Connection Fails
- Verify Mono secret key
- Check token format
- Test with Mono sandbox environment
- Review API response format

### File Upload Issues
- Check media directory permissions
- Verify file size limits
- Test different file formats
- Check storage configuration