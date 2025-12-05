import streamlit as st
import webfunc as wb
import datafile as df
import pandas as pd


def tutor_dashboard():
    ss = st.session_state
    tutor_name = ss.get("tutor_name", "Tutor")

    # ------------------------------
    # SIDEBAR NAVIGATION
    # ------------------------------
    st.sidebar.title("Tutor Portal")

    def is_active(page): 
        return ss.page == page

    b1 = st.sidebar.button("Home", use_container_width=True,
                           type="primary" if is_active("Tutor_Home") else "secondary")
    b2 = st.sidebar.button("Pending Requests", use_container_width=True,
                           type="primary" if is_active("Tutor_Requests") else "secondary")
    b3 = st.sidebar.button("My Sessions", use_container_width=True,
                           type="primary" if is_active("Tutor_Sessions") else "secondary")
    b4 = st.sidebar.button("Logout", use_container_width=True)

    if b1: wb.navigate("Tutor_Home")
    elif b2: wb.navigate("Tutor_Requests")
    elif b3: wb.navigate("Tutor_Sessions")
    elif b4: wb.logout()

    page = ss.page

    # ------------------------------
    # PAGE 1 — HOME
    # ------------------------------
    if page == "Tutor_Home":
        st.title(f"Welcome, {tutor_name}")
        st.caption("Tutor Dashboard Overview")

        pending = ss.pending_requests
        accepted = ss.tutor_sessions

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Pending Requests")
            st.metric("Waiting for your approval", len(pending))

        with col2:
            st.subheader("Confirmed Sessions")
            st.metric("Upcoming sessions", len(accepted))

        st.divider()
        st.info("Use the sidebar to manage incoming requests or view confirmed appointments.")

    # ------------------------------
    # PAGE 2 — PENDING REQUESTS
    # ------------------------------
    elif page == "Tutor_Requests":
        st.title("📥 Pending Session Requests")

        # Filter for this specific tutor
        requests = [req for req in ss.pending_requests if req["tutor"] == tutor_name]

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

                # Accept button
                if c1.button(f"Accept Request {i+1}", key=f"accept_{i}", use_container_width=True):
                    # Move request from pending → tutor_sessions
                    ss.tutor_sessions.append(req)

                    # Mark student's request as approved
                    for entry in ss.schedule:
                        if (entry["tutor"] == req["tutor"] and
                            entry["date"] == req["date"] and
                            entry["time"] == req["time"]):
                            entry["status"] = "approved"

                    # Remove from pending
                    ss.pending_requests.remove(req)

                    st.success("Request approved!")
                    st.rerun()

                # Reject button
                if c2.button(f"Reject Request {i+1}", key=f"reject_{i}", use_container_width=True):
                    ss.pending_requests.remove(req)
                    st.warning("Request rejected.")
                    st.rerun()

    # ------------------------------
    # PAGE 3 — CONFIRMED SESSIONS
    # ------------------------------
    elif page == "Tutor_Sessions":
        st.title("📅 Confirmed Sessions")

        sessions = ss.tutor_sessions

        if not sessions:
            st.info("You currently have no confirmed sessions.")
            return

        df_sessions = pd.DataFrame(sessions)
        df_sessions = df_sessions.sort_values(["date", "time"])

        st.dataframe(df_sessions, use_container_width=True, hide_index=True)
