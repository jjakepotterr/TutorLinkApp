import streamlit as st
import webfunc as wb
import datafile as df
import pandas as pd


def tutor_dashboard():
    ss = st.session_state

    tutor_uid = ss.get("tutor_uid", None)
    tutor_name = ss.get("tutor_name", None)

    if tutor_uid is None:
        st.error("Tutor session invalid. Please log in again.")
        return

    st.sidebar.title("Tutor Portal")

    def nav(btn, page):
        if st.sidebar.button(btn, use_container_width=True):
            wb.navigate(page)

    nav("Home", "Tutor_Home")
    nav("Pending Requests", "Tutor_Requests")
    nav("My Sessions", "Tutor_Sessions")

    if st.sidebar.button("Logout"):
        wb.logout()

    page = ss.page

    # -------------------------------------
    # HOME
    # -------------------------------------
    if page == "Tutor_Home":
        st.title(f"Welcome, {tutor_name}")

        pending = [r for r in df.PENDING_REQUESTS if r["tutor"] == tutor_uid]
        approved = [s for s in df.TUTOR_SESSIONS if s["tutor"] == tutor_uid]

        st.metric("Pending Requests", len(pending))
        st.metric("Approved Sessions", len(approved))
        return

    # -------------------------------------
    # PENDING REQUESTS
    # -------------------------------------
    if page == "Tutor_Requests":
        st.title("Pending Session Requests")

        requests = [r for r in df.PENDING_REQUESTS if r["tutor"] == tutor_uid]

        if not requests:
            st.info("You have no pending session requests.")
            return

        for i, req in enumerate(requests):
            with st.container(border=True):
                st.write(f"**Student:** {req['student']}")
                st.write(f"**Subject:** {req['subject']}")
                st.write(f"**Date:** {req['date']}")
                st.write(f"**Time:** {req['time']}")

                c1, c2 = st.columns(2)

                # ACCEPT
                if c1.button(f"Accept", use_container_width=True):
                    req["status"] = "approved"
                    df.TUTOR_SESSIONS.append(req)
                    df.PENDING_REQUESTS.remove(req)

                    st.success("Request approved.")
                    st.rerun()

                # REJECT
                if c2.button(f"Reject", use_container_width=True):
                    df.PENDING_REQUESTS.remove(req)
                    st.warning("Request rejected.")
                    st.rerun()

    # -------------------------------------
    # APPROVED SESSIONS
    # -------------------------------------
    if page == "Tutor_Sessions":
        st.title("Approved Sessions")

        sessions = [s for s in df.TUTOR_SESSIONS if s["tutor"] == tutor_uid]

        if not sessions:
            st.info("No approved sessions yet.")
            return

        df_s = pd.DataFrame(sessions)
        st.dataframe(
            df_s[["student", "subject", "date", "time", "status"]],
            use_container_width=True, hide_index=True
        )
