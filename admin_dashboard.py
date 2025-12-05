import streamlit as st
import student_helper as sh
import webfunc as wb
import pandas as pd
import datetime as dt
import admin_helper as ah
import random
import datafile as df


def admin_dashboard():
    ss = st.session_state

    # Sidebar
    st.sidebar.title("Admin Portal")

    def is_active(p):
        return ss.page == p

    b1 = st.sidebar.button("Student Database", use_container_width=True,
                           type="primary" if is_active("Student_Database") else "secondary")
    b2 = st.sidebar.button("Tutor Database", use_container_width=True,
                           type="primary" if is_active("Tutor_Database") else "secondary")
    b3 = st.sidebar.button("Logout", use_container_width=True)

    if b1:
        wb.navigate("Student_Database")
    elif b2:
        wb.navigate("Tutor_Database")
    elif b3:
        wb.logout()

    page = ss.page

    # -----------------------------
    # ADMIN LANDING
    # -----------------------------
    if page == "Admin_Home":
        st.title("Welcome, Admin")
        st.caption("Use the sidebar to manage students, tutors, or system data.")
        st.divider()

    # -----------------------------
    # TUTOR DATABASE VIEW
    # -----------------------------
    elif page == "Tutor_Database":
        st.session_state.last_rated_tutor = None
        st.session_state.last_rating_score = None

        st.title("🔎 Tutor Database")

        query = st.text_input("Search by subject or tutor name", placeholder="e.g., Algebra")

        query_l = (query or "").lower()
        tutors = st.session_state.tutors

        # Basic search
        results = [
            name for name, t in tutors.items()
            if query_l in name.lower() or
               any(query_l in s.lower() for s in t["subjects"])
        ]

        st.caption(f"{len(results)} result(s)")
        st.divider()

        if not results:
            st.warning("No tutors found.")
        else:
            for name in results:
                tutor_card_admin(name)

    # -----------------------------
    # STUDENT DATABASE VIEW
    # -----------------------------
    elif page == "Student_Database":
        st.title("🔎 Student Database")

        query = st.text_input("Search by student name or ID", placeholder="e.g., Jared")

        query_l = (query or "").lower()
        student_dict = df.students

        results = [
            sid for sid, s in student_dict.items()
            if query_l in sid.lower() or query_l in s["name"].lower()
        ]

        st.caption(f"{len(results)} result(s)")
        st.divider()

        if st.button("Add Student User"):
            wb.navigate("Add_Student_Form")

        if not results:
            st.warning("No matching students.")
        else:
            for sid in results:
                ah.student_card(sid)

    # -----------------------------
    # ADD STUDENT FORM
    # -----------------------------
    elif page == "Add_Student_Form":
        st.title("Add New Student")

        with st.form("add_student"):
            new_id = st.text_input("Student ID (unique)", placeholder="e.g., AB123")
            name = st.text_input("Legal Name")
            major = st.text_input("Major")
            year = st.text_input("Year")
            email = st.text_input("Email")
            password = st.text_input("Login Password")

            submitted = st.form_submit_button("Create Student")

            if submitted:
                if new_id in df.students:
                    st.error("That student ID already exists.")
                else:
                    # Add to master lists
                    df.students[new_id] = {
                        "name": name,
                        "major": major,
                        "year": year,
                        "email": email
                    }
                    df.CREDENTIALS[new_id] = {
                        "password": password,
                        "role": "student",
                        "UID": new_id
                    }
                    st.success("Student added successfully!")
                    wb.navigate("Student_Database")


# ============================
# TUTOR CARD FOR ADMIN VIEW
# ============================
def tutor_card_admin(tutor_name: str):
    t = st.session_state.tutors[tutor_name]
    with st.container(border=True):
        left, right = st.columns([3, 1])

        with left:
            st.subheader(t["name"])
            st.caption(", ".join(t["subjects"]))
            st.write(t["bio"])
            st.markdown(sh.star_bar(t["rating"]), unsafe_allow_html=True)

        with right:
            st.caption(f"Ratings: {t['ratings_count']}")
            st.caption(f"Updated: {t['last_updated']}")

            if st.button(f"Remove {tutor_name}", key=f"fire_{tutor_name}",
                         use_container_width=True):
                del st.session_state.tutors[tutor_name]
                st.warning(f"Tutor {tutor_name} removed.")
                st.rerun()
