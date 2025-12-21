from supabase.client import Client
from datetime import date
from enum import Enum

class Status(Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"

class InsightsService:
    @staticmethod
    def upsert(db: Client, user_id: str, insights: str):
        try:
            today = date.today()
            period = today.strftime("%Y-%m")
            user = db.auth.get_user(user_id).user
            email = user.email
            db.table("email_job").upsert({
                "idempotency_key": f"monthly:{user_id}:{period}",
                "user_id": user_id,
                'period': period,
                "status": Status.PENDING,
                "payload": {
                    "to": email,
                    "subject": f"Your Food Insights for {period}",
                    "content": insights
                }
            },
            on_conflict="idempotency_key"
            ).execute()

            db.rpc("pgmq_send", {
                "queue_name": "email_jobs",
                "message": {
                    "job_key": f"monthly:{user_id}:{period}",
                }
            }).execute()
        except Exception as e:
            print(f"Error upserting email: {e}")
            raise e