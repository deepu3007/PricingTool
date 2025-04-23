from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import products, predictions, factors, analytics
from app.core.config import settings
from app.db.session import create_tables

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Price Map Prediction Tool API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"]
)
app.include_router(
    predictions.router, prefix=f"{settings.API_V1_STR}/predictions", tags=["predictions"]
)
app.include_router(
    factors.router, prefix=f"{settings.API_V1_STR}/factors", tags=["factors"]
)
app.include_router(
    analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"]
)


@app.on_event("startup")
async def startup_event():
    create_tables()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
