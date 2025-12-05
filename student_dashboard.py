import streamlit as st
import student_helper as sh
import webfunc as wb
import pandas as pd
import datetime as dt


def student_dashboard():
    ss = st.session_state
    st.sidebar.title("Student Portal")

    def is_active(page):
        return ss.page == page

    # Sidebar navigation
    b1 = st.sidebar.button("Profile", use_container_width=True,
                           type="primary" if is_active("Profile") else "secondary")
    b2 = st.sidebar.button("Find Tutors", use_container_width=True,
                           type="primary" if is_active("Find_Tutors") else "secondary")
    b3 = st.sidebar.button("My Schedule", use_container_width=True,
                           type="primary" if is_active("Schedule") else "secondary")
    b4 = st.sidebar.button("Rate Tutor", use_container_width=True)
    b5 = st.sidebar.button("Logout", use_container_width=True, type="primary")

    if b1: wb.navigate("Profile")
    elif b2: wb.navigate("Find_Tutors")
    elif b3: wb.navigate("Schedule")
    elif b4: wb.navigate("Survey")
    elif b5: wb.logout()

    page = ss.page

    # -------------------------------
    # PROFILE PAGE
    # -------------------------------
    if page == "Profile":
        ss.last_rated_tutor = None
        ss.last_rating_score = None

        s = ss.student
        st.title(f"Welcome, {s['name']}")
        st.caption("Student Profile")

        c1, c2 = st.columns([3, 2])

        with c1:
            st.subheader("About You")
            st.write(f"**Name:** {s['name']}")
            st.write(f"**Major:** {s['major']}")
            st.write(f"**Year:** {s['year']}")
            st.write(f"**Email:** {s['email']}")

        with c2:
            st.subheader("Quick Stats")
            total = len(ss.history)
            uniq = len(set(h["tutor"] for h in ss.history))
            st.metric("Sessions Completed", total)
            st.metric("Tutors Worked With", uniq)

        st.divider()
        st.subheader("History")
        if ss.history:
            dfh = pd.DataFrame(ss.history).sort_values("ts", ascending=False)
            st.dataframe(dfh[["date", "time", "tutor", "subject", "notes"]],
                         use_container_width=True, hide_index=True)
        else:
            st.info("No completed sessions yet.")

    # -------------------------------
    # FIND TUTORS PAGE
    # -------------------------------
    elif page == "Find_Tutors":
        ss.last_rated_tutor = None
        ss.last_rating_score = None

        st.title("🔎 Find Tutors")

        query = st.text_input("Search by subject", placeholder="e.g., Algebra")
        results = sh.search_tutors_by_subject((query or "").strip())

        st.caption(f"{len(results)} tutor(s) found.")
        st.divider()

        for name in results:
            tutor_card(name)

    # -------------------------------
    # TUTOR PROFILE PAGE (FIXED)
    # -------------------------------
    elif page == "Tutor_Profile":
        tutor_name = ss.get("selected_tutor")
        if not tutor_name:
            st.error("No tutor selected.")
            return

        sh.tutor_profile_view(tutor_name)

    # -------------------------------
    # STUDENT SCHEDULE
    # -------------------------------
    elif page == "Schedule":
        st.title("📅 My Schedule")

        schedule = ss.get("schedule", [])

        if not schedule:
            st.info("You have no scheduled or requested sessions.")
            return

        df_sched = pd.DataFrame(schedule).sort_values(["date", "time"])

        st.write("### Your Session Requests")
        st.dataframe(df_sched[["tutor", "subject", "date", "time", "status"]],
                     use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Manage Pending Requests")

        pending = [req for req in schedule if req["status"] == "pending"]

        for i, req in enumerate(pending):
            with st.container(border=True):
                st.write(f"**Tutor:** {req['tutor']}")
                st.write(f"**Subject:** {req['subject']}")
                st.write(f"**Date:** {req['date']}")
                st.write(f"**Time:** {req['time']}")
                st.write("**Status:** 🟡 Pending")

                if st.button(f"Cancel Request {i+1}", key=f"cancel_{i}"):
                    ss.schedule.remove(req)
                    if req in ss.pending_requests:
                        ss.pending_requests.remove(req)
                    st.warning("Request canceled.")
                    st.rerun()


# -------------------------------
# TUTOR CARD COMPONENT
# -------------------------------
def tutor_card(tutor_name: str):
    t = st.session_state.tutors[tutor_name]

    with st.container(border=True):
        c1, c2 = st.columns([3, 1])

        with c1:
            st.subheader(tutor_name)
            st.caption(", ".join(t["subjects"]))
            st.write(t["bio"])
            st.markdown(sh.star_bar(t["rating"]), unsafe_allow_html=True)

        with c2:
            if st.button("View Profile", key=f"open_{tutor_name}", use_container_width=True):
                st.session_state.selected_tutor = tutor_name
                wb.navigate("Tutor_Profile")
