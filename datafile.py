
import datetime as dt
import student_helper as sh

students = { "AZC02": {
            "name": "Jared Dudley",
            "major": "Computer Science (BS)",
            "year": "Sophomore",
            "email": "jared.dudley@example.edu",
        },
        "MZ83D": {
            "name": "Aaron Fogle",
            "major": "Biochemistry (BS)",
            "year": "Senior",
            "email": "fogle.aaron@angrychihuahua.net"
        }
        
    } 

tutors = {
            "Jerry Spinelli": {
                "name": "Jerry Spinelli",
                "subjects": ["Algebra", "Algebra 2", "Calculus"],
                "bio": "Patient Algebra II tutor with focus on factoring, quadratics, and functions.",
                "rating": 4,
                "ratings_count": 3,
                "last_updated": dt.date(2025, 10, 20).isoformat(),
                "dates_available": sh.generate_timeslots()
            },
            "Shek Wes": {
                "name": "Shek Wes",
                "subjects": ["Algebra", "Algebra 2", "Geometry"],
                "bio": "Energetic Algebra II tutor who loves real-world problem modeling.",
                "rating": None,
                "ratings_count": 0,
                "last_updated": None,
                "dates_available": sh.generate_timeslots()
            },            
            "Herbert Perbert": {
                "name": "Herbert Perbert",
                "subjects": ["English", "English II", "Philosophy"],
                "bio": "English Major #TeachingNow. When I am not tutoring I am fishing!!",
                "rating": 0.2,
                "ratings_count": 0,
                "last_updated": None,
                "dates_available": sh.generate_timeslots()
            },
        }
history = [
    {"date": dt.date(2025, 11, 18), "tutor": "Jerry Spinelli", "subject": "Algebra II", "notes": "Quadratics review"},
    {"date": dt.date(2025, 10, 20), "tutor": "Jerry Spinelli", "subject": "Algebra II", "notes": "Functions & graphs"},
    {"date": dt.date(2025, 6, 7), "tutor": "Herbert Perbert", "subject": "Precalculus", "notes": "Unit Circle"}
]