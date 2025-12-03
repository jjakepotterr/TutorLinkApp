import streamlit as st
import datetime as dt
from datetime import datetime, timedelta
import random

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

def generate_timeslots():
    timeslots = []
    current_day = (datetime.now()).replace(hour = 7, minute = 0, second = 0, microsecond = 0)
    for n in range(1,8):
        for m in range(0, 13):
            if random.randint(0,2) == 1:
                timeslots.append(current_day + timedelta(days = n, hours = m))
    return timeslots
