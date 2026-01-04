from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    """Display all tasks for the current user"""
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(
        Task.due_date.asc(),
        Task.priority.desc(),
        Task.created_at.desc()
    ).all()
    
    # Filter tasks by status if requested
    status_filter = request.args.get('status')
    if status_filter:
        tasks = [task for task in tasks if task.status == status_filter]
    
    # Count tasks by status
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    stats = {
        'total': len(all_tasks),
        'pending': len([t for t in all_tasks if t.status == 'pending']),
        'in_progress': len([t for t in all_tasks if t.status == 'in_progress']),
        'completed': len([t for t in all_tasks if t.status == 'completed'])
    }
    
    from datetime import date
    today = date.today()
    
    return render_template('dashboard.html', tasks=tasks, stats=stats, status_filter=status_filter, today=today)


@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date')
        
        if not title:
            flash('Task title is required', 'error')
            return render_template('create_task.html')
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return render_template('create_task.html')
        
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=current_user.id
        )
        
        try:
            db.session.add(task)
            db.session.commit()
            flash('Task created successfully!', 'success')
            return redirect(url_for('tasks.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the task', 'error')
            return render_template('create_task.html')
    
    return render_template('create_task.html')


@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task"""
    task = Task.query.get_or_404(task_id)
    
    # Ensure the task belongs to the current user
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task', 'error')
        return redirect(url_for('tasks.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status', 'pending')
        priority = request.form.get('priority', 'medium')
        due_date_str = request.form.get('due_date')
        
        if not title:
            flash('Task title is required', 'error')
            return render_template('edit_task.html', task=task)
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format', 'error')
                return render_template('edit_task.html', task=task)
        
        task.title = title
        task.description = description
        task.status = status
        task.priority = priority
        task.due_date = due_date
        task.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the task', 'error')
            return render_template('edit_task.html', task=task)
    
    return render_template('edit_task.html', task=task)


@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    
    # Ensure the task belongs to the current user
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task', 'error')
        return redirect(url_for('tasks.dashboard'))
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the task', 'error')
    
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_status(task_id):
    """Update task status via AJAX"""
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['pending', 'in_progress', 'completed']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    task.status = new_status
    task.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash('Task status updated successfully!', 'success')
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred while updating the status'}), 500

