from flask import current_app
from flask_mail import Mail, Message
from models import db, Task, User
from datetime import date, datetime

mail = Mail()

def send_daily_task_notifications():
    """Send daily email notifications to all users about today's tasks"""
    try:
        users = User.query.all()
        today = date.today()
        
        for user in users:
            # Get today's tasks ordered by priority
            today_tasks = Task.query.filter_by(user_id=user.id).filter(
                Task.due_date == today,
                Task.status != 'completed'
            ).order_by(
                Task.priority.desc(),
                Task.created_at.asc()
            ).all()
            
            if not today_tasks:
                continue  # Skip users with no tasks due today
            
            # Organize tasks by priority
            high_priority = [t for t in today_tasks if t.priority == 'high']
            medium_priority = [t for t in today_tasks if t.priority == 'medium']
            low_priority = [t for t in today_tasks if t.priority == 'low']
            
            # Create email content
            subject = f"📋 Your Tasks for Today - {today.strftime('%B %d, %Y')}"
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4CAF50;">Good Morning, {user.username}!</h2>
                    <p>Here are your tasks due today ({today.strftime('%B %d, %Y')}):</p>
                    
                    {f'''
                    <div style="background-color: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 15px 0;">
                        <h3 style="margin-top: 0; color: #c62828;">🔴 High Priority ({len(high_priority)} tasks)</h3>
                        <ul>
                        {''.join([f'<li><strong>{task.title}</strong> - {task.description or "No description"}</li>' for task in high_priority])}
                        </ul>
                    </div>
                    ''' if high_priority else ''}
                    
                    {f'''
                    <div style="background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; margin: 15px 0;">
                        <h3 style="margin-top: 0; color: #e65100;">🟠 Medium Priority ({len(medium_priority)} tasks)</h3>
                        <ul>
                        {''.join([f'<li><strong>{task.title}</strong> - {task.description or "No description"}</li>' for task in medium_priority])}
                        </ul>
                    </div>
                    ''' if medium_priority else ''}
                    
                    {f'''
                    <div style="background-color: #e8f5e9; border-left: 4px solid #4CAF50; padding: 15px; margin: 15px 0;">
                        <h3 style="margin-top: 0; color: #2e7d32;">🟢 Low Priority ({len(low_priority)} tasks)</h3>
                        <ul>
                        {''.join([f'<li><strong>{task.title}</strong> - {task.description or "No description"}</li>' for task in low_priority])}
                        </ul>
                    </div>
                    ''' if low_priority else ''}
                    
                    <p style="margin-top: 30px;">
                        <a href="{current_app.config.get('APP_URL', 'http://localhost:5000')}/dashboard" 
                           style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            View All Tasks
                        </a>
                    </p>
                    
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        This is an automated email from Task Manager. 
                        You're receiving this because you have tasks due today.
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
Good Morning, {user.username}!

Here are your tasks due today ({today.strftime('%B %d, %Y')}):

"""
            if high_priority:
                text_body += f"\nHIGH PRIORITY ({len(high_priority)} tasks):\n"
                for task in high_priority:
                    text_body += f"- {task.title}: {task.description or 'No description'}\n"
            
            if medium_priority:
                text_body += f"\nMEDIUM PRIORITY ({len(medium_priority)} tasks):\n"
                for task in medium_priority:
                    text_body += f"- {task.title}: {task.description or 'No description'}\n"
            
            if low_priority:
                text_body += f"\nLOW PRIORITY ({len(low_priority)} tasks):\n"
                for task in low_priority:
                    text_body += f"- {task.title}: {task.description or 'No description'}\n"
            
            # Send email
            msg = Message(
                subject=subject,
                recipients=[user.email],
                html=html_body,
                body=text_body
            )
            
            mail.send(msg)
            current_app.logger.info(f"Daily notification sent to {user.email}")
        
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending daily notifications: {str(e)}")
        return False

