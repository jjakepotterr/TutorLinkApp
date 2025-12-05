import streamlit as st
import login_tl as login
import admin_dashboard as admin
import student_dashboard as student
import webfunc as wb
import datafile as df

# NEW: Tutor dashboard import
import tutor_dashboard as tutor


def initialize_globals():
    """Ensures all global session variables exist."""
    ss = st.session_state

    # -----------------------
    # Navigation
    # -----------------------
    wb.init_nav()

    # -----------------------
    # Student Fields
    # -----------------------
    if "schedule" not in ss:
        ss.schedule = []  # pending + approved sessions

    if "history" not in ss:
        ss.history = []  # completed sessions after survey

    # -----------------------
    # Tutor Fields
    # -----------------------
    if "pending_requests" not in ss:
        ss.pending_requests = []  # all request objects system-wide

    if "tutor_sessions" not in ss:
        ss.tutor_sessions = []  # accepted sessions for logged-in tutor only

    # -----------------------
    # Tutors (datafile → session)
    # -----------------------
    if "tutors" not in ss:
        ss.tutors = df.tutors

    # -----------------------
    # 🔥 FIXED: Students (datafile → session)
    # Required for Admin Dashboard
    # -----------------------
    if "students" not in ss:
        ss.students = df.students


def main():
    ss = st.session_state
    initialize_globals()

    # -----------------------
    # Not logged in → show login page
    # -----------------------
    if "is_logged_in" not in ss or not ss.is_logged_in:
        login.login_page()
        return

    # -----------------------
    # ROUTE USERS
    # -----------------------
    role = ss.get("role")

    if role == "student":
        student.student_dashboard()
        return

    elif role == "tutor":
        tutor.tutor_dashboard()
        return

    elif role == "admin":
        admin.admin_dashboard()
        return

    else:
        st.error("Unknown user role. Logging out for safety.")
        wb.logout()


if __name__ == "__main__":
    main()
