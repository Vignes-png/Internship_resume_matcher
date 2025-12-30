# Internship Resume – Job Match & Skill Gap Analyzer

### 🧠 What This Project Does
This project analyzes how well a resume matches a job description by:
- Extracting skills from both resume & job description
- Comparing skills using TF-IDF similarity
- Measuring semantic similarity using sentence embeddings
- Identifying:
  - ✅ Matched skills
  - ⚠ Missing / suggested skills
- Generating actionable recommendations to improve resume relevance
- Supporting multi-job comparison and ranking

### ℹ️ About the Data
The skills list and job description files included in `/data`
are **sample datasets for demonstration and testing purposes only**.

Users may replace them with:
- Their own resumes
- Real job descriptions
- Custom skill dictionaries

### 🚀 Tech Used
Python · NLP · TF-IDF · Sentence Transformers · Streamlit

### 💻 How to Run
pip install -r requirements.txt

python -m streamlit run src/app_streamlit.py

### 📂 Project Structure
- /src — all program logic
- /data — skill dictionary & sample jobs
- requirements.txt — dependencies

### 🖥️ Preview
<img width="1775" height="865" alt="image" src="https://github.com/user-attachments/assets/b1124125-c219-47eb-948f-d29d0cc410a3" />
<img width="1615" height="837" alt="image" src="https://github.com/user-attachments/assets/605bc578-b85a-4d37-a48f-3a743e82ad5c" />
<img width="1363" height="835" alt="image" src="https://github.com/user-attachments/assets/1fd4b9ae-e710-4d45-8402-0189024629ae" />




