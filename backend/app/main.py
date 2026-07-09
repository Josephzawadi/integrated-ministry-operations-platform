from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.database import engine, Base
from app.routes import auth, schools, inspections, complaints, school_data, resources, field_visits, tsc_services, registry

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Integrated Ministry Operations Platform",
    description="Unified platform for managing educational institutions and TSC services",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(schools.router)
app.include_router(inspections.router)
app.include_router(complaints.router)
app.include_router(school_data.router)
app.include_router(resources.router)
app.include_router(field_visits.router)
app.include_router(tsc_services.router)
app.include_router(registry.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Integrated Ministry Operations Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

def custom_openapi():
    """Custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Integrated Ministry Operations Platform",
        version="1.0.0",
        description="API documentation for all modules",
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
