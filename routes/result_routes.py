from flask import Blueprint, render_template, session

result_bp = Blueprint('result', __name__)

@result_bp.route('/result')
def result():
    score = session.get('score', 0)
    skills = session.get('detected_skills', [])
    return render_template('result.html', score=score, skills=skills)
