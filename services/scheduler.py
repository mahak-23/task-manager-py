from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask
from services.email_service import send_daily_task_notifications
import atexit

scheduler = BackgroundScheduler()

def init_scheduler(app: Flask):
    """Initialize the scheduler for daily email notifications"""
    with app.app_context():
        # Schedule daily emails at 8:00 AM UTC (adjust timezone as needed)
        scheduler.add_job(
            func=send_daily_task_notifications,
            trigger=CronTrigger(hour=8, minute=0),  # 8 AM UTC daily
            id='daily_task_notifications',
            name='Send daily task notifications',
            replace_existing=True
        )
        
        scheduler.start()
        
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

