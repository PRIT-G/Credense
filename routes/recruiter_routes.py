from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import json
import os
from utils.user_manager import UserManager

recruiter_bp = Blueprint('recruiter', __name__)
user_manager = UserManager()

def login_required_recruiter(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')
        if not user or user.get('role') != 'recruiter':
            flash('Recruiter access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@recruiter_bp.route('/recruiter/dashboard')
@login_required_recruiter
def dashboard():
    # Load all users to filter employees
    all_users = user_manager.load_users()
    employees = {k: v for k, v in all_users.items() if v.get('role') == 'employee'}
    
    # Load all questions
    questions_data = {}
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mcq_bank')
    if os.path.exists(base_path):
        for filename in os.listdir(base_path):
            if filename.endswith('.json'):
                skill_name = filename.replace('.json', '')
                try:
                    with open(os.path.join(base_path, filename), 'r') as f:
                        questions_data[skill_name] = json.load(f)
                except json.JSONDecodeError:
                    questions_data[skill_name] = []

    return render_template('dashboard_recruiter.html', employees=employees, questions_data=questions_data)

@recruiter_bp.route('/recruiter/add_question', methods=['POST'])
@login_required_recruiter
def add_question():
    skill = request.form.get('skill')
    question_text = request.form.get('question')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    correct_answer = request.form.get('correct_answer')
    
    if not all([skill, question_text, option1, option2, option3, option4, correct_answer]):
         flash('All fields are required', 'error')
         return redirect(url_for('recruiter.dashboard', tab='questions'))

    # Load JSON
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mcq_bank')
    os.makedirs(base_path, exist_ok=True)
    
    file_path = os.path.join(base_path, f"{skill.lower()}.json")
    
    data = []
    if os.path.exists(file_path):
        with open(file_path, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    
    new_id = len(data) + 1
    new_q = {
        "id": new_id,
        "question": question_text,
        "options": [option1, option2, option3, option4],
        "answer": correct_answer
    }
    
    data.append(new_q)
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
            
    flash(f'Question added successfully to {skill}!', 'success')
    return redirect(url_for('recruiter.dashboard', tab='questions'))

@recruiter_bp.route('/recruiter/delete_question/<skill>/<int:q_id>')
@login_required_recruiter
def delete_question(skill, q_id):
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mcq_bank')
    file_path = os.path.join(base_path, f"{skill}.json")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Filter out the question
        new_data = [q for q in data if q['id'] != q_id]
        
        # Re-save
        with open(file_path, 'w') as f:
            json.dump(new_data, f, indent=4)
        flash('Question deleted.', 'success')
    else:
        flash('Skill file not found.', 'error')
        
    return redirect(url_for('recruiter.dashboard', tab='questions'))

@recruiter_bp.route('/recruiter/edit_question', methods=['POST'])
@login_required_recruiter
def edit_question():
    skill = request.form.get('skill')
    q_id = int(request.form.get('q_id'))
    question_text = request.form.get('question')
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    option3 = request.form.get('option3')
    option4 = request.form.get('option4')
    correct_answer = request.form.get('correct_answer')
    
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mcq_bank')
    file_path = os.path.join(base_path, f"{skill}.json")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        for q in data:
            if q['id'] == q_id:
                q['question'] = question_text
                q['options'] = [option1, option2, option3, option4]
                q['answer'] = correct_answer
                break
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        flash('Question updated.', 'success')
    
    return redirect(url_for('recruiter.dashboard', tab='questions'))
@recruiter_bp.route('/recruiter/delete_candidate/<username>')
@login_required_recruiter
def delete_candidate(username):
    # Security check: Ensure we only delete employees, not admins or other recruiters
    # (unless we want to allow that, but safer to restrict)
    user = user_manager.get_user(username)
    if user and user.get('role') == 'employee':
        if user_manager.delete_user(username):
            flash(f'Candidate {username} deleted successfully.', 'success')
        else:
            flash('Failed to delete user.', 'error')
    else:
        flash('Cannot delete this user (Invalid permission or user not found).', 'error')
        
    return redirect(url_for('recruiter.dashboard'))
