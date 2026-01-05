from google import genai
import json
import os
from flask import current_app

def generate_questions_ai(skills, level, num_questions=15):
    """
    Generates MCQ questions using Gemini API based on skills and expertise level.
    """
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key or api_key == 'YOUR_API_KEY_HERE' or not api_key:
        print("DEBUG: AI Generation skipped - Gemini API Key missing or default.")
        return None

    print(f"DEBUG: Attempting AI generation for {num_questions} questions at {level} level for skills: {skills}")
    
    try:
        client = genai.Client(api_key=api_key)
        
        difficulty_note = ""
        if level == "Senior" or level == "Expert":
            difficulty_note = "Match difficulty for a Senior/Expert level candidate. Focus on architectural trade-offs, scalability, and deep internal workings."
        elif level == "Intermediate":
            difficulty_note = "Match difficulty for an Intermediate level candidate. Focus on design patterns, best practices, and performance optimization."
        else:
            difficulty_note = "Match difficulty for a Junior level candidate. Focus on core fundamentals and basic problem-solving."
    
        prompt = f"""
        You are an expert technical interviewer and hiring manager.
        Your task is to generate a role-specific assessment quiz for a job applicant.
        
        The quiz must evaluate:
        1. Core skills required for the technical domain: {", ".join(skills)}
        2. Practical, real-world problem-solving ability
        3. Conceptual understanding appropriate to the experience level: {level}
        
        Follow these rules strictly:
        - Generate EXACTLY {num_questions} (fifteen) multiple-choice questions (MCQs).
        - Questions must be relevant to the candidate's skills: {", ".join(skills)}.
        - Prefer practical and scenario-based questions over pure theory.
        - Avoid irrelevant or outdated technologies.
        - {difficulty_note}
        
        The output MUST be a valid JSON array of objects. Each object must have:
        - id: A unique integer.
        - question: The question text.
        - options: A list of 4 strings.
        - answer: The correct option string (matching one of the options).
        
        Return ONLY the raw JSON array.
        """
    
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        result_text = response.text.strip()
        
        # Clean markdown
        if result_text.startswith('```'):
            result_text = '\n'.join(result_text.split('\n')[1:-1])
        
        questions = json.loads(result_text.strip())
        print(f"DEBUG: Successfully generated {len(questions)} AI questions.")
        
        for i, q in enumerate(questions):
            q['id'] = i + 1
            if 'skill' not in q:
                q['skill'] = 'AI-Generated'
        
        return questions
    except Exception as e:
        print(f"DEBUG: AI Generation failed: {e}")
        return None
