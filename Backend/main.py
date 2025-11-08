from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routes.readiness_routes import router as readiness_router
from Backend.routes.ai_routes import router as ai_router  # 👈 add this import

app = FastAPI(title="Bridge AI Backend", version="1.0")

# --- Enable CORS for your frontend ---
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

# --- Register all routers ---
app.include_router(readiness_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")  # 👈 register AI endpoints

@app.get("/")
def root():
    return {"message": "Bridge AI Backend is running", "version": "v1"}
