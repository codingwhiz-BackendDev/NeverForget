# Birthday Notification System

## Quick Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Generate VAPID keys:**

   ```bash
   python generate_vapid_keys.py
   ```

3. **Update settings.py** with your VAPID keys:

   ```python
   VAPID_PRIVATE_KEY = 'your_private_key_here'
   VAPID_PUBLIC_KEY = 'your_public_key_here'
   VAPID_CLAIMS = {
       'sub': 'mailto:your-email@example.com',
       'aud': 'https://fcm.googleapis.com'
   }
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Testing

### Test Push Notifications

```bash
# Send test notification
curl -X POST http://127.0.0.1:8000/api/trigger-birthday-notifications/ \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### Check Today's Birthdays

```bash
# Dry run (won't send notifications)
python manage.py check_birthdays --dry-run

# Send actual notifications
python manage.py check_birthdays
```

## How It Works

1. **Daily check** via `check_birthdays` management command
2. **Finds birthdays** for today's date
3. **Sends notifications** to community owners
4. **Logs results** for tracking

## Automation

Set up a daily cron job:

```bash
# Check birthdays daily at 9 AM
0 9 * * * cd /path/to/project && python manage.py check_birthdays
```

## API Endpoints

- `POST /api/trigger-birthday-notifications/` - Manual trigger
- `GET/POST /api/notification-preferences/` - User preferences
- `GET /api/notification-logs/` - Notification history

The system automatically sends push notifications when there are birthdays to celebrate!
