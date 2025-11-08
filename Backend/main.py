from fastapi import FastAPI
from Backend.routes import ai_routes  # ✅ import the router module

app = FastAPI(title="Bridge Backend API")

# ✅ include the router
app.include_router(ai_routes.router)

@app.get("/")
def root():
    return {"message": "Bridge Backend API is running 🚀"}