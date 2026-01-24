import os
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from pathlib import Path
from .models import DeviceToken

def initialize_firebase():
    """
    Initializes Firebase Admin SDK if not already initialized.
    """
    if not firebase_admin._apps:
        # Try to find the service account key file
        cred_path = os.path.join(settings.BASE_DIR, 'firebase-adminsdk.json')
        
        if os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("✅ Firebase Admin SDK Initialized")
            except Exception as e:
                print(f"❌ Firebase Initialization Error: {e}")
        else:
            print(f"⚠️ Firebase service account file not found at {cred_path}. Push notifications will not be sent.")

def send_push_notification(user, title, message, data=None):
    """
    Sends FCM push notification to all devices registered for the user.
    """
    initialize_firebase()
    
    if not firebase_admin._apps:
        return

    tokens = list(DeviceToken.objects.filter(user=user).values_list('token', flat=True))
    
    if not tokens:
        print(f"ℹ️ No device tokens found for user {user.email}")
        return

    # Create the message
    notification = messaging.Notification(
        title=title,
        body=message,
    )

    # Use Multicast to send to multiple tokens at once
    fcm_message = messaging.MulticastMessage(
        notification=notification,
        data=data or {},
        tokens=tokens,
    )

    try:
        response = messaging.send_multicast(fcm_message)
        print(f"✅ FCM Multicast sent. Success count: {response.success_count}, Failure count: {response.failure_count}")
        
        # Optionally cleanup invalid tokens
        if response.failure_count > 0:
            for index, res in enumerate(response.responses):
                if not res.success:
                    # Token is likely invalid or expired
                    DeviceToken.objects.filter(token=tokens[index]).delete()
                    print(f"🗑️ Invalid token removed: {tokens[index]}")
                    
    except Exception as e:
        print(f"❌ Error sending FCM message: {e}")
