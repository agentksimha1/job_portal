import streamlit as st
import sqlite3
from datetime import datetime
import uuid

DB_FILE = "jobs.db"

# ------------------- DB UTILS -------------------
def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            job_title TEXT,
            company_name TEXT,
            skills TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            application_id TEXT PRIMARY KEY,
            job_id TEXT,
            student_name TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_jobs():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM jobs").fetchall()
    conn.close()
    return [
        {
            "job_id": r[0],
            "job_title": r[1],
            "company_name": r[2],
            "skills": r[3].split(","),
            "location": r[4]
        }
        for r in rows
    ]

def get_applications():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM applications ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return rows

def add_job(title, company, skills, location):
    conn = get_connection()
    conn.execute(
        "INSERT INTO jobs VALUES (?,?,?,?,?)",
        (
            str(uuid.uuid4()),
            title,
            company,
            ",".join(skills),
            location
        )
    )
    conn.commit()
    conn.close()

def apply_job(job_id, student_name):
    conn = get_connection()
    conn.execute(
        "INSERT INTO applications VALUES (?,?,?,?,?)",
        (
            str(uuid.uuid4()),
            job_id,
            student_name,
            "submitted",
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()

# ------------------- STREAMLIT UI -------------------
st.set_page_config(page_title="Mini Job Portal", layout="wide")
st.title("💼 Mini Job Portal (Streamlit Native)")

tab1, tab2, tab3 = st.tabs(["Jobs", "Applications", "Add Job"])

with tab1:
    st.subheader("Available Jobs")
    for job in get_jobs():
        st.markdown(f"### {job['job_title']}")
        st.write(job["company_name"], "—", job["location"])
        st.write("Skills:", ", ".join(job["skills"]))

        name = st.text_input(
            "Your Name",
            key=f"name_{job['job_id']}"
        )
        if st.button("Apply", key=f"apply_{job['job_id']}"):
            apply_job(job["job_id"], name)
            st.success("Application submitted!")
        st.divider()

with tab2:
    st.subheader("Applications")
    for app in get_applications():
        st.write(
            f"{app[2]} → Job {app[1]} | {app[3]} | {app[4]}"
        )

with tab3:
    st.subheader("Add New Job")
    title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    skills = st.text_input("Skills (comma-separated)")
    location = st.selectbox("Location", ["Remote", "Onsite"])

    if st.button("Add Job"):
        add_job(title, company, [s.strip() for s in skills.split(",")], location)
        st.success("Job added!")
        st.rerun()







