# 🏡 HomeReady — Palmetto-Panthers

## Challenge Statement(s) Addressed 🎯
- **How might we empower individuals and families to better prepare for homeownership by providing personalized readiness scores, recommendations, and guidance—especially in underserved communities?**
- **How might we make financial readiness accessible and understandable for first-time homebuyers through AI-driven, multilingual, and data-informed tools?**

---

## 🤯 Project Description
**HomeReady** is an AI-powered financial readiness web application designed to help users assess and improve their preparedness for homeownership. Users enter income, debts, rent, savings, credit score, target home price and down-payment info. The backend calculates a **Home Readiness Score** and returns a breakdown with **personalized recommendations** (budgeting changes, DPA programs, lender counseling, target price bands). The app supports **multilingual intake** (text/voice), automatically translating to English for backend analysis, and stores user reports securely for follow-up.

**Core user journey:** Sign up → Complete profile → Submit readiness form → View score & tips → Track progress over time → Export/share report with counselor.

---

## 💰 Project Value
**Target Users**
- First-time homebuyers in LMI communities
- Residents seeking clear, bite-sized financial steps
- Housing counselors / nonprofits who support clients

**Tangible Benefits**
- Converts complex finance into a single, transparent **score** with actionable steps
- Surfaces **Down Payment Assistance (DPA)** programs and realistic **price ranges**
- Encourages sustained financial habits and accelerates time-to-homeownership
- Provides counselors a shared source of truth for progress tracking

---

## 💻 Tech Overview
**Frontend**
- React + TypeScript (Vite)
- Tailwind CSS
- Firebase Authentication (Email/Password + Google Sign-in)
- Firestore (user profiles, saved reports)

**Backend**
- FastAPI (Python)
- Pydantic schemas
- Readiness scoring service (`readiness_service.py`)
- Uvicorn
- Optional: MongoDB or PostgreSQL (long-term analytics)

**AI / Integrations**
- Hugging Face translation models (multilingual intake)
- Firebase Storage / Cloudinary (document & image uploads)
- Deployment: Render (FastAPI) + Vercel (React)

**High-level Flow**
```
React Form → FastAPI /readiness/score → ReadinessService → Score + Breakdown → React renders cards & charts



Sequence Diagram: https://github.com/user-attachments/assets/80278445-2bb3-4dcf-b0a7-4c293a92f69a



```

---

## 🔌 Key Endpoints (example)
- `POST /api/v1/auths/login` – handled by Firebase Auth (frontend SDK)
- `POST /api/v1/auths/signup` – handled by Firebase Auth (frontend SDK)
- `POST /api/v1/users/init` – initialize profile in backend DB with `uid` (optional)
- `POST /api/v1/readiness/score` – compute readiness score (JWT required)
- `GET  /api/v1/readiness/history` – previous scores for trendline (JWT required)

---

## 🗂 Suggested Repo Structure
```
HomeReady/
├─ frontend/               # React + TS + Vite
│  ├─ src/
│  │  ├─ components/
│  │  ├─ pages/
│  │  ├─ services/        # api client
│  │  └─ styles/
│  └─ .env
├─ backend/                # FastAPI
│  ├─ Backend/services/readiness_service.py
│  ├─ Backend/schemas/readiness_model.py
│  ├─ main.py
│  └─ requirements.txt
└─ README.md
```

---

## 📽 Link to Demo Presentation
- Canva/Slides: ****

---




---

## 🏫 School Name
**Claflin University**

---

## 🏷 Team Name
**Palmetto-Panthers**

---

## ✨ Contributors

**April Ossai,** 
**Subash Neupane,** 
**Amrinder Singh,** 
**Javarius**

> 🏆 Built for equitable access to homeownership readiness.
