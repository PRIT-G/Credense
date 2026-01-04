from flask import Blueprint, render_template, session, redirect, url_for, flash
from utils.user_manager import UserManager

employee_bp = Blueprint('employee', __name__)
user_manager = UserManager()

@employee_bp.route('/employee/dashboard')
def dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'employee':
        return redirect(url_for('auth.login'))
    
    # Reload user data to get latest scores/status
    full_user_data = user_manager.get_user(user['username'])
    
    return render_template('dashboard_employee.html', user=full_user_data)
