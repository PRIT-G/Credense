from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.user_manager import UserManager
import random
import string

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()

def generate_captcha():
    """Generates a simple 5-character alphanumeric captcha."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        captcha = generate_captcha()
        session['captcha'] = captcha
        return render_template('login.html', captcha=captcha)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        captcha_input = request.form.get('captcha')
        
        # Verify Captcha
        if not captcha_input or captcha_input.upper() != session.get('captcha', '').upper():
            flash('Invalid Captcha. Please try again.', 'error')
            return redirect(url_for('auth.login'))
        
        # Authenticate User
        user = user_manager.authenticate(username, password)
        if user:
            session['user'] = user
            flash(f"Welcome back, {user.get('name', username)}!", 'success')
            
            # Redirect based on role
            role = user.get('role')
            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'recruiter':
                return redirect(url_for('recruiter.dashboard'))
            elif role == 'employee':
                return redirect(url_for('employee.dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Public registration for Employees."""
    if request.method == 'GET':
        return render_template('register.html') # Need to create this or reuse login with mode
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if not username or not password:
             flash('Username and password are required.', 'error')
             return redirect(url_for('auth.register'))

        if user_manager.create_user(username, password, role='employee', name=name):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))
