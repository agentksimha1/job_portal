# portal_ui.py
import streamlit as st
import requests

# Replace this with the public URL of your Flask backend Space
API_URL = "https://krishnasimha-portal-backend.hf.space"

st.set_page_config(page_title="Job Portal UI", layout="wide")
st.title("💼 Mini Job Portal")

tab1, tab2, tab3 = st.tabs(["Jobs", "Applications", "Add Job"])

# ------------------- TAB 1: Jobs -------------------
with tab1:
    st.subheader("Available Jobs")
    try:
        jobs = requests.get(f"{API_URL}/jobs").json()
        if not jobs:
            st.info("No jobs available at the moment.")
        for job in jobs:
            st.markdown(f"### {job['job_title']}")
            st.write(f"{job['company_name']} — {job['location']}")
            st.write("Skills:", ", ".join(job["skills"]))

            name = st.text_input("Your Name", key=f"name_{job['job_id']}")
            if st.button("Apply", key=f"apply_{job['job_id']}"):
                if not name.strip():
                    st.warning("Please enter your name to apply.")
                else:
                    resp = requests.post(f"{API_URL}/apply", json={
                        "job_id": job["job_id"],
                        "student_name": name
                    })
                    if resp.status_code == 200:
                        st.success("Application submitted successfully!")
                    else:
                        st.error("Failed to submit application.")
            st.divider()
    except Exception as e:
        st.error(f"Failed to fetch jobs: {e}")

# ------------------- TAB 2: Applications -------------------
with tab2:
    st.subheader("Applications")
    try:
        apps = requests.get(f"{API_URL}/applications").json()
        if not apps:
            st.info("No applications yet.")
        for app in apps:
            st.write(
                f"{app['student_name']} → Job {app['job_id']} | Status: {app['status']} | Applied on: {app['timestamp']}"
            )
    except Exception as e:
        st.error(f"Failed to fetch applications: {e}")

# ------------------- TAB 3: Add Job -------------------
with tab3:
    st.subheader("Add New Job")
    title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    skills = st.text_input("Skills (comma-separated)")
    location = st.selectbox("Location", ["Remote", "Onsite"])

    if st.button("Add Job"):
        if not title.strip() or not company.strip() or not skills.strip():
            st.warning("Please fill all the fields.")
        else:
            resp = requests.post(f"{API_URL}/add_job", json={
                "job_title": title.strip(),
                "company_name": company.strip(),
                "skills": [s.strip() for s in skills.split(",")],
                "location": location
            })
            if resp.status_code == 200:
                st.success("Job added successfully!")
                st.rerun()  # Works in recent Streamlit versions
            else:
                st.error("Failed to add job.")













