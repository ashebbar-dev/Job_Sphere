from flask_mail import Message
from flask import current_app
import openai
import os

def send_email_notification(to, subject, body):
    """Send email notification"""
    try:
        # Get mail instance from app extensions
        mail = current_app.extensions.get('mail')

        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[to]
        )
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def generate_ai_email(context, purpose):
    """Generate AI-powered email content using OpenAI"""
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""Generate a professional email for the following purpose: {purpose}

Context: {context}

Generate ONLY the email body text without subject line. Keep it professional, concise, and friendly."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional email writer for a college placement system."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"AI email generation error: {e}")
        return None
