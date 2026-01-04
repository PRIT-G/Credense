from flask import Blueprint, render_template, request, session, redirect, url_for
from core.test_generator import generate_test
from core.scorer import calculate_score
from utils.user_manager import UserManager
import datetime

test_bp = Blueprint('test', __name__)
user_manager = UserManager()

@test_bp.route('/start_test', methods=['POST'])
def start_test():
    # User confirmed skills, generate test
    skills = session.get('detected_skills', [])
    level = session.get('detected_level', 'Intermediate')
    questions = generate_test(skills, level=level)
    session['test_questions'] = questions
    return redirect(url_for('test.test_page'))

@test_bp.route('/test')
def test_page():
    questions = session.get('test_questions', [])
    if not questions:
        return redirect(url_for('upload.upload_page'))
    return render_template('skill_test.html', questions=questions)

@test_bp.route('/submit_test', methods=['POST'])
def submit_test():
    user_answers = request.form.to_dict()
    questions = session.get('test_questions', [])
    
    # Build correct answers map
    correct_answers = {str(q['id']): q['answer'] for q in questions}
    
    clean_user_answers = {}
    for key, value in user_answers.items():
        if key.startswith('q_'):
            q_id = key.split('_')[1]
            clean_user_answers[q_id] = value
            
    score = calculate_score(clean_user_answers, correct_answers)
    session['score'] = score
    
    # Persist score to user profile
    user = session.get('user')
    if user and user.get('role') == 'employee':
        # Retrieve current scores
        current_user_data = user_manager.get_user(user['username'])
        scores = current_user_data.get('scores', {})
        
        # Add new score. Assuming General Assessment for now as skill specific logic in generator is opaque here.
        # Ideally we loop through questions, find their skill, and average.
        # For this hackathon scope: "Assessment <Date>"
        score_key = f"Assessment {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        scores[score_key] = score
        
        user_manager.update_user(user['username'], scores=scores)

    return redirect(url_for('result.result'))
