from fastapi import FastAPI
from Backend.routes.ai_routes import router as ai_router

app = FastAPI(title="Bridge AI Backend")
app.include_router(ai_router, prefix="/ai")

@app.get("/")
def root():
    return {"message": "Bridge AI Backend is running"}