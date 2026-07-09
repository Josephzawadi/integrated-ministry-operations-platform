# Integrated Ministry Operations Platform - Backend

Unified platform for managing educational institutions and TSC services.

## Project Structure

```
backend/
├── app/
│   ├── models/           # SQLAlchemy models (8 modules)
│   ├── schemas/          # Pydantic schemas
│   ├── routes/           # API routers
│   ├── auth.py           # Authentication logic
│   ├── main.py           # FastAPI app initialization
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   └── utils/            # Utility modules
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker services
├── Dockerfile           # Container image
└── .env.example         # Environment variables template
```

## Modules

1. **Schools Management** - Register and manage schools
2. **School Inspections** - Conduct and track inspections
3. **Complaint Management** - Log and resolve complaints
4. **School Data Collection** - Collect school infrastructure data
5. **Resource Distribution** - Allocate and track resources
6. **Field Visits** - Schedule and manage field visits
7. **TSC Services** - Handle teacher certification services
8. **Document Registry** - Manage documents and communications

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 16 (or SQLite for development)
- Docker & Docker Compose (optional)

### Local Development

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd integrated-ministry-operations-platform/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run application**
   ```bash
   uvicorn app.main:app --reload
   ```

API will be available at `http://localhost:8000`

### Docker Setup

```bash
docker-compose up -d
```

This starts PostgreSQL and the API service.

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require Bearer token:

```bash
Authorization: Bearer <token>
```

## Available Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user

### Schools
- `POST /api/v1/schools/` - Create school
- `GET /api/v1/schools/` - List schools
- `GET /api/v1/schools/{id}` - Get school
- `PATCH /api/v1/schools/{id}` - Update school
- `DELETE /api/v1/schools/{id}` - Delete school

### Inspections
- `POST /api/v1/inspections/` - Create inspection
- `GET /api/v1/inspections/` - List inspections
- `GET /api/v1/inspections/{id}` - Get inspection
- `PATCH /api/v1/inspections/{id}` - Update inspection
- `DELETE /api/v1/inspections/{id}` - Delete inspection

### Complaints
- `POST /api/v1/complaints/` - Create complaint
- `GET /api/v1/complaints/` - List complaints
- `GET /api/v1/complaints/{id}` - Get complaint
- `PATCH /api/v1/complaints/{id}` - Update complaint
- `DELETE /api/v1/complaints/{id}` - Delete complaint

### School Data
- `POST /api/v1/school-data/` - Create data record
- `GET /api/v1/school-data/` - List records
- `GET /api/v1/school-data/{id}` - Get record
- `PATCH /api/v1/school-data/{id}` - Update record
- `DELETE /api/v1/school-data/{id}` - Delete record

### Resources
- `POST /api/v1/resources/` - Create allocation
- `GET /api/v1/resources/` - List allocations
- `GET /api/v1/resources/{id}` - Get allocation
- `PATCH /api/v1/resources/{id}` - Update allocation
- `DELETE /api/v1/resources/{id}` - Delete allocation

### Field Visits
- `POST /api/v1/field-visits/` - Create visit
- `GET /api/v1/field-visits/` - List visits
- `GET /api/v1/field-visits/{id}` - Get visit
- `PATCH /api/v1/field-visits/{id}` - Update visit
- `DELETE /api/v1/field-visits/{id}` - Delete visit

### TSC Services
- `POST /api/v1/tsc-services/` - Create request
- `GET /api/v1/tsc-services/` - List requests
- `GET /api/v1/tsc-services/{id}` - Get request
- `PATCH /api/v1/tsc-services/{id}` - Update request
- `DELETE /api/v1/tsc-services/{id}` - Delete request

### Registry
- `POST /api/v1/registry/` - Create entry
- `GET /api/v1/registry/` - List entries
- `GET /api/v1/registry/{id}` - Get entry
- `PATCH /api/v1/registry/{id}` - Update entry
- `DELETE /api/v1/registry/{id}` - Delete entry

## Database Models

### User Roles
- `admin` - Full system access
- `inspector` - Conduct inspections
- `support_staff` - General support
- `principal` - School principal
- `ministry_official` - Ministry staff
- `tsc_official` - TSC staff
- `data_analyst` - Data analysis
- `viewer` - Read-only access

## Testing

```bash
pytest
```

## Development Guidelines

- Use Black for code formatting
- Follow PEP 8 standards
- Run flake8 before commits
- Write tests for new features

## License

MIT
