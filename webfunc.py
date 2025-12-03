import streamlit as st

def init_nav():
    ss = st.session_state
    if "nav_history" not in ss:
        ss.nav_history = ["home"]
    if "nav_index" not in ss:
        ss.nav_index = 0
    if "page" not in ss:
        ss.page = "home"
        
def logout():
    st.session_state.is_logged_in = False
    navigate("home")


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