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

    st.sidebar.title("Admin Portal")

    def is_active(p): return st.session_state.page == p

    b1 = st.sidebar.button("Student Database", use_container_width=True, type="primary" if is_active("Student_Database") else "secondary")
    b2 = st.sidebar.button("Tutor Database", use_container_width=True, type="primary" if is_active("Tutor_Database") else "secondary")
    b3 = st.sidebar.button("Logout", use_container_width = True, type="primary")

    if b1: wb.navigate("Student_Database")
    elif b2: wb.navigate("Tutor_Database")
    elif b3: wb.logout()

    page = st.session_state.page

    # =========================
    # Pages
    # =========================

    if page == "Admin_Home":

        st.title("Welcome, Admin")
        st.text("Review the left navigation panel to view records and perform operations.")
        st.caption("Admin perspective demo")
        st.divider()

    elif page == "Tutor_Database":
        # clear last rating banner when leaving Survey
        st.session_state.last_rated_tutor = None
        st.session_state.last_rating_score = None

        st.title("🔎 Search Tutor Database")
        
        query = st.text_input("Keywords", placeholder="e.g., algebra")
        results = sh.search_tutors_by_subject((query or "").strip())
        st.caption(f"{len(results)} result(s)")
        st.divider()

        if not results:
            st.warning("No tutors matched that subject. Try 'algebra'.")
        else:
            for name in results:
                tutor_card(name)

    elif page == "Student_Database":

        st.title("🔎 Search Student Database")
        query = st.text_input("Keywords")
        results = ah.search_students_by_name((query or "").strip())
        st.caption(f"{len(results)} result(s)")
        st.divider()

        if st.button("Add Student User"):
            wb.navigate("Add_Student_Form")

        
        if not results:
            st.warning("No results found.")
        else:
            for name in results:
                ah.student_card(name)

    elif page == "Tutor_Profile_Admin":
        # clear last rating banner when leaving Survey
        st.session_state.last_rated_tutor = None
        st.session_state.last_rating_score = None

        st.title("Tutor Profile")
        tutor_names = list(st.session_state.tutors.keys())
        default_index = 0
        if st.session_state.selected_tutor in tutor_names:
            default_index = tutor_names.index(st.session_state.selected_tutor)
        selected = st.selectbox("Select a tutor", tutor_names, index=default_index)
        sh.tutor_profile_view(selected)

    elif page == "Add_Student_Form":
        with st.form("add_student"):
            st.write("Enter credentials for new user.")
            _uname_ = st.text_input("Username")
            _password_ = st.text_input("Password")
            entry = { _uname_ : { "password" : _password_, "role" : "student", "UID" : random.randint(0, 9999)  }}
            submitted = st.form_submit_button("Confirm")

            if submitted:
                df.CREDENTIALS.update(entry)
                wb.navigate("Student_Database")



def tutor_card(tutor_name: str):
    t = st.session_state.tutors[tutor_name]
    with st.container(border=True):
        left, right = st.columns([3, 2], vertical_alignment="center")
        with left:
            st.subheader(t["name"])
            st.caption(", ".join(sorted(set(t["subjects"]))))
            st.write(t["bio"])
            st.markdown(sh.star_bar(t["rating"]), unsafe_allow_html=True)
            if t["ratings_count"]:
                st.caption(f"{t['ratings_count']} rating(s) • Updated {t['last_updated']}")
            else:
                st.caption("Be the first to rate this tutor after a session.")
        with right:
            if st.button("Manage", key=f"open_{tutor_name}", use_container_width=True):
                st.session_state.selected_tutor = tutor_name
                wb.navigate("Tutor_Profile_Admin")
            if st.button("Fire Tutor", key=f"fire_{tutor_name}", use_container_width=True):
                del st.session_state.tutors[tutor_name]

