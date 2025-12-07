import streamlit as st
import datetime as dt
import datafile as df


# ---------------------------------------------------
# STAR BAR
# ---------------------------------------------------
def star_bar(rating, max_stars=5):
    if rating is None:
        return '<span style="color:#aaa;">No ratings yet</span>'
    full = int(rating)
    empty = max_stars - full
    html = "&#9733;" * full + '<span style="color:#ddd;">' + ("&#9733;" * empty) + "</span>"
    return f'<span style="color:#f4c150; font-size:1.1rem;">{html}</span>'


# ---------------------------------------------------
# SEARCH TUTORS
# ---------------------------------------------------
def search_tutors_by_subject(query):
    if not query:
        return list(st.session_state.tutors.keys())
    q = query.lower()
    return [
        name for name, t in st.session_state.tutors.items()
        if any(q in s.lower() for s in t["subjects"])
    ]


# ---------------------------------------------------
# HISTORY ENTRY
# ---------------------------------------------------
def add_history_entry(tutor_name, subject, notes=""):
    now = dt.datetime.now()
    st.session_state.history.append({
        "ts": now.isoformat(),
        "date": now.date(),
        "time": now.strftime("%H:%M"),
        "tutor": tutor_name,
        "subject": subject,
        "notes": notes
    })


# ---------------------------------------------------
# TUTOR PROFILE (MAIN FIX HERE)
# ---------------------------------------------------
def tutor_profile_view(tutor_name):
    t = st.session_state.tutors[tutor_name]

    st.header(tutor_name)
    st.caption(", ".join(t["subjects"]))
    st.write(t["bio"])
    st.markdown(star_bar(t["rating"]), unsafe_allow_html=True)
    st.divider()

    subject = st.selectbox("Subject", t["subjects"])
    date = st.date_input("Date")
    time = st.time_input("Time")

    if st.button("Request Session", use_container_width=True):

        req = {
            "student": st.session_state.student["name"],
            "student_id": st.session_state.user,
            "tutor": t["UID"],                # UID stored globally
            "tutor_name": tutor_name,
            "subject": subject,
            "date": date,
            "time": time.strftime("%H:%M"),
            "status": "pending"
        }

        # GLOBAL DATABASE STORAGE
        df.PENDING_REQUESTS.append(req)

        # Sync into UI
        st.session_state.pending_requests = df.PENDING_REQUESTS

        # Student's local schedule
        st.session_state.schedule.append(req)

        st.success("Session request sent to tutor!")
