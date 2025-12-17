from supabase.client import Client

class EmailService:
    @staticmethod
    def send(db: Client, to: str, content: str):
        try:
            subject = "Your Food Insights"
            body = f"Hello,\n\nHere are your food insights:\n\n{content}\n\nBest regards,\nFood Tracker Team"
            db.functions.invoke("resend-email", {
                "to": to,
                "subject": subject,
                "html": body
            })
        except Exception as e:
            print(f"Error sending email: {e}")
            raise e