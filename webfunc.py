import streamlit as st

def init_nav():
    """Initialize navigation structure in session_state."""
    ss = st.session_state

    if "nav_history" not in ss:
        ss.nav_history = ["home"]

    if "nav_index" not in ss:
        ss.nav_index = 0

    if "page" not in ss:
        ss.page = "home"


def logout():
    """Log out user and reset navigation."""
    ss = st.session_state
    ss.is_logged_in = False
    ss.role = None
    ss.user = None

    # Reset page state
    ss.page = "home"
    ss.nav_history = ["home"]
    ss.nav_index = 0

    # Clear user-specific data
    ss.pop("student", None)
    ss.pop("tutor_name", None)
    ss.pop("schedule", None)
    ss.pop("history", None)
    ss.pop("pending_requests", None)
    ss.pop("tutor_sessions", None)

    st.rerun()


def _current_page():
    """Get the current page from history stack."""
    ss = st.session_state
    init_nav()
    idx = min(ss.nav_index, len(ss.nav_history) - 1)
    return ss.nav_history[idx]


def navigate(target: str, replace: bool = False):
    """Navigate to a different page."""
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
