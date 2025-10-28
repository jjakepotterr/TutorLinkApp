
# streamlit_app.py
# Demo TutorLink-style app for a student named Jared Dudley
# Run with: streamlit run streamlit_app.py

import streamlit as st
import pandas as pd
import datetime as dt
import math
import re
import random

st.set_page_config(page_title="Tutor Demo - Jared Dudley", page_icon="🎓", layout="wide")

# -----------------------------
# Utilities
# -----------------------------

def init_state():
    if "student" not in st.session_state:
        st.session_state.student = {
            "name": "Jared Dudley",
            "major": "Computer Science (Student)",
            "year": "Sophomore",
            "email": "jared.dudley@example.edu",
        }
    if "tutors" not in st.session_state:
        # Pre-seed two Algebra II tutors.
        st.session_state.tutors = {
            "Jerry Spinelli": {
                "name": "Jerry Spinelli",
                "subjects": ["Algebra II", "Algebra 2", "Algebra"],
                "bio": "Patient Algebra II tutor with focus on factoring, quadratics, and functions.",
                # Give one tutor a *bad* existing rating to show the effect
                "rating": 1.8,       # out of 5
                "ratings_count": 3,
                "last_updated": dt.date(2025, 10, 20).isoformat(),
            },
            "Shek Wes": {
                "name": "Shek Wes",
                "subjects": ["Algebra II", "Algebra 2", "Algebra"],
                "bio": "Energetic Algebra II tutor who loves real‑world problem modeling.",
                # No rating yet (so the student's survey can create it)
                "rating": None,
                "ratings_count": 0,
                "last_updated": None,
            },
        }
    if "history" not in st.session_state:
        # Seed with a couple of past sessions to show the dashboard.
        st.session_state.history = [
            {"date": dt.date(2025, 10, 18), "tutor": "Jerry Spinelli", "subject": "Algebra II", "notes": "Quadratics review"},
            {"date": dt.date(2025, 10, 20), "tutor": "Jerry Spinelli", "subject": "Algebra II", "notes": "Functions & graphs"},
        ]
    if "selected_tutor" not in st.session_state:
        st.session_state.selected_tutor = None

def star_bar(rating: float | None, max_stars: int = 5) -> str:
    """Return HTML stars for a given rating (supports fractional stars)."""
    if rating is None:
        return '<span style="color:#999;">No ratings yet</span>'
    # Clamp
    rating = max(0.0, min(float(rating), float(max_stars)))
    full = int(rating)
    frac = rating - full
    empty = max_stars - full - (1 if frac > 0 else 0)

    stars_html = ""
    # full stars
    stars_html += "&#9733;" * full
    # half star (approximate with a half‑filled star using CSS mask)
    if frac >= 0.25 and frac < 0.75:
        # Use a styled half star
        stars_html += '''
        <span style="display:inline-block; position:relative; width:1.1em;">
            <span style="position:absolute; width:1.1em; color:#ddd;">&#9733;</span>
            <span style="position:absolute; width:0.55em; overflow:hidden; color:#f4c150;">&#9733;</span>
        </span>
        '''
    elif frac >= 0.75:
        # Treat as full star if very close
        stars_html += "&#9733;"
        empty -= 1
    # empty stars
    stars_html += '<span style="color:#ddd;">' + ("&#9733;" * max(0, empty)) + "</span>"

    return f'<span style="color:#f4c150; font-size:1.1rem; letter-spacing:1px;">{stars_html}</span> <span style="font-weight:600; color:#444; margin-left:6px;">{rating:.2f}/5</span>'

def search_tutors_by_subject(query: str) -> list[str]:
    """Return tutor names whose subjects match the query (case‑insensitive partials)."""
    if not query:
        return list(st.session_state.tutors.keys())
    q = query.strip().lower()
    matches = []
    for name, t in st.session_state.tutors.items():
        if any(q in s.lower() for s in t["subjects"]):
            matches.append(name)
    return matches

def ai_score_from_survey(text_feedback: str, helpfulness: int, clarity: int, punctuality: int) -> float:
    """
    Offline 'AI' rater: lightweight heuristic sentiment + sliders -> 1..5.
    (If you want to plug a real LLM later, swap this function call.)
    """
    pos_words = {"great", "helpful", "clear", "amazing", "good", "fantastic", "friendly", "patient", "excellent", "understood", "understand", "thanks", "thank you", "respectful"}
    neg_words = {"bad", "confusing", "rude", "late", "unhelpful", "terrible", "didn't", "dont", "don't", "worse", "waste", "boring", "couldn't", "cant", "can't", "noisy", "unprepared"}

    t = text_feedback.lower()
    pos_hits = sum(t.count(w) for w in pos_words)
    neg_hits = sum(t.count(w) for w in neg_words)

    # Base sentiment score from text
    base = 3.0 + (0.35 * pos_hits) - (0.5 * neg_hits)

    # Slider contribution (normalize each 1..5 to -1..+1 then weight)
    def norm(x): return (x - 3) / 2.0  # 1->-1, 3->0, 5->+1
    slider_adj = 0.9 * norm(helpfulness) + 0.8 * norm(clarity) + 0.6 * norm(punctuality)

    score = base + slider_adj
    score = max(1.0, min(5.0, score))

    # Nudge to one decimal place
    return round(score * 2) / 2.0

def update_tutor_rating(tutor_name: str, new_score: float):
    t = st.session_state.tutors[tutor_name]
    if t["rating"] is None or t["ratings_count"] == 0:
        t["rating"] = float(new_score)
        t["ratings_count"] = 1
    else:
        # Simple running average
        total = t["rating"] * t["ratings_count"]
        total += new_score
        t["ratings_count"] += 1
        t["rating"] = total / t["ratings_count"]
    t["last_updated"] = dt.date.today().isoformat()

def add_history_entry(tutor_name: str, subject: str, notes: str = ""):
    st.session_state.history.append({
        "date": dt.date.today(),
        "tutor": tutor_name,
        "subject": subject,
        "notes": notes,
    })

def tutor_card(tutor_name: str):
    t = st.session_state.tutors[tutor_name]
    with st.container(border=True):
        left, right = st.columns([3, 2], vertical_alignment="center")
        with left:
            st.subheader(t["name"])
            st.caption(", ".join(sorted(set(t["subjects"]))))
            st.write(t["bio"])
            stars = star_bar(t["rating"])
            st.markdown(stars, unsafe_allow_html=True)
            if t["ratings_count"]:
                st.caption(f"{t['ratings_count']} rating(s) • Updated {t['last_updated']}")
            else:
                st.caption("Be the first to rate this tutor after a session.")
        with right:
            if st.button("Open profile", key=f"open_{tutor_name}"):
                st.session_state.selected_tutor = tutor_name
                st.session_state.page = "Tutor Profile"
                st.rerun()

def tutor_profile_view(tutor_name: str):
    t = st.session_state.tutors[tutor_name]
    st.header(t["name"])
    st.write(t["bio"])
    st.write("**Subjects:** " + ", ".join(sorted(set(t["subjects"]))))
    st.markdown(star_bar(t["rating"]), unsafe_allow_html=True)
    if t["ratings_count"]:
        st.caption(f"{t['ratings_count']} rating(s) • Updated {t['last_updated']}")
    else:
        st.caption("No ratings yet — finish a session & submit a survey to generate one.")

    st.divider()
    st.subheader("Book / Start Session (Demo)")
    col1, col2 = st.columns(2)
    with col1:
        subj = st.selectbox("Choose subject", sorted(set(t["subjects"])), key=f"book_subj_{tutor_name}")
    with col2:
        if st.button("Start demo session"):
            # In a real app you'd route to a call/meeting — we just add history
            add_history_entry(tutor_name, subj, "Demo session started")
            st.success(f"Session with {tutor_name} started for {subj}. After ending, submit a survey to rate.")
    st.info("When your session ends, go to **Survey** in the sidebar to submit feedback.")

# -----------------------------
# App Layout
# -----------------------------

init_state()

st.sidebar.title("🎓 Student Portal")
page = st.sidebar.radio(
    "Navigate",
    ["Profile", "Find Tutors", "Tutor Profile", "Survey"],
    index=["Profile", "Find Tutors", "Tutor Profile", "Survey"].index(st.session_state.get("page", "Profile")) if "page" in st.session_state else 0,
)

# -----------------------------
# Profile (Student) with Dashboard
# -----------------------------
if page == "Profile":
    st.session_state.page = "Profile"
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
    st.subheader("📊 Tutor History")
    if st.session_state.history:
        hist_df = pd.DataFrame(st.session_state.history)
        hist_df = hist_df.sort_values("date", ascending=False)
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
    else:
        st.info("No sessions yet. Book a tutor from the **Find Tutors** page.")

# -----------------------------
# Find Tutors (Search by subject)
# -----------------------------
elif page == "Find Tutors":
    st.session_state.page = "Find Tutors"
    st.title("🔎 Find Tutors by Subject")

    query = st.text_input("Search any subject", placeholder="e.g., algebra").strip()
    results = search_tutors_by_subject(query or "")
    st.caption(f"{len(results)} result(s)")
    st.divider()

    if not results:
        st.warning("No tutors matched that subject. Try 'algebra'.")
    else:
        for name in results:
            tutor_card(name)

# -----------------------------
# Tutor Profile
# -----------------------------
elif page == "Tutor Profile":
    st.session_state.page = "Tutor Profile"
    st.title("👨‍🏫 Tutor Profile")

    tutor_names = list(st.session_state.tutors.keys())
    default_index = 0
    if st.session_state.selected_tutor and st.session_state.selected_tutor in tutor_names:
        default_index = tutor_names.index(st.session_state.selected_tutor)

    selected = st.selectbox("Select a tutor", tutor_names, index=default_index)
    tutor_profile_view(selected)

# -----------------------------
# Survey (rate tutor; AI‑assisted scoring)
# -----------------------------
elif page == "Survey":
    st.session_state.page = "Survey"
    st.title("📝 Post‑Session Survey")

    tutor = st.selectbox("Which tutor did you meet?", list(st.session_state.tutors.keys()))

    with st.form("survey_form", clear_on_submit=False):
        st.write("Please rate your session (1 = poor, 5 = excellent).")
        c1, c2, c3 = st.columns(3)
        with c1:
            helpfulness = st.slider("Helpfulness", 1, 5, 3)
        with c2:
            clarity = st.slider("Clarity", 1, 5, 3)
        with c3:
            punctuality = st.slider("Punctuality", 1, 5, 3)

        feedback = st.text_area("What worked well? What could be better?", placeholder="Your comments...")

        submitted = st.form_submit_button("Submit Survey & Generate AI Rating")
        if submitted:
            score = ai_score_from_survey(feedback, helpfulness, clarity, punctuality)
            update_tutor_rating(tutor, score)
            add_history_entry(tutor, "Algebra II", "Survey submitted")
            st.success(f"Thanks! An AI‑assisted rating of **{score:.1f}/5** was generated and saved to {tutor}'s profile.")
            st.info("Go to **Tutor Profile** to see the updated star rating.")

    st.caption("Note: This demo uses an offline heuristic to simulate an AI rating. You can plug in a real LLM later.")

# Footer
st.divider()
st.caption("Demo app • Streamlit • Student perspective (Jared Dudley) • © 2025")
