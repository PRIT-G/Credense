from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.user_manager import UserManager

admin_bp = Blueprint('admin', __name__)
user_manager = UserManager()

def login_required_admin(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')
        if not user or user.get('role') != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/dashboard')
@login_required_admin
def dashboard():
    users = user_manager.load_users()
    # Filter out sensitive data only if necessary for view, but admin sees all ideally
    return render_template('dashboard_admin.html', users=users, user=session.get('user'))

@admin_bp.route('/admin/create_user', methods=['POST'])
@login_required_admin
def create_user():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    name = request.form.get('name')
    
    if not all([username, password, role]):
        flash('All fields are required.', 'error')
    elif user_manager.create_user(username, password, role, name=name):
        flash(f'User {username} created successfully.', 'success')
    else:
        flash(f'User {username} already exists.', 'error')
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/delete_user/<username>')
@login_required_admin
def delete_user(username):
    if username == 'admin': # Prevent deleting default admin
        flash('Cannot delete root admin user.', 'error')
    elif user_manager.delete_user(username):
        flash(f'User {username} deleted.', 'success')
    else:
        flash(f'Failed to delete user {username}.', 'error')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/update_user', methods=['POST'])
@login_required_admin
def update_user():
    current_username = request.form.get('current_username')
    new_username = request.form.get('new_username')
    name = request.form.get('name')
    new_password = request.form.get('new_password')
    
    # Handle Rename
    if new_username and new_username != current_username:
        if user_manager.rename_user(current_username, new_username):
            flash(f'Renamed {current_username} to {new_username}.', 'success')
            current_username = new_username # Continue updates on new name
        else:
            flash(f'Failed to rename {current_username} (Target might exist).', 'error')
            return redirect(url_for('admin.dashboard'))

    # Handle Name Update
    if name:
        user_manager.update_user(current_username, name=name)

    # Handle Password Update
    if new_password:
        if user_manager.reset_password(current_username, new_password):
            flash(f'Password updated for {current_username}.', 'success')
        else:
            flash(f'Failed to update password for {current_username}.', 'error')
        
    return redirect(url_for('admin.dashboard'))
