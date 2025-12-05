import streamlit as st
import datetime as dt
from datetime import datetime, timedelta
import webfunc as wb
import random


# ============================================================
# ⭐ STAR RATING WIDGET
# ============================================================
def star_bar(rating: float | None, max_stars: int = 5) -> str:
    if rating is None:
        return '<span style="color:#999;">No ratings yet</span>'

    rating = max(0.0, min(float(rating), float(max_stars)))
    full = int(rating)
    frac = rating - full
    empty = max_stars - full - (1 if frac > 0 else 0)

    stars_html = "&#9733;" * full
    if 0.25 <= frac < 0.75:
        stars_html += """
        <span style="display:inline-block; position:relative; width:1.1em;">
            <span style="position:absolute; width:1.1em; color:#ddd;">&#9733;</span>
            <span style="position:absolute; width:0.55em; overflow:hidden; color:#f4c150;">&#9733;</span>
        </span>
        """
    elif frac >= 0.75:
        stars_html += "&#9733;"
        empty -= 1

    stars_html += '<span style="color:#ddd;">' + ("&#9733;" * empty) + "</span>"
    return f'<span style="color:#f4c150; font-size:1.1rem;">{stars_html}</span>'


# ============================================================
# 🔎 SEARCH TUTORS
# ============================================================
def search_tutors_by_subject(query: str) -> list[str]:
    """Return all tutors whose subjects match the query."""
    if not query:
        return list(st.session_state.tutors.keys())

    q = query.strip().lower()
    return [
        name
        for name, t in st.session_state.tutors.items()
        if any(q in s.lower() for s in t["subjects"])
    ]


# ============================================================
# 🤖 AI RATING (LIGHTWEIGHT VERSION)
# ============================================================
def ai_rate_tutor(survey: dict) -> int:
    clarity_map = {"Poor": 1, "Fair": 2, "Good": 4, "Great": 5}
    pace_adj = {"Too slow": -0.5, "Just right": 0.5, "Too fast": -0.5}
    patience_map = {"No": 1, "Somewhat": 3, "Yes": 5}

    comments = survey.get("comments", "").lower()

    pos_words = ["great", "helpful", "clear", "amazing", "good", "fantastic", "patient"]
    neg_words = ["bad", "confusing", "rude", "late", "terrible"]

    score = 3.0
    score += sum(comments.count(w) for w in pos_words) * 0.3
    score -= sum(comments.count(w) for w in neg_words) * 0.4

    score += 0.5 * (clarity_map.get(survey["clarity"], 3) - 3)
    score += pace_adj.get(survey["pace"], 0)
    score += 0.5 * (patience_map.get(survey["patience"], 3) - 3)

    return int(max(1, min(5, round(score))))


# ============================================================
# ⭐ UPDATE TUTOR RATING
# ============================================================
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


# ============================================================
# 📘 ADD SESSION TO HISTORY
# ============================================================
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


# ============================================================
# 🧑‍🏫 FULL TUTOR PROFILE VIEW
# (Shows booking UI + sends request to tutor)
# ============================================================
def tutor_profile_view(tutor_name: str):
    t = st.session_state.tutors[tutor_name]

    st.header(t["name"])
    st.write(t["bio"])
    st.write("**Subjects:** " + ", ".join(t["subjects"]))
    st.markdown(star_bar(t["rating"]), unsafe_allow_html=True)

    if t["ratings_count"]:
        st.caption(f"{t['ratings_count']} rating(s) • Updated {t['last_updated']}")
    else:
        st.caption("No ratings yet.")

    st.divider()
    st.subheader("📅 Request a Session")

    # ---------------------
    # SUBJECT SELECTION
    # ---------------------
    subject = st.selectbox(
        "Choose subject",
        sorted(t["subjects"]),
        key=f"subject_{tutor_name}"
    )

    # ---------------------
    # DATE INPUT
    # ---------------------
    date = st.date_input(
        "Choose a date",
        min_value=dt.date.today(),
        key=f"date_{tutor_name}"
    )

    # ---------------------
    # TIME INPUT
    # ---------------------
    time = st.time_input(
        "Choose a time",
        key=f"time_{tutor_name}"
    )

    # ---------------------
    # REQUEST BUTTON
    # ---------------------
    if st.button("Request Session", use_container_width=True,
                 key=f"request_btn_{tutor_name}"):

        student_id = st.session_state.user
        student_name = st.session_state.student["name"]

        request_data = {
            "student": student_name,
            "student_id": student_id,
            "tutor": tutor_name,
            "subject": subject,
            "date": str(date),
            "time": time.strftime("%H:%M"),
            "status": "pending"
        }

        # Add to student's schedule
        st.session_state.schedule.append(request_data)

        # Add to tutor's inbox
        st.session_state.pending_requests.append(request_data)

        st.success("Session request sent!")

    st.caption("Your request will appear as *Pending* until the tutor accepts or rejects it.")
