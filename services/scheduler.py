from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from services.email_service import send_daily_task_notifications
import atexit

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def init_scheduler(app):
    """Initialize the scheduler for daily email notifications"""

    scheduler.add_job(
        func=send_daily_task_notifications,
        trigger=CronTrigger(hour=8, minute=0),  # ✅ 8:00 AM daily (UTC)
        args=[app],
        id="daily_task_notifications",
        replace_existing=True,
    )

    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
