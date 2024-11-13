from datetime import datetime, timedelta
from firebase_admin import messaging

class FCMManager:
    """Firebase Cloud Messaging Manager"""
    def __init__(self):
        self.last_notification = {}
        self.notification_cooldown = timedelta(minutes=15)

    def send_notification(self, token, title, body, data=None):
        """Send FCM notification"""
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=token,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        icon='energy_icon',
                        color='#2d8bac',
                        sound='default'
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound='default',
                            badge=1
                        )
                    )
                )
            )
            response = messaging.send(message)
            return True
        except Exception as e:
            print(f"FCM notification error: {e}")
            return False

    def can_send_notification(self, user_id):
        """Check if notification can be sent based on cooldown"""
        now = datetime.now()
        if user_id in self.last_notification:
            if now - self.last_notification[user_id] < self.notification_cooldown:
                return False
        self.last_notification[user_id] = now
        return True
