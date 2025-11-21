# 🚀 DEMETRA AI Analytics - Backend API

> Centralized AI-powered advertising analytics dashboard with automated hourly data synchronization

## 📋 Overview

This FastAPI backend provides a unified analytics platform for advertising campaigns across multiple channels (Facebook, Instagram, Google Ads, TikTok) with automated data synchronization and AI-powered insights.

## ✨ Features

- **Multi-Channel Integration**: Facebook, Instagram, Google Ads, TikTok
- **Automated Hourly Sync**: APScheduler-based data synchronization
- **Mock Data Generation**: Realistic campaign data using Faker
- **Database Management**: PostgreSQL with SQLAlchemy ORM
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Real-time Monitoring**: Scheduler status and sync tracking

## 🏗️ Architecture

```
├── app/
│   ├── configs/          # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   └── utils/            # Utilities and helpers
├── alembic/              # Database migrations
└── tests/                # Test files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Poetry (recommended) or pip

### Installation

1. **Clone and setup**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. **Database setup**
```bash
alembic upgrade head
python setup_database.py
```

4. **Start server**
```bash
uvicorn app.main:app --reload
```

## 📡 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check

### Mock Data & Testing
- `GET /api/test/mock-data` - Individual channel mock data
- `GET /api/test/mock-all` - Combined channel data
- `POST /api/test/sync-now` - Manual sync trigger

### Scheduler Management
- `GET /api/scheduler/status` - Scheduler status and jobs
- `POST /api/scheduler/sync-now` - Manual scheduler sync
- `POST /api/scheduler/start` - Start scheduler
- `POST /api/scheduler/stop` - Stop scheduler

### API Documentation
- `GET /docs` - Interactive Swagger UI
- `GET /redoc` - ReDoc documentation

## 🔄 Automated Sync System

### Hourly Synchronization
- **Frequency**: Every hour at minute 0 (1:00, 2:00, 3:00...)
- **Data Sources**: All 4 advertising platforms
- **Duplicate Prevention**: Campaign ID-based deduplication
- **Error Handling**: Graceful failure recovery with logging

### Sync Process
1. Fetch fresh campaign data from mock APIs
2. Check for existing campaigns by `campaign_id`
3. Insert new campaigns to database
4. Log sync results and statistics

## 🗄️ Database Schema

### Campaign Model
```python
class Campaign(Base):
    id: int (Primary Key)
    campaign_id: str (Unique)
    channel: str (facebook/instagram/google_ads/tiktok)
    conversion_rate: float
    cost: float
    roi: float
    clicks: int
    impressions: int
    engagement: int
    date: date
    created_at: datetime
```

## 🧪 Testing

### Run Tests
```bash
# Individual tests
python test_mock_api.py
python test_sync_service.py
python test_scheduler.py

# Database tests
python test_database.py
python test_models_only.py
```

### API Testing with Bruno
Use the provided Bruno collection in `../adv_ai-api-collection/` for comprehensive API testing.

### Manual Testing
```bash
# Test basic API
curl http://localhost:8000/

# Test mock data
curl http://localhost:8000/api/test/mock-data

# Test sync
curl -X POST http://localhost:8000/api/test/sync-now

# Check scheduler
curl http://localhost:8000/api/scheduler/status
```

## ⚙️ Configuration

### Environment Variables (.env)
```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/dbname
DEBUG=True
LOG_LEVEL=INFO
```

### Scheduler Configuration
```python
# Modify in app/services/scheduler.py
CronTrigger(minute=0)        # Every hour
CronTrigger(minute="*/30")   # Every 30 minutes
CronTrigger(hour=2, minute=0) # Daily at 2 AM
```

## 📊 Data Flow

```
Mock APIs → Scheduler → Sync Service → Database → API Endpoints
    ↓           ↓           ↓            ↓           ↓
Facebook    Hourly      Campaign     PostgreSQL   REST API
Instagram   Trigger     Validation   Storage      Responses
Google Ads  APScheduler Deduplication SQLAlchemy  JSON Data
TikTok      Cron Jobs   Error Handle  Alembic     Documentation
```

## 🔍 Monitoring & Logs

### Scheduler Monitoring
- Check status: `GET /api/scheduler/status`
- View next run time and active jobs
- Monitor sync success/failure rates

### Logging
- Scheduler start/stop events
- Sync job execution results
- Error details and stack traces
- Campaign sync statistics

## 🚀 Deployment

### Docker (Recommended)
```bash
docker-compose up -d
```

### Manual Deployment
```bash
# Production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🛠️ Development

### Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── configs/
│   │   ├── database.py      # Database configuration
│   │   └── database_flexible.py
│   ├── models/              # SQLAlchemy models
│   │   ├── campaign.py
│   │   ├── alert.py
│   │   └── ...
│   ├── routers/             # API route handlers
│   │   ├── test_mock.py
│   │   └── scheduler.py
│   ├── services/            # Business logic
│   │   ├── mock_api.py      # Mock data generation
│   │   ├── sync_service.py  # Data synchronization
│   │   └── scheduler.py     # APScheduler service
│   └── utils/               # Utilities
├── alembic/                 # Database migrations
├── tests/                   # Test files
└── docs/                    # Documentation
```

### Adding New Features
1. Create models in `app/models/`
2. Add API routes in `app/routers/`
3. Implement business logic in `app/services/`
4. Create database migrations with Alembic
5. Add tests and update documentation

## 📈 Performance

### Optimization Features
- Database connection pooling
- Async/await support with FastAPI
- Efficient bulk database operations
- Scheduled background tasks
- Error recovery and retry logic

### Scalability
- Horizontal scaling with multiple workers
- Database read replicas support
- Caching layer ready (Redis)
- Microservices architecture compatible

## 🔐 Security

### Current Implementation
- CORS middleware configured
- Environment variable configuration
- SQL injection prevention (SQLAlchemy ORM)
- Input validation with Pydantic

### Production Recommendations
- Add authentication/authorization
- Implement rate limiting
- Use HTTPS/TLS encryption
- Add request/response logging
- Database connection encryption

## 📚 Dependencies

### Core Dependencies
- **FastAPI**: Modern web framework
- **SQLAlchemy**: ORM and database toolkit
- **APScheduler**: Task scheduling
- **Alembic**: Database migrations
- **Psycopg2**: PostgreSQL adapter

### Development Dependencies
- **Faker**: Mock data generation
- **Pytest**: Testing framework
- **Uvicorn**: ASGI server

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues
- **Database Connection**: Check DATABASE_URL in .env
- **Scheduler Not Running**: Verify APScheduler installation
- **API 404 Errors**: Ensure all routers are imported in main.py

### Getting Help
- Check the `/docs` endpoint for API documentation
- Review test files for usage examples
- Check logs for detailed error information

---

**Built with ❤️ for DEMETRA Systems - Centralized AI Analytics Platform**
