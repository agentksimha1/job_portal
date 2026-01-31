import streamlit as st
import requests

API_URL = "http://127.0.0.1:7860"  # your Flask backend URL

st.title("Job Portal")

tab1, tab2 = st.tabs(["Jobs", "Applications"])

with tab1:
    st.header("Available Jobs")
    jobs = requests.get(f"{API_URL}/jobs").json()
    for job in jobs:
        st.subheader(job["job_title"])
        st.write("Company:", job["company_name"])
        st.write("Location:", job["location"])
        st.write("Skills:", ", ".join(job["skills"]))
        if st.button(f"Apply for {job['job_title']}", key=job["job_id"]):
            student_name = st.text_input("Your Name", key=job["job_id"]+"_name")
            if student_name:
                resp = requests.post(f"{API_URL}/apply", json={"job_id": job["job_id"], "student_name": student_name})
                if resp.json()["status"]=="success":
                    st.success("Applied successfully!")

with tab2:
    st.header("Applications")
    apps = requests.get(f"{API_URL}/applications").json()
    for app in apps:
        st.write(f"{app['student_name']} applied for job {app['job_id']} | Status: {app['status']}")















