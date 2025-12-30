def infer_job_role(job_text):
    job_text = job_text.lower()

    if any(x in job_text for x in ["data analyst", "business insights", "power bi", "dashboard"]):
        return "data_analyst"

    if any(x in job_text for x in ["ml", "machine learning", "tensorflow", "pytorch", "model"]):
        return "ml_intern"

    if any(x in job_text for x in ["backend", "flask", "api", "server", "deployment"]):
        return "backend_intern"

    if any(x in job_text for x in ["software", "c++", "java", "debugging"]):
        return "software_intern"

    return "general"


RECOMMENDATION_RULES = {

    "flask": "Build a small Flask API project and deploy it locally or on Render",
    "api": "Include one project where you consume or expose a REST API",
    "backend": "Add a backend mini-project (authentication, CRUD, API routing)",

    "sql": "Do a dataset project using SQL queries (joins, filtering, aggregations)",
    "excel": "Add an Excel data cleaning or reporting project",
    "power bi": "Create a Power BI dashboard and attach a screenshot in resume",
    "tableau": "Include one visualization dashboard project",

    "tensorflow": "Add a TensorFlow model training project with evaluation metrics",
    "pytorch": "Include at least one PyTorch model experiment",
    "model validation": "Show a proper train-validation-test split in your ML project",
    "feature engineering": "Add a section explaining your feature engineering steps",

    "git": "Push all projects to GitHub and include links in resume",
    "docker": "Containerize one project using Docker basics"
}

ROLE_PRIORITY = {

    "data_analyst": {
        "high": ["sql", "excel", "power bi", "tableau"],
        "medium": ["pandas", "numpy"],
        "low": ["tensorflow", "pytorch"]
    },

    "ml_intern": {
        "high": ["tensorflow", "pytorch", "model validation", "feature engineering"],
        "medium": ["pandas", "numpy", "sql"],
        "low": ["power bi", "excel"]
    },

    "backend_intern": {
        "high": ["flask", "api", "backend"],
        "medium": ["sql", "docker"],
        "low": ["tensorflow"]
    },

    "software_intern": {
        "high": ["java", "c++", "debugging"],
        "medium": ["git"],
        "low": ["flask"]
    },

    "general": {
        "high": [],
        "medium": [],
        "low": []
    }
}

def generate_recommendations(missing_skills, job_text):
    
    role = infer_job_role(job_text)
    role_weights = ROLE_PRIORITY.get(role, ROLE_PRIORITY["general"])

    high, medium, low = [], [], []

    for skill in missing_skills:

        suggestion = RECOMMENDATION_RULES.get(skill, f"Improve or add a project related to {skill}")

        if skill in role_weights["high"]:
            high.append((skill, suggestion))

        elif skill in role_weights["medium"]:
            medium.append((skill, suggestion))

        else:
            low.append((skill, suggestion))

    return {
        "role": role,
        "high": high,
        "medium": medium,
        "low": low
    }


