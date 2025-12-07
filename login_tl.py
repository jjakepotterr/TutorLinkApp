import streamlit as st
import datafile as df
import webfunc as wb


def login_page():     # <-- FIXED NAME
    st.title("TutorLink Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        user = df.CREDENTIALS.get(username)

        if not user or user["password"] != password:
            st.error("Incorrect username or password.")
            return

        st.session_state.is_logged_in = True
        st.session_state.user = username
        st.session_state.role = user["role"]

        # ---------------------------------------
        # STUDENT LOGIN
        # ---------------------------------------
        if user["role"] == "student":
            uid = user["UID"]
            st.session_state.student = df.students[uid]
            st.session_state.history = []
            st.session_state.schedule = []
            wb.navigate("Profile")
            st.rerun()

        # ---------------------------------------
        # TUTOR LOGIN (FIXED)
        # ---------------------------------------
        elif user["role"] == "tutor":
            uid = user["UID"]
            st.session_state.tutor_uid = uid

            tutor_name = None
            for name, tdata in df.tutors.items():
                if tdata["UID"] == uid:
                    tutor_name = name
                    break

            st.session_state.tutor_name = tutor_name

            wb.navigate("Tutor_Home")
            st.rerun()

        # ---------------------------------------
        # ADMIN LOGIN
        # ---------------------------------------
        elif user["role"] == "admin":
            wb.navigate("Admin_Home")
            st.rerun()
