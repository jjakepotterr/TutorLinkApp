import streamlit as st
import datafile as df
import webfunc as wb

def login_page():
    st.title("TutorLink Login")

    st.write("### Choose your login type:")
    
    role_option = st.radio(
        "",
        ["Student Login", "Tutor Login", "Admin Login"],
        horizontal=False
    )

    # -------------------------
    # STUDENT LOGIN
    # -------------------------
    if role_option == "Student Login":
        st.subheader("Student Login")

        username = st.text_input("Student ID (e.g., AZC02)")
        password = st.text_input("Password", type="password")

        if st.button("Login as Student", use_container_width=True):
            if username in df.CREDENTIALS:
                user = df.CREDENTIALS[username]
                if user["role"] == "student" and user["password"] == password:

                    st.session_state.is_logged_in = True
                    st.session_state.role = "student"
                    st.session_state.user = username
                    st.session_state.student = df.students[username]

                    # initialize schedule + history
                    st.session_state.schedule = []
                    st.session_state.history = []

                    # load tutor data
                    st.session_state.tutors = df.tutors

                    wb.navigate("Profile")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid student credentials.")
            else:
                st.error("Student ID not found.")

    # -------------------------
    # TUTOR LOGIN
    # -------------------------
    elif role_option == "Tutor Login":
        st.subheader("Tutor Login")

        username = st.text_input("Tutor Username (e.g., jerry)")
        password = st.text_input("Password", type="password")

        if st.button("Login as Tutor", use_container_width=True):
            if username in df.CREDENTIALS:
                user = df.CREDENTIALS[username]
                if user["role"] == "tutor" and user["password"] == password:

                    st.session_state.is_logged_in = True
                    st.session_state.role = "tutor"
                    st.session_state.user = username

                    # Find this tutor's NAME (e.g. "Jerry Spinelli")
                    tutor_name = None
                    for tname, tdata in df.tutors.items():
                        if tdata["UID"] == user["UID"]:
                            tutor_name = tname
                            break

                    st.session_state.tutor_name = tutor_name

                    # Initialize tutor inbox and session list
                    if "pending_requests" not in st.session_state:
                        st.session_state.pending_requests = []
                    if "tutor_sessions" not in st.session_state:
                        st.session_state.tutor_sessions = []

                    st.success("Tutor login successful!")
                    wb.navigate("Tutor_Home")
                    st.rerun()

                else:
                    st.error("Invalid tutor credentials.")
            else:
                st.error("Tutor username not found.")

    # -------------------------
    # ADMIN LOGIN
    # -------------------------
    elif role_option == "Admin Login":
        st.subheader("Admin Login")

        username = st.text_input("Admin Username")
        password = st.text_input("Password", type="password")

        if st.button("Login as Admin", use_container_width=True):
            if username in df.CREDENTIALS:
                user = df.CREDENTIALS[username]
                if user["role"] == "admin" and user["password"] == password:

                    st.session_state.is_logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.user = username

                    # load tutor data
                    st.session_state.tutors = df.tutors

                    st.success("Admin login successful!")
                    wb.navigate("Admin_Home")
                    st.rerun()

                else:
                    st.error("Invalid admin credentials.")
            else:
                st.error("Admin username not found.")
