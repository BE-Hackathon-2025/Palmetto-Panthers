import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

if not firebase_admin._apps:
    cred = credentials.Certificate("Backend/config/firebase_service_key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

uid = "xenfzFaXTmWWwpbxQFw6hyUji8I2"  # existing user UID

readiness_data = {
    "credit_score": 620,
    "monthly_income": 2800,
    "monthly_debt": 950,
    "down_payment_savings": 3500,
    "emergency_savings_months": 1,
    "employment_status": "Full-time",
    "years_stable_income": 1,
    "monthly_rent": 1100,
    "expected_home_price": 220000,
    "readiness_score": 60,
    "qualification_threshold": 78,
    "summary": (
        "**Updated User Summary:** Subash currently has a readiness score of 60. "
        "With full-time employment and moderate debt, the focus should be on increasing emergency savings "
        "and improving the credit score to at least 640+. The estimated home budget is $220K, "
        "requiring an additional $4-5K in down payment funds for readiness."
    ),
    "last_updated": datetime.now(),
}

# Merge to existing user doc
db.collection("users").document(uid).set(readiness_data, merge=True)

print(f"✅ User {uid} readiness profile updated successfully.")