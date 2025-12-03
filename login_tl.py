import streamlit as st
import datafile

CREDENTIALS = {
    "jdudley03": {"password": "abcdef123", "role": "student", "UID" : "AZC02"},
    "tladmin": {"password": "admin", "role": "admin", "UID": "0"},
    "aaronfogle84": {"password": "123456", "role": "student", "UID" : "MZ83D"}
}

def init_session_state():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

def login(username: str, password: str):
    if username in CREDENTIALS and CREDENTIALS[username]["password"] == password:
        st.session_state.is_logged_in = True
        st.session_state.user_role = CREDENTIALS[username]["role"]
        st.session_state.student = datafile.students[CREDENTIALS[username]["UID"]]
        st.session_state.page = "dashboard"
        return True
    else:
        st.error("Invalid username or password")
        return False

def show_home():
    st.title("Welcome to TutorLink 2025")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("For Students", use_container_width=True, key="home_student"):
            st.session_state.page = "student_login"
    with col2:
        if st.button("For Admins", use_container_width=True, key="home_admin"):
            st.session_state.page = "admin_login"

def show_student_login():
    st.header("Student Login")
    with st.form("student_lgn"):
        username = st.text_input("Username", key="stu_name")
        password = st.text_input("Password", type="password", key="stu_pwd")
        submitted = st.form_submit_button("Login")
        if submitted:
            login(username, password)

def show_admin_login():
    st.header("Administrator Login")
    with st.form("admin_lgn"):
        st.text("ADMINS - MAKE SURE TO USE A VPN AND COVER YOUR KEYBOARD WHEN ENTERING CREDENTIALS.")
        username = st.text_input("Username", key="adm_name")
        password = st.text_input("Password", type="password", key="adm_pwd")
        submitted = st.form_submit_button("Login")
        if submitted:
            login(username, password)
