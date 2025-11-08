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

![Architecture Diagram](https://img.plantuml.biz/plantuml/png/dLJ1RXen4BtlLumuLA2oshH7990Wb8OsLMYWpILIPDQ67U6rBTjBIcck_O1-Oh-aOo-Ka215hRJIhkmtC-_Dl5cFNWgO5UY07WONkXJNWl4Dz6rUe1Uvhwn84iEinnmDKnw-E66F3XetOWvzOw19eRb_FPks6i0SZAnMNYX-31wX5NFc1FGhNqHS-3Z635Y-ea1eZfZp_ScupaSVnx3XW12KpdbjHJRzV5dZXeCawNPXYajL6UXsay0uxUtfT624KeAhhnVQbj0K9KEP6URSlROSj8NtMY-bQ2NxgBGNQ7OWju9v4J8-2Mf15dEErGtwOg9DPPhx924qVSoWGju6v3DDCg7vuMPsL6Woxi3aQZg3hA8wBaE57hOnnbYzG2aU4WAblU5WJmW2Sd-R30VfBerUHUJZsc_Fti1v3EA7ecalIEh0jU3KqDo3rp1ahfXhPdbivwLUeZhLpMarBucVZFV_qCcwMKy3Vi3_DUqHd-260yu9vr2hJEgSqTJfaYqfUv0Kd8wAxc6QXvWJuguCvJZW3CK28sUwMdHmp-d9sNrCvcBkPf2ZBNvddjXqO22OfOdjQBPkrHPLJjlN1YkKRmCNS-_QuDWQrP8-QCmS_LrCrWRFx59ujxD1BFjLM5niWDfIBqMzOxoaeMHq-h5ri4nJcq22oHOiXC-BO_CSKbB3yae6TzKQNi6SPAsulbVFNBNTCPjJTyYcw94q67PNCYeWN915yah2nWOGzMVUcnRwdcfQ7kGMjEZqLkARfw49u-gTPkj0umB373Ud1dOkCLz18mAjCDhwnei32jYjOHkf6N_OEUjliof35VmkrqkRTHQEJmlpclvbDJ7UY1ugTYealPD4QUgpNjCWzl7jMEUTjTew-Ftp5w2In1XA8aq-TBSgXR5QCuayseDyWqp6uqz8fbTBMA2GF9xKso2-6R86ZzciI5duy_u1)




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
- Canva/Slides: **[Add your link here]**

---




---

## 🏫 School Name
**Claflin University**

---

## 🏷 Team Name
**Palmetto-Panthers**

---

## ✨ Contributors

**April Ossai** 
**Subash Neupane** 
**Amrinder Singh** 
**Javarius**

> 🏆 Built for equitable access to homeownership readiness.
