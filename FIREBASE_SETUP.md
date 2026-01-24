# Firebase Push Notification Setup Guide

This guide explains how to set up and use the Firebase Cloud Messaging (FCM) system integrated into the project.

## 1. Firebase Console Configuration

1.  Go to the [Firebase Console](https://console.firebase.google.com/).
2.  Create a new project (or select an existing one).
3.  Go to **Project Settings** (gear icon) -> **Service Accounts**.
4.  Click **Generate New Private Key**.
5.  A JSON file will be downloaded. **Rename this file to `firebase-adminsdk.json`**.
6.  Place this file in the **root directory** of your project (the same folder as `manage.py`).

## 2. Dependencies & Database

1.  Ensure you have installed the requirements:
    ```bash
    pip install firebase-admin
    ```
2.  Run migrations to create the `DeviceToken` table:
    ```bash
    python manage.py makemigrations notifications
    python manage.py migrate notifications
    ```

## 3. How to Register Device Tokens

Before a user can receive push notifications, their device (mobile/web) must register its FCM token with the backend.

-   **Endpoint:** `POST /notify/tokens/`
-   **Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
-   **Body (JSON):**
    ```json
    {
        "token": "YOUR_FCM_DEVICE_TOKEN_HERE",
        "platform": "android" 
    }
    ```
    *(Platform options: `android`, `ios`, `web`)*

## 4. Testing the Notifications

### Automated Triggers:
Notifications are automatically sent in the following scenarios:
1.  **Chat Messages**: When a user receives a message in a private chat or group.
2.  **Manual Calls**: When using `notifications.helper.send_notification(user, title, message)`.

### Testing via Postman:
1.  Log in as **User A** and get the token.
2.  Send a `POST` request to `/notify/tokens/` with a fake (or real) FCM token.
3.  Log in as **User B** and send a chat message to **User A**.
4.  Check the Django Console/Terminal. You should see:
    -   `✅ FCM Multicast sent` (If the token is valid)
    -   `🗑️ Invalid token removed` (If the token was fake/expired)

## 5. Troubleshooting (Bengali)

-   **Service Account Error:** যদি ফাইলটি রুট ফোল্ডারে না থাকে, তবে টার্মিনালে `⚠️ Firebase service account file not found` মেসেজ আসবে।
-   **Invalid Token:** আপনি যদি কোনো র‍্যান্ডম স্ট্রিং টোকেন হিসেবে সেভ করেন, Firebase সেটাকে রিজেক্ট করে দিবে এবং আমাদের কোডটি অটোমেটিক ডাটাবেজ থেকে ওই টোকেনটি ডিলিট করে দিবে।
-   **Notifications Not Received:** চেক করুন ইউজারের জন্য ডাটাবেজে অন্তত একটি ভ্যালিড টোকেন আছে কি না। `python manage.py shell`-এ গিয়ে `DeviceToken.objects.all()` চেক করতে পারেন।

---
**Note:** Always keep the `firebase-adminsdk.json` file private. Do not commit it to version control (it is already in `.gitignore`).
