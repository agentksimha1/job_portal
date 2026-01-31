# portal_ui.py
import streamlit as st
import requests

API_URL = "https://krishnasimha-portal-backend.hf.space"  # Your deployed API

st.set_page_config(page_title="Job Portal UI", layout="wide")
st.title("💼 Job Portal")

tab1, tab2, tab3 = st.tabs(["Jobs", "Applications", "Add Job"])

with tab1:
    st.subheader("Available Jobs")
    jobs = requests.get(f"{API_URL}/jobs").json()
    for job in jobs:
        st.markdown(f"### {job['job_title']}")
        st.write(job["company_name"], "—", job["location"])
        st.write("Skills:", ", ".join(job["skills"]))

        name = st.text_input("Your Name", key=f"name_{job['job_id']}")
        if st.button("Apply", key=f"apply_{job['job_id']}"):
            requests.post(f"{API_URL}/apply", json={"job_id": job["job_id"], "student_name": name})
            st.success("Application submitted!")
        st.divider()

with tab2:
    st.subheader("Applications")
    apps = requests.get(f"{API_URL}/applications").json()
    for app in apps:
        st.write(
            f"{app['student_name']} → Job {app['job_id']} | {app['status']} | {app['timestamp']}"
        )

with tab3:
    st.subheader("Add New Job")
    title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    skills = st.text_input("Skills (comma-separated)")
    location = st.selectbox("Location", ["Remote", "Onsite"])
    if st.button("Add Job"):
        requests.post(
            f"{API_URL}/add_job",
            json={
                "job_title": title,
                "company_name": company,
                "skills": [s.strip() for s in skills.split(",")],
                "location": location
            }
        )
        st.success("Job added!")
        st.experimental_rerun()









