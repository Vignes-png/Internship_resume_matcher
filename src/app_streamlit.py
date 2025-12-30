import streamlit as st
import pdfplumber
from skill_extract import load_skills, extract_skills
from similarity_tfidf import compute_tfidf_similarity
from embedding_similarity import compute_embedding_similarity
from match_scoring import compute_skill_overlap_score, compute_combined_match_score
from recommend_engine import generate_recommendations


st.set_page_config(page_title="Internship Resume Matcher", layout="wide")

st.title("🎯 Internship Resume – Job Match & Skill Gap Analyzer")
st.write("AI + NLP based matching using TF-IDF + Sentence Embeddings")

# Load skills database
skills_dict = load_skills("../data/skills.json")


col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume Input")

    upload_resume = st.file_uploader(
        "Upload resume (PDF or TXT)",
        type=["pdf", "txt"]
    )

    resume_text = st.text_area(
        "Or paste resume text",
        height=280
    )

    # If file uploaded → extract text
    if upload_resume is not None:

        if upload_resume.type == "application/pdf":
            with pdfplumber.open(upload_resume) as pdf:
                resume_text = "\n".join(
                    page.extract_text() or "" for page in pdf.pages
                )

        elif upload_resume.type == "text/plain":
            resume_text = upload_resume.read().decode("utf-8")

        st.success("Resume text extracted successfully ✔")


with col2:
    st.subheader("💼 Job Description(s)")

    multi_mode = st.toggle("Compare against multiple jobs")

    job_text = ""
    job_files = []

    if multi_mode:
        job_files = st.file_uploader(
            "Upload one or more job descriptions (TXT)",
            type=["txt"],
            accept_multiple_files=True
        )

        st.info("Each file will be evaluated and ranked.")

    else:
        job_text = st.text_area(
            "Paste job description",
            height=280
        )


# ==========================================================
# RUN MATCH ANALYSIS
# ==========================================================

if st.button("⚡ Run Match Analysis"):

    # ------------------------------------------------------
    # SINGLE JOB MODE
    # ------------------------------------------------------
    if not multi_mode:

        if not resume_text or not job_text:
            st.warning("Please provide BOTH resume and job description.")
            st.stop()

        st.success("Running match analysis...")

        resume_skills = extract_skills(resume_text, skills_dict)
        job_skills = extract_skills(job_text, skills_dict)

        resume_set = set(resume_skills["found"])
        job_set = set(job_skills["found"])

        matched_skills, skill_score = compute_skill_overlap_score(
            resume_set,
            job_set
        )

        missing_skills = job_set - resume_set

        tfidf_score = compute_tfidf_similarity(resume_text, job_text)
        embed_score = compute_embedding_similarity(resume_text, job_text)

        final_score = compute_combined_match_score(
            skill_score,
            tfidf_score,
            embed_score
        )

        reco = generate_recommendations(missing_skills, job_text)

        st.header("📊 Match Summary")

        colA, colB, colC = st.columns(3)

        colA.metric("Final Match Score", f"{round(final_score,1)}%")
        colB.metric("TF-IDF Similarity", tfidf_score)
        colC.metric("Embedding Similarity", embed_score)

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("✅ Matched Skills")
            st.write(sorted(list(matched_skills)))

        with c2:
            st.subheader("⚠ Missing Skills")
            st.write(sorted(list(missing_skills)))

        st.subheader("🧠 Recommended Improvements")

        for skill, action in reco["high"]:
            st.markdown(f"🔴 **HIGH PRIORITY** — {skill}: {action}")

        for skill, action in reco["medium"]:
            st.markdown(f"🟡 **MEDIUM** — {skill}: {action}")

        for skill, action in reco["low"]:
            st.markdown(f"⚪ Optional — {skill}: {action}")


    # ------------------------------------------------------
    # MULTI-JOB MODE (RANKING)
    # ------------------------------------------------------
    else:

        if not resume_text or not job_files:
            st.warning("Upload resume + at least ONE job file.")
            st.stop()

        st.success("Evaluating jobs and ranking them...")

        results = []

        for job_file in job_files:

            job_file.seek(0)
            job_text = job_file.read().decode("utf-8")

            resume_skills = extract_skills(resume_text, skills_dict)
            job_skills = extract_skills(job_text, skills_dict)

            resume_set = set(resume_skills["found"])
            job_set = set(job_skills["found"])

            matched_skills, skill_score = compute_skill_overlap_score(
                resume_set,
                job_set
            )

            missing_skills = job_set - resume_set

            tfidf_score = compute_tfidf_similarity(resume_text, job_text)
            embed_score = compute_embedding_similarity(resume_text, job_text)

            final_score = compute_combined_match_score(
                skill_score,
                tfidf_score,
                embed_score
            )

            reco = generate_recommendations(missing_skills, job_text)

            results.append({
                "job_name": job_file.name,
                "score": final_score,
                "matched": list(matched_skills),
                "missing": list(missing_skills),
                "tfidf": tfidf_score,
                "embed": embed_score,
                "reco": reco
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        st.header("🏆 Internship Match Rankings")

        for i, r in enumerate(results, start=1):

            st.subheader(f"{i}) {r['job_name']} — {round(r['score'],1)}%")

            colA, colB = st.columns(2)

            with colA:
                st.write("✅ Matched:", r["matched"])

            with colB:
                st.write("⚠ Missing:", r["missing"])

            st.write(f"TF-IDF: {r['tfidf']}  |  Embedding: {r['embed']}")

            st.write("🧠 Recommendations:")

            for s, a in r["reco"]["high"]:
                st.markdown(f"🔴 **HIGH** — {s}: {a}")

            for s, a in r["reco"]["medium"]:
                st.markdown(f"🟡 **MEDIUM** — {s}: {a}")

            for s, a in r["reco"]["low"]:
                st.markdown(f"⚪ Optional — {s}: {a}")
