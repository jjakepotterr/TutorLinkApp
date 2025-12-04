import streamlit as st
import student_helper as sh
import webfunc as wb
import pandas as pd
import datetime as dt

def student_dashboard():
    ss = st.session_state
    st.sidebar.title("Student Portal")

    def is_active(p): return st.session_state.page == p

    b1 = st.sidebar.button("Profile", use_container_width=True, type="primary" if is_active("Profile") else "secondary", key = "btn_profile")
    b2 = st.sidebar.button("TutorLink Search", use_container_width=True, type="primary" if is_active("Find_Tutors") else "secondary", key = "btn_tutor")
    b3 = st.sidebar.button("Schedule", use_container_width=True, type="primary" if is_active("Schedule") else "secondary", key = "btn_schedule")
    b4 = st.sidebar.button("Rate Tutor", use_container_width = True)
    b5 = st.sidebar.button("Logout", use_container_width = True, type="primary", key = "btn_exit")
   

    if b1: wb.navigate("Profile")
    elif b2: wb.navigate("Find_Tutors")
    elif b3: wb.navigate("Schedule")
    elif b4: wb.navigate("Survey")
    elif b5: wb.logout()


    page = st.session_state.page

    # =========================
    # P A G E S
    # =========================

    if page == "Profile":
        # clear last rating banner when leaving Survey
        st.session_state.last_rated_tutor = None
        st.session_state.last_rating_score = None

        s = st.session_state.student
        st.title("Welcome, " + s["name"])
        st.caption("Student perspective demo")

        top_l, top_r = st.columns([3, 2])
        with top_l:
            st.subheader("Profile")
            st.write(f"**Name:** {s['name']}")
            st.write(f"**Role:** Student")
            st.write(f"**Major:** {s['major']}")
            st.write(f"**Year:** {s['year']}")
            st.write(f"**Email:** {s['email']}")

        with top_r:
            st.subheader("Quick Stats")
            total_sessions = len(st.session_state.history)
            distinct_tutors = len(set(h["tutor"] for h in st.session_state.history))
            st.metric("Total Sessions", total_sessions)
            st.metric("Tutors Met", distinct_tutors)

        st.divider()
        st.subheader("Tutor History")
        if st.session_state.history:
            # normalize legacy rows
            normalized = []
            for r in st.session_state.history:
                rr = dict(r)
                if "ts" not in rr:
                    base_dt = dt.datetime.combine(rr.get("date", dt.date.today()), dt.time())
                    rr["ts"] = base_dt.isoformat(timespec="seconds")
                if "time" not in rr:
                    rr["time"] = dt.datetime.fromisoformat(rr["ts"]).strftime("%H:%M")
                normalized.append(rr)

            hist_df = pd.DataFrame(normalized).sort_values("ts", ascending=False)
            st.dataframe(
                hist_df[["date", "time", "tutor", "subject", "notes"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No sessions yet. Book a tutor from the Tutor Link page.")

    elif page == "Find_Tutors":
        # clear last rating banner when leaving Survey
        st.session_state.last_rated_tutor = None
        st.session_state.last_rating_score = None

        st.title("🔎 Find Tutors by Subject")
        query = st.text_input("Search any subject", placeholder="e.g., algebra")
        results = sh.search_tutors_by_subject((query or "").strip())
        st.caption(f"{len(results)} result(s)")
        st.divider()

        if not results:
            st.warning("No tutors matched that subject. Try 'algebra'.")
        else:
            for name in results:
                tutor_card(name)

    elif page == "Tutor Profile":
        # clear last rating banner when leaving Survey
        st.session_state.last_rated_tutor = None
        st.session_state.last_rating_score = None

        st.title("👨‍🏫 Tutor Profile")
        tutor_names = list(st.session_state.tutors.keys())
        default_index = 0
        if st.session_state.selected_tutor in tutor_names:
            default_index = tutor_names.index(st.session_state.selected_tutor)
        selected = st.selectbox("Select a tutor", tutor_names, index=default_index)
        sh.tutor_profile_view(selected)

    elif page == "Survey":
        st.title("Post-Session Survey")
        tutor_names = list(st.session_state.tutors.keys())

        default_idx = 0
        if "prefill_tutor" in st.session_state:
            try:
                default_idx = tutor_names.index(st.session_state.prefill_tutor)
            except ValueError:
                default_idx = 0

        tutor_name = st.selectbox("Which tutor did you meet?", tutor_names, index=default_idx)

        st.markdown("#### Quick questions")
        q1 = st.selectbox("Clarity of explanations", ["Poor", "Fair", "Good", "Great"])
        q2 = st.selectbox("Pace of session", ["Too slow", "Just right", "Too fast"])
        q3 = st.selectbox("Was the tutor patient and helpful?", ["No", "Somewhat", "Yes"])

        st.markdown("#### Optional comments")
        comments = st.text_area("Anything else you'd like to add? (keywords influence the AI rater)")

        rated_now = False
        if st.button("Rate with AI", use_container_width=True):
            survey = {"clarity": q1, "pace": q2, "patience": q3, "comments": comments}
            rating = sh.ai_rate_tutor(survey)
            sh.update_tutor_rating(tutor_name, float(rating))

            first_subject = st.session_state.tutors[tutor_name]["subjects"][0] if st.session_state.tutors[tutor_name]["subjects"] else "N/A"
            sh.add_history_entry(tutor_name, first_subject, "Survey submitted")

            st.session_state.last_rated_tutor = tutor_name
            st.session_state.last_rating_score = rating
            rated_now = True

        # Persist and render the success + go-to-profile even after rerun
        just_rated_tutor = st.session_state.get("last_rated_tutor")
        if rated_now or just_rated_tutor:
            shown_tutor = tutor_name if rated_now else just_rated_tutor
            shown_score = st.session_state.get("last_rating_score")
            if shown_score is not None:
                st.success(f"AI rated this session: {shown_score} ⭐")

            if st.button(f"Go to {shown_tutor}'s profile →", use_container_width=True):
                st.session_state.selected_tutor = shown_tutor
                st.session_state.prefill_tutor = shown_tutor
                st.session_state.page = "Tutor Profile"
                st.rerun()

    elif page == "Tutor_Booking":
        st.header(f"Timeslots for {st.session_state.selected_tutor}")
        t = st.session_state.tutors[st.session_state.selected_tutor]

    elif page == "Schedule":
        st.title("My Schedule")
        if not st.session_state.schedule:
            st.header("Your schedule is currently empty.")


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
            if st.button("Open profile", key=f"open_{tutor_name}", use_container_width=True):
                st.session_state.selected_tutor = tutor_name
                wb.navigate("Tutor Profile")

