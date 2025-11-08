from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routes.readiness_routes import router as readiness_router

app = FastAPI(title="Bridge AI Backend", version="1.0")

# Allow local + deployed frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "https://claflinhomeowner.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules under /api/v1
app.include_router(readiness_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Bridge AI Backend is running", "version": "v1"}
