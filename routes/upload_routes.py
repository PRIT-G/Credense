from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import os
from werkzeug.utils import secure_filename
from core.resume_parser import parse_resume
from core.skill_extractor import extract_skills
from utils.user_manager import UserManager

upload_bp = Blueprint('upload', __name__)
user_manager = UserManager()

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_page():
    # Renamed function to avoid conflict with blueprint name if needed, but endpoint is /upload
    # Checking auth
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.register'))
    if user.get('role') != 'employee':
        flash('Only employees can upload resumes.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'resume' not in request.files:
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process Resume
            text = parse_resume(filepath)
            analysis = extract_skills(text)
            skills = analysis['skills']
            level = analysis['level']
            
            # Store in session
            session['detected_skills'] = skills
            session['detected_level'] = level
            session['filename'] = filename
            
            # Update User Profile if logged in
            if user:
                user_manager.update_user(
                    user['username'],
                    resume_uploaded=True,
                    resume_path=filename,
                    detected_skills=skills,
                    expertise_level=level
                )
            
            return redirect(url_for('upload.detected_skills'))
            
    return render_template('upload.html')

@upload_bp.route('/detected_skills')
def detected_skills():
    skills = session.get('detected_skills', [])
    level = session.get('detected_level', 'Intermediate')
    return render_template('detected_skills.html', skills=skills, level=level)
