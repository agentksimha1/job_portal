import streamlit as st
import sqlite3
from datetime import datetime
import uuid
from flask import Flask, jsonify, request
import threading

DB_FILE = "jobs.db"

# ------------------- DB Setup -------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
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

# ------------------- Flask REST API -------------------
app = Flask(__name__)

def get_jobs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    rows = c.fetchall()
    conn.close()
    jobs = []
    for row in rows:
        job_id, title, company, skills_csv, location = row
        jobs.append({
            "job_id": job_id,
            "job_title": title,
            "company_name": company,
            "skills": skills_csv.split(","),
            "location": location
        })
    return jobs

def get_applications():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM applications ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    apps = []
    for row in rows:
        apps.append({
            "application_id": row[0],
            "job_id": row[1],
            "student_name": row[2],
            "status": row[3],
            "timestamp": row[4]
        })
    return apps

def add_job(job_id, title, company, skills, location):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO jobs (job_id, job_title, company_name, skills, location)
        VALUES (?,?,?,?,?)
    """, (job_id, title, company, ",".join(skills), location))
    conn.commit()
    conn.close()

def add_application(job_id, student_name):
    application_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO applications (application_id, job_id, student_name, status, timestamp)
        VALUES (?,?,?,?,?)
    """, (application_id, job_id, student_name, "submitted", timestamp))
    conn.commit()
    conn.close()
    return {"status": "submitted", "application_id": application_id, "timestamp": timestamp}

# Flask endpoints
@app.route("/jobs", methods=["GET"])
def api_get_jobs():
    return jsonify(get_jobs())

@app.route("/applications", methods=["GET"])
def api_get_applications():
    return jsonify(get_applications())

@app.route("/apply", methods=["POST"])
def api_apply_job():
    payload = request.json
    job_id = payload.get("job_id")
    student_name = payload.get("student_name")
    return jsonify(add_application(job_id, student_name))

# Run Flask in a background thread
def run_api():
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)

api_thread = threading.Thread(target=run_api, daemon=True)
api_thread.start()

# ------------------- Streamlit UI -------------------
st.title("💼 Mini Job Portal + Live Agent Demo")

tab1, tab2, tab3 = st.tabs(["Jobs", "Applications", "Add New Job"])

with tab1:
    st.subheader("Available Jobs")
    jobs = get_jobs()
    if not jobs:
        st.info("No jobs available yet.")
    for job in jobs:
        st.write(f"**{job['job_title']}** at {job['company_name']} ({job['location']})")
        st.write(f"Skills: {', '.join(job['skills'])}")
        st.markdown("---")

with tab2:
    st.subheader("Submitted Applications")
    apps = get_applications()
    if not apps:
        st.info("No applications submitted yet.")
    for app in apps:
        st.write(f"**{app['student_name']}** applied to Job ID {app['job_id']} — {app['status']} ({app['timestamp']})")
        st.markdown("---")

with tab3:
    st.subheader("Add a New Job Posting")
    new_job_title = st.text_input("Job Title", key="job_title")
    new_company = st.text_input("Company Name", key="company_name")
    new_skills = st.text_input("Skills (comma-separated)", key="skills")
    new_location = st.selectbox("Location", ["Remote", "Onsite"], key="location")
    if st.button("Add Job"):
        job_id = f"J{int(datetime.utcnow().timestamp())}"
        skills_list = [s.strip() for s in new_skills.split(",")]
        add_job(job_id, new_job_title, new_company, skills_list, new_location)
        st.success(f"Job {new_job_title} added!")





