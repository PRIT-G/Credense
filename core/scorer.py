def calculate_score(user_answers, correct_answers):
    """
    Calculates the score.
    user_answers: dict {question_id: selected_option}
    correct_answers: dict {question_id: correct_option}
    """
    total = len(correct_answers)
    if total == 0:
        return 0
    
    correct_count = 0
    for q_id, answer in user_answers.items():
        if correct_answers.get(q_id) == answer:
            correct_count += 1
            
    return int((correct_count / total) * 100)
