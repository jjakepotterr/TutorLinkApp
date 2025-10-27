# Search_system.py
# (C) Marlon Hernandez 2025

class Tutor:
    def __init__(self, name, subject, ratings):
        self.name = name
        self.subject = subject
        self.ratings = ratings  # list of integers (1–5)

    def average_rating(self):
        if not self.ratings:
            return 0
        return round(sum(self.ratings) / len(self.ratings), 2)

    def __str__(self):
        return f"{self.name} teaches {self.subject} ({self.average_rating()}⭐)"


def search_tutor(subject_name, tutors):
    # normalize case for matching
    subject_name = subject_name.strip().lower()
    found = [t for t in tutors if subject_name in t.subject.lower()]

    if not found:
        print("\n❌ No tutor found for that subject.\n")
    else:
        print("\n🔍 Search Results:")
        for t in found:
            print("------------------------------")
            print(f"Tutor: {t.name}")
            print(f"Subject: {t.subject}")
            print(f"Average Rating: {t.average_rating()}⭐")
            print("------------------------------")
        print()


def main():
    tutors = [
        Tutor("Dr. Smith", "Calculus 1", [5, 4, 5, 5]),
        Tutor("Ms. Johnson", "Physics", [3, 4, 4]),
        Tutor("Mr. Lee", "Computer Science", [5, 5, 4, 5, 5]),
    ]

    while True:
        print("===== Tutor Search System =====")
        print("1. Search by subject")
        print("2. View all tutors")
        print("3. Exit")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            subject = input("\nEnter the subject name (e.g., Calculus 1, Physics, Computer Science): ")
            search_tutor(subject, tutors)

        elif choice == "2":
            print("\nAll Tutors:")
            for t in tutors:
                print(f"- {t}")
            print()

        elif choice == "3":
            print("Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()