import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIG ----------------
BACKEND_URL = "https://krishnasimha-portal-backend.hf.space"

st.set_page_config(
    page_title="Admin – Job Portal",
    layout="wide"
)

st.title("🛠️ Job Portal Admin Dashboard")

# ---------------- HELPERS ----------------
def fetch_jobs():
    res = requests.get(f"{BACKEND_URL}/jobs")
    res.raise_for_status()
    return res.json()

def fetch_applications():
    res = requests.get(f"{BACKEND_URL}/applications")
    res.raise_for_status()
    return res.json()

def add_job(payload):
    res = requests.post(f"{BACKEND_URL}/add_job", json=payload)
    res.raise_for_status()
    return res.json()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["📋 Jobs", "📨 Applications", "➕ Add Job"]
)

# ==========================================================
# 📋 JOBS VIEW
# ==========================================================
if page == "📋 Jobs":
    st.subheader("📋 All Jobs in Database")

    try:
        jobs = fetch_jobs()

        if not jobs:
            st.info("No jobs found in database.")
        else:
            df = pd.DataFrame(jobs)
            df["skills"] = df["skills"].apply(lambda x: ", ".join(x))

            st.dataframe(
                df,
                use_container_width=True
            )

            st.caption(f"Total jobs: {len(df)}")

    except Exception as e:
        st.error("Failed to fetch jobs")
        st.code(str(e))

# ==========================================================
# 📨 APPLICATIONS VIEW
# ==========================================================
elif page == "📨 Applications":
    st.subheader("📨 Applications Received")

    try:
        apps = fetch_applications()

        if not apps:
            st.info("No applications yet.")
        else:
            df = pd.DataFrame(apps)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.caption(f"Total applications: {len(df)}")

    except Exception as e:
        st.error("Failed to fetch applications")
        st.code(str(e))

# ==========================================================
# ➕ ADD JOB
# ==========================================================
elif page == "➕ Add Job":
    st.subheader("➕ Add New Job")

    with st.form("add_job_form"):
        title = st.text_input("Job Title")
        company = st.text_input("Company Name")
        skills = st.text_input("Skills (comma separated)")
        location = st.selectbox("Location", ["Remote", "Onsite", "Hybrid"])

        submitted = st.form_submit_button("Add Job")

        if submitted:
            if not title or not company or not skills:
                st.warning("Please fill all fields.")
            else:
                payload = {
                    "job_title": title,
                    "company_name": company,
                    "skills": [s.strip() for s in skills.split(",")],
                    "location": location
                }

                try:
                    res = add_job(payload)
                    st.success(f"Job added successfully 🎉")
                    st.code(res)

                except Exception as e:
                    st.error("Failed to add job")
                    st.code(str(e))
















