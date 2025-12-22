from supabase.client import Client
from typing import Any
from datetime import date
from enum import Enum

class Status(Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

class InsightsService:
    @staticmethod
    def upsert(db: Client, user: Any, insights: str):
        try:
            today = date.today()
            period = today.strftime("%Y-%m")
            email = user.email
            db.table("email_job").upsert({
                "idempotency_key": f"monthly:{user.id}:{period}",
                "user_id": user.id,
                'period': period,
                "status": Status.PENDING.value,
                "payload": {
                    "to": email,
                    "subject": f"Your Food Insights for {period}",
                    "content": insights
                }
            },
            on_conflict="idempotency_key"
            ).execute()
        except Exception as e:
            print(f"Error upserting email: {e}")
            raise e