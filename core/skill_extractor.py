import re

def extract_skills(text):
    """
    Extracts skills, expertise level, and years of experience from text.
    Returns a dict with 'skills', 'level', and 'years'.
    """
    found_skills = set()
    text_lower = text.lower()
    
    keywords = {
        'python': ['python', 'pandas', 'numpy', 'flask', 'django', 'scipy'],
        'sql': ['sql', 'mysql', 'postgresql', 'database', 'sqlite', 'oracle'],
        'ml': ['machine learning', 'deep learning', 'scikit-learn', 'tensorflow', 'keras', 'pytorch', 'ai', 'artificial intelligence'],
        'dsa': ['data structures', 'algorithms', 'sorting', 'searching', 'linked list', 'graph', 'tree', 'queue', 'stack'],
        'web': ['html', 'css', 'javascript', 'react', 'node', 'frontend', 'backend', 'full stack', 'angular', 'vue'],
        'c': ['c programming', 'pointers', 'memory management'],
        'cpp': ['c++', 'cpp', 'stl', 'object oriented'],
        'java': ['java', 'spring', 'hibernate', 'jvm', 'j2ee'],
        'computernetwork': ['computer network', 'networking', 'tcp/ip', 'osi model', 'http', 'https', 'dns'],
        'os': ['operating system', 'linux', 'unix', 'shell scripting', 'bash', 'concurrency', 'multithreading'],
        'cloud': ['aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'cloud computing'],
        'dbms': ['dbms', 'database management system', 'relational database', 'nosql', 'mongodb', 'redis']
    }

    for skill, terms in keywords.items():
        for term in terms:
            if skill == 'c' and term == 'c programming':
                 if re.search(r'\bc\b', text_lower) or re.search(r'c programming', text_lower):
                     found_skills.add(skill)
                     break
            elif re.search(r'\b' + re.escape(term) + r'\b', text_lower):
                found_skills.add(skill)
                break
    
    # Detect Level
    level = "Intermediate" # Default
    if any(word in text_lower for word in ['senior', 'lead', 'architect', 'principal', 'expert']):
        level = "Senior"
    elif any(word in text_lower for word in ['junior', 'intern', 'fresher', 'entry', 'beginner']):
        level = "Junior"

    # Detect Years of Experience (Basic heuristic)
    years = 0
    patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?'
    ]
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                years = int(match.group(1))
                break
            except:
                pass

    # Refine level based on years if available
    if years >= 5:
        level = "Senior"
    elif years > 0 and years < 2:
        level = "Junior"

    return {
        "skills": list(found_skills),
        "level": level,
        "years": years
    }
