import json
import re

def load_skills(path):
    with open(path, "r") as f:
        return json.load(f)


def extract_skills(text, skills_dict):

    text_lower = text.lower()
    found = set()

    for category, skills in skills_dict.items():
        for skill in skills:
            skill = skill.strip().lower()

            # ignore very short tokens (< 3 chars)
            if len(skill) < 3:
                continue

            # build whole-word / phrase regex pattern
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text_lower):
                found.add(skill)

    return {"found": list(found)}
