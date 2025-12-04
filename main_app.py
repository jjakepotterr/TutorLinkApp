import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import datetime as dt
import numpy as np
import login_tl as lm
import admin_dashboard as adb
import student_dashboard as sdb
import datafile

st.set_page_config(page_title="TutorLink Demo", layout="wide")

ss = st.session_state
if "students" not in ss:
    ss.students = datafile.students
if "tutors" not in ss:
    ss.tutors = datafile.tutors
if "history" not in ss:
    ss.history = datafile.history

if "schedule" not in ss:
    ss.schedule = []

lm.init_session_state()
if not st.session_state.is_logged_in:
    if st.session_state.page == "home":
        lm.show_home()
    elif st.session_state.page == "student_login":
        lm.show_student_login()
    elif st.session_state.page == "admin_login":
        lm.show_admin_login()
else:
    if st.session_state.user_role == "student":
        sdb.student_dashboard()
    elif st.session_state.user_role == "admin":
        adb.admin_dashboard()