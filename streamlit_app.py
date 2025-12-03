# streamlit_app.py
# Demo TutorLink-style app for a student named Jared Dudley
# Run with: streamlit run streamlit_app.py

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import datetime as dt
import numpy as np
from streamlit_calendar import streamlit_calendar

st.set_page_config(page_title="TutorLink Demo - Jared Dudley", page_icon="🎓", layout="wide")

# =========================
# Session-State Bootstraps
# =========================

def generate_timeslots():
    timeslots = []
    current_day = (datetime.now()).replace(hour = 7, minute = 0, second = 0, microsecond = 0)
    for n in range(1,8):
        for m in range(0, 13):
            if random.randint(0,2) == 1:
                timeslots.append(current_day + timedelta(days = n, hours = m))
    return timeslots

t1 = generate_timeslots()
t2 = generate_timeslots()
t3 = generate_timeslots()

def init_state():
    ss = st.session_state
    if "active_session" not in ss:
        ss.active_session = None  # {"tutor": str, "subject": str, "material_note": str|None, "started_at": iso}

    if "admin" not in ss:
        ss.admin = {
            "name": "Admin"
        }

    if "student" not in ss:
        ss.student = {
            "name": "Jared Dudley",
            "major": "Computer Science (Student)",
            "year": "Sophomore",
            "email": "jared.dudley@example.edu",
        }

    if "tutors" not in ss:
        ss.tutors = {
            "Jerry Spinelli": {
                "name": "Jerry Spinelli",
                "subjects": ["Algebra", "Algebra 2", "Calculus"],
                "bio": "Patient Algebra II tutor with focus on factoring, quadratics, and functions.",
                "rating": 4,
                "ratings_count": 3,
                "last_updated": dt.date(2025, 10, 20).isoformat(),
            },
            "Shek Wes": {
                "name": "Shek Wes",
                "subjects": ["Algebra", "Algebra 2", "Geometry"],
                "bio": "Energetic Algebra II tutor who loves real-world problem modeling.",
                "rating": None,
                "ratings_count": 0,
                "last_updated": None,
            },            
            "Herbert Perbert": {
                "name": "Herbert Perbert",
                "subjects": ["English", "English II", "Philosophy"],
                "bio": "English Major #TeachingNow. When I am not tutoring I am fishing",
                "rating": 0.2,
                "ratings_count": 0,
                "last_updated": None,
            },
        }

    if "history" not in ss:
        # legacy seed rows (without ts/time) are normalized at render time
        ss.history = [
            {"date": dt.date(2025, 10, 18), "tutor": "Jerry Spinelli", "subject": "Algebra II", "notes": "Quadratics review"},
            {"date": dt.date(2025, 10, 20), "tutor": "Jerry Spinelli", "subject": "Algebra II", "notes": "Functions & graphs"},
        ]

    if "selected_tutor" not in ss:
        ss.selected_tutor = None 

    # persist which tutor was last rated so the “Go to profile” button can survive reruns
    if "last_rated_tutor" not in ss:
        ss.last_rated_tutor = None
    if "last_rating_score" not in ss:
        ss.last_rating_score = None

def init_nav():
    ss = st.session_state
    if "nav_history" not in ss:
        ss.nav_history = ["Profile"]
    if "nav_index" not in ss:
        ss.nav_index = 0
    if "page" not in ss:
        ss.page = "Profile"

def _current_page():
    ss = st.session_state
    if "nav_history" not in ss or "nav_index" not in ss:
        init_nav()
    idx = min(ss.nav_index, len(ss.nav_history) - 1)
    return ss.nav_history[idx]

def navigate(target: str, replace: bool = False):
    ss = st.session_state
    init_nav()
    if replace and ss.nav_history:
        ss.nav_history[ss.nav_index] = target
    else:
        ss.nav_history = ss.nav_history[: ss.nav_index + 1]
        ss.nav_history.append(target)
        ss.nav_index += 1
    ss.page = target
    st.rerun()

# =========================
# Helpers
# =========================
def star_bar(rating: float | None, max_stars: int = 5) -> str:
    if rating is None:
        return '<span style="color:#999;">No ratings yet</span>'
    rating = max(0.0, min(float(rating), float(max_stars)))
    full = int(rating)
    frac = rating - full
    empty = max_stars - full - (1 if frac > 0 else 0)

    stars_html = "&#9733;" * full
    if 0.25 <= frac < 0.75:
        stars_html += '''
        <span style="display:inline-block; position:relative; width:1.1em;">
            <span style="position:absolute; width:1.1em; color:#ddd;">&#9733;</span>
            <span style="position:absolute; width:0.55em; overflow:hidden; color:#f4c150;">&#9733;</span>
        </span>
        '''
    elif frac >= 0.75:
        stars_html += "&#9733;"
        empty -= 1
    stars_html += '<span style="color:#ddd;">' + ("&#9733;" * max(0, empty)) + "</span>"
    return f'<span style="color:#f4c150; font-size:1.1rem; letter-spacing:1px;">{stars_html}</span> <span style="font-weight:600; color:#444; margin-left:6px;">{rating:.2f}/5</span>'

def search_tutors_by_subject(query: str) -> list[str]:
    if not query:
        return list(st.session_state.tutors.keys())
    q = query.strip().lower()
    out = []
    for name, t in st.session_state.tutors.items():
        if any(q in s.lower() for s in t["subjects"]):
            out.append(name)
    return out

def _valid_note(text: str) -> bool:
    return bool(text and text.strip() and len(text.strip()) <= 50)

# ---------- Offline "AI" rating ----------
def ai_score_from_survey(text_feedback: str, helpfulness: int, clarity: int, punctuality: int) -> float:
    pos_words = {"great", "helpful", "clear", "amazing", "good", "fantastic", "friendly", "patient", "excellent", "understood", "understand", "thanks", "thank you", "respectful"}
    neg_words = {"bad", "confusing", "rude", "late", "unhelpful", "terrible", "didn't", "dont", "don't", "worse", "waste", "boring", "couldn't", "cant", "can't", "noisy", "unprepared"}

    t = (text_feedback or "").lower()
    pos_hits = sum(t.count(w) for w in pos_words)
    neg_hits = sum(t.count(w) for w in neg_words)

    base = 3.0 + (0.35 * pos_hits) - (0.5 * neg_hits)

    def norm(x): return (x - 3) / 2.0
    slider_adj = 0.9 * norm(helpfulness) + 0.8 * norm(clarity) + 0.6 * norm(punctuality)

    score = max(1.0, min(5.0, base + slider_adj))
    return round(score * 2) / 2.0

def ai_rate_tutor(survey: dict) -> int:
    clarity_map = {"Poor": 1, "Fair": 2, "Good": 4, "Great": 5}
    pace_adj = {"Too slow": -0.5, "Just right": 0.5, "Too fast": -0.5}
    patience_map = {"No": 1, "Somewhat": 3, "Yes": 5}

    clarity_num = clarity_map.get(survey.get("clarity"), 3)
    helpfulness_num = patience_map.get(survey.get("patience"), 3)
    punctuality_num = 3
    base = ai_score_from_survey(survey.get("comments", ""), helpfulness_num, clarity_num, punctuality_num)
    base += pace_adj.get(survey.get("pace"), 0.0)
    return int(max(1, min(5, round(base))))

def update_tutor_rating(tutor_name: str, new_score: float):
    t = st.session_state.tutors[tutor_name]
    if t["rating"] is None or t["ratings_count"] == 0:
        t["rating"] = float(new_score)
        t["ratings_count"] = 1
    else:
        total = t["rating"] * t["ratings_count"]
        total += new_score
        t["ratings_count"] += 1
        t["rating"] = total / t["ratings_count"]
    t["last_updated"] = dt.date.today().isoformat()

def add_history_entry(tutor_name: str, subject: str, notes: str = ""):
    now = dt.datetime.now()
    st.session_state.history.append({
        "ts": now.isoformat(timespec="seconds"),
        "date": now.date(),
        "time": now.strftime("%H:%M"),
        "tutor": tutor_name,
        "subject": subject,
        "notes": notes,
    })

# =========================
# Tutor UI Pieces
# =========================
def tutor_card(tutor_name: str):
    t = st.session_state.tutors[tutor_name]
    with st.container(border=True):
        left, right = st.columns([3, 2], vertical_alignment="center")
        with left:
            st.subheader(t["name"])
            st.caption(", ".join(sorted(set(t["subjects"]))))
            st.write(t["bio"])
            st.markdown(star_bar(t["rating"]), unsafe_allow_html=True)
            if t["ratings_count"]:
                st.caption(f"{t['ratings_count']} rating(s) • Updated {t['last_updated']}")
            else:
                st.caption("Be the first to rate this tutor after a session.")
        with right:
            if st.button("Open profile", key=f"open_{tutor_name}", use_container_width=True):
                st.session_state.selected_tutor = tutor_name
                print(st.session_state.selected_tutor)
                navigate("Tutor Profile")

def tutor_profile_view(tutor_name: str):
    t = st.session_state.tutors[tutor_name]
    st.header(t["name"])
    st.write(t["bio"])
    st.write("**Subjects:** " + ", ".join(sorted(set(t["subjects"]))))
    st.markdown(star_bar(t["rating"]), unsafe_allow_html=True)
    if t["ratings_count"]:
        st.caption(f"{t['ratings_count']} rating(s) • Updated {t['last_updated']}")
    else:
        st.caption("No ratings yet — finish a session and submit a survey to generate one.")

    st.divider()
    st.subheader("Book / Start Session (Demo)")
    col1, col2 = st.columns(2)
    with col1:
        subj = st.selectbox("Choose subject", sorted(set(t["subjects"])), key=f"book_subj_{tutor_name}")

    with col2:
        active = st.session_state.get("active_session")
        is_active_here = bool(active and active.get("tutor") == tutor_name)

        if not is_active_here:
            if st.button("Book Session", key=f"start_{tutor_name}", use_container_width=True):
                st.session_state.active_session = {
                    "tutor": tutor_name,
                    "subject": subj,
                    "material_note": None,  # will be provided after start
                    "started_at": dt.datetime.now().isoformat(),

                }
  #              st.toast(f"Session with {tutor_name} started for {subj}")
 #               st.rerun()
                navigate("Tutor_Booking")
        else:
            note_key = f"material_note_{tutor_name}"
            existing = active.get("material_note") or ""
            note = st.text_input("Material learned (1–50 chars) *", value=existing, key=note_key, max_chars=50)
            st.session_state.active_session["material_note"] = note.strip()

            if not _valid_note(note):
                st.caption(":red[Required. Enter 1–50 characters.]")
            else:
                st.caption(f"{50 - len(note.strip())} characters left")

            stop_disabled = not _valid_note(note)
            if st.button("Stop session and open survey", key=f"stop_{tutor_name}", use_container_width=True, disabled=stop_disabled):
                material = st.session_state.active_session.get("material_note", "").strip()
                add_history_entry(tutor_name, active.get("subject", subj), material)
                st.session_state.prefill_tutor = tutor_name
                st.session_state.active_session = None
                navigate("Survey")

    st.info("After starting, enter the material learned. Then press Stop to open the Survey.")

# =========================
# Bootstrapping (run first)
# =========================
init_state()
init_nav()

# =========================
# Sidebar / Nav
# =========================
st.sidebar.title("🎓 Student Portal")

def is_active(p): return st.session_state.page == p

b1 = st.sidebar.button("Profile", use_container_width=True, type="primary" if is_active("Profile") else "secondary")
b2 = st.sidebar.button("Tutor Link", use_container_width=True, type="primary" if is_active("Find Tutors") else "secondary")
b3 = st.sidebar.button("Schedule", use_container_width=True, type="primary" if is_active("Schedule") else "secondary")

if b1: navigate("Profile")
elif b2: navigate("Find Tutors")
elif b3: navigate("Schedule")

page = st.session_state.page

# =========================
# Pages
# =========================
if page == "Profile":
    # clear last rating banner when leaving Survey
    st.session_state.last_rated_tutor = None
    st.session_state.last_rating_score = None

    s = st.session_state.student
    st.title("👋 Welcome, " + s["name"])
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

elif page == "Find Tutors":
    # clear last rating banner when leaving Survey
    st.session_state.last_rated_tutor = None
    st.session_state.last_rating_score = None

    st.title("🔎 Find Tutors by Subject")
    query = st.text_input("Search any subject", placeholder="e.g., algebra")
    results = search_tutors_by_subject((query or "").strip())
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
    tutor_profile_view(selected)

elif page == "Survey":
    st.title("📝 Post-Session Survey")
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
    if st.button("Rate with AI 🚀", use_container_width=True):
        survey = {"clarity": q1, "pace": q2, "patience": q3, "comments": comments}
        rating = ai_rate_tutor(survey)
        update_tutor_rating(tutor_name, float(rating))

        first_subject = st.session_state.tutors[tutor_name]["subjects"][0] if st.session_state.tutors[tutor_name]["subjects"] else "N/A"
        add_history_entry(tutor_name, first_subject, "Survey submitted")

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

elif page == "Schedule":
    st.title("My Schedule")
    days_cols = st.columns(7)
    
        


# =========================
# Footer
# =========================
st.divider()
st.caption("Demo app • Streamlit • Student perspective (Jared Dudley) • © 2025")
