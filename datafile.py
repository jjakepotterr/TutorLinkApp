# ---------------------------
# USER CREDENTIALS
# ---------------------------

CREDENTIALS = {
    # ------------------
    # Admin Accounts
    # ------------------
    "admin": {"password": "admin123", "role": "admin", "UID": 1},
}

# ---------------------------
# STUDENT ACCOUNTS (LOGIN)
# ---------------------------

CREDENTIALS.update({
    "AZC02": {"password": "pass123", "role": "student", "UID": "AZC02"},
    "MZ83D": {"password": "pass123", "role": "student", "UID": "MZ83D"},
    "NU48D": {"password": "pass123", "role": "student", "UID": "NU48D"},
})

# ---------------------------
# TUTOR ACCOUNTS (LOGIN)
# ---------------------------

CREDENTIALS.update({
    "jerry":   {"password": "jerry123", "role": "tutor", "UID": 2001},
    "shek":    {"password": "shek123",  "role": "tutor", "UID": 2002},
    "herbert": {"password": "herb123",  "role": "tutor", "UID": 2003},
})


# ---------------------------
# STUDENT DATA
# ---------------------------
students = {
    "AZC02": {
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
    },

    "NU48D": {
        "name": "Rodrick Hoover",
        "major": "Business Administration (BS)",
        "year": "Super Senior",
        "email": "hooverdrick@mypennstate.edu"
    }
}


# ---------------------------
# TUTOR DATA
# ---------------------------
tutors = {
    "Jerry Spinelli": {
        "UID": 2001,
        "name": "Jerry Spinelli",
        "subjects": ["Algebra", "Algebra 2", "Calculus"],
        "bio": "Patient Algebra II tutor with focus on factoring, quadratics, and functions.",
        "rating": 4,
        "ratings_count": 3,
        "last_updated": "2025-01-01",
    },
    "Shek Wes": {
        "UID": 2002,
        "name": "Shek Wes",
        "subjects": ["Algebra", "Algebra 2", "Geometry"],
        "bio": "Energetic Algebra II tutor who loves real-world problem modeling.",
        "rating": None,
        "ratings_count": 0,
        "last_updated": "2025-01-01",
    },
    "Herbert Perbert": {
        "UID": 2003,
        "name": "Herbert Perbert",
        "subjects": ["English", "English II", "Philosophy"],
        "bio": "English Major #TeachingNow. When I am not tutoring I am fishing.",
        "rating": 0.2,
        "ratings_count": 1,
        "last_updated": "2025-01-01",
    },
}

# ---------------------------
# BOOKING SYSTEM STRUCTURES
# ---------------------------
PENDING_REQUESTS = []       # Student → Tutor booking requests
TUTOR_SESSIONS = {}         # tutor_name → list of approved sessions
