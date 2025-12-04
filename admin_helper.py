import streamlit as st
import webfunc as wb
import student_helper as sh

def search_students_by_name(query: str) -> list[str]:
    if not query:
        return list(st.session_state.students.keys())
    q = query.strip().lower()
    out = []
    for name, s in st.session_state.students.items():
        if any(q in s.lower() for s in s["name"]):
            out.append(name)
    return out

def student_card(student_name: str):
    s = st.session_state.students[student_name]
    with st.container(border=True):
        left, right = st.columns([3, 2], vertical_alignment="center")
        with left:
            st.subheader(s["name"])
            st.write(s["major"])
            st.write(s["year"])
            st.write(s["email"])

        with right:
            if st.button("Delete Student", key=f"open_{student_name}", use_container_width=True):
                del st.session_state.students[student_name]
                st.rerun()
                
