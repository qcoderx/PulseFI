# PulseFi Backend - The Trust Engine for SME Lending

## 🚀 Project Overview

PulseFi is an intelligent platform that solves the "Billion-Naira Trust Gap" by programmatically verifying SME authenticity and financial health. This Django backend powers the Twin Score System that de-risks SME lending through multi-modal verification.

### 🎯 Product Objective
Build a functional MVP for Zenith Bank Zecathon 5.0 that demonstrates PulseFi's unique capability to bridge the trust gap between credible SMEs and cautious lenders.

## 🏗️ Architecture

### Core Components
- **Pulse Score (0-100)**: Validates SME authenticity through multi-source verification
- **Profit Score**: Analyzes financial health and growth potential
- **Marketplace**: Connects verified SMEs with pre-vetted lenders

### Technology Stack
- **Backend Framework**: Django + Django REST Framework
- **Database**: MongoDB with Djongo
- **AI Integration**: Google Gemini 2.5 Flash & OCR
- **Open Banking**: Mono API
- **Authentication**: JWT Tokens
- **File Handling**: Django Storages

## 📁 Project Structure

```
backend/
├── pulsefi/                 # Main Django project
│   ├── settings.py         # Project configuration
│   ├── urls.py            # Main URL routing
│   └── apps/              # Django applications
│       ├── users/         # Authentication & user management
│       ├── sme/           # SME-specific functionality
│       ├── lender/        # Lender marketplace
│       ├── core/          # Business logic & AI services
│       └── utils/         # Helper functions
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## 🔧 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/sme/register` | SME registration |
| POST | `/api/auth/lender/register` | Lender registration |
| POST | `/api/auth/login` | User login (returns JWT) |

### SME Onboarding & Verification
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sme/profile` | Submit "Stated Truth" form |
| POST | `/api/sme/upload/cac` | Upload CAC certificate |
| POST | `/api/sme/upload/video` | Upload live verification video |
| POST | `/api/sme/mono/connect` | Connect Mono bank account |
| GET | `/api/sme/dashboard` | Get scores and status |

### Lender Marketplace
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/lender/marketplace` | List verified SMEs |
| GET | `/api/lender/marketplace/<sme_id>` | Get SME detailed profile |

## 🎯 Core Features

### Epic 1: SME Onboarding & Pulse Score Generation
1. **Triple Verification System**:
   - **Stated Truth**: Business profile form
   - **Visual Truth**: Live business location video
   - **Financial Truth**: Mono bank account connection
   - **Document Truth**: CAC certificate verification

2. **Pulse Engine AI**:
   - OCR processing of CAC documents
   - Video content analysis
   - Cross-referencing across all data sources
   - Consistency scoring (0-100)

### Epic 2: Profit Score Analysis
1. **Financial Health Assessment**:
   - Cash flow analysis
   - Revenue trend identification
   - Customer behavior patterns
   - Growth trajectory scoring

### Epic 3: Investor Marketplace
1. **Curated SME Discovery**:
   - Pulse-verified SMEs only (score ≥ 75)
   - Advanced filtering by industry, location, score
   - Detailed financial analytics

## 🗄️ Database Models

### Core Models
- **User**: Base user model with JWT authentication
- **SMEUser**: Extended SME profile with verification data
- **LenderUser**: Lender profile with preferences
- **BusinessProfile**: SME business information
- **VerificationData**: CAC, video, and bank verification records
- **Score**: Pulse and Profit scores with historical data

## 🤖 AI Services

### Pulse Engine (`core/services/pulse_engine.py`)
```python
class PulseEngine:
    def verify_business_authenticity(self, sme_id: str) -> PulseScore:
        """
        Cross-references:
        - CAC data vs Stated Truth vs Bank Account Name
        - Stated Business Type vs Video Analysis
        - Financial claims vs Actual bank data
        """
```

### Profit Engine (`core/services/profit_engine.py`)
```python
class ProfitEngine:
    def analyze_financial_health(self, sme_id: str) -> ProfitScore:
        """
        Analyzes:
        - Transaction patterns
        - Revenue consistency
        - Expense management
        - Growth indicators
        """
```

## 🔐 Security Features

- JWT-based authentication
- File upload validation and scanning
- Secure Mono API integration
- CORS configuration for frontend
- Environment-based configuration

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- MongoDB
- Mono API credentials
- Google AI Studio API key

### Installation Steps
1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp .env.example .env
   # Configure your environment variables
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Environment Variables

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=mongodb://localhost:27017/pulsefi

# API Keys
MONO_SECRET_KEY=your-mono-secret
GOOGLE_AI_API_KEY=your-gemini-key

# File Storage
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.sme
python manage.py test apps.lender
```

## 👥 Team Responsibilities

### Backend 1 (Lasisi - Team Lead)
- Core AI (Pulse Engine)
- Authentication & SME endpoints
- JWT security implementation

### Backend 2 (Abdulrahman)
- Profit Engine development
- Database models & lender endpoints
- MongoDB integration

## 📊 Demo Success Metrics

Our backend is successful if we can demonstrate:

1. **Real-time Verification**: SME completes onboarding in <5 minutes
2. **AI Accuracy**: Pulse Score accurately detects inconsistencies
3. **Data Flow**: Seamless integration between verification steps
4. **Performance**: API responses under 200ms for critical endpoints

## 🔄 Workflow Integration

### Phase 1: API Contract (First 2 Hours)
- Define and freeze all API endpoints
- Create serializers and request/response schemas
- Set up mock endpoints for frontend development

### Phase 2: Parallel Development
- Backend 1: Pulse Engine & SME endpoints
- Backend 2: Profit Engine & Lender endpoints
- Continuous integration and testing

### Phase 3: Integration & Demo Prep
- End-to-end testing with frontend
- Performance optimization
- Demo script validation

## 🐛 Troubleshooting

### Common Issues
1. **MongoDB Connection**: Ensure MongoDB is running on default port
2. **Mono Integration**: Verify API credentials and webhook configuration
3. **File Uploads**: Check storage configuration and file size limits
4. **AI Services**: Validate Google AI API key and quota

### Logs & Monitoring
- Django debug toolbar for development
- Custom logging for AI service calls
- Error tracking for Mono API interactions

## 📞 Support

For backend-related issues, contact:
- **Lasisi**: Pulse Engine & Authentication
- **Abdulrahman**: Profit Engine & Database

---

**Built for Zecathon 5.0 - Transforming SME Lending Through Trust** 🚀