# frontend/dashboard.py
import streamlit as st
import requests
import urllib3
import pandas as pd
import plotly.express as px
import time
from streamlit_autorefresh import st_autorefresh


# -----------------------------------------------------------
# FIX 1: define ss_has BEFORE first use
# -----------------------------------------------------------
def ss_has(key: str) -> bool:
    """Support both dict-like and attribute-like session_state in tests."""
    try:
        return key in st.session_state
    except TypeError:
        return hasattr(st.session_state, key)


# keep a single Session so cookies persist between requests
# Support both dict-like and object-like session_state
try:
    has_session_req = "session_req" in st.session_state
except TypeError:
    has_session_req = hasattr(st.session_state, "session_req")

if not has_session_req:
    st.session_state.session_req = requests.Session()

session_req = st.session_state.session_req
session_req.trust_env = False

# Some tests use FakeSess without headers → guard it
if not hasattr(session_req, "headers"):
    session_req.headers = {}
session_req.headers.update({"Accept": "application/json"})

API_BASE = "http://localhost:5000/api"
ST_ORIGIN = "http://localhost:8501"

st.set_page_config(page_title="APAS Dashboard", layout="wide")
st_autorefresh(interval=90100, key="refresh_app")

VERIFY_SSL = False
if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Session state
if not ss_has("logged_in"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None


# persistent requests.Session so cookies (session) are preserved across requests
def get_requests_session():
    if not ss_has("requests_session"):
        s = requests.Session()
        s.verify = VERIFY_SSL
        st.session_state.requests_session = s
    return st.session_state.requests_session


# create session early so it's available to login and subsequent calls
sess = get_requests_session()


def safe_json(res):
    try:
        return res.json()
    except Exception:
        return {
            "success": False,
            "message": res.text or "Non-JSON response",
            "status_code": res.status_code,
        }


def do_login():
    username = st.session_state.get("login_username")
    password = st.session_state.get("login_password")
    if not username or not password:
        st.error("Enter username and password.")
        return
    try:
        s = get_requests_session()
        res = s.post(f"{API_BASE}/login", json={"username": username, "password": password}, timeout=10)
        data = safe_json(res)
        if res.status_code == 200 and data.get("success"):
            st.session_state.logged_in = True
            st.session_state.role = data["role"]
            st.session_state.username = data["username"]
            st.success(f"Welcome, {st.session_state.username} ({st.session_state.role})")
            st.rerun()
        else:
            st.error(data.get("message", "Invalid credentials."))
    except Exception as e:
        st.error(f"Connection error: {e}")


# Login screen
if not st.session_state.logged_in:
    st.title("🎓 APAS - Academic Performance Analytics System")
    st.subheader("Login")
    st.text_input("Username", key="login_username")
    st.text_input("Password", type="password", key="login_password")
    st.button("Login", on_click=do_login)
    st.markdown("**Demo accounts:** admin/adminpass, instructor1/instructorpass, student1/studentpass")
    st.stop()


# Logout
if st.button("Logout"):
    # FIX 2: Safe clear for SimpleNamespace
    try:
        st.session_state.clear()
    except Exception:
        st.session_state.__dict__.clear()
    st.rerun()


role = st.session_state.role
username = st.session_state.username
st.sidebar.title("Navigation")
st.sidebar.write(f"👤 {username} ({role})")

SESSION_TIMEOUT = 900   # 15 mins

# Session tracking
if not ss_has("last_active"):
    st.session_state.last_active = time.time()
else:
    if time.time() - st.session_state.last_active > SESSION_TIMEOUT:
        st.warning("Session expired. Please login again.")

        # FIX 2: Safe clear
        try:
            st.session_state.clear()
        except Exception:
            st.session_state.__dict__.clear()
        st.rerun()

st.session_state.last_active = time.time()


def fetch_settings():
    try:
        s = get_requests_session()
        r = s.get(f"{API_BASE}/settings", timeout=10)
        data = safe_json(r)
        if r.status_code == 200:
            return data
    except:
        pass
    return {"risk_threshold": 0.6, "model_version": "1"}


settings = fetch_settings()
threshold = float(settings.get("risk_threshold", 0.6))
model_version = settings.get("model_version", "1")


# ====================================================
# STUDENT DASHBOARD
# FIX 3: Normalize scalar API response → list
# ====================================================
if role == "student":
    st.title("📊 Student Dashboard")
    s = get_requests_session()
    res = s.get(f"{API_BASE}/student/{username}", timeout=10)
    data = safe_json(res)

    # FIX for scalar responses
    if not isinstance(data, (list, tuple)):
        data = []

    if res.status_code == 200:
        df = pd.DataFrame(data)
        if not df.empty:
            st.dataframe(df[['course','marks','attendance','risk_score','instructor_name','timestamp']])
            fig = px.bar(df, x="course", y="risk_score", color="risk_score", title="Risk by Course")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No records found.")
    else:
        st.error(data.get("message", "Failed to fetch student data."))

    st.stop()


# ====================================================
# INSTRUCTOR DASHBOARD
# same scalar fix on rdata
# ====================================================
if role == "instructor":
    st.title("🧑‍🏫 Instructor Dashboard")

    s = get_requests_session()
    r = s.get(f"{API_BASE}/instructor/{username}", timeout=10)
    rdata = safe_json(r)

    if not isinstance(rdata, (list, tuple)):
        rdata = []

    if r.status_code == 200:
        df = pd.DataFrame(rdata)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No class data yet.")
    else:
        st.error(rdata.get("message", "Failed to load class data."))

    st.stop()


# ====================================================
# ADMIN DASHBOARD
# also needs scalar normalization
# ====================================================
if role == "admin":
    st.title("🧑‍💼 Admin Dashboard")

    s = get_requests_session()
    res = s.get(f"{API_BASE}/all_records", timeout=30)
    rdata = safe_json(res)

    if not isinstance(rdata, (list, tuple)):
        rdata = []

    if res.status_code == 200:
        df = pd.DataFrame(rdata)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No records available")
    else:
        st.error(rdata.get("message", "Failed to load analytics"))

    st.stop()
