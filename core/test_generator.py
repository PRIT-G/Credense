import json
import random
import os

from core.ai_generator import generate_questions_ai

def generate_test(skills, level='Intermediate', num_total_questions=15):
    """
    Generates a test based on detected skills and level.
    Tries AI generation first, falls back to local JSON bank.
    """
    # 1. Try AI Generation
    ai_questions = generate_questions_ai(skills, level, num_questions=num_total_questions)
    if ai_questions and len(ai_questions) >= num_total_questions:
        return ai_questions[:num_total_questions]
    
    # 2. Fallback or Padding with Local JSON
    test_questions = ai_questions if ai_questions else []
    if test_questions:
        print(f"DEBUG: AI returned {len(test_questions)} questions. Padding to reach {num_total_questions}.")
    else:
        print(f"DEBUG: Falling back to local bank for {num_total_questions} questions at {level} level.")

    base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mcq_bank')
    
    # 2a. Attempt to get from Specific Skills
    pool = []
    for skill in (skills or []):
        file_path = os.path.join(base_path, f"{skill}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    all_questions = json.load(f)
                    for q in all_questions:
                        q['skill'] = skill
                    pool.extend(all_questions)
                except Exception as e:
                    print(f"DEBUG: Error loading {skill}.json: {e}")
    
    # 2b. Add General Questions to Pool
    general_path = os.path.join(base_path, "general.json")
    if os.path.exists(general_path):
        with open(general_path, 'r') as f:
            try:
                general_qs = json.load(f)
                for q in general_qs:
                    q['skill'] = "General"
                pool.extend(general_qs)
            except Exception as e:
                print(f"DEBUG: Error loading general.json: {e}")

    # 2c. If pool still too small, pull from EVERYTHING available
    if len(pool) < num_total_questions:
        print("DEBUG: Specific + General pool too small. Pulling from ALL available packs.")
        for file in os.listdir(base_path):
            if file.endswith(".json") and file not in [f"{s}.json" for s in skills] and file != "general.json":
                with open(os.path.join(base_path, file), 'r') as f:
                    try:
                        other_qs = json.load(f)
                        for q in other_qs:
                            q['skill'] = file.split('.')[0]
                        pool.extend(other_qs)
                    except:
                        pass

    if not pool:
        print("DEBUG: Local question pool is empty even after pulling all.")
        return []

    # Filter Pool by Level (with soft fallback)
    level_pool = [q for q in pool if q.get('level') == level]
    if not level_pool and (level == 'Senior' or level == 'Junior' or level == 'Expert'):
        # Senior/Expert fallback to Intermediate
        level_pool = [q for q in pool if q.get('level') == 'Intermediate']
    
    if not level_pool:
        level_pool = pool

    # Sample exactly 15
    num_to_sample = min(len(level_pool), num_total_questions)
    test_questions = random.sample(level_pool, num_to_sample)
    
    # FINAL SAFETY: If somehow still < 15, and we have more in pool, just grab from anywhere
    if len(test_questions) < num_total_questions:
        remaining = num_total_questions - len(test_questions)
        others = [q for q in pool if q not in test_questions]
        test_questions.extend(random.sample(others, min(len(others), remaining)))

    print(f"DEBUG: Final local test size: {len(test_questions)}")
    
    # Shuffle and Re-index
    random.shuffle(test_questions)
    for idx, q in enumerate(test_questions):
        q['id'] = idx + 1

    return test_questions
