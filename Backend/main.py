from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routes import readiness_routes 

app = FastAPI(title="Bridge AI Backend", version="1.0")

# CORS settings
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

# Register v1 routes
app.include_router(readiness_routes, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Bridge AI Backend is running", "version": "v1"}
