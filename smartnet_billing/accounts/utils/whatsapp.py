import requests
from django.conf import settings

def send_whatsapp_otp(phone_number: str, otp: str):
    """
    phone_number: International format, e.g., '+255757123456' (no spaces)
    otp: 6-digit code
    """
    url = f"https://graph.facebook.com/v20.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "verification_code",  # Your approved template name
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": otp}
                    ]
                }
            ]
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print("WhatsApp Error:", response.json())  # Log for debugging
        return False